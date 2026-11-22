ROLE: implementation planner. A feature has been approved. You get the
approved requirements and the repository file tree BEFORE implementation.
Write the implementation plan with EXACTLY these three sections:

FILES
<repo-relative path of every file you would create or modify, one per line>

TASKS
T1: <short title>
    depends_on: (none)
    refs: R1, R2
T2: <short title>
    depends_on: T1
    refs: R3
(... ordered so dependencies come first; every requirement must be covered
 by the refs of at least one task)

GATES
<the verification gates you would run before closing the feature>

--- APPROVED REQUIREMENTS ---
R1: WHEN a client requests `GET /api/system`, the system shall return `free_ram_mb` taken from `MemAvailable` in `/proc/meminfo` (converted to MB).

R2: IF `/proc/meminfo` is missing or malformed, THEN the system shall return `free_ram_mb` as null without failing the request.

R3: The UI top bar shall display the sum of `ram_mb` of every `up` entry and the free RAM from `/api/system`, refreshed on every poll.

R4: WHEN any value is unavailable, the UI shall display `—` for that value.

R5: The system summary read shall not require Docker or subprocess calls (direct file read of `/proc/meminfo`).

--- FEATURE TITLE ---
f8_ram_summary review APPROVED (5/5)

--- REPOSITORY FILE TREE (before implementation) ---
.opencode/agent/implementer.md
.opencode/agent/leader.md
.opencode/agent/reviewer.md
.opencode/agent/spec-author.md
AGENTS.md
HARNESS.md
README.md
dashboard.yaml
design-system/atalaia/MASTER.md
docs/architecture.md
docs/conventions.md
docs/specs.md
docs/verification.md
harness/CHECKPOINTS.md
harness/feature_list.json
harness/init.sh
harness/progress/current.md
harness/progress/history.md
harness/progress/impl_f1_scanner.md
harness/progress/impl_f2_ui.md
harness/progress/impl_f3_actions.md
harness/progress/impl_f4_archive.md
harness/progress/impl_f5_truth_containers.md
harness/progress/impl_f6_ram.md
harness/progress/impl_f7_stop_all.md
harness/progress/review_f1_scanner.md
harness/progress/review_f2_ui.md
harness/progress/review_f3_actions.md
harness/progress/review_f4_archive.md
harness/progress/review_f5_truth_containers.md
harness/progress/review_f6_ram.md
harness/progress/review_f7_stop_all.md
harness/specs/f1_scanner/APPROVAL
harness/specs/f1_scanner/design.md
harness/specs/f1_scanner/requirements.md
harness/specs/f1_scanner/review.md
harness/specs/f1_scanner/tasks.md
harness/specs/f2_ui/APPROVAL
harness/specs/f2_ui/design.md
harness/specs/f2_ui/requirements.md
harness/specs/f2_ui/review.md
harness/specs/f2_ui/tasks.md
harness/specs/f3_actions/APPROVAL
harness/specs/f3_actions/design.md
harness/specs/f3_actions/requirements.md
harness/specs/f3_actions/review.md
harness/specs/f3_actions/tasks.md
harness/specs/f4_archive/APPROVAL
harness/specs/f4_archive/design.md
harness/specs/f4_archive/requirements.md
harness/specs/f4_archive/review.md
harness/specs/f4_archive/tasks.md
harness/specs/f5_truth_containers/APPROVAL
harness/specs/f5_truth_containers/design.md
harness/specs/f5_truth_containers/requirements.md
harness/specs/f5_truth_containers/review.md
harness/specs/f5_truth_containers/tasks.md
harness/specs/f6_ram/APPROVAL
harness/specs/f6_ram/design.md
harness/specs/f6_ram/requirements.md
harness/specs/f6_ram/review.md
harness/specs/f6_ram/tasks.md
harness/specs/f7_stop_all/design.md
harness/specs/f7_stop_all/requirements.md
harness/specs/f7_stop_all/review.md
harness/specs/f7_stop_all/tasks.md
harness/tools/audit-security.sh
harness/tools/check-traceability.py
harness/tools/validate-feature-list.py
opencode.json
pyproject.toml
scripts/e2e_actions_demo.py
scripts/e2e_archive_demo.py
scripts/e2e_stopall_demo.py
src/atalaia/__init__.py
src/atalaia/actions.py
src/atalaia/api.py
src/atalaia/archive.py
src/atalaia/detail.py
src/atalaia/detectors.py
src/atalaia/ids.py
src/atalaia/models.py
src/atalaia/scanner.py
tests/test_actions.py
tests/test_actions_stopall.py
tests/test_api.py
tests/test_api_actions.py
tests/test_api_archive.py
tests/test_api_containers.py
tests/test_api_detail.py
tests/test_api_ram.py
tests/test_api_stopall.py
tests/test_archive.py
tests/test_detail.py
tests/test_detectors.py
tests/test_ids.py
tests/test_scanner.py
tests/test_web.py
tests/test_web_static.py
web/app.js
web/index.html
web/style.css

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- web/app.js (first 60 lines of 12215 bytes) ---
const state = { items: [], selected: null, search: "", type: "", status: "", tab: "actius" };

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function fmtUptime(seconds) {
  if (seconds === null || seconds === undefined) return "—";
  if (seconds < 60) return seconds + "s";
  if (seconds < 3600) return Math.floor(seconds / 60) + "m";
  if (seconds < 86400) return Math.floor(seconds / 3600) + "h " + Math.floor((seconds % 3600) / 60) + "m";
  return Math.floor(seconds / 86400) + "d " + Math.floor((seconds % 86400) / 3600) + "h";
}

