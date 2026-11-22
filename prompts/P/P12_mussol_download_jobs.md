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
R1: The downloads module shall expose a `JobStatus` enum with `queued`, `downloading`, `transcoding`, `completed`, and `failed` members.

R2: The system shall change a `DownloadJob` state only through behavior methods that return `Result` and reject invalid transitions.

R3: When a URL is submitted, the system shall create one queued job per resolved track.

R4: When a queued job runs, the system shall drive it through download, transcode, and store stages, updating its status at each stage, and any stage failure shall mark the job failed without escaping as an exception.

R5: The system shall expose job submission, listing, and detail over HTTP with DTOs, and errors shall follow `problem+json`.

R6: The system shall serve HTTP bound to `127.0.0.1` only.

R7: The system shall track per-job progress between 0 and 100 across the pipeline stages.

R8: When a submitted URL is not supported, the system shall return the typed error and create no jobs.

--- FEATURE TITLE ---
feat(jobs): run submitted jobs automatically and survive restarts

--- REPOSITORY FILE TREE (before implementation) ---
.gitignore
.opencode/agent/implementer.md
.opencode/agent/leader.md
.opencode/agent/reviewer.md
.opencode/agent/spec-author.md
AGENTS.md
HARNESS.md
README.md
docs/architecture.md
docs/conventions.md
docs/log-reader-protocol.md
docs/specs.md
docs/verification.md
harness/CHECKPOINTS.md
harness/decisions/0001-process-runner-lives-in-shared.md
harness/decisions/_template.md
harness/feature_list.json
harness/init.sh
harness/progress/current.md
harness/progress/history.md
harness/progress/impl_app_launcher.md
harness/progress/impl_audio_extract.md
harness/progress/impl_download_jobs.md
harness/progress/impl_library_store.md
harness/progress/impl_project_foundation.md
harness/progress/impl_spotify_lists.md
harness/progress/impl_web_frontend.md
harness/progress/impl_youtube_mix_lists.md
harness/progress/impl_youtube_source.md
harness/specs/app_launcher/APPROVAL
harness/specs/app_launcher/design.md
harness/specs/app_launcher/requirements.md
harness/specs/app_launcher/tasks.md
harness/specs/audio_extract/APPROVAL
harness/specs/audio_extract/design.md
harness/specs/audio_extract/requirements.md
harness/specs/audio_extract/tasks.md
harness/specs/download_jobs/APPROVAL
harness/specs/download_jobs/design.md
harness/specs/download_jobs/requirements.md
harness/specs/download_jobs/tasks.md
harness/specs/library_store/APPROVAL
harness/specs/library_store/design.md
harness/specs/library_store/requirements.md
harness/specs/library_store/tasks.md
harness/specs/project_foundation/APPROVAL
harness/specs/project_foundation/design.md
harness/specs/project_foundation/requirements.md
harness/specs/project_foundation/tasks.md
harness/specs/spotify_lists/APPROVAL
harness/specs/spotify_lists/design.md
harness/specs/spotify_lists/requirements.md
harness/specs/spotify_lists/tasks.md
harness/specs/web_frontend/APPROVAL
harness/specs/web_frontend/design.md
harness/specs/web_frontend/requirements.md
harness/specs/web_frontend/tasks.md
harness/specs/youtube_mix_lists/APPROVAL
harness/specs/youtube_mix_lists/design.md
harness/specs/youtube_mix_lists/requirements.md
harness/specs/youtube_mix_lists/tasks.md
harness/specs/youtube_source/APPROVAL
harness/specs/youtube_source/design.md
harness/specs/youtube_source/requirements.md
harness/specs/youtube_source/tasks.md
harness/tools/audit-security.sh
harness/tools/check-traceability.py
harness/tools/scan.py
harness/tools/validate-feature-list.py
main.py
opencode.json
pyproject.toml
src/mussol/__init__.py
src/mussol/api/__init__.py
src/mussol/api/app.py
src/mussol/api/dtos.py
src/mussol/audio/__init__.py
src/mussol/audio/audio_file.py
src/mussol/audio/audio_format.py
src/mussol/audio/builder.py
src/mussol/audio/errors.py
src/mussol/audio/extractor.py
src/mussol/audio/profile.py
src/mussol/launcher.py
src/mussol/library/__init__.py
src/mussol/library/errors.py
src/mussol/library/library_record.py
src/mussol/library/store.py
src/mussol/shared/__init__.py
src/mussol/shared/process.py
src/mussol/shared/result.py
src/mussol/sources/__init__.py
src/mussol/sources/errors.py
src/mussol/sources/runner.py
src/mussol/sources/source_type.py
src/mussol/sources/spotify.py
src/mussol/sources/track.py
src/mussol/sources/value_objects.py
src/mussol/sources/youtube.py
tests/test_api.py
tests/test_audio_extractor.py
tests/test_audio_format.py
tests/test_audio_profile.py
tests/test_download_job.py
tests/test_download_service.py
tests/test_ffmpeg_builder.py
tests/test_launcher.py
tests/test_library_record.py
tests/test_library_store.py
tests/test_module_boundaries.py
tests/test_package.py
tests/test_quality_gates.py
tests/test_result.py
tests/test_source_types.py
tests/test_source_url.py
tests/test_spotify_adapter.py
tests/test_web.py
tests/test_youtube_adapter.py
tests/test_youtube_download.py
web/app.js
web/index.html
web/styles.css

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- harness/tools/scan.py (first 60 lines of 13089 bytes) ---
#!/usr/bin/env python3
"""Deterministic project scanner (harness project-scanner module).

v1 scope: Python AST analysis plus a generic file-count fallback.
The project is parsed exactly once; all queries are answered from indexes.

Usage (from the project root):
  python3 harness/tools/scan.py --summary          Project overview (default)
  python3 harness/tools/scan.py --impact FILE      Impact analysis for one file
  python3 harness/tools/scan.py --duplicates       Symbols defined in 2+ modules
  python3 harness/tools/scan.py --style [N]        Style sample of N files (default 3)
  python3 harness/tools/scan.py --root DIR         Scan a different root

Exit codes: 0 ok, 2 usage error.
"""

