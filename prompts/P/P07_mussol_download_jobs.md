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

Write ONLY the plan (the three sections). No prose outside them.