function fmtRam(mb) {
  if (mb === null || mb === undefined) return "—";
  if (mb >= 1024) return (mb / 1024).toFixed(1) + " GB";
  return Math.round(mb) + " MB";
}

function applyFilters(items) {
  return items.filter((p) => {
    if (state.tab === "actius" && p.archived) return false;
    if (state.tab === "arxivats" && !p.archived) return false;
    if (state.status && p.status !== state.status) return false;
    if (state.type && p.type !== state.type) return false;
    const needle = state.search.toLowerCase();
    if (needle && !p.name.toLowerCase().includes(needle) && !p.path.toLowerCase().includes(needle)) return false;
    return true;
  });
}

function renderTabs(items) {
  const archived = items.filter((p) => p.archived).length;
  document.getElementById("count-actius").textContent = "(" + (items.length - archived) + ")";
  document.getElementById("count-arxivats").textContent = "(" + archived + ")";
  document.getElementById("tab-actius").classList.toggle("active", state.tab === "actius");
  document.getElementById("tab-actius").setAttribute("aria-selected", String(state.tab === "actius"));
  document.getElementById("tab-arxivats").classList.toggle("active", state.tab === "arxivats");
  document.getElementById("tab-arxivats").setAttribute("aria-selected", String(state.tab === "arxivats"));
}

function renderSummary(items) {
  const up = items.filter((p) => p.status === "up").length;
  const summary = document.getElementById("summary");
  summary.textContent = "";
  summary.appendChild(el("span", "dot " + (up > 0 ? "up" : "down")));
  summary.appendChild(document.createTextNode(" " + up + "/" + items.length + " amunt"));
}

