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
R1: When a library payload entry carries no `enriched_at`, the panel shall derive the enrichment state `none` for that card.  - AC-1.1: The `enriched_at` guard shall run first: a record with an interpreter   but no `enriched_at` is `none`, because editing an interpreter never sets   `enriched_at` (`tests/test_download_service.py` 1014–1039). - AC-1.2: The derivation shall read no payload field other than `enriched_at`,   `artist` and `has_cover`.

R2: When a library payload entry carries `enriched_at` and has no interpreter or no cover, the panel shall derive the enrichment state `partial`.  - AC-2.1: `enriched_at` set, `artist` null or empty, cover present → `partial`. - AC-2.2: `enriched_at` set, interpreter present, `has_cover` false → `partial`. - AC-2.3: `enriched_at` set, both missing → `partial`.

R3: When a library payload entry carries `enriched_at`, an interpreter and a cover, the panel shall derive the enrichment state `complete`.  - AC-3.1: The cover shall be read from `has_cover`, never from `cover_url`: the   API fills `cover_url` for every record, including one with no cover file   (`src/mussol/api/app.py` 271 → `src/mussol/downloads/service.py` 279–287).

R4: The panel shall render the enrichment marker on every library card, in the state derived for it.  - AC-4.1: The marker shall have one construction site, inside `updateRow`, and   it shall be built from the `item` that row is being updated with. - AC-4.2: `buildRow` shall build no marker.

R5: While a card's enrichment state is `complete`, the panel shall draw its marker in the accent token.  - AC-5.1: The colour shall come from `var(--color-accent)` and from nothing   else. - AC-5.2: The marker text shall meet AA contrast on both card backgrounds the   panel renders into (`--color-card` and `--color-primary`); `design.md` § D4   carries the measured ratios.

R6: While a card's enrichment state is `partial`, the panel shall draw its marker in the muted token with the destructive token as its border.  - AC-6.1: The text colour shall be `var(--color-muted)`; the border colour shall   be `var(--color-destructive)`. - AC-6.2: The text and the border shall each meet their WCAG contrast threshold   on both card backgrounds (`design.md` § D4).

R7: While a card's enrichment state is `none`, the panel shall draw its marker in the muted token without a border.  - AC-7.1: The colour shall be `var(--color-muted)`, the neutral colour the   panel's own action buttons already use. - AC-7.2: The marker shall carry no border and no background.

R8: The enrichment marker shall state its state in words, in addition to its colour.  - AC-8.1: The visible text of the marker shall be the state word: `untagged`,   `partial` or `tagged`. - AC-8.2: The marker's `title` shall name the state and, for `partial`, which   fields are missing. - AC-8.3: No state shall be carried by colour alone.

R9: When a poll returns a payload whose `enriched_at`, `artist` or `has_cover` changed for a cached card, the panel shall show that card's marker in the new state.  - AC-9.1: `rowSignature` shall keep carrying `artist`, `has_cover` and   `enriched_at` (`web/app.js` 136, 141, 142); this feature adds no field to it. - AC-9.2: The marker shall be rebuilt by `updateRow`, which already rebuilds the   whole action row on every refresh (`web/app.js` 221, 240–257).

R10: The panel shall not change the enrich action for a card in state `none`.  - AC-10.1: `enrichButton` shall keep its label, its request and its position in   the action row. - AC-10.2: No card action shall be disabled, dimmed or hidden because of its   enrichment state.

R11: The feature shall not introduce a colour outside the existing palette tokens, nor any dependency loaded from the network.  - AC-11.1: No new token shall be added to `:root`, and no hex colour literal   shall appear in the rules this feature adds. - AC-11.2: `test_page_has_no_external_network_dependencies` and   `test_scripts_use_safe_sinks_only` shall stay green.

R12: The enrichment state shall not depend on album or date.  - AC-12.1: `web/app.js` shall not name `album` or `date`. - AC-12.2: `LibraryDto`, `LibraryRecord` and the `library_records` columns shall   keep exactly the fields they have today.

