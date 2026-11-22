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
R1: Each library record shall persist an interpreter (artist), resolved from the catalogue lookup, from the tags already embedded in the audio file, or from the title pattern, in that order.

R2: Each item exposed over `GET /library` shall carry its interpreter, and the card shall show it.

R3: The panel shall allow filtering the list by interpreter with a text query.

R4: The panel shall allow sorting by title, interpreter or date added, with an ascending/descending direction.

R5: Filtering and sorting shall survive the polling refreshes.

--- FEATURE TITLE ---
close(interpreter_filter_sort): traceability table and R1 coverage

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
harness/progress/impl_backfill_enrichment.md
harness/progress/impl_cover_thumbnails.md
harness/progress/impl_delete_library_media.md
harness/progress/impl_download_jobs.md
harness/progress/impl_job_execution.md
harness/progress/impl_legacy_path_migration.md
harness/progress/impl_library_grouping.md
harness/progress/impl_library_panel.md
harness/progress/impl_library_render_reconciliation.md
harness/progress/impl_library_store.md
harness/progress/impl_list_folders.md
harness/progress/impl_list_pause_resume.md
harness/progress/impl_media_playback.md
harness/progress/impl_media_tags.md
harness/progress/impl_metadata_enrichment.md
harness/progress/impl_missing_cover_fetch.md
harness/progress/impl_panel_layout_fix.md
harness/progress/impl_project_foundation.md
harness/progress/impl_shared_cover_cache_fix.md
harness/progress/impl_spotify_lists.md
harness/progress/impl_titled_media_files.md
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
harness/specs/backfill_enrichment/APPROVAL
harness/specs/backfill_enrichment/design.md
harness/specs/backfill_enrichment/requirements.md
harness/specs/backfill_enrichment/tasks.md
harness/specs/cover_thumbnails/APPROVAL
harness/specs/cover_thumbnails/design.md
harness/specs/cover_thumbnails/requirements.md
harness/specs/cover_thumbnails/tasks.md
harness/specs/delete_library_media/APPROVAL
harness/specs/delete_library_media/design.md
harness/specs/delete_library_media/requirements.md
harness/specs/delete_library_media/tasks.md
harness/specs/download_jobs/APPROVAL
harness/specs/download_jobs/design.md
harness/specs/download_jobs/requirements.md
harness/specs/download_jobs/tasks.md
harness/specs/interpreter_filter_sort/design.md
harness/specs/interpreter_filter_sort/requirements.md
harness/specs/interpreter_filter_sort/tasks.md
harness/specs/job_execution/APPROVAL
harness/specs/job_execution/design.md
harness/specs/job_execution/requirements.md
harness/specs/job_execution/tasks.md
harness/specs/legacy_path_migration/APPROVAL
harness/specs/legacy_path_migration/design.md
harness/specs/legacy_path_migration/requirements.md
harness/specs/legacy_path_migration/tasks.md
harness/specs/library_grouping/APPROVAL
harness/specs/library_grouping/design.md
harness/specs/library_grouping/requirements.md
harness/specs/library_grouping/tasks.md
harness/specs/library_panel/APPROVAL
harness/specs/library_panel/design.md
harness/specs/library_panel/requirements.md
harness/specs/library_panel/tasks.md
harness/specs/library_render_reconciliation/APPROVAL
harness/specs/library_render_reconciliation/design.md
harness/specs/library_render_reconciliation/requirements.md
harness/specs/library_render_reconciliation/tasks.md
harness/specs/library_store/APPROVAL
harness/specs/library_store/design.md
harness/specs/library_store/requirements.md
harness/specs/library_store/tasks.md
harness/specs/list_folders/APPROVAL
harness/specs/list_folders/design.md
harness/specs/list_folders/requirements.md
harness/specs/list_folders/tasks.md
harness/specs/list_pause_resume/APPROVAL
harness/specs/list_pause_resume/design.md
harness/specs/list_pause_resume/requirements.md
harness/specs/list_pause_resume/tasks.md
harness/specs/media_playback/APPROVAL
harness/specs/media_playback/design.md
harness/specs/media_playback/requirements.md
harness/specs/media_playback/tasks.md
harness/specs/media_tags/APPROVAL
harness/specs/media_tags/design.md
harness/specs/media_tags/requirements.md
harness/specs/media_tags/tasks.md
harness/specs/metadata_enrichment/APPROVAL
harness/specs/metadata_enrichment/design.md
harness/specs/metadata_enrichment/requirements.md
harness/specs/metadata_enrichment/tasks.md
harness/specs/missing_cover_fetch/APPROVAL
harness/specs/missing_cover_fetch/design.md
harness/specs/missing_cover_fetch/requirements.md
harness/specs/missing_cover_fetch/tasks.md
harness/specs/panel_layout_fix/APPROVAL
harness/specs/panel_layout_fix/design.md
harness/specs/panel_layout_fix/requirements.md
harness/specs/panel_layout_fix/tasks.md
harness/specs/project_foundation/APPROVAL
harness/specs/project_foundation/design.md
harness/specs/project_foundation/requirements.md
harness/specs/project_foundation/tasks.md
harness/specs/shared_cover_cache_fix/APPROVAL
harness/specs/shared_cover_cache_fix/design.md
harness/specs/shared_cover_cache_fix/requirements.md
harness/specs/shared_cover_cache_fix/tasks.md
harness/specs/spotify_lists/APPROVAL
harness/specs/spotify_lists/design.md
harness/specs/spotify_lists/requirements.md
harness/specs/spotify_lists/tasks.md
harness/specs/titled_media_files/APPROVAL
harness/specs/titled_media_files/design.md
harness/specs/titled_media_files/requirements.md
harness/specs/titled_media_files/tasks.md
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
src/mussol/metadata/__init__.py
src/mussol/metadata/catalog.py
src/mussol/metadata/cover.py
src/mussol/metadata/tagger.py
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
tests/fixtures/mb.json
tests/metadata_fixtures/silence.flac
tests/metadata_fixtures/silence.m4a
tests/metadata_fixtures/silence.mp3
tests/metadata_fixtures/silence.opus
tests/test_api.py
tests/test_audio_extractor.py
tests/test_audio_format.py
tests/test_audio_profile.py
tests/test_catalog.py
tests/test_download_job.py
tests/test_download_service.py
tests/test_ffmpeg_builder.py
tests/test_job_store.py
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
tests/test_tagger.py
tests/test_web.py
tests/test_youtube_adapter.py
tests/test_youtube_download.py
web/app.js
web/index.html
web/styles.css

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- tests/test_download_service.py (first 60 lines of 20091 bytes) ---
"""DownloadService: fan-out, staged runs, and failure marking."""