function renderTypes(items) {
  const select = document.getElementById("type");
  const current = select.value;
  const kinds = [...new Set(items.map((p) => p.type))].sort();
  select.textContent = "";
  select.appendChild(el("option", "", "tipus: tots")).value = "";
  for (const kind of kinds) {
--- harness/tools/check-traceability.py (first 60 lines of 10470 bytes) ---
#!/usr/bin/env python3
"""Check requirement traceability for harness specs (Protocol v1).

For each feature with a spec (harness/specs/<name>/requirements.md), collects
the R<n> identifiers, merges the traceability tables from every
harness/progress/impl_*.md, and verifies:
  1. every R<n> appears in at least one table row;
  2. every test identifier referenced by a row exists literally under tests/
     (file name or file content match).

Per Protocol §5, requirements whose table Status is not "done" are reported
as unresolved (they do not create gaps).

Usage:
  check-traceability.py --all [--json] [root]
  check-traceability.py --feature NAME [--json] [root]

Exit codes: 0 covered, 1 gaps, 2 usage error.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQ_RE = re.compile(r"\bR(\d+)\b")
ROW_RE = re.compile(r"^\|\s*(R\d+)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|")


def find_requirements(root: Path, feature: str) -> set[str]:
    req_file = root / "harness" / "specs" / feature / "requirements.md"
    if not req_file.is_file():
        return set()
    return {f"R{m}" for m in REQ_RE.findall(req_file.read_text(encoding="utf-8"))}


ATTR_RE = re.compile(r"(?im)^\s*feature\s*:\s*([a-z0-9_-]+)\s*$")


def _merge_impl_table(
    text: str,
    impl_name: str,
    feature: str | None,
    merged: dict[str, list[str]],
    statuses: dict[str, str],
) -> None:
    """Fold one impl_*.md file's rows into the merged tables (protocol v1.1)."""
    owner = ATTR_RE.search(text)
    if owner is None:
        if feature is not None:
            statuses.setdefault("__unattributed__", impl_name)
        return
    if feature is not None and owner.group(1) != feature:
        return
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if m is None:
            continue
--- src/atalaia/api.py (first 60 lines of 10247 bytes) ---
import subprocess
from collections.abc import Callable
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .actions import KNOWN_ACTIONS, run_action, run_stop_all, stop_all_targets
from .actions import action_log_tail, declared_actions
from .archive import archive as archive_id
from .archive import load_archived
from .archive import unarchive as unarchive_id
from .detectors import docker_containers, docker_ports, probe_docker, probe_port_owned, probe_process
from .detectors import build_cwd_map, docker_ram_map, process_rows, ram_for_path, uptime_for_path
from .detail import read_readme, tail_log, uptime_seconds, git_info
from .ids import project_id, resolve_id
from .models import Project, default_roots
from .scanner import compose_host_ports, discover_projects, readme_port, resolve_port
from pydantic import BaseModel


class ActionBody(BaseModel):
    confirm: bool = False

SERVE_HOST = "127.0.0.1"
SERVE_PORT = 8901


def project_status(
    project: Project,
    uptime: int | None = None,
    docker_port: int | None = None,
    scan_port: int | None = None,
    archived: bool = False,
    containers_running: bool = False,
    rows: list | None = None,
    cwd_map: dict | None = None,
    ram_mb: float | None = None,
) -> dict:
    docker = probe_docker(project)
    open_port = probe_port_owned(project.port or docker_port, str(project.path))
    if project.container is not None:
        process = "down"
    else:
        process = probe_process(project, rows=rows, cwd_map=cwd_map)
    alive = docker == "up" or open_port or process == "up" or containers_running
    return {
        "id": project_id(project.path, project.container),
        "name": project.name,
        "path": str(project.path),
        "type": project.kind,
        "status": "up" if alive else "down",
        "port": project.port or docker_port or scan_port,
        "uptime": uptime,
        "ram_mb": ram_mb,
        "protected": project.protected,
        "archived": archived,
        "group": project.group,
        "container": project.container,
--- harness/tools/audit-security.sh (first 60 lines of 8973 bytes) ---
#!/usr/bin/env bash
# audit-security.sh — SAST + dependency scan for the security-audit module.
#
# Runs the stack-appropriate tools that are available and degrades to
# checklist-only when they are not (§6.3). The installer never runs this script;
# a non-zero exit means HIGH findings and the reviewer must reject approval.
#
# Usage: bash harness/tools/audit-security.sh [--stack=<stack>]
# Exit codes: 0 = no HIGH findings (or checklist-only), 1 = HIGH findings, 2 = usage error

set -uo pipefail

JSON=0
STACK=""
for arg in "$@"; do
  case "$arg" in
    --json) JSON=1 ;;
    --stack=*) STACK="${arg#--stack=}" ;;
    *) echo "unknown argument: $arg" >&2; exit 2 ;;
  esac
done

if [ -z "$STACK" ]; then
  if [ -f "tsconfig.json" ]; then STACK="typescript"
  elif [ -f "package.json" ]; then STACK="node"
  elif [ -f "build.gradle" ] && { [ -f "AndroidManifest.xml" ] || [ -f "app/src/main/AndroidManifest.xml" ]; }; then STACK="android"
  elif [ -f "build.gradle" ] || [ -f "pom.xml" ]; then STACK="java"
  elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then STACK="python"
  elif [ -f "Cargo.toml" ]; then STACK="rust"
  else STACK="generic"
  fi
fi

REPORT="$(mktemp)"
trap 'rm -f "$REPORT"' EXIT
HIGH=0
SKIPPED=()

if [ "$JSON" -eq 0 ]; then
  echo "# Security Audit Report (stack: $STACK)"
  echo ""
fi

FINDINGS_JSON="[]"
MODE="automated"

json_escape() {  # json_escape <string> — quote for embedding in JSON
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr '\n' ' '
}