--- FEATURE TITLE ---
close(enrichment_state_coloring): three-state enrichment badge

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
harness/progress/impl_enrichment_state_coloring.md
harness/progress/impl_external_tool_availability.md
harness/progress/impl_interpreter_editing.md
harness/progress/impl_interpreter_filter_sort.md
harness/progress/impl_job_execution.md
harness/progress/impl_legacy_path_migration.md
harness/progress/impl_library_grouping.md
harness/progress/impl_library_panel.md
harness/progress/impl_library_render_reconciliation.md
harness/progress/impl_library_store.md
harness/progress/impl_list_folders.md
harness/progress/impl_list_pause_resume.md
harness/progress/impl_master_volume.md
harness/progress/impl_media_playback.md
harness/progress/impl_media_tags.md
harness/progress/impl_metadata_enrichment.md
harness/progress/impl_missing_cover_fetch.md
harness/progress/impl_panel_layout_fix.md
harness/progress/impl_playlist_dropdown_panel.md
harness/progress/impl_playlist_rename.md
harness/progress/impl_project_foundation.md
harness/progress/impl_runner_timeout.md
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
harness/specs/enrichment_state_coloring/design.md
harness/specs/enrichment_state_coloring/requirements.md
harness/specs/enrichment_state_coloring/tasks.md
harness/specs/external_tool_availability/APPROVAL
harness/specs/external_tool_availability/design.md
harness/specs/external_tool_availability/requirements.md
harness/specs/external_tool_availability/tasks.md
harness/specs/interpreter_editing/APPROVAL
harness/specs/interpreter_editing/design.md
harness/specs/interpreter_editing/requirements.md
harness/specs/interpreter_editing/tasks.md
harness/specs/interpreter_filter_sort/APPROVAL
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
harness/specs/master_volume/APPROVAL
harness/specs/master_volume/design.md
harness/specs/master_volume/requirements.md
harness/specs/master_volume/tasks.md
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
harness/specs/playlist_dropdown_panel/APPROVAL
harness/specs/playlist_dropdown_panel/design.md
harness/specs/playlist_dropdown_panel/requirements.md
harness/specs/playlist_dropdown_panel/tasks.md
harness/specs/playlist_rename/APPROVAL
harness/specs/playlist_rename/design.md
harness/specs/playlist_rename/requirements.md
harness/specs/playlist_rename/tasks.md
harness/specs/project_foundation/APPROVAL
harness/specs/project_foundation/design.md
harness/specs/project_foundation/requirements.md
harness/specs/project_foundation/tasks.md
harness/specs/runner_timeout/APPROVAL
harness/specs/runner_timeout/design.md
harness/specs/runner_timeout/requirements.md
harness/specs/runner_timeout/tasks.md
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
src/mussol/audio/timeouts.py
src/mussol/downloads/__init__.py
src/mussol/downloads/errors.py
src/mussol/downloads/job.py
src/mussol/downloads/job_status.py
src/mussol/downloads/job_store.py
src/mussol/downloads/list.py
src/mussol/downloads/service.py
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
src/mussol/sources/timeouts.py
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
tests/test_process_runner.py
tests/test_quality_gates.py
tests/test_result.py
tests/test_runner_policy.py
tests/test_source_types.py
tests/test_source_url.py
tests/test_spotify_adapter.py
tests/test_tagger.py
tests/test_tool_availability.py
tests/test_web.py
tests/test_youtube_adapter.py
tests/test_youtube_download.py
web/app.js
web/index.html
web/styles.css

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- tests/test_web.py (first 60 lines of 59321 bytes) ---
"""Static frontend: serving, structure, tokens, and safety checks."""

import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from mussol.api.app import create_app
from mussol.audio.audio_format import AudioFormat
from mussol.audio.extractor import AudioExtractor
from mussol.downloads.job_store import JobStore
from mussol.downloads.service import DownloadService
from mussol.library.store import LibraryStore
from mussol.shared.process import BackendResult, ProcessFailure
from mussol.shared.result import Ok, Result
from mussol.sources.youtube import YoutubeAdapter

WEB_DIR = Path(__file__).resolve().parent.parent / "web"


class StubRunner:
    def run(self, argv: list[str], *, timeout: float) -> Result[BackendResult, ProcessFailure]:
        return Ok(BackendResult(returncode=0, stdout="", stderr=""))


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


def _client(tmp_path: Path) -> TestClient:
    return TestClient(create_app(_service(tmp_path), web_dir=WEB_DIR))


def _css_rule(text: str, selector: str) -> str:
    """Return one CSS rule block, starting at its selector."""
    start = text.index(selector)
    return text[start : text.index("}", start) + 1]


