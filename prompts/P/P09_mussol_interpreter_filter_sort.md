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

Write ONLY the plan (the three sections). No prose outside them.