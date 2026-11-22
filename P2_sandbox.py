"""P2 sandbox: worktree per repo, còpia de fitxers de l'executor, tests reals.

Flux per tasca:
  1. checkout net del pre_ref
  2. copiar els fitxers que l'executor va lliurar
  3. copiar els tests (i fixtures) que el post_ref va afegir/tocar
  4. córrer els tests de la feature → % verds = nota del planner
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SANDBOX = Path("/tmp/opencode/P2-sandbox")
TEST_PAT = re.compile(r"(^|/)(tests?|__tests__)/|\.test\.|\.spec\.|test_[^/]+\.py$|_test\.[a-z]+$",
                      re.I)
FIXTURE_PAT = re.compile(r"fixtures?/|conftest\.py$", re.I)


def sh(cmd: list[str], cwd: Path, timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)


def ensure_worktree(repo_name: str, ref: str) -> Path:
    """Worktree net del repo al ref donat (un per repo, reutilitzat)."""
    src = Path.home() / "Documents/CV/projects" / repo_name
    dst = SANDBOX / repo_name
    if dst.exists():
        # reset net al ref
        sh(["git", "checkout", "-f", ref], cwd=dst)
        sh(["git", "clean", "-fdx", "-e", "node_modules", "-e", ".venv"], cwd=dst)
        return dst
    SANDBOX.mkdir(parents=True, exist_ok=True)
    sh(["git", "worktree", "add", "--detach", str(dst), ref], cwd=src)
    return dst


def install_deps(wt: Path) -> None:
    """Instal·la deps una vegada per worktree (uv per Python, npm per Node)."""
    if (wt / "pyproject.toml").exists() and not (wt / ".venv").exists():
        r = sh(["uv", "sync", "--frozen"], cwd=wt, timeout=600)
        if r.returncode != 0:
            sh(["uv", "sync"], cwd=wt, timeout=600)
    if (wt / "package.json").exists() and not (wt / "node_modules").exists():
        sh(["npm", "install", "--no-audit", "--no-fund"], cwd=wt, timeout=600)


def py_cmd(wt: Path, args: list[str]) -> list[str]:
    venv = wt / ".venv" / "bin" / "python"
    return [str(venv)] + args if venv.exists() else ["python3"] + args


def test_files_at(repo: Path, ref: str) -> list[str]:
    """Fitxers de test (i fixtures) que el ref conté — per copiar-los al sandbox."""
    r = sh(["git", "ls-tree", "-r", "--name-only", ref], cwd=repo)
    out = []
    for p in r.stdout.splitlines():
        if TEST_PAT.search(p) or FIXTURE_PAT.search(p):
            out.append(p)
    return out


def run_tests(wt: Path, files: list[str], repo_name: str) -> tuple[int, int, str]:
    """Córrer els tests donats. Retorna (verds, total, output)."""
    if not files:
        return 0, 0, "(no test files)"
    # separem per runner (sense snapshots, fixtures ni conftest com a tests executables)
    runnable = [f for f in files
                if not f.endswith(".snap") and not f.endswith(".json")
                and not f.endswith("conftest.py")]
    py = [f for f in runnable if f.endswith(".py")]
    js = [f for f in runnable if not f.endswith(".py")]
    verds = total = 0
    out_parts = []
    if py:
        cmd = py_cmd(wt, ["-m", "pytest", "-q", "--no-header", "-x" if False else "--tb=no"] + py)
        r = sh(cmd, cwd=wt, timeout=300)
        out_parts.append(r.stdout[-3000:])
        m = re.search(r"(\d+) passed", r.stdout)
        p = int(m.group(1)) if m else 0
        m2 = re.search(r"(\d+) failed", r.stdout)
        f = int(m2.group(1)) if m2 else 0
        m3 = re.search(r"(\d+) error", r.stdout)
        e = int(m3.group(1)) if m3 else 0
        verds += p
        total += p + f + e
    if js:
        has_vitest = (wt / "vitest.config.ts").exists() or (wt / "vitest.config.mts").exists() \
            or (wt / "vitest.config.js").exists()
        if has_vitest:
            cmd = ["npx", "vitest", "run", "--reporter=default"] + js
        else:
            cmd = ["node", "--test"] + js
        r = sh(cmd, cwd=wt, timeout=300)
        out_parts.append(r.stdout[-3000:])
        # vitest: "N passed" / "Tests  N passed" ; node:test: "# pass N"
        m = re.search(r"Tests\s+(\d+)\s+passed", r.stdout) or re.search(r"(\d+)\s+passed", r.stdout)
        p = int(m.group(1)) if m else 0
        m2 = re.search(r"Tests\s+(\d+)\s+failed", r.stdout) or re.search(r"(\d+)\s+failed", r.stdout)
        f = int(m2.group(1)) if m2 else 0
        # node:test format: "# pass 3"
        if not p and not f:
            m3 = re.search(r"#\s+pass\s+(\d+)", r.stdout)
            m4 = re.search(r"#\s+fail\s+(\d+)", r.stdout)
            p = int(m3.group(1)) if m3 else 0
            f = int(m4.group(1)) if m4 else 0
        # vitest suma "passed" amb "skipped"? no — passed és només verds
        verds += p
        total += p + f
        # si vitest no va arrencar (startup error) i no hi ha comptes, marca 0/0 com a error
        if total == 0 and ("Startup Error" in r.stdout or r.returncode not in (0, 1)):
            out_parts.append(f"[vitest failed to start: rc={r.returncode}]")
    return verds, total, "\n".join(out_parts)


def parse_executor_files(text: str) -> dict[str, str]:
    """Parseja la sortida de l'executor.

    Suporta dos formats (els models varien):
      A) === FILE: path === \\n <contingut> \\n === END FILE ===   (el demanat)
      B) === FILE: path === \\n ```lang \\n <contingut> \\n ``` \\n següent FILE
         (el que realment emeten: sense END, amb fences markdown)
    També neteja fences de ``` que emboliquin el contingut.
    """
    files: dict[str, str] = {}
    # separa per marcadors de FILE (o END FILE com a tall)
    parts = re.split(r"===\s*FILE:\s*(.+?)\s*===", text)
    # parts[0] = prosa abans del primer FILE; després (path, body, path, body, ...)
    for i in range(1, len(parts), 2):
        path = parts[i].strip().lstrip("/")
        body = parts[i + 1] if i + 1 < len(parts) else ""
        # talla al següent END FILE si hi és
        body = re.split(r"===\s*END FILE\s*===", body)[0]
        # treu fences markdown ``` al voltant del contingut
        body = body.strip()
        body = re.sub(r"^```[\w]*\n", "", body)
        body = re.sub(r"\n```$", "", body)
        if path and not path.startswith("..") and body:
            files[path] = body
    return files


def apply_files(wt: Path, files: dict[str, str]) -> int:
    """Escriu els fitxers de l'executor al worktree. Retorna n escrits."""
    n = 0
    for rel, content in files.items():
        p = wt / rel
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            n += 1
        except (OSError, ValueError):
            continue
    return n


def copy_tests(wt: Path, repo: Path, ref: str) -> list[str]:
    """Copia els tests del ref al worktree (i retorna els paths copiats)."""
    files = test_files_at(repo, ref)
    for rel in files:
        r = sh(["git", "show", f"{ref}:{rel}"], cwd=repo)
        if r.returncode != 0:
            continue
        p = wt / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(r.stdout, encoding="utf-8")
    return files