def test_root_serves_required_landmarks(tmp_path: Path) -> None:
    response = _client(tmp_path).get("/")

    assert response.status_code == 200
    for marker in (
        'id="job-form"',
        'id="source-url"',
        'id="format-picker"',
        'id="job-list"',
--- tests/test_download_service.py (first 60 lines of 54612 bytes) ---
"""DownloadService: fan-out, staged runs, and failure marking."""

import json
import os
import sqlite3
from collections.abc import Callable
from pathlib import Path

import pytest

from mussol.audio.audio_format import AudioFormat
from mussol.audio.extractor import AudioExtractor
from mussol.downloads.errors import (
    CoverAlreadyPresent,
    CoverUnavailable,
    EnrichmentFailed,
    EnrichmentSkipped,
    InterpreterFileMissing,
    InterpreterFormatUnsupported,
    InterpreterNameInvalid,
    InterpreterTagWriteFailed,
    JobNotFound,
    ListNameInvalid,
    ListNameTaken,
    ListNotFound,
    ListRenameBlocked,
    ListRenameFailed,
)
from mussol.downloads.job import JobId
from mussol.downloads.job_status import JobStatus
from mussol.downloads.job_store import JobStore
from mussol.downloads.list import DownloadList, ListId
from mussol.downloads.service import DownloadService, RenameError
from mussol.library.errors import StorageError
from mussol.library.store import LibraryStore
from mussol.metadata.catalog import CatalogLookup, MetadataNotFound, TrackMetadata
from mussol.metadata.tagger import Tagger
from mussol.shared.process import (
    BackendResult,
    BackendRunner,
    ProcessFailure,
    ProcessTimeout,
    ProcessUnavailable,
)
from mussol.shared.result import Err, Ok, Result
from mussol.sources.errors import DownloadFailed, UnsupportedSource
from mussol.sources.source_type import SourceType
from mussol.sources.timeouts import DOWNLOAD_TIMEOUT_SECONDS, THUMBNAIL_TIMEOUT_SECONDS
from mussol.sources.value_objects import SourceUrl
from mussol.sources.youtube import YoutubeAdapter


class ScriptedRunner:
    """Simulates yt-dlp and ffmpeg by materializing their outputs."""

    def __init__(self, metadata: object) -> None:
        self._metadata = metadata
        self.calls: list[list[str]] = []

    def metadata_response(self) -> BackendResult:
--- tests/test_api.py (first 60 lines of 38733 bytes) ---
"""API boundary: full request/response cycles through TestClient."""

import json
import sqlite3
import threading
import time
from pathlib import Path

from fastapi.testclient import TestClient
from pytest import MonkeyPatch, mark

from mussol.api.app import LOCALHOST, create_app, serve
from mussol.api.dtos import JobDto, LibraryDto
from mussol.audio.audio_format import AudioFormat
from mussol.audio.extractor import AudioExtractor
from mussol.downloads.job import DownloadJob
from mussol.downloads.job_status import JobStatus
from mussol.downloads.job_store import JobStore
from mussol.downloads.service import DownloadService
from mussol.library.errors import LibraryError, StorageError
from mussol.library.store import LibraryStore
from mussol.metadata.tagger import Tagger
from mussol.shared.process import (
    BackendResult,
    ProcessFailure,
    ProcessTimeout,
    ProcessUnavailable,
    SubprocessRunner,
)
from mussol.shared.result import Err, Ok, Result
from mussol.sources.source_type import SourceType
from mussol.sources.timeouts import DOWNLOAD_TIMEOUT_SECONDS, METADATA_TIMEOUT_SECONDS
from mussol.sources.track import TrackDescriptor
from mussol.sources.value_objects import TrackTitle
from mussol.sources.youtube import YoutubeAdapter


class StubRunner:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def run(self, argv: list[str], *, timeout: float) -> Result[BackendResult, ProcessFailure]:
        self.calls.append(argv)
        if "--dump-single-json" in argv:
            payload = {"entries": [{"id": "aaa", "title": "song"}]}
            return Ok(BackendResult(returncode=0, stdout=json.dumps(payload), stderr=""))
        if "-o" in argv:
            template = argv[argv.index("-o") + 1]
            media = Path(template.replace("%(ext)s", "webm"))
            media.write_bytes(b"media")
            Path(template.replace("%(ext)s", "jpg")).write_bytes(b"thumbnail")
            return Ok(BackendResult(returncode=0, stdout=f"{media}\n", stderr=""))
        Path(argv[-1]).write_bytes(b"audio")
        return Ok(BackendResult(returncode=0, stdout="", stderr=""))


def _service(tmp_path: Path) -> DownloadService:
    media = tmp_path / "media"
    media.mkdir(exist_ok=True)
    runner = StubRunner()
--- web/app.js (first 60 lines of 34564 bytes) ---
"use strict";

const POLL_INTERVAL_MS = 2000;
const MASTER_VOLUME_KEY = "mussol.master-volume";

const form = document.getElementById("job-form");
const urlInput = document.getElementById("source-url");
const formatPicker = document.getElementById("format-picker");
const submitButton = document.getElementById("submit-job");
const errorSummary = document.getElementById("error-summary");
const formErrors = document.getElementById("form-errors");
const toolWarning = document.getElementById("tool-warning");
const urlError = document.getElementById("source-url-error");
const formatError = document.getElementById("format-error");
const jobList = document.getElementById("job-list");
const jobsEmpty = document.getElementById("jobs-empty");
const downloadList = document.getElementById("download-list");
const downloadsEmpty = document.getElementById("downloads-empty");
const playlistList = document.getElementById("playlist-list");
const playlistsEmpty = document.getElementById("playlists-empty");
let listsByName = {};
let activeTag = null;
let activeArtistQuery = "";
let sortKey = "created_at";
let sortDirection = "asc";
let masterLevel = 1;
let renderedKeys = [];
let renderedPanelKeys = [];
let payloadHasPlaylists = false;
let lastJobsSignature = "";
let lastToolWarningSignature = "";
const rowsById = new Map();
const headersByName = new Map();
const panelsByName = new Map();
const openPlaylists = new Set();

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
--- src/mussol/downloads/service.py (first 60 lines of 27036 bytes) ---
"""Download orchestration over the published module APIs."""

from __future__ import annotations

import logging
import sqlite3
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

from mussol.audio.audio_format import AudioFormat
from mussol.audio.extractor import AudioExtractor
from mussol.audio.profile import AudioProfile
from mussol.downloads.errors import (
    CoverAlreadyPresent,
    CoverUnavailable,
    EnrichmentFailed,
    EnrichmentSkipped,
    InterpreterFileMissing,
    InterpreterFormatUnsupported,
    InterpreterNameInvalid,
    InterpreterTagWriteFailed,
    JobNotFound,
    ListNameInvalid,
    ListNameTaken,
    ListNotFound,
    ListRenameBlocked,
    ListRenameFailed,
)
from mussol.downloads.job import DownloadJob, JobId
from mussol.downloads.job_status import JobStatus
from mussol.downloads.job_store import JobStore
from mussol.downloads.list import (
    DownloadList,
    ListId,
    ListSummary,
    sanitize_list_name,
)
from mussol.library.errors import (
    InvalidFilename,
    LibraryError,
    RecordNotFound,
    StorageError,
)
from mussol.library.library_record import LibraryRecord
from mussol.library.store import LibraryStore
from mussol.metadata.catalog import CatalogLookup, TrackMetadata
from mussol.metadata.cover import fetch_cover
from mussol.metadata.tagger import SUPPORTED_SUFFIXES, Tagger
from mussol.shared.process import BackendRunner
from mussol.shared.result import Err, Ok, Result
from mussol.sources.errors import DownloadFailed, UnsupportedSource
from mussol.sources.source_type import SourceType
from mussol.sources.track import TrackDescriptor
from mussol.sources.value_objects import SourceUrl
from mussol.sources.youtube import YoutubeAdapter, YouTubeKind, YouTubeRef

SubmitError = UnsupportedSource | DownloadFailed
RenameError = ListNotFound | ListNameInvalid | ListNameTaken | ListRenameBlocked | ListRenameFailed
InterpreterEditError = (
--- web/styles.css (first 60 lines of 14111 bytes) ---
/* mussol — dark slate palette grounded in ui-ux-pro-max guidance. */

:root {
  --color-background: #0F172A;
  --color-foreground: #F8FAFC;
  --color-primary: #1E293B;
  --color-secondary: #334155;
  --color-card: #1B2336;
  --color-accent: #22C55E;
  --color-on-accent: #0F172A;
  --color-muted: #94A3B8;
  --color-border: #475569;
  --color-destructive: #EF4444;
  --space-1: 8px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;
  --radius: 8px;
  --transition: 200ms;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  background: var(--color-background);
  color: var(--color-foreground);
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size: 16px;
  line-height: 1.5;
}

.shell {
  max-width: 1100px;
  margin: 0 auto;
  padding: var(--space-1) var(--space-2) var(--space-2);
  height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr;
  gap: var(--space-1);
  min-height: 0;
}

.columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
  align-items: stretch;
  min-height: 0;
}

/* Downloads pane split: the playlist panel takes only what its content needs,
   up to a cap, and the list takes the rest. It must be a flex column and not a
   grid: a `minmax(0, 60%)` grid track claimed its whole cap even when the
   content was shorter, leaving a 169px void between the two panes. In flex the
   percentage cap still resolves against this container's definite height, but
   nothing is reserved. With no playlist the panel collapses to nothing, and
--- src/mussol/library/store.py (first 60 lines of 14085 bytes) ---
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
--- tests/test_library_store.py (first 60 lines of 14039 bytes) ---
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

Write ONLY the plan (the three sections). No prose outside them.