import json
from pathlib import Path

from mussol.audio.audio_format import AudioFormat
from mussol.audio.extractor import AudioExtractor
from mussol.downloads.errors import (
    CoverAlreadyPresent,
    CoverUnavailable,
    EnrichmentFailed,
    EnrichmentSkipped,
    JobNotFound,
    ListNotFound,
)
from mussol.downloads.job import JobId
from mussol.downloads.job_status import JobStatus
from mussol.downloads.job_store import JobStore
from mussol.downloads.service import DownloadService
from mussol.library.store import LibraryStore
from mussol.shared.process import BackendResult, BackendRunner
from mussol.shared.result import Ok
from mussol.sources.errors import DownloadFailed, UnsupportedSource
from mussol.sources.source_type import SourceType
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
            media = Path(template.replace("%(ext)s", "webm"))
            media.write_bytes(b"media")
            thumbnail = Path(template.replace("%(ext)s", "jpg"))
            thumbnail.write_bytes(b"thumbnail")
            return BackendResult(returncode=0, stdout=f"{media}\n", stderr="")
        Path(argv[-1]).write_bytes(b"audio")
        return BackendResult(returncode=0, stdout="", stderr="")


class DownloadFailingRunner(ScriptedRunner):
    def run(self, argv: list[str]) -> BackendResult:
        self.calls.append(argv)
        if "--dump-single-json" in argv:
            return self.metadata_response()
        return BackendResult(returncode=1, stdout="", stderr="boom")

--- tests/test_api.py (first 60 lines of 17763 bytes) ---
"""API boundary: full request/response cycles through TestClient."""

import json
import sqlite3
import threading
import time
from pathlib import Path

