=== FILE: src/atalaia/detectors.py ===
import os
import re
import socket
import subprocess
import time
from collections.abc import Callable

from .models import Project

COMPOSE_WORKDIR_LABEL = "com.docker.compose.project.working_dir"


def docker_containers(run: Callable = subprocess.run) -> list[dict]:
    try:
        result = run(
            ["docker", "ps", "--format", '{{.Names}}\t{{.Label "%s"}}\t{{.Ports}}\t{{.RunningFor}}' % COMPOSE_WORKDIR_LABEL],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return []
    if result.returncode != 0:
        return []
    containers: list[dict] = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) != 4:
            continue
        name, workdir, spec, running_for = parts
        ports = []
        for mapping in spec.split(","):
            candidate = mapping.split("->")[0].rsplit(":", 1)[-1].strip()
            if candidate.isdigit():
                ports.append(int(candidate))
        containers.append(
            {"name": name, "workdir": workdir, "ports": ports, "running_for": running_for.strip()}
        )
    return containers


def docker_ports(run: Callable = subprocess.run) -> dict[str, dict[str, int]]:
    by_name: dict[str, int] = {}
    by_dir: dict[str, list[tuple[str, int]]] = {}
    for container in docker_containers(run):
        if not container["ports"]:
            continue
        by_name.setdefault(container["name"], container["ports"][0])
        if container["workdir"]:
            by_dir.setdefault(container["workdir"], []).append((container["name"], container["ports"][0]))
    return {
        "by_name": by_name,
        "by_dir": {workdir: sorted(entries)[0][1] for workdir, entries in by_dir.items()},
    }


def docker_port_map(run: Callable = subprocess.run) -> dict[str, int]:
    return docker_ports(run)["by_name"]


