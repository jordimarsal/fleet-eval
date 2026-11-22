You are an implementer working from a plan. Write the EXACT files the plan asks for.

--- PLAN ---
# Tasks: f4_archive

- [x] T1: Implement archive.py (load/save idempotent, corrupt-tolerant) + tests
      depends_on: (none)
      refs: R1, R6
      evidence: harness/logs/f4_archive/batch-1.log

- [x] T2: POST /api/projects/{pid}/archive i /unarchive (404 desconegut, 202 idempotent) + tests
      depends_on: T1
      refs: R2, R3, R4
      evidence: harness/logs/f4_archive/batch-1.log

- [x] T3: camp archived a project_status (llista i detall) + tests
      depends_on: T1
      refs: R5
      evidence: harness/logs/f4_archive/batch-1.log

- [x] T4: UI tabs actius/arxivats amb comptadors + filtratge + tests estàtics
      depends_on: T3
      refs: R7, R9
      evidence: harness/logs/f4_archive/batch-1.log

- [x] T5: UI botons arxivar/desarxivar al drawer + tests estàtics
      depends_on: T4
      refs: R8
      evidence: harness/logs/f4_archive/batch-1.log

- [x] T6: Full gates green + e2e (arxivar → desapareix d'actius → desarxivar → torna) + review/traçabilitat
      depends_on: T1, T2, T3, T4, T5
      refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10
      evidence: harness/specs/f4_archive/review.md + harness/logs/f4_archive/batch-2.log


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
harness/progress/review_f1_scanner.md
harness/progress/review_f2_ui.md
harness/progress/review_f3_actions.md
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
harness/tools/audit-security.sh
harness/tools/check-traceability.py
harness/tools/validate-feature-list.py
opencode.json
pyproject.toml
scripts/e2e_actions_demo.py
src/atalaia/__init__.py
src/atalaia/actions.py
src/atalaia/api.py
src/atalaia/detail.py
src/atalaia/detectors.py
src/atalaia/ids.py
src/atalaia/models.py
src/atalaia/scanner.py
tests/test_actions.py
tests/test_api.py
tests/test_api_actions.py
tests/test_api_detail.py
tests/test_detail.py
tests/test_detectors.py
tests/test_ids.py
tests/test_scanner.py
tests/test_web.py
tests/test_web_static.py
uv.lock
web/app.js
web/index.html
web/style.css

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- harness/tools/check-traceability.py ---
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
--- web/app.js ---
const state = { items: [], selected: null, search: "", type: "", status: "" };

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

function applyFilters(items) {
  return items.filter((p) => {
    if (state.status && p.status !== state.status) return false;
    if (state.type && p.type !== state.type) return false;
    const needle = state.search.toLowerCase();
    if (needle && !p.name.toLowerCase().includes(needle) && !p.path.toLowerCase().includes(needle)) return false;
    return true;
  });
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
    select.appendChild(el("option", "", kind)).value = kind;
  }
  if (kinds.includes(current)) select.value = current;
}

