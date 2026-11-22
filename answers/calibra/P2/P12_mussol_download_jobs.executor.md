=== FILE: src/mussol/downloads/__init__.py ===
"""Download jobs and service for mussol."""

from __future__ import annotations

from .errors import (
    DownloadFailed,
    JobNotFound,
    UnsupportedSource,
)
from .job import JobId, JobStatus, DownloadJob
from .service import DownloadService

__all__ = [
    "DownloadFailed",
    "DownloadJob",
    "DownloadService",
    "JobId",
    "JobNotFound",
    "JobStatus",
    "UnsupportedSource",
]

=== END FILE ===

=== FILE: src/mussol/downloads/errors.py ===
"""Errors specific to download job processing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class JobNotFound(Exception):
    """A download job was not found by its ID."""

    job_id: str

    def __str__(self) -> str:
        return f"Job {self.job_id!r} not found"


@dataclass(frozen=True)
class DownloadFailed(Exception):
    """A download step failed with a reason."""

    job_id: str
    reason: str

    def __str__(self) -> str:
        return f"Download of {self.job_id!r} failed: {self.reason}"


@dataclass(frozen=True)
class UnsupportedSource(Exception):
    """The source type is not supported for downloading."""

    source_type: str

    def __str__(self) -> str:
        return f"Unsupported source type: {self.source_type}"

=== END FILE ===

=== FILE: src/mussol/downloads/job.py ===
"""Value objects and state machine for download jobs."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any


class JobStatus(Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    TRANSCODING = "transcoding"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class JobId:
    """Opaque identifier for a download job."""

    value: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __str__(self) -> str:
        return self.value


@dataclass
class DownloadJob:
    """A single download job with mutable status tracking."""

    id: JobId
    url: str
    title: str | None
    format_name: str
    media_root: Path
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )
    status: JobStatus = JobStatus.PENDING
    error_message: str | None = None
    output_path: Path | None = None

    def mark_downloading(self) -> None:
        if self.status is not JobStatus.PENDING:
            raise ValueError("Cannot start downloading from status %s", self.status)
        self.status = JobStatus.DOWNLOADING

    def mark_transcoding(self) -> None:
        if self.status is not JobStatus.DOWNLOADING:
            raise ValueError("Cannot start transcoding from status %s", self.status)
        self.status = JobStatus.TRANSCODING

    def mark_completed(self, path: Path) -> None:
        if self.status is not JobStatus.TRANSCODING:
            raise ValueError("Cannot complete from status %s", self.status)
        self.status = JobStatus.COMPLETED
        self.output_path = path

    def mark_failed(self, reason: str) -> None:
        self.status = JobStatus.FAILED
        self.error_message = reason

=== END FILE ===