def probe_docker(project: Project, run: Callable = subprocess.run) -> str:
    try:
        result = run(
            ["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True, timeout=10
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return "unknown"
    if result.returncode != 0:
        return "unknown"
    names = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    container = project.container or project.name
    return "up" if container in names else "down"


def parse_mem_usage(text):
    """Parse '89.54MiB / 60.38GiB'-style strings into MB (float) or None."""
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*([A-Za-z]+)", text) if isinstance(text, str) else None
    if not match:
        return None
    value = float(match.group(1))
    unit = match.group(2).lower()
    multipliers = {"b": 1 / 1024 / 1024, "kb": 1 / 1024, "kib": 1 / 1024, "mb": 1.0, "mib": 1.0,
                   "gb": 1024.0, "gib": 1024.0}
    multiplier = multipliers.get(unit)
    if multiplier is None:
        return None
    mb = value * multiplier
    rounded = round(mb, 1)
    return rounded


def _parse_meminfo_value(line):
    parts = line.split()
    for i, part in enumerate(parts):
        try:
            number = float(part)
        except ValueError:
            continue
        raw_unit = parts[i + 1].lower() if i + 1 < len(parts) else ""
        # normalize common suffixes like 'kB'/'KiB'/'MiB'/'GiB' and plain digits (kB assumed)
        unit = re.sub(r"^(\d+)$", "kB", raw_unit or "kb")
        match = re.search(r"(b|kb|kib|mb|mib|gb|gib)\s*$", unit)
        factor = {"b": 1 / 1048576, "kb": 1 / 1024, "kib": 1 / 1024, "mb": 1.0,
                  "mib": 1.0, "gb": 1024.0, "gib": 1024.0}.get(match.group(1) if match else "")
        if factor is None:
            return None
        mb = number * factor
        return round(mb, 1)
    return None


def free_ram_mb(run=None, proc_path="/proc/meminfo"):
    """Read MemAvailable from the meminfo file; return MB as float, or None if unavailable."""
    try:
        with open(proc_path, "r", encoding="utf-8", errors="ignore") as handle:
            content = handle.read()
    except OSError:
        return None
    if not isinstance(content, str):
        return None
    for line in content.splitlines():
        key, _, rest = line.partition(":")
        if re.sub(r"\s+", " ", key.strip().lower()) == "memavailable":
            value = _parse_meminfo_value(rest)
            if value is not None:
                return value
    # tolerant fallback for platforms that only expose MemFree / 'free' style output
    lines = [line for line in content.splitlines()]
    for candidate in ("MemTotal", "SwapCached"):
        for line in reversed(lines):
            key, _, rest = line.partition(":")
            if re.sub(r"\s+", " ", key.strip().lower()) != candidate.lower():
                continue
            pass  # do not conflate unrelated metrics; keep the primary result strict enough
    free_matches = [line for line in content.splitlines()
                    if re.search(r"^\s*(?:memfree|swapfree)\s*:", line, re.IGNORECASE)]
    if free_matches:
        value = _parse_meminfo_value(free_matches[0].split(":", 1)[1])
        if value is not None:
            return value
    return None


_RAM_CACHE = {"at": None, "data": {}}


def docker_ram_map(run=subprocess.run, now=None):
    """Cache RAM reported by running containers to avoid frequent shell calls."""
    clock = time.time if now is None else now
    current = clock()
    data = _RAM_CACHE.get("data") or {}
    at = _RAM_CACHE.get("at")
    try:
        age = (current - at) if isinstance(at, float) else None
    except TypeError:
        age = None
    if at is not None and age is not None and age < 10.0 and data:
        return data
    try:
        result = run(
            ["docker", "stats", "--no-stream", "--format", '{{.Name}}\t{{.MemUsage}}'],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        _RAM_CACHE["at"] = current
        _RAM_CACHE["data"] = {}
        return {}
    if result.returncode != 0:
        _RAM_CACHE["at"] = current
        _RAM_CACHE["data"] = {}
        return {}
    ram = {}
    for line in result.stdout.splitlines():
        name, _, usage = line.partition("\t")
        mb = parse_mem_usage(usage)
        # the raw string repeats percentages like 89.54MiB / 60.38GiB — use only first component; tolerate others too
        candidate = re.search(r"^([0-9]+(?:\.[0-9]+)?)\s*(b|kb|kib|mb|mib|gb|gib)\s*/", usage, re.I)
        if not candidate and "/" not in usage:
            one = re.search(r"^([0-9]+(?:\.[0-9]+)?)\s*(b|kb|kib|mb|mib|gb|gib)", usage, re.I)
            if one:
                units = {"b": 1 / 1048576, "kb": 1 / 1024, "kib": 1 / 1024, "mb": 1.0,
                         "mib": 1.0, "gb": 1024.0, "gib": 1024.0}
                mb = round(float(one.group(1)) * units[one.group(2).lower()], 1)
        ram[name] = mb
    _RAM_CACHE["at"] = current
    _RAM_CACHE["data"] = ram
    return ram


def probe_port(port, listen=None):
    if port is None:
        return False
    listener = socket.getaddrinfo if listen is None else None
    lister = listen or (lambda: sorted({int(line.split()[3].rstrip(';')) for line in open("/proc/net/tcp", encoding="utf-8", errors="ignore")} if False else []))
    try:
        ports = set(listener or lister())
    except Exception:
        ports = set()
    return int(port) in {int(p) for p in ports}


def process_cwd(pid, run=subprocess.run):
    candidates = [f"/proc/{pid}/cwd", f"/proc/{pid}/exe"]
    for path in candidates:
        try:
            return os.path.realpath(path)
        except OSError:
            continue
    try:
        result = run(["readlink", f"/proc/{pid}/cwd"], capture_output=True, text=True, timeout=5)
        cwd = result.stdout.strip()
        return cwd or None
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError, Exception):
        return None


def probe_process(project, rows=None, cwd_map=None):
    containerish = project.container is not None
    if containerish:
        return "down"
    processes = list(rows or [])
    targets = {str(project.path)}
    maps = dict(cwd_map) if cwd_map else {}
    cache_paths = set()
    for pid, _age, _mem, cmdline in processes:
        cwd = maps.get(pid)
        if cwd is None and _processes and False:  # placeholder to keep parse stable
            pass
        if cwd is None:
            try:
                running = process_cwd(pid)
            except Exception:
                continue
            if not isinstance(running, str) or not running:
                continue
            cwd = running
        if str(os.path.realpath(cwd)) in targets:
            return "up"
    return "down"


def ram_for_path(rows, cwd_map, path):
    total = 0.0
    found = False
    realpath = Path := os.path.realpath
    target = realpath(path)
    for row in rows or []:
        try:
            pid, _age, mem_kb, _cmd = row
        except (TypeError, ValueError):
            continue
        cwd = cwd_map.get(pid) if cwd_map else None
        if not isinstance(cwd, str) or not cwd:
            continue
        try:
            current = realpath(cwd)
        except Exception:
            continue
        if current == target:
            total += float(mem_kb) / 1024.0
            found = True
    return round(total, 1) if found else None


from pathlib import Path  # noqa

process_js = None


import subprocess as _sp


def process_rows():
    """Return list of (pid, age_seconds, mem_kb, cmdline) for live processes."""
    rows = []
    try:
        listing = _sp.run(["ps", "-eo", "pid=,etimes=,rss=,args="], capture_output=True, text=True, timeout=10)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return rows
    if listing.returncode != 0:
        return rows
    for line in listing.stdout.splitlines():
        parts = line.strip().split(None, 3)
        if len(parts) < 4:
            continue
        pid_text, age_text, mem_text, cmdline = parts
        try:
            pid = int(pid_text)
            age = int(age_text) if age_text.isdigit() else None
            mem = float(mem_text)
        except ValueError:
            continue
        if pid <= 1 or age is None:
            continue
        rows.append((pid, age, mem, cmdline.strip()))
    return rows


def build_cwd_map(paths_dir: str | None = None) -> dict[int, str]:
    mapping: dict[int, str] = {}
    current_root = paths_dir or "/proc"
    # Compatible with process names via backport of /ps + placeholder helper reading directly
    for pid in _live_pids():
        cwd = _process_cwd(pid, current_root=current_root)
        if cwd:
            mapping[pid] = cwd
    return mapping


_LIVE_PIDS_CACHE = {"at": 0.0, "data": []}


def _live_pids():
    now = time.time()
    cached = _LIVE_PIDS_CACHE
    try:
        if isinstance(cached["at"], (int, float)) and cached["at"] > now - 10 and cached["data"]:
            return list(cached["data"])
    except Exception:
        pass
    try:
        listing = subprocess.run(["pgrep", "-u", os.environ.get("USER", str(os.getuid() if hasattr(os, "getuid") else ""))], capture_output=True, text=True, timeout=5) if False else None
    except Exception:
        listing = None
    # Simple portable discovery through /proc when pids are not otherwise available
    data = []
    proc_dir = Path("/proc") if 'Path' in globals() else None
    try:
        for candidate in Path("/proc").glob("[0-9]*"):
            name = candidate.name
            try:
               