function renderTable() {
  const tbody = document.getElementById("rows");
  tbody.textContent = "";
  const visible = applyFilters(state.items);
  document.getElementById("empty").classList.toggle("hidden", visible.length > 0);

  for (const p of visible) {
    const tr = el("tr");
    tr.tabIndex = 0;
    tr.dataset.id = p.id;
    if (p.id === state.selected) tr.classList.add("selected");

    const statusTd = el("td");
--- tests/test_scanner.py ---
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

--- harness/tools/validate-feature-list.py ---
#!/usr/bin/env python3
"""Validate a harness feature_list.json against Protocol v1 rules.

The JSON Schema (templates/feature_list.schema.json) is the documented
contract; this script enforces the same rules with the stdlib only — no
jsonschema dependency on installed projects.

Usage: validate-feature-list.py [--json] <feature-list.json>
Exit codes: 0 valid, 1 invalid, 2 usage error.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections.abc import Callable

STATUSES = ("pending", "spec_ready", "in_progress", "blocked", "done")
AUDIT_LEVELS = ("basic", "standard", "strict")
NAME_RE = re.compile(r"^[a-z0-9_]+$")


def parse_args(argv: list[str]) -> "tuple[bool, str] | int":
    """Parse CLI flags; return (as_json, path) or exit code 2."""
    as_json = False
    path: str | None = None
    for a in argv:
        if a == "--json":
            as_json = True
        elif a.startswith("-"):
            print(f"unknown argument: {a}", file=sys.stderr)
            return 2
        else:
            if path is not None:
                print(
                    "usage: validate-feature-list.py [--json] <feature-list.json>",
                    file=sys.stderr,
                )
                return 2
            path = a
    if path is None:
        print("usage: validate-feature-list.py [--json] <feature-list.json>", file=sys.stderr)
        return 2
    return as_json, path


def _validate_project_section(data: dict, err: "Callable[[str, str, str], None]") -> None:
    project = data.get("project")
    if not isinstance(project, dict):
        err("project", "missing", "project section is required")
        return
    name = project.get("name")
    if not isinstance(name, str) or not name:
        err("project.name", "missing", "project.name must be a non-empty string")
    if not isinstance(project.get("parallel"), bool):
        err("project.parallel", "invalid_type", "project.parallel must be a boolean")
    modules = project.get("modules")
    if not isinstance(modules, list) or not all(isinstance(m, str) for m in modules):
--- src/atalaia/api.py ---
import subprocess
from collections.abc import Callable
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .actions import KNOWN_ACTIONS, declared_actions, run_action
from .actions import action_log_tail, declared_actions
from .detectors import docker_ports, probe_docker, probe_port, probe_process
from .detail import ps_lines, read_readme, tail_log, uptime_from_lines, uptime_seconds, git_info
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
) -> dict:
    docker = probe_docker(project)
    open_port = probe_port(project.port or docker_port)
    process = probe_process(project)
    alive = docker == "up" or open_port or process == "up"
    return {
        "id": project_id(project.path),
        "name": project.name,
        "path": str(project.path),
        "type": project.kind,
        "status": "up" if alive else "down",
        "port": project.port or docker_port or scan_port,
        "uptime": uptime,
        "protected": project.protected,
    }


def detail_payload(project: Project, docker_port: int | None = None, scan_port: int | None = None) -> dict:
    payload = project_status(project, uptime=uptime_seconds(project), docker_port=docker_port, scan_port=scan_port)
    payload["git"] = git_info(project)
    payload["readme"] = read_readme(project)
    payload["log"] = tail_log(project)
    payload["actions"] = declared_actions(project)
    payload["action_log"] = action_log_tail(project)
    return payload


class NoCacheStaticFiles(StaticFiles):
    def file_response(self, *args, **kwargs):
        response = super().file_response(*args, **kwargs)
--- src/atalaia/scanner.py ---
from pathlib import Path
import re

from .models import Project, is_protected


MIN_PY_FILES = 3


EXCLUDED_DIR_NAMES = {"node_modules", "venv", "__pycache__", "build", "dist", "target", "bck"}


def _has_python_files(project_dir: Path) -> bool:
    return sum(1 for p in project_dir.glob("*.py") if p.is_file()) >= MIN_PY_FILES


def detect_kind(project_dir: Path) -> str | None:
    if (project_dir / "docker-compose.yml").exists() or (project_dir / "docker-compose.yaml").exists():
        return "compose"
    if (project_dir / "package.json").exists():
        return "node"
    if (project_dir / "pom.xml").exists():
        return "java"
    if (project_dir / "CMakeLists.txt").exists():
        return "cpp"
    if (project_dir / "pyproject.toml").exists():
        return "python"
    if _has_python_files(project_dir):
        return "python"
    if next(project_dir.glob("run-*.sh"), None) is not None:
        return "script"
    if (project_dir / "dashboard.yaml").exists():
        return "custom"
    return None


MAX_SCAN_DEPTH = 3


def _project_from(child: Path) -> Project | None:
    kind = detect_kind(child)
    if kind is None:
        return None
    return Project(
        name=child.name,
        path=child,
        kind=kind,
        port=valid_port(load_descriptor(child).get("port")),
        protected=is_protected(child),
    )


def discover_projects(roots: list[Path]) -> list[Project]:
    found: list[Project] = []
    for root in roots:
        if not root.is_dir():
            continue
        found.extend(_scan_dir(root, depth=MAX_SCAN_DEPTH))
    return found

--- tests/test_api_actions.py ---
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import atalaia.api as api_module
import atalaia.actions as actions_module
from atalaia.actions import action_log_path
from atalaia.api import create_app
from atalaia.models import Project


@pytest.fixture(autouse=True)
def isolated_state(monkeypatch, tmp_path):
    monkeypatch.setattr(actions_module, "STATE_DIR", tmp_path / "state")
    return tmp_path / "state"


def project(tmp_path, name="app", start=None, stop=None, protected=False):
    tmp_path.mkdir(parents=True, exist_ok=True)
    lines = []
    if start:
        lines.append(f"start: {start!r}")
    if stop:
        lines.append(f"stop: {stop!r}")
    if lines:
        (tmp_path / "dashboard.yaml").write_text("\n".join(lines) + "\n")
    return Project(name=name, path=tmp_path, kind="node", port=None, protected=protected)


def client_for(*projects):
    return TestClient(create_app(discover=lambda roots: list(projects)))


def test_start_launches_202(tmp_path):
    app = project(tmp_path / "app", start="true")
    from atalaia.ids import project_id

    response = client_for(app).post(f"/api/projects/{project_id(app.path)}/start")
    assert response.status_code == 202
    body = response.json()
    assert body["status"] == "launched"
    assert isinstance(body["pid"], int)
    assert action_log_path(app).parent.is_dir()


def test_stop_returns_exit(tmp_path):
    app = project(tmp_path / "app", stop="true")
    from atalaia.ids import project_id

    response = client_for(app).post(f"/api/projects/{project_id(app.path)}/stop")
    assert response.status_code == 200
    assert response.json() == {"status": "stopped", "exit": 0}


def test_undeclared_action_404(tmp_path):
    app = project(tmp_path / "app", start="true")
    from atalaia.ids import project_id

    response = client_for(app).post(f"/api/projects/{project_id(app.path)}/stop")
--- tests/test_api_detail.py ---
import subprocess
from pathlib import Path

from fastapi.testclient import TestClient

import atalaia.actions as actions_module
from atalaia.api import create_app
from atalaia.ids import project_id
from atalaia.models import Project


def make_repo(tmp_path):
    tmp_path.mkdir(parents=True)
    (tmp_path / "README.md").write_text("# repo test\n")
    run = lambda *args, **kwargs: subprocess.run(*args, **kwargs, capture_output=True, text=True, cwd=tmp_path)
    run(["git", "init", "-q"])
    run(["git", "config", "user.email", "t@t"])
    run(["git", "config", "user.name", "t"])
    (tmp_path / "f.txt").write_text("x")
    run(["git", "add", "."])
    run(["git", "commit", "-q", "-m", "init commit"])
    return tmp_path


def make_app(tmp_path):
    repo = make_repo(tmp_path / "repo")
    projects = [
        Project(name="repo", path=repo, kind="python", port=None, protected=False),
        Project(name="web", path=tmp_path.parent / "web", kind="node", port=3000, protected=False),
    ]
    return TestClient(create_app(discover=lambda roots: projects))


def test_detail_returns_git_readme_uptime_log(tmp_path):
    response = make_app(tmp_path).get(f"/api/projects/{project_id(tmp_path / 'repo')}")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "repo"
    assert body["git"]["branch"] in ("main", "master")
    assert body["git"]["commit"]["message"] == "init commit"
    assert body["readme"] == "# repo test\n"
    assert body["log"] == []
    assert body["uptime"] is None or isinstance(body["uptime"], int)
    assert body["actions"] == []
    assert body["action_log"] == []


def test_unknown_id_is_404(tmp_path):
    response = make_app(tmp_path).get("/api/projects/" + "0" * 12)
    assert response.status_code == 404
    assert response.json() == {"detail": "unknown project"}


def test_non_hex_id_is_404(tmp_path):
    response = make_app(tmp_path).get("/api/projects/../../etc/passwd")
    assert response.status_code == 404


def test_list_includes_id_and_uptime_fields(tmp_path):
    response = make_app(tmp_path).get("/api/projects")

Output ONLY the files, each in this format:

=== FILE: relative/path.ext ===
<file contents>
=== END FILE ===

No prose outside the file blocks. Do not invent extra files beyond what the plan asks.