from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from mussol.api.app import LOCALHOST, create_app, serve
from mussol.audio.audio_format import AudioFormat
from mussol.audio.extractor import AudioExtractor
from mussol.downloads.job import DownloadJob
from mussol.downloads.job_status import JobStatus
from mussol.downloads.job_store import JobStore
from mussol.downloads.service import DownloadService
from mussol.library.store import LibraryStore
from mussol.shared.process import BackendResult
from mussol.sources.source_type import SourceType
from mussol.sources.track import TrackDescriptor
from mussol.sources.value_objects import TrackTitle
from mussol.sources.youtube import YoutubeAdapter


class StubRunner:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def run(self, argv: list[str]) -> BackendResult:
        self.calls.append(argv)
        if "--dump-single-json" in argv:
            payload = {"entries": [{"id": "aaa", "title": "song"}]}
            return BackendResult(returncode=0, stdout=json.dumps(payload), stderr="")
        if "-o" in argv:
            template = argv[argv.index("-o") + 1]
            media = Path(template.replace("%(ext)s", "webm"))
            media.write_bytes(b"media")
            Path(template.replace("%(ext)s", "jpg")).write_bytes(b"thumbnail")
            return BackendResult(returncode=0, stdout=f"{media}\n", stderr="")
        Path(argv[-1]).write_bytes(b"audio")
        return BackendResult(returncode=0, stdout="", stderr="")


def _service(tmp_path: Path) -> DownloadService:
    media = tmp_path / "media"
    media.mkdir(exist_ok=True)
    runner = StubRunner()
    return DownloadService(
        adapter=YoutubeAdapter(),
        extractor=AudioExtractor(),
        store=LibraryStore(db_path=tmp_path / "lib.db", media_root=media),
        job_store=JobStore(tmp_path / "jobs.db"),
        download_runner=runner,
        transcode_runner=runner,
        media_root=media,
    )


--- web/app.js (first 60 lines of 14534 bytes) ---
"use strict";

const POLL_INTERVAL_MS = 2000;

const form = document.getElementById("job-form");
const urlInput = document.getElementById("source-url");
const formatPicker = document.getElementById("format-picker");
const submitButton = document.getElementById("submit-job");
const errorSummary = document.getElementById("error-summary");
const urlError = document.getElementById("source-url-error");
const formatError = document.getElementById("format-error");
const jobList = document.getElementById("job-list");
const jobsEmpty = document.getElementById("jobs-empty");
const downloadList = document.getElementById("download-list");
const downloadsEmpty = document.getElementById("downloads-empty");
let listsByName = {};
let activeTag = null;
let activeArtistQuery = "";
let sortKey = "created_at";
let sortDirection = "asc";
let renderedKeys = [];
let lastJobsSignature = "";
const rowsById = new Map();
const headersByName = new Map();

function selectedFormat() {
  const checked = formatPicker.querySelector("input[name='format']:checked");
  return checked ? checked.value : "";
}

function validate() {
  const messages = [];
  if (urlInput.value.trim() === "") {
    messages.push("Enter a media URL.");
  }
  if (selectedFormat() === "") {
    messages.push("Choose an audio format.");
  }
  return messages;
}

function showFieldErrors() {
  urlError.textContent = "Enter a media URL.";
  urlError.hidden = urlInput.value.trim() !== "";
  formatError.textContent = "Choose an audio format.";
  formatError.hidden = selectedFormat() !== "";
}