from __future__ import annotations

import ast
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

EXCLUDED_DIRS = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", "__pycache__",
    "node_modules", ".tox", ".mypy_cache", ".pytest_cache",
    "build", "dist", ".harness", "harness",
}
REGION_RE = re.compile(r"#\s*region\s+(.+)")


@dataclass
class SourceFile:
    path: Path  # relative to the project root
    module: str  # dotted module name, e.g. "core.models"
    imports: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    docstring: str | None = None
    entry_point: bool = False
    regions: list[str] = field(default_factory=list)
    dependencies: set[str] = field(default_factory=set)  # resolved relative paths


class Scanner:
    """Parses every Python file once, then serves queries from dict indexes."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.files: list[SourceFile] = []
        self._by_module: dict[str, SourceFile] = {}
        self._dependents: dict[str, set[str]] = {}

    def scan(self) -> None:
        for p in self.root.rglob("*.py"):
            if set(p.parts) & EXCLUDED_DIRS:
                continue
            sf = self._parse(p)
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
--- harness/tools/check-traceability.py (first 60 lines of 7837 bytes) ---
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


ATTR_RE = re.compile(r"(?im)^\s*feature\s*:\s*([A-Za-z0-9_-]+)\s*$")


def collect_tables(
    root: Path, feature: str | None = None
) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Merge only those impl_*.md tables attributed to `feature` (protocol v1.1)."""
    merged: dict[str, list[str]] = {}
    statuses: dict[str, str] = {}
    progress = root / "harness" / "progress"
    if not progress.is_dir():
        return merged, statuses
    for impl in sorted(progress.glob("impl_*.md")):
        text = impl.read_text(encoding="utf-8")
        owner = ATTR_RE.search(text)
        if owner is None:
            if feature is not None:
                statuses.setdefault("__unattributed__", impl.name)
            continue
        if feature is not None and owner.group(1) != feature:
            continue
        for line in text.splitlines():
