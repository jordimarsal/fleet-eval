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
R1: The system shall persist the set of archived project ids in a file under the user's state directory, surviving server restarts.

R2: WHEN a client requests `POST /api/projects/{id}/archive`, the system shall add the id to the archived set and respond 202; archiving an already archived project shall succeed without error.

R3: WHEN a client requests `POST /api/projects/{id}/unarchive`, the system shall remove the id from the archived set and respond 202; unarchiving a non-archived project shall succeed without error.

R4: IF the id is unknown, THEN the system shall respond 404 for archive and unarchive requests.

R5: The system shall include an `archived` boolean in every project payload returned by the list and detail endpoints.

R6: WHEN the state file is missing or malformed, the system shall treat the archived set as empty and continue working.

R7: The UI shall show two tabs — actius and arxivats — with counts, hiding archived projects from the actius tab and non-archived ones from the arxivats tab.

R8: The UI shall offer an arxivar action in the detail drawer of every non-archived project and a desarxivar action for every archived one.

R9: WHEN the archive state changes, the UI shall reflect the new tab assignment immediately after the next refresh.

R10: The system shall not modify any file inside the scanned project trees to store archive state.

--- FEATURE TITLE ---
f4_archive done (APPROVAL) + tancament de sessio

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
web/app.js
web/index.html
web/style.css

--- KEY SOURCE FILES (before implementation, excerpts) ---
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
--- web/app.js (first 60 lines of 8432 bytes) ---
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

--- harness/tools/validate-feature-list.py (first 60 lines of 6665 bytes) ---
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
--- web/style.css (first 60 lines of 5813 bytes) ---
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
--- src/atalaia/api.py (first 60 lines of 5535 bytes) ---
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
--- harness/init.sh (first 60 lines of 5019 bytes) ---
#!/usr/bin/env bash
# init-verify.sh — Project verification script
#
# This script is copied to harness/init.sh during harness installation.
# Run from the project root: ./harness/init.sh
# Run at session start and before marking any feature as done.

set -u
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ok()    { printf "${GREEN}[OK]${NC}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$1"; }
fail()  { printf "${RED}[FAIL]${NC}  %s\n" "$1"; }

EXIT_CODE=0

echo "── 1. Checking harness files ──────────────────────────"

# Entry point + tool directory at the project root (claude or opencode)
if [ -f "CLAUDE.md" ]; then
  ok "Exists CLAUDE.md"
elif [ -f "AGENTS.md" ]; then
  ok "Exists AGENTS.md"
else
  fail "Missing entry point: CLAUDE.md or AGENTS.md"
  EXIT_CODE=1
fi

if [ -d ".claude" ] || [ -d ".opencode" ]; then
  ok "Exists .claude/ or .opencode/"
else
  fail "Missing tool directory: .claude/ or .opencode/"
  EXIT_CODE=1
fi

for f in harness/CHECKPOINTS.md harness/feature_list.json harness/progress/current.md docs/architecture.md docs/conventions.md docs/verification.md docs/specs.md; do
  if [ ! -f "$f" ]; then
    fail "Missing base file: $f"
    EXIT_CODE=1
  else
    ok "Exists $f"
  fi
done

if [ -d "harness/specs" ]; then
  ok "Exists harness/specs/"
else
  fail "Missing directory: harness/specs/"
  EXIT_CODE=1
fi

echo ""
echo "── 2. Validating harness/feature_list.json ────────────"

if command -v python3 >/dev/null 2>&1; then
  python3 - <<'PY' || EXIT_CODE=1
import json, os, sys

Write ONLY the plan (the three sections). No prose outside them.