function showErrorSummary(messages) {
  errorSummary.textContent = "";
  const heading = document.createElement("p");
  heading.textContent = "There is a problem";
  errorSummary.appendChild(heading);
  const list = document.createElement("ul");
  for (const message of messages) {
    const item = document.createElement("li");
    item.textContent = message;
    list.appendChild(item);
  }
  errorSummary.appendChild(list);
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
--- src/mussol/library/store.py (first 60 lines of 12898 bytes) ---
"""SQLite-backed library owned exclusively by this module."""

from __future__ import annotations

import json
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
from mussol.library.library_record import LibraryRecord, decode_tags, to_relative
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

_COLUMNS = (
    "id, source, source_id, title, format, path, created_at, media_path, tags, enriched_at, artist"
)


class LibraryStore:
    def __init__(self, db_path: Path, media_root: Path) -> None:
        self._db_path = db_path
        self._media_root = media_root
        self._prepare_schema()

    def _prepare_schema(self) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(_SCHEMA)
            for column in ("media_path", "tags", "enriched_at", "artist"):
                try:
                    conn.execute(f"ALTER TABLE library_records ADD COLUMN {column} TEXT")
                except sqlite3.OperationalError:
                    pass
        self._migrate_legacy_paths()
        self._backfill_media_paths()

    def _backfill_media_paths(self) -> None:
        with sqlite3.connect(self._db_path) as conn:
            rows = conn.execute(
                "SELECT id, path FROM library_records WHERE media_path IS NULL"
            ).fetchall()
            for record_id, path in rows:
--- tests/test_library_store.py (first 60 lines of 10651 bytes) ---
"""LibraryStore: round-trip, idempotency, and missing records."""

import sqlite3
from pathlib import Path

import pytest

from mussol.audio.audio_format import AudioFormat
from mussol.library.errors import InvalidFilename, RecordNotFound
from mussol.library.store import LibraryStore
from mussol.sources.source_type import SourceType


def _store(tmp_path: Path) -> LibraryStore:
    return LibraryStore(db_path=tmp_path / "lib.db", media_root=tmp_path / "media")


def test_save_and_find_round_trip(tmp_path: Path) -> None:
    store = _store(tmp_path)

    saved = store.save_new(SourceType.YOUTUBE, "aaa", "first", AudioFormat.MP3, "first.mp3")

    assert saved.is_ok() is True
    record = saved.unwrap()
    assert record.path == Path("first.mp3")

    found = store.find(record.id)

    assert found.is_ok() is True
    assert found.unwrap() == record


def test_library_update_tags_round_trip(tmp_path: Path) -> None:
    store = _store(tmp_path)
    saved = store.save_new(
        SourceType.YOUTUBE, "aaa", "first", AudioFormat.MP3, "first.mp3"
    ).unwrap()

    updated = store.update_tags(saved.id, ("rock", "live"))

    assert updated.is_ok() is True
    assert updated.unwrap().tags == ("rock", "live")
    assert store.find(saved.id).unwrap().tags == ("rock", "live")


def test_library_update_tags_unknown_record(tmp_path: Path) -> None:
    result = _store(tmp_path).update_tags("ghost", ("rock",))

    assert result.is_err() is True
    assert isinstance(result.unwrap_err(), RecordNotFound)


def test_legacy_absolute_paths_migrate_to_relative(tmp_path: Path) -> None:
    db = tmp_path / "lib.db"
    media = tmp_path / "media"
    media.mkdir()
    LibraryStore(db, media)
    _insert_legacy(db, "legacy1", str(media / "Blade.mp3"), str(media / "Blade.webm"))

    store = LibraryStore(db, media)
--- src/mussol/api/app.py (first 60 lines of 10241 bytes) ---
"""Localhost HTTP boundary: DTOs in, problem+json out."""

import queue
import threading
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from mussol.api.dtos import (
    JobDto,
    JobRequestDto,
    LibraryDto,
    ListSummaryDto,
    ProblemDto,
    TagReplacementDto,
)
from mussol.audio.audio_format import AudioFormat
from mussol.downloads.errors import (
    CoverAlreadyPresent,
    CoverUnavailable,
    EnrichmentFailed,
    EnrichmentSkipped,
)
from mussol.downloads.job import JobId
from mussol.downloads.service import DownloadService
from mussol.library.errors import RecordNotFound
from mussol.library.library_record import LibraryRecord, normalize_tags
from mussol.sources.errors import DownloadFailed, UnsupportedSource
from mussol.sources.value_objects import SourceUrl

LOCALHOST = "127.0.0.1"


def create_app(
    service: DownloadService,
    web_dir: Path | None = None,
    media_dir: Path | None = None,
) -> FastAPI:
    app = FastAPI(title="mussol")

    pending: queue.Queue[JobId] = queue.Queue()

    def worker() -> None:
        while True:
            service.run_job(pending.get())
            pending.task_done()

    threading.Thread(target=worker, daemon=True, name="job-worker").start()
    for recovered in service.restore_pending():
        pending.put(recovered.id)

    @app.exception_handler(RequestValidationError)
    async def validation_problem(request: Request, exc: RequestValidationError) -> JSONResponse:
        return _problem(422, "Invalid request", str(exc.errors()))

    @app.exception_handler(Exception)
--- src/mussol/sources/youtube.py (first 60 lines of 9195 bytes) ---
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


@dataclass(frozen=True)
class ResolvedTracks:
    title: str | None
    tracks: list[TrackDescriptor]


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


Write ONLY the plan (the three sections). No prose outside them.