extract_bandit_json() {  # <report-file-with-bandit-json> → findings array fragment
  python3 - "$1" <<'PYEOF' 2>/dev/null || true
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    print("[]")
    raise SystemExit(0)
out = []
for r in d.get("results", []):
--- tests/test_detectors.py (first 60 lines of 8359 bytes) ---
import subprocess
from pathlib import Path

from atalaia.detectors import probe_docker, docker_containers, docker_port_map, docker_ports, docker_ram_map, parse_mem_usage, probe_port, probe_port_owned, probe_process, ram_for_path
from atalaia.models import Project
from atalaia.scanner import discover_projects, load_descriptor


def project(name="web", kind="node"):
    return Project(name=name, path=Path(f"/tmp/{name}"), kind=kind, port=None, protected=False)


def test_dashboard_yaml_override(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    (app / "package.json").write_text("{}")
    (app / "dashboard.yaml").write_text("port: 3000\nstart: npm run dev\n")

    found = discover_projects([tmp_path])
    assert found[0].port == 3000


def test_malformed_yaml_falls_back(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    (app / "package.json").write_text("{}")
    (app / "dashboard.yaml").write_text("port: [unclosed\n  bad: : :\n")

    assert load_descriptor(app) == {}
    found = discover_projects([tmp_path])
    assert found[0].port is None


def test_invalid_port_ignored(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    (app / "package.json").write_text("{}")
    (app / "dashboard.yaml").write_text("port: 99999\n")

    assert discover_projects([tmp_path])[0].port is None


class FakeRun:
    def __init__(self, stdout="", returncode=0, error=None):
        self.stdout = stdout
        self.returncode = returncode
        self.error = error

    def __call__(self, *args, **kwargs):
        if self.error is not None:
            raise self.error
        return self


def test_probe_docker_up():
    run = FakeRun(stdout="web\ndb\n")
    assert probe_docker(project("web"), run=run) == "up"


def test_probe_docker_down():
--- web/style.css (first 60 lines of 7260 bytes) ---
:root {
  --color-background: #0f172a;
  --color-foreground: #f8fafc;
  --color-card: #1b2336;
  --color-muted: #272f42;
  --color-muted-foreground: #94a3b8;
  --color-border: #475569;
  --color-accent: #22c55e;
  --color-destructive: #ef4444;
  --font-mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --font-sans: "IBM Plex Sans", system-ui, -apple-system, sans-serif;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --radius: 6px;
}

@media (prefers-color-scheme: light) {
  :root {
    --color-background: #f8fafc;
    --color-foreground: #0f172a;
    --color-card: #ffffff;
    --color-muted: #e2e8f0;
    --color-muted-foreground: #475569;
    --color-border: #cbd5e1;
  }
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--color-background);
  color: var(--color-foreground);
  font: 14px/1.5 var(--font-sans);
}

.topbar {
  display: flex;
  align-items: baseline;
  gap: var(--space-4);
  padding: var(--space-3) var(--space-6);
  border-bottom: 1px solid var(--color-border);
}

.topbar h1 {
  margin: 0;
  font: 600 16px/1 var(--font-mono);
  letter-spacing: 1px;
}

.summary { color: var(--color-muted-foreground); font-family: var(--font-mono); font-size: 12px; }
.tick { margin-left: auto; color: var(--color-muted-foreground); font-family: var(--font-mono); font-size: 12px; }

.toolbar {
  display: flex;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
--- tests/test_scanner.py (first 60 lines of 6745 bytes) ---
from pathlib import Path

from atalaia.models import Project, is_protected
from atalaia.scanner import compose_host_ports, detect_kind, discover_projects, readme_port, resolve_port


def test_project_is_frozen():
    p = Project(name="x", path=Path("/tmp/x"), kind="node", port=None, protected=False)
    assert p.name == "x"
    assert p.port is None


def test_homelab_is_protected():
    assert is_protected(Path.home() / "homelab" / "wekan") is True
    assert is_protected(Path.home() / "works" / "java") is False


def test_discover_finds_projects(tmp_path):
    node = tmp_path / "web"
    node.mkdir()
    (node / "package.json").write_text("{}")
    comp = tmp_path / "infra"
    comp.mkdir()
    (comp / "docker-compose.yml").write_text("services: {}")
    plain = tmp_path / "notes"
    plain.mkdir()
    (plain / "README.md").write_text("hi")

    found = discover_projects([tmp_path])
    by_name = {p.name: p for p in found}
    assert by_name["web"].kind == "node"
    assert by_name["infra"].kind == "compose"
    assert "notes" not in by_name


def test_discover_skips_missing_root(tmp_path):
    found = discover_projects([tmp_path / "nope"])
    assert found == []


def test_discover_skips_hidden(tmp_path):
    hidden = tmp_path / ".git"
    hidden.mkdir()
    (hidden / "package.json").write_text("{}")
    assert discover_projects([tmp_path]) == []


def test_discover_recurses_nested(tmp_path):
    nested = tmp_path / "tools" / "converter"
    nested.mkdir(parents=True)
    (nested / "pyproject.toml").write_text("[project]\nname='c'\n")
    (nested / "run-serve.sh").write_text("#!/bin/sh\n")
    deep = tmp_path / "a" / "b" / "c" / "d"
    deep.mkdir(parents=True)
    (deep / "package.json").write_text("{}")

    by_name = {p.name: p for p in discover_projects([tmp_path])}
    assert by_name["converter"].kind == "python"
    assert "d" not in by_name

--- src/atalaia/detectors.py (first 60 lines of 6744 bytes) ---
import os
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

Write ONLY the plan (the three sections). No prose outside them.