--- src/mussol/sources/youtube.py (first 60 lines of 7121 bytes) ---
"""YouTube source adapter: classification and metadata resolution."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from mussol.shared.result import Err, Ok, Result
from mussol.sources.errors import DownloadFailed, UnsupportedSource
from mussol.sources.runner import BackendRunner
from mussol.sources.source_type import SourceType
from mussol.sources.track import TrackDescriptor
from mussol.sources.value_objects import SourceUrl, TrackTitle


class YouTubeKind(Enum):
    VIDEO = "video"
    PLAYLIST = "playlist"


@dataclass(frozen=True)
class YouTubeRef:
    kind: YouTubeKind
    video_id: str | None
    playlist_id: str | None

    def __post_init__(self) -> None:
        if self.kind is YouTubeKind.VIDEO and not self.video_id:
            raise ValueError("YouTubeRef of kind video requires a video_id")
        if self.kind is YouTubeKind.PLAYLIST and not self.playlist_id:
            raise ValueError("YouTubeRef of kind playlist requires a playlist_id")

    def describe(self) -> str:
        if self.kind is YouTubeKind.PLAYLIST:
            return f"https://www.youtube.com/playlist?list={self.playlist_id}"
        return f"https://www.youtube.com/watch?v={self.video_id}"


_YOUTUBE_HOSTS = frozenset(
    {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "music.youtube.com",
        "youtu.be",
    }
)

_UNVIEWABLE_LIST_PREFIXES = ("RD",)
_UNVIEWABLE_LISTS = frozenset({"WL", "LL"})


def _is_unviewable(playlist_id: str) -> bool:
    return playlist_id in _UNVIEWABLE_LISTS or playlist_id.startswith(_UNVIEWABLE_LIST_PREFIXES)


class YoutubeAdapter:
--- tests/test_youtube_adapter.py (first 60 lines of 6396 bytes) ---
"""YouTube adapter: classification of URLs into typed references."""

import json
import sys

import pytest

from mussol.sources.errors import DownloadFailed, UnsupportedSource
from mussol.sources.runner import BackendResult, BackendRunner, SubprocessRunner
from mussol.sources.source_type import SourceType
from mussol.sources.value_objects import SourceUrl
from mussol.sources.youtube import YoutubeAdapter, YouTubeKind


@pytest.mark.parametrize(
    ("raw", "kind", "video_id", "playlist_id"),
    [
        (
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            YouTubeKind.VIDEO,
            "dQw4w9WgXcQ",
            None,
        ),
        (
            "https://music.youtube.com/watch?v=dQw4w9WgXcQ",
            YouTubeKind.VIDEO,
            "dQw4w9WgXcQ",
            None,
        ),
        ("https://youtu.be/dQw4w9WgXcQ", YouTubeKind.VIDEO, "dQw4w9WgXcQ", None),
        (
            "https://www.youtube.com/shorts/dQw4w9WgXcQ",
            YouTubeKind.VIDEO,
            "dQw4w9WgXcQ",
            None,
        ),
        (
            "https://www.youtube.com/playlist?list=PLABC123",
            YouTubeKind.PLAYLIST,
            None,
            "PLABC123",
        ),
        (
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLABC123",
            YouTubeKind.PLAYLIST,
            "dQw4w9WgXcQ",
            "PLABC123",
        ),
        (
            "https://www.youtube.com/watch?v=WIgPGiHfBBc&list=RDMM&start_radio=1",
            YouTubeKind.VIDEO,
            "WIgPGiHfBBc",
            None,
        ),
        (
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDabc123",
            YouTubeKind.VIDEO,
            "dQw4w9WgXcQ",
            None,
        ),
--- harness/tools/validate-feature-list.py (first 60 lines of 6135 bytes) ---
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

STATUSES = ("pending", "spec_ready", "in_progress", "blocked", "done")
AUDIT_LEVELS = ("basic", "standard", "strict")
NAME_RE = re.compile(r"^[a-z0-9_]+$")


def main(argv: list[str]) -> int:
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

    errors: list[dict[str, str]] = []

    def err(path_in_doc: str, code: str, message: str) -> None:
        errors.append({"path": path_in_doc, "code": code, "message": message})

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"file not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        err("", "invalid_json", f"not valid JSON: {e}")
        data = None

    if isinstance(data, dict):
--- tests/test_download_service.py (first 60 lines of 5539 bytes) ---
"""DownloadService: fan-out, staged runs, and failure marking."""

import json
from pathlib import Path

from mussol.audio.audio_format import AudioFormat
from mussol.audio.extractor import AudioExtractor
from mussol.downloads.errors import JobNotFound
from mussol.downloads.job import JobId
from mussol.downloads.job_status import JobStatus
from mussol.downloads.service import DownloadService
from mussol.library.store import LibraryStore
from mussol.shared.process import BackendResult, BackendRunner
from mussol.sources.errors import DownloadFailed, UnsupportedSource
from mussol.sources.value_objects import SourceUrl
from mussol.sources.youtube import YoutubeAdapter


class ScriptedRunner:
    """Simulates yt-dlp and ffmpeg by materializing their outputs."""

    def __init__(self, metadata: object) -> None:
        self._metadata = metadata
        self.calls: list[list[str]] = []

    def metadata_response(self) -> BackendResult:
        return BackendResult(returncode=0, stdout=json.dumps(self._metadata), stderr="")

    def run(self, argv: list[str]) -> BackendResult:
        self.calls.append(argv)
        if "--dump-single-json" in argv:
            return self.metadata_response()
        if "-o" in argv:
            template = argv[argv.index("-o") + 1]
            Path(template.replace("%(ext)s", "webm")).write_bytes(b"media")
        else:
            Path(argv[-1]).write_bytes(b"audio")
        return BackendResult(returncode=0, stdout="", stderr="")


class DownloadFailingRunner(ScriptedRunner):
    def run(self, argv: list[str]) -> BackendResult:
        self.calls.append(argv)
        if "--dump-single-json" in argv:
            return self.metadata_response()
        return BackendResult(returncode=1, stdout="", stderr="boom")


def _service(tmp_path: Path, runner: BackendRunner) -> DownloadService:
    media = tmp_path / "media"
    media.mkdir(exist_ok=True)
    return DownloadService(
        adapter=YoutubeAdapter(),
        extractor=AudioExtractor(),
        store=LibraryStore(db_path=tmp_path / "lib.db", media_root=media),
        download_runner=runner,
        transcode_runner=runner,
        media_root=media,
    )

--- src/mussol/library/store.py (first 60 lines of 5205 bytes) ---
"""SQLite-backed library owned exclusively by this module."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from mussol.audio.audio_format import AudioFormat
from mussol.library.errors import (
    InvalidFilename,
    LibraryError,
    RecordNotFound,
    StorageError,
)
from mussol.library.library_record import LibraryRecord
from mussol.shared.result import Err, Ok, Result
from mussol.sources.source_type import SourceType

_SCHEMA = """CREATE TABLE IF NOT EXISTS library_records (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL,
  source_id TEXT NOT NULL,
  title TEXT NOT NULL,
  format TEXT NOT NULL,
  path TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE (source, source_id, format)
)"""

_COLUMNS = "id, source, source_id, title, format, path, created_at"


class LibraryStore:
    def __init__(self, db_path: Path, media_root: Path) -> None:
        self._db_path = db_path
        self._media_root = media_root

    def save_new(
        self,
        source: SourceType,
        source_id: str,
        title: str,
        format: AudioFormat,
        filename: str,
    ) -> Result[LibraryRecord, LibraryError]:
        resolved = self._resolve_filename(filename)
        if resolved.is_err():
            return Err(resolved.unwrap_err())
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(_SCHEMA)
                row = conn.execute(
                    f"SELECT {_COLUMNS} FROM library_records "
                    "WHERE source = ? AND source_id = ? AND format = ?",
                    (source.value, source_id, format.value),
                ).fetchone()
                if row is not None:
                    return Ok(self._to_record(row))

Write ONLY the plan (the three sections). No prose outside them.