=== FILE: src/mussol/downloads/service.py ===
"""DownloadService orchestrates download and transcode steps."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mussol.audio.audio_format import AudioFormat
from mussol.audio.extractor import AudioExtractor
from mussol.downloads.errors import DownloadFailed, JobNotFound
from mussol.downloads.job import DownloadJob, JobId, JobStatus
from mussol.library.store import LibraryStore
from mussol.shared.process import BackendResult, BackendRunner
from mussol.sources.errors import UnsupportedSource
from mussol.sources.value_objects import SourceUrl
from mussol.sources.youtube import YoutubeAdapter


class DownloadService:
    """Orchestrates downloading a single URL through yt-dlp then ffmpeg."""

    def __init__(
        self,
        adapter: YoutubeAdapter,
        extractor: AudioExtractor,
        store: LibraryStore,
        download_runner: BackendRunner,
        transcode_runner: BackendRunner,
        media_root: Path,
    ) -> None:
        self.adapter = adapter
        self.extractor = extractor
        self.store = store
        self.download_runner = download_runner
        self.transcode_runner = transcode_runner
        self.media_root = media_root
        self._jobs: dict[str, DownloadJob] = {}

    def submit(self, url: str) -> JobId:
        ref = self.adapter.classify(SourceUrl(url))
        if ref.kind is not self.adapter.VIDEO:
            raise UnsupportedSource("only videos supported")
        metadata = self.adapter.resolve_metadata(ref)
        job = DownloadJob(
            id=JobId(),
            url=url,
            title=metadata.get("title"),
            format_name="webm",
            media_root=self.media_root,
        )
        self._jobs[job.id.value] = job
        return job.id

    def run(self, job_id: JobId) -> None:
        job = self._get_job(job_id)
        job.mark_downloading()
        try:
            result = self.download_runner.run([
                "yt-dlp", "--dump-single-json", "-o", "%(id)s.%(ext)s", job.url,
            ])
            if result.returncode != 0:
                job.mark_failed(result.stderr or "download failed")
                return
            meta = json.loads(result.stdout)
            video_id = meta.get("id", "")
            download_path = self.media_root / f"{video_id}.webm"
            job.mark_transcoding()
            transcode_result = self.transcode_runner.run([
                "ffmpeg", "-i", str(download_path), "-vn", "-c:a", "libopus",
                str(self.media_root / f"{video_id}.opus"),
            ])
            if transcode_result.returncode != 0:
                job.mark_failed(transcode_result.stderr or "transcode failed")
                return
            job.mark_completed(self.media_root / f"{video_id}.opus")
            self.store.save_new(
                source="youtube",
                source_id=video_id,
                title=job.title or "",
                format=AudioFormat.OPUS,
                filename=f"{video_id}.opus",
            )
        except Exception as exc:
            job.mark_failed(str(exc))

    def status(self, job_id: JobId) -> DownloadJob | None:
        return self._jobs.get(job_id.value)

    def _get_job(self, job_id: JobId) -> DownloadJob:
        job = self._jobs.get(job_id.value)
        if job is None:
            raise JobNotFound(job_id.value)
        return job

=== END FILE ===

=== FILE: src/mussol/api/dtos.py ===
"""DTOs for the download jobs API."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubmitRequest:
    url: str


@dataclass(frozen=True)
class SubmitResponse:
    job_id: str


@dataclass(frozen=True)
class StatusResponse:
    job_id: str
    status: str
    error_message: str | None = None
    output_path: str | None = None

=== END FILE ===

=== FILE: src/mussol/api/app.py ===
"""FastAPI application wiring for download jobs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from mussol.api.dtos import SubmitRequest, SubmitResponse, StatusResponse
from mussol.audio.extractor import AudioExtractor
from mussol.downloads.service import DownloadService
from mussol.library.store import LibraryStore
from mussol.sources.youtube import YoutubeAdapter


def create_app(
    media_root: Path,
    db_path: Path,
    download_runner: Any,
    transcode_runner: Any,
) -> FastAPI:
    adapter = YoutubeAdapter()
    extractor = AudioExtractor()
    store = LibraryStore(db_path=db_path, media_root=media_root)
    service = DownloadService(
        adapter=adapter,
        extractor=extractor,
        store=store,
        download_runner=download_runner,
        transcode_runner=transcode_runner,
        media_root=media_root,
    )

    app = FastAPI(title="mussol")

    @app.post("/jobs/submit", response_model=SubmitResponse)
    async def submit(req: SubmitRequest) -> SubmitResponse:
        job_id = service.submit(req.url)
        return SubmitResponse(job_id=str(job_id))

    @app.get("/jobs/{job_id}", response_model=StatusResponse)
    async def status(job_id: str) -> StatusResponse:
        job = service.status(type("JobId", (), {"value": job_id})())
        if job is None:
            return JSONResponse(status_code=404, content={"detail": "not found"})
        return StatusResponse(
            job_id=job.id.value,
            status=job.status.value,
            error_message=job.error_message,
            output_path=str(job.output_path) if job.output_path else None,
        )

    return app


def serve(app: FastAPI, host: str = "127.0.0.1", port: int = 8000) -> None:
    import uvicorn
    uvicorn.run(app, host=host, port=port)

=== END FILE ===

=== FILE: tests/test_download_job.py ===
"""Tests for JobId, JobStatus and DownloadJob."""

import pytest

from mussol.downloads.errors import JobNotFound
from mussol.downloads.job import DownloadJob, JobId, JobStatus
from pathlib import Path


class TestJobId:
    def test_default_is_hex(self) -> None:
        jid = JobId()
        assert len(jid.value) == 32
        assert all(c in "0123456789abcdef" for c in jid.value)

    def test_str_returns_value(self) -> None:
        jid = JobId("abc")
        assert str(jid) == "abc"


class TestDownloadJobLifecycle:
    def _make_job(self, **overrides: object) -> DownloadJob:
        return DownloadJob(
            id=JobId(),
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            title="Test Title",
            format_name="webm",
            media_root=Path("/tmp"),
            **overrides,
        )

    def test_initial_status_pending(self) -> None:
        job = self._make_job()
        assert job.status is JobStatus.PENDING

    def test_mark_downloading(self) -> None:
        job = self._make_job()
        job.mark_downloading()
        assert job.status is JobStatus.DOWNLOADING

    def test_mark_transcoding(self) -> None:
        job = self._make_job()
        job.mark_downloading()
        job.mark_transcoding()
        assert job.status is JobStatus.TRANSCODING

    def test_mark_completed(self) -> None:
        job = self._make_job()
        job.mark_downloading()
        job.mark_transcoding()
        path = Path("/media/test.opus")
        job.mark_completed(path)
        assert job.status is JobStatus.COMPLETED
        assert job.output_path == path

    def test_mark_failed(self) -> None:
        job = self._make_job()
        job.mark_failed("boom")
        assert job.status is JobStatus.FAILED
        assert job.error_message == "boom"

    def test_cannot_start_download_from_wrong_state(self) -> None:
        job = self._make_job(status=JobStatus.DOWNLOADING)
        with pytest.raises(ValueError):
            job.mark_downloading()

    def test_cannot_complete_from_wrong_state(self) -> None:
        job = self._make_job()
        with pytest.raises(ValueError):
            job.mark_completed(Path("/x"))

=== END FILE ===

=== FILE: tests/test_youtube_adapter.py ===
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
    ],
)
def test_classify(raw: str, kind: YouTubeKind, video_id: str | None, playlist_id: str | None) -> None:
    ref = YoutubeAdapter().classify(SourceUrl(raw))
    assert ref.kind is kind
    if video_id is not None:
        assert ref.video_id == video_id
    else:
        assert ref.video_id is None
    if playlist_id is not None:
        assert ref.playlist_id == playlist_id
    else:
        assert ref.playlist_id is None


class TestResolveMetadata:
    def _runner(self, metadata: object) -> BackendRunner:
        class Scripted(BackendRunner):
            def run(self, argv: list[str]) -> BackendResult:
                return BackendResult(returncode=0, stdout=json.dumps(metadata), stderr="")
        return Scripted()

    def test_video_metadata(self) -> None:
        meta = {"id": "abc123", "title": "My Song"}
        adapter = YoutubeAdapter()
        result = adapter.resolve_metadata(adapter.classify(SourceUrl("https://www.youtube.com/watch?v=abc123")), self._runner(meta))
        assert isinstance(result, dict)
        assert result["id"] == "abc123"
        assert result["title"] == "My Song"

    def test_playlist_metadata(self) -> None:
        meta = {"entries": [{"id": "x"}, {"id": "y"}]}
        adapter = YoutubeAdapter()
        result = adapter.resolve_metadata(adapter.classify(SourceUrl("https://www.youtube.com/playlist?list=PLABC")), self._runner(meta))
        assert len(result.get("entries", [])) == 2

=== END FILE ===

=== FILE: tests/test_download_service.py ===
"""DownloadService: fan-out, staged runs, and failure marking."""

import json
from pathlib import Path

from mussol.audio.audio_format import AudioFormat
from mussol.audio.extractor import AudioExtractor
from mussol.downloads.errors import JobNotFound
from mussol.downloads.job import JobId
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


class TestSubmitAndRunSuccess:
    def test_submit_returns_job_id(self, tmp_path: Path) -> None:
        svc = _service(tmp_path, ScriptedRunner({"id": "abc", "title": "Song"}))
        jid = svc.submit("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert isinstance(jid, JobId)

    def test_run_completes_and_stores(self, tmp_path: Path) -> None:
        svc = _service(tmp_path, ScriptedRunner({"id": "abc", "title": "Song"}))
        jid = svc.submit("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        svc.run(jid)
        job = svc.status(jid)
        assert job is not None
        assert job.status.value == "completed"
        assert job.output_path is not None


class TestFailureCases:
    def test_download_failure_marks_failed(self, tmp_path: Path) -> None:
        svc = _service(tmp_path, DownloadFailingRunner({"id": "abc", "title": "Song"}))
        jid = svc.submit("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        svc.run(jid)
        job = svc.status(jid)
        assert job is not None
        assert job.status.value == "failed"
        assert job.error_message == "boom"

    def test_unsupported_source_raises(self, tmp_path: Path) -> None:
        svc = _service(tmp_path, ScriptedRunner({}))
        with pytest.raises(UnsupportedSource):
            svc.submit("https://www.youtube.com/playlist?list=PLABC")


class TestJobNotFound:
    def test_status_missing_job(self, tmp_path: Path) -> None:
        svc = _service(tmp_path, ScriptedRunner({}))
        assert svc.status(JobId("nonexistent")) is None

=== END FILE ===

=== FILE: tests/test_api.py ===
"""Tests for the download jobs API endpoints."""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from mussol.api.app import create_app
from mussol.downloads.job import JobId
from mussol.shared.process import BackendResult, BackendRunner


class StubRunner(BackendRunner):
    """Minimal runner that returns JSON metadata and succeeds."""

    def __init__(self, metadata: object) -> None:
        self._metadata = metadata

    def run(self, argv: list[str]) -> BackendResult:
        if "--dump-single-json" in argv:
            return BackendResult(returncode=0, stdout=json.dumps(self._metadata), stderr="")
        return BackendResult(returncode=0, stdout="", stderr="")


def _app(tmp_path: Path) -> tuple[TestClient, dict]:
    media = tmp_path / "media"
    media.mkdir(exist_ok=True)
    app = create_app(
        media_root=media,
        db_path=tmp_path / "lib.db",
        download_runner=StubRunner({"id": "abc", "title": "Song"}),
        transcode_runner=StubRunner({}),
    )
    client = TestClient(app)
    return client, {"media": str(media)}


class TestSubmitEndpoint:
    def test_submit_returns_job_id(self, tmp_path: Path) -> None:
        client, _ = _app(tmp_path)
        resp = client.post("/jobs/submit", json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
        assert resp.status_code == 200
        data = resp.json()
        assert "job_id" in data
        assert len(data["job_id"]) > 0

    def test_submit_rejects_playlist(self, tmp_path: Path) -> None:
        client, _ = _app(tmp_path)
        resp = client.post("/jobs/submit", json={"url": "https://www.youtube.com/playlist?list=PLABC"})
        assert resp.status_code == 500


class TestStatusEndpoint:
    def test_status_success(self, tmp_path: Path) -> None:
        client, _ = _app(tmp_path)
        submit_resp = client.post("/jobs/submit", json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
        job_id = submit_resp.json()["job_id"]
        status_resp = client.get(f"/jobs/{job_id}")
        assert status_resp.status_code == 200
        data = status_resp.json()
        assert data["job_id"] == job_id
        assert data["status"] == "pending"

    def test_status_not_found(self, tmp_path: Path) -> None:
        client, _ = _app(tmp_path)
        resp = client.get("/jobs/nonexistent")
        assert resp.status_code == 404

=== END FILE ===