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
R1: WHEN `seekandemploy apply notes <id> --set <text>` runs against an existing application id, the system shall persist `<text>` as that application's `notes` field.

R2: WHEN `seekandemploy apply notes <id> --clear` runs against an existing application id, the system shall persist NULL as that application's `notes` field.

R3: WHEN a notes edit succeeds, the system shall print to stdout the application line in the tracker-glance format (`[<id>] <status> <company> - <title>`) followed by the report path (`report: <path>`).

R4: WHEN a notes edit succeeds, the system shall regenerate the static HTML snapshot from the current database contents at the path given by `--out` (default `applications.html`).

R5: WHEN notes are edited, the system shall not append any row to `application_event`.

R6: WHEN notes are edited, the system shall not alter the application's status, company, title, url, salary expectation, salary currency, applied date, or source job-offer link.

R7: WHEN `apply notes` receives an id with no matching application, the system shall print `error: application <id> not found` to stderr and exit with code 1, leaving the HTML snapshot untouched.

R8: The system shall accept `--set <text>` and `--clear` only individually, requiring exactly one per invocation, and shall answer an invocation with both flags or with neither as a usage error with exit code 2.

--- FEATURE TITLE ---
chore(session): close apply-notes-edit as done (25/25) after completion gate

--- REPOSITORY FILE TREE (before implementation) ---
.dockerignore
.env.example
.gitignore
.opencode/agent/implementer.md
.opencode/agent/leader.md
.opencode/agent/reviewer.md
.opencode/agent/spec-author.md
AGENTS.md
Dockerfile
Makefile
README.md
alembic.ini
applications.html
compose.yaml
dashboard.yaml
docs/architecture.md
docs/conventions.md
docs/specs.md
docs/verification.md
harness/CHECKPOINTS.md
harness/feature_list.json
harness/init.sh
harness/progress/current.md
harness/progress/history.md
harness/progress/impl_application_tracking.md
harness/progress/impl_batch-source-activation.md
harness/progress/impl_collection-scheduler.md
harness/progress/impl_connector-framework.md
harness/progress/impl_core-models-persistence.md
harness/progress/impl_cv-profile-generation.md
harness/progress/impl_generic-html-audit.md
harness/progress/impl_generic-html-selector-inference.md
harness/progress/impl_laya-server-start.md
harness/progress/impl_laya-typed-scoring.md
harness/progress/impl_matching-engine.md
harness/progress/impl_modality-unknown-recovery.md
harness/progress/impl_project-skeleton.md
harness/progress/impl_resilient-offer-mapping.md
harness/progress/impl_scoring-on-matching.md
harness/progress/impl_scoring-pending-count.md
harness/progress/impl_scoring-progress.md
harness/progress/impl_source-audit-persistence.md
harness/progress/impl_sources-table-controls.md
harness/progress/impl_telegram-alerts.md
harness/progress/impl_vendor-source-presets.md
harness/progress/impl_web-dashboard.md
harness/progress/impl_web-source-activation.md
harness/progress/review_batch-source-activation.md
harness/progress/review_collection-scheduler.md
harness/progress/review_connector-framework.md
harness/progress/review_core-models-persistence.md
harness/progress/review_cv-profile-generation.md
harness/progress/review_generic-html-audit.md
harness/progress/review_generic-html-selector-inference.md
harness/progress/review_laya-server-start.md
harness/progress/review_laya-typed-scoring.md
harness/progress/review_matching-engine.md
harness/progress/review_modality-unknown-recovery.md
harness/progress/review_project-skeleton.md
harness/progress/review_resilient-offer-mapping.md
harness/progress/review_scoring-on-matching.md
harness/progress/review_scoring-pending-count.md
harness/progress/review_scoring-progress.md
harness/progress/review_source-audit-persistence.md
harness/progress/review_sources-table-controls.md
harness/progress/review_telegram-alerts.md
harness/progress/review_vendor-source-presets.md
harness/progress/review_web-dashboard.md
harness/progress/review_web-source-activation.md
harness/specs/application-tracking/design.md
harness/specs/application-tracking/requirements.md
harness/specs/application-tracking/tasks.md
harness/specs/batch-source-activation/design.md
harness/specs/batch-source-activation/requirements.md
harness/specs/batch-source-activation/tasks.md
harness/specs/collection-scheduler/design.md
harness/specs/collection-scheduler/requirements.md
harness/specs/collection-scheduler/tasks.md
harness/specs/connector-framework/design.md
harness/specs/connector-framework/requirements.md
harness/specs/connector-framework/tasks.md
harness/specs/core-models-persistence/design.md
harness/specs/core-models-persistence/requirements.md
harness/specs/core-models-persistence/tasks.md
harness/specs/cv-profile-generation/design.md
harness/specs/cv-profile-generation/requirements.md
harness/specs/cv-profile-generation/tasks.md
harness/specs/generic-html-audit/design.md
harness/specs/generic-html-audit/requirements.md
harness/specs/generic-html-audit/tasks.md
harness/specs/generic-html-selector-inference/design.md
harness/specs/generic-html-selector-inference/requirements.md
harness/specs/generic-html-selector-inference/tasks.md
harness/specs/laya-server-start/APPROVAL.md
harness/specs/laya-server-start/design.md
harness/specs/laya-server-start/requirements.md
harness/specs/laya-server-start/tasks.md
harness/specs/laya-typed-scoring/design.md
harness/specs/laya-typed-scoring/requirements.md
harness/specs/laya-typed-scoring/tasks.md
harness/specs/llm-scoring/APPROVAL.md
harness/specs/llm-scoring/design.md
harness/specs/llm-scoring/requirements.md
harness/specs/llm-scoring/tasks.md
harness/specs/llm-scoring/verification.md
harness/specs/matching-engine/design.md
harness/specs/matching-engine/requirements.md
harness/specs/matching-engine/tasks.md
harness/specs/modality-unknown-recovery/design.md
harness/specs/modality-unknown-recovery/requirements.md
harness/specs/modality-unknown-recovery/tasks.md
harness/specs/project-skeleton/design.md
harness/specs/project-skeleton/requirements.md
harness/specs/project-skeleton/tasks.md
harness/specs/resilient-offer-mapping/design.md
harness/specs/resilient-offer-mapping/requirements.md
harness/specs/resilient-offer-mapping/tasks.md
harness/specs/scoring-on-matching/design.md
harness/specs/scoring-on-matching/requirements.md
harness/specs/scoring-on-matching/tasks.md
harness/specs/scoring-pending-count/design.md
harness/specs/scoring-pending-count/requirements.md
harness/specs/scoring-pending-count/tasks.md
harness/specs/scoring-progress/design.md
harness/specs/scoring-progress/requirements.md
harness/specs/scoring-progress/tasks.md
harness/specs/source-audit-persistence/design.md
harness/specs/source-audit-persistence/requirements.md
harness/specs/source-audit-persistence/tasks.md
harness/specs/sources-table-controls/design.md
harness/specs/sources-table-controls/requirements.md
harness/specs/sources-table-controls/tasks.md
harness/specs/telegram-alerts/design.md
harness/specs/telegram-alerts/requirements.md
harness/specs/telegram-alerts/tasks.md
harness/specs/vendor-source-presets/design.md
harness/specs/vendor-source-presets/requirements.md
harness/specs/vendor-source-presets/tasks.md
harness/specs/web-dashboard/audit-1-usability-findings.md
harness/specs/web-dashboard/audit-2-visual-a11y-findings.md
harness/specs/web-dashboard/audit-3-copy-findings.md
harness/specs/web-dashboard/design.md
harness/specs/web-dashboard/requirements.md
harness/specs/web-dashboard/tasks.md
harness/specs/web-source-activation/design.md
harness/specs/web-source-activation/requirements.md
harness/specs/web-source-activation/tasks.md
pyproject.toml
src/seekandemploy/__init__.py
src/seekandemploy/alerts.py
src/seekandemploy/app.py
src/seekandemploy/applications_report.py
src/seekandemploy/audit.py
src/seekandemploy/audit_progress.py
src/seekandemploy/batch_activation.py
src/seekandemploy/batch_activation_progress.py
src/seekandemploy/cli.py
src/seekandemploy/collect.py
src/seekandemploy/collection.py
src/seekandemploy/connectors/__init__.py
src/seekandemploy/connectors/ashby.py
src/seekandemploy/connectors/bamboohr.py
src/seekandemploy/connectors/base.py
src/seekandemploy/connectors/classify.py
src/seekandemploy/connectors/generic_api.py
src/seekandemploy/connectors/generic_html.py
src/seekandemploy/connectors/greenhouse.py
src/seekandemploy/connectors/lever.py
src/seekandemploy/connectors/normalize.py
src/seekandemploy/connectors/personio.py
src/seekandemploy/connectors/probe.py
src/seekandemploy/connectors/recruitee.py
src/seekandemploy/connectors/registry.py
src/seekandemploy/connectors/remote_es.py
src/seekandemploy/connectors/smartrecruiters.py
src/seekandemploy/connectors/sync.py
src/seekandemploy/connectors/vendor_presets.py
src/seekandemploy/connectors/workable.py
src/seekandemploy/db.py
src/seekandemploy/extraction/__init__.py
src/seekandemploy/extraction/files.py
src/seekandemploy/extraction/heuristic.py
src/seekandemploy/extraction/llm.py
src/seekandemploy/extraction/models.py
src/seekandemploy/extraction/skills.py
src/seekandemploy/health.py
src/seekandemploy/laya/__init__.py
src/seekandemploy/laya/answers.py
src/seekandemploy/laya/client.py
src/seekandemploy/laya/questions.py
src/seekandemploy/laya_server_launcher.py
src/seekandemploy/laya_server_state.py
src/seekandemploy/logging_setup.py
src/seekandemploy/matching.py
src/seekandemploy/matching_runner.py
src/seekandemploy/migrations/env.py
src/seekandemploy/migrations/script.py.mako
src/seekandemploy/migrations/versions/0001_initial_schema.py
src/seekandemploy/migrations/versions/0002_add_source_config.py
src/seekandemploy/migrations/versions/0003_add_source_run_state.py
src/seekandemploy/migrations/versions/0004_add_job_offer_description.py
src/seekandemploy/migrations/versions/0005_add_match_scoring.py
src/seekandemploy/migrations/versions/0006_add_source_audit.py
src/seekandemploy/migrations/versions/0007_add_applications.py
src/seekandemploy/models.py
src/seekandemploy/profile_generation.py
src/seekandemploy/repository.py
src/seekandemploy/scheduler.py
src/seekandemploy/score.py
src/seekandemploy/scoring/__init__.py
src/seekandemploy/scoring/availability.py
src/seekandemploy/scoring/progress.py
src/seekandemploy/scoring/salary.py
src/seekandemploy/scoring/scorer.py
src/seekandemploy/scoring/server_command.py
src/seekandemploy/scoring/state.py
src/seekandemploy/scoring/verdict.py
src/seekandemploy/scoring/views.py
src/seekandemploy/scoring_progress.py
src/seekandemploy/scoring_runner.py
src/seekandemploy/selector_inference.py
src/seekandemploy/settings.py
src/seekandemploy/web/__init__.py
src/seekandemploy/web/catalogs.py
src/seekandemploy/web/dependencies.py
src/seekandemploy/web/errors.py
src/seekandemploy/web/helpers.py
src/seekandemploy/web/i18n.py
src/seekandemploy/web/models.py
src/seekandemploy/web/query.py
src/seekandemploy/web/router.py
src/seekandemploy/web/routes_applications.py
src/seekandemploy/web/routes_dashboard.py
src/seekandemploy/web/routes_matches.py
src/seekandemploy/web/routes_matching.py
src/seekandemploy/web/routes_offers.py
src/seekandemploy/web/routes_profiles.py
src/seekandemploy/web/routes_scoring.py
src/seekandemploy/web/routes_scoring_server.py
src/seekandemploy/web/routes_sources.py
src/seekandemploy/web/sorting.py
src/seekandemploy/web/static/PROVENANCE.md
src/seekandemploy/web/static/htmx.min.js
src/seekandemploy/web/static/styles.css
src/seekandemploy/web/templates/base.html
src/seekandemploy/web/templates/configure_source.html
src/seekandemploy/web/templates/dashboard.html
src/seekandemploy/web/templates/error.html
src/seekandemploy/web/templates/matches.html
src/seekandemploy/web/templates/offers.html
src/seekandemploy/web/templates/partials/audit_feedback.html
src/seekandemploy/web/templates/partials/audit_report.html
src/seekandemploy/web/templates/partials/batch_confirm.html
src/seekandemploy/web/templates/partials/batch_feedback.html
src/seekandemploy/web/templates/partials/batch_report.html
src/seekandemploy/web/templates/partials/configure_fields.html
src/seekandemploy/web/templates/partials/draft_fields.html
src/seekandemploy/web/templates/partials/listing.html
src/seekandemploy/web/templates/partials/profile_fields.html
src/seekandemploy/web/templates/partials/profile_summary.html
src/seekandemploy/web/templates/partials/scoring_progress.html
src/seekandemploy/web/templates/partials/scoring_server_status.html
src/seekandemploy/web/templates/partials/source_preview.html
src/seekandemploy/web/templates/partials/sources_fragment.html
src/seekandemploy/web/templates/partials/sources_table.html
src/seekandemploy/web/templates/probe.html
src/seekandemploy/web/templates/profile_delete.html
src/seekandemploy/web/templates/profile_form.html
src/seekandemploy/web/templates/profile_generate.html
src/seekandemploy/web/templates/profile_review.html
src/seekandemploy/web/templates/profiles.html
src/seekandemploy/web/templates/sources.html
tests/conftest.py
tests/fixtures/ashby/docplanner_job_board.json
tests/fixtures/bamboohr/jobandtalent_careers.json
tests/fixtures/factorial_jobs.html
tests/fixtures/generic_html_heading_titles.html
tests/fixtures/generic_html_no_listing.html
tests/fixtures/greenhouse/affirm_jobs.json
tests/fixtures/lever/contentsquare_postings.json
tests/fixtures/personio/holidaypirates.xml
tests/fixtures/recruitee/sequra_offers.json
tests/fixtures/remote_es/readme_slice.md
tests/fixtures/smartrecruiters/ecovadis_postings.json
tests/fixtures/teamtailor_jobs.html
tests/fixtures/workable/kahoot_jobs.json
tests/integration/__init__.py
tests/integration/test_docker.py
tests/integration/test_laya_server_live.py
tests/integration/test_scoring_live.py
tests/test_alerts.py
tests/test_app.py
tests/test_applications_api.py
tests/test_applications_cli.py
tests/test_applications_models.py
tests/test_applications_report.py
tests/test_audit.py
tests/test_audit_progress.py
tests/test_batch_activation.py
tests/test_batch_activation_progress.py
tests/test_classify.py
tests/test_collect.py
tests/test_collection.py
tests/test_connectors_ashby.py
tests/test_connectors_bamboohr.py
tests/test_connectors_base.py
tests/test_connectors_generic_api.py
tests/test_connectors_generic_html.py
tests/test_connectors_greenhouse.py
tests/test_connectors_lever.py
tests/test_connectors_normalize.py
tests/test_connectors_personio.py
tests/test_connectors_probe.py
tests/test_connectors_recruitee.py
tests/test_connectors_registry.py
tests/test_connectors_smartrecruiters.py
tests/test_connectors_sync.py
tests/test_connectors_unknown_modality.py
tests/test_connectors_vendor_presets.py
tests/test_connectors_workable.py
tests/test_db.py
tests/test_extraction_files.py
tests/test_extraction_heuristic.py
tests/test_extraction_llm.py
tests/test_extraction_models.py
tests/test_extraction_skills.py
tests/test_health.py
tests/test_integration_connectors.py
tests/test_laya_client.py
tests/test_laya_questions.py
tests/test_laya_server_launcher.py
tests/test_laya_server_state.py
tests/test_logging_setup.py
tests/test_matching.py
tests/test_matching_runner.py
tests/test_migration_0006.py
tests/test_models.py
tests/test_profile_generation.py
tests/test_project.py
tests/test_remote_es.py
tests/test_repository.py
tests/test_scheduler.py
tests/test_score_cli.py
tests/test_scoring_availability.py
tests/test_scoring_progress.py
tests/test_scoring_progress_store.py
tests/test_scoring_removal.py
tests/test_scoring_runner.py
tests/test_scoring_salary.py
tests/test_scoring_scorer.py
tests/test_scoring_server_command.py
tests/test_scoring_state.py
tests/test_scoring_verdict.py
tests/test_selector_inference.py
tests/test_settings.py
tests/test_web_dashboard.py
tests/test_web_errors.py
tests/test_web_generation.py
tests/test_web_i18n.py
tests/test_web_layout.py
tests/test_web_matches.py
tests/test_web_models.py
tests/test_web_offers.py
tests/test_web_profiles.py
tests/test_web_scoring_availability.py
tests/test_web_scoring_progress.py
tests/test_web_scoring_server.py
tests/test_web_sorting.py
tests/test_web_source_activation.py
tests/test_web_sources.py
tests/test_web_sources_controls.py
tests/test_web_triggers.py

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- tests/test_scheduler.py (first 60 lines of 48812 bytes) ---
"""Tests for the collection scheduler, the scheduled cycle, and the lifespan."""

import logging
from collections.abc import Iterator
from datetime import date, datetime, timedelta, timezone
from typing import Any

import pytest
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from seekandemploy.alerts import AlertLocale, HttpxTelegramTransport, TelegramTransport
from seekandemploy.app import create_app
from seekandemploy.audit import AuditReport, AuditResult, AuditVerdict
from seekandemploy.audit_progress import AuditReportStore
from seekandemploy.batch_activation import (
    BatchOutcome,
    BatchProgressObserver,
    BatchReport,
    BatchResult,
)
from seekandemploy.batch_activation_progress import BatchReportStore
from seekandemploy.collection import CollectionResult, RunOutcome
from seekandemploy.connectors.base import HttpTransport, HttpxTransport
from seekandemploy.db import init_database, make_session_factory
from apscheduler.jobstores.base import ConflictingIdError
from seekandemploy.matching_runner import MatchingResult
from seekandemploy.models import ConnectorType
from seekandemploy.scoring.views import ScoredReview
from seekandemploy.scoring_progress import ScoringProgressStore
from seekandemploy.scoring_runner import ScoringProfileRun, ScoringResult

from seekandemploy.scheduler import (
    AUDIT_NOW_DELAY_SECONDS,
    AUDIT_NOW_JOB_ID,
    BATCH_ACTIVATION_DELAY_SECONDS,
    BATCH_ACTIVATION_JOB_ID,
    COLLECT_NOW_DELAY_SECONDS,
    COLLECT_NOW_JOB_PREFIX,
    COLLECTION_JOB_ID,
    SCORE_NOW_DELAY_SECONDS,
    SCORE_NOW_JOB_ID,
    audit_now_job,
    batch_activation_job,
    build_collection_scheduler,
    collect_source_job,
    run_cycle,
    schedule_audit_now,
    schedule_batch_activation_now,
    schedule_collect_now,
    schedule_score_now,
    score_now_job,
)
from seekandemploy.settings import Settings


--- tests/test_repository.py (first 60 lines of 43736 bytes) ---
"""Tests for the persistence repository functions."""

from collections.abc import Iterator
from datetime import date, datetime
from typing import Final

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from seekandemploy.db import init_database, make_session_factory
from seekandemploy.models import (
    ConnectorType,
    JobOffer,
    Match,
    MatchProfile,
    Modality,
    Source,
    SourceStatus,
)
from seekandemploy.repository import (
    activate_source,
    browse_job_offers,
    browse_sources,
    count_audited_sources,
    count_job_offers,
    count_match_profiles,
    count_matches,
    count_sources,
    count_unscored_matches,
    delete_match_profile,
    delete_matches_for_profile,
    get_job_offer,
    get_match,
    get_match_profile,
    get_source,
    job_offers_by_source,
    job_offers_with_source,
    list_job_offers,
    list_match_profiles,
    list_matches,
    list_sources,
    offer_counts_by_source,
    record_audit_outcome,
    save_match_profile,
    save_source,
    matches_by_profile,
    unmatched_job_offers,
    update_match_profile,
    update_source,
    upsert_job_offer,
    upsert_match,
)
from seekandemploy.web.models import PAGE_SIZE as PAGE


@pytest.fixture
def session(sqlite_url: str) -> Iterator[Session]:
    """Yield a session over a freshly migrated database."""
    engine = init_database(sqlite_url)
--- tests/test_web_scoring_server.py (first 60 lines of 37601 bytes) ---
"""HTTP tests for the laya.cpp status fragment and the dashboard start/stop controls.

Offline by default: the availability probe is monkeypatched in
`seekandemploy.web.dependencies` — the single namespace both `refresh` and
`available` route through — the launcher is a recording fake installed on
`app.state.laya_server_launcher`, and the store is primed through its public
API. No test opens a socket. The single exception is the R24 stop-mechanics
test, which drives a **real** `LayaServerLauncher` against a real
`sys.executable -c` sleeping child (offline, milliseconds, cleaned up in a
`finally`) so the SIGTERM-and-reap contract is proven end to end.
"""

import logging
import os
import re
import signal
import sys
import time
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any, Final

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

import seekandemploy.web.dependencies as dependencies
from seekandemploy.app import create_app
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.laya_server_launcher import (
    LayaServerLaunchError,
    LayaServerLauncher,
    LayaServerStopError,
    STOP_GRACE_SECONDS,
    STOP_KILL_GRACE_SECONDS,
)
from seekandemploy.laya_server_state import FailureKind, LayaServerStore, ServerPhase
from seekandemploy.models import MatchProfile
from seekandemploy.repository import save_match_profile
from seekandemploy.settings import Settings
from seekandemploy.web.routes_scoring_server import (
    SCORING_SERVER_PATH,
    SCORING_SERVER_START_PATH,
    SCORING_SERVER_STOP_PATH,
)

COMMAND: Final[str] = "laya-cli --server --port {port} --variant {variant}"
RESOLVED_ARGV: Final[list[str]] = [
    "laya-cli",
    "--server",
    "--port",
    "8080",
    "--variant",
    "multilingual",
]
BASE_URL: Final[str] = "http://127.0.0.1:8080/v1"
WORKDIR: Final[str] = "/srv/laya.cpp"
LOG_PATH: Final[str] = "laya-server.log"
--- tests/test_web_triggers.py (first 60 lines of 34419 bytes) ---
"""Tests for the manual triggers: per-source collect now and run matching now."""

from collections.abc import Iterator
from typing import Any, Final

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session, sessionmaker

from seekandemploy.app import create_app
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.models import (
    ConnectorType,
    JobOffer,
    MatchProfile,
    Modality,
    Source,
    SourceStatus,
)
from seekandemploy.repository import save_match_profile, save_source
from seekandemploy.scheduler import (
    COLLECTION_JOB_ID,
    COLLECT_NOW_JOB_PREFIX,
    SCORE_NOW_JOB_ID,
)
from seekandemploy.settings import Settings
from seekandemploy.web.dependencies import get_scoring_available

ACCEPTED_MESSAGE_EN: Final[str] = (
    "Collection of Acme scheduled. Reload this view in a few seconds to see the result."
)
ACCEPTED_MESSAGE_ES: Final[str] = (
    "Se ha programado la recopilación de Acme. Recarga esta vista en unos segundos "
    "para ver el resultado."
)
COLLECTED_BANNER_EN: Final[str] = (
    "Collection scheduled. Reload this view in a few seconds to see the result."
)


@pytest.fixture
def session_factory(sqlite_url: str) -> Iterator[sessionmaker[Session]]:
    engine: Engine = init_database(sqlite_url)
    yield make_session_factory(engine)
    engine.dispose()


def _seed_source(
    session_factory: sessionmaker[Session],
    company: str = "Acme",
    status: SourceStatus = SourceStatus.active,
) -> int:
    """Persist one source and return its id."""
    with session_factory() as session:
        source = save_source(
            session,
            Source(
                company=company,
--- src/seekandemploy/web/catalogs.py (first 60 lines of 34173 bytes) ---
"""Bilingual translation catalogs: plain dictionaries, identical key sets.

Every fixed interface string of the frontend lives here. `translate` looks up
the active catalog and falls back to the English one, then to the raw key.
Copy avoids plural-form machinery: counters stay inside parentheses, the
numeral usually follows an invariant noun, and `offer_age_one` picks the
singular when `days == 1`.
"""

from typing import Final

EN_CATALOG: Final[dict[str, str]] = {
    # Brand and chrome
    "app_name": "seekandemploy",
    "footer_tagline": "seekandemploy — your personal job radar",
    "language_name_en": "English",
    "language_name_es": "Español",
    "skip_to_content": "Skip to content",
    # Navigation
    "nav_dashboard": "Dashboard",
    "nav_offers": "Offers",
    "nav_profiles": "Profiles",
    "nav_sources": "Sources",
    # Scoring progress (navigation live region)
    "scoring_progress_running": "Scoring {done}/{total}",
    "scoring_progress_summary": (
        "{scored} scored · {failed} failed profiles · {pending} pending"
    ),
    "scoring_progress_nothing": "Nothing to score",
    "scoring_progress_pending": "{pending} pending scoring",
    "scoring_progress_up_to_date": "Up to date",
    # Actions
    "action_search": "Search",
    "action_reset": "Reset",
    "action_save": "Save",
    "action_save_changes": "Save changes",
    "action_create": "Create profile",
    "action_cancel": "Cancel",
    "action_delete": "Delete",
    "action_delete_profile": "Delete profile",
    "action_edit": "Edit",
    "action_new_profile": "New profile",
    "action_run_matching": "Run matching now",
    "action_start_scoring_server": "Start scoring server",
    "action_stop_scoring_server": "Stop scoring server",
    "action_collect_now": "Collect now",
    "action_back_to_profiles": "Back to profiles",
    "action_back_home": "Back to dashboard",
    # Pagination
    "pagination_previous": "Previous",
    "pagination_next": "Next",
    "pagination_status": "Page {page} of {last}",
    "pagination_label": "Pagination",
    # Dashboard
    "dashboard_title": "Dashboard",
    "dashboard_subtitle": "The state of your job search at a glance.",
    "stat_offers": "Offers",
    "stat_matches": "Matches",
    "stat_profiles": "Profiles",
    "stat_sources": "Sources",
--- tests/test_web_sources.py (first 60 lines of 34051 bytes) ---
"""Tests for the sources view and its collection state rendering."""

from collections.abc import Iterator
from datetime import datetime
from typing import Final

import pytest
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from seekandemploy.app import create_app
from seekandemploy.audit import AuditResult, AuditVerdict
from seekandemploy.audit_progress import AuditReportStore
from seekandemploy.batch_activation import BatchOutcome, BatchResult
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.models import ConnectorType, Source, SourceStatus
from seekandemploy.repository import get_source, record_audit_outcome, save_source
from seekandemploy.scheduler import AUDIT_NOW_JOB_ID, BATCH_ACTIVATION_JOB_ID
from seekandemploy.settings import Settings

FIXED_SUCCESS: Final[datetime] = datetime(2026, 9, 4, 12, 0, 0)
FIXED_ERROR: Final[datetime] = datetime(2026, 9, 4, 18, 30, 0)


@pytest.fixture
def session_factory(sqlite_url: str) -> Iterator[sessionmaker[Session]]:
    engine: Engine = init_database(sqlite_url)
    yield make_session_factory(engine)
    engine.dispose()


@pytest.fixture
def client(sqlite_url: str) -> Iterator[TestClient]:
    settings = Settings(environment="test", log_level="INFO", database_url=sqlite_url)
    with TestClient(create_app(settings)) as test_client:
        yield test_client


@pytest.fixture
def audit_app(
    sqlite_url: str, session_factory: sessionmaker[Session]
) -> Iterator[tuple[TestClient, FastAPI, AsyncIOScheduler]]:
    """Client over an app whose scheduler is an unstarted instance under test control."""
    app = create_app(
        Settings(environment="test", log_level="INFO", database_url=sqlite_url)
    )
    with TestClient(app) as test_client:
        scheduler = AsyncIOScheduler()
        app.state.scheduler = scheduler
        app.state.session_factory = session_factory
        yield test_client, app, scheduler


def _seed_source(
    session_factory: sessionmaker[Session],
    company: str,
    connector: ConnectorType = ConnectorType.greenhouse,
--- src/seekandemploy/web/routes_sources.py (first 60 lines of 33384 bytes) ---
"""Sources view: collection state, collect/audit triggers, and activation."""

import logging
from collections.abc import Mapping, Sequence
from dataclasses import asdict
from datetime import date
from math import ceil
from typing import Any, Final
from urllib.parse import urlencode, parse_qs

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session
from starlette.datastructures import FormData

from seekandemploy.audit import (
    DEFAULT_AUDIT_CONNECTORS,
    AuditReport,
    AuditVerdict,
)
from seekandemploy.audit_progress import AuditReportStore
from seekandemploy.batch_activation import BatchReport, list_batch_candidates
from seekandemploy.batch_activation_progress import BatchReportStore
from seekandemploy.connectors.base import (
    DEFAULT_TIMEOUT_SECONDS,
    ConnectorError,
    HttpxTransport,
)
from seekandemploy.connectors.generic_html import GenericHtmlConfig
from seekandemploy.connectors.probe import probe_connector
from seekandemploy.connectors.registry import build_connector
from seekandemploy.connectors.vendor_presets import preset_for
from seekandemploy.models import ConnectorType, Source, SourceStatus
from seekandemploy.repository import (
    activate_source,
    browse_sources,
    count_audited_sources,
    count_sources,
    get_source,
)
from seekandemploy.scheduler import (
    schedule_audit_now,
    schedule_batch_activation_now,
    schedule_collect_all_now,
    schedule_collect_now,
)
from seekandemploy.selector_inference import infer_generic_html_config
from seekandemploy.web.dependencies import get_locale, get_session, get_today
from seekandemploy.web.helpers import is_htmx_request
from seekandemploy.web.i18n import Locale, render, translate
from seekandemploy.web.models import (
    ACTIVATABLE_CONNECTORS,
    PAGE_SIZE,
    AuditFeedbackFragment,
    AuditReportFragment,
    AuditRow,
    BatchConfirmFragment,
    BatchReportFragment,
--- tests/test_web_source_activation.py (first 60 lines of 28500 bytes) ---
"""Tests for the source activation loop: configure, preview, and activate.

Every exercise is network-free: preview fetches go through the monkeypatched
`_fetch_source_page` seam, over an in-memory-file SQLite database and a
`TestClient` whose `app.state.session_factory` is swapped to the test factory.
"""

from collections.abc import Iterator
from typing import Any, Final

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from seekandemploy.app import create_app
from seekandemploy.connectors.base import ConnectorError
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.models import ConnectorType, Source, SourceStatus
from seekandemploy.repository import get_source, save_source
from seekandemploy.settings import Settings
from seekandemploy.web import routes_sources
from seekandemploy.web.models import ConfigureFormInput, ConfigurePage

VALID_FORM: Final[dict[str, str]] = {
    "list_selector": "li",
    "title_selector": "a",
    "link_selector": "a",
    "location_selector": "",
    "description_selector": "",
    "published_selector": "",
    "published_attribute": "",
    "remote_keywords": "",
    "hybrid_keywords": "",
}


@pytest.fixture
def session_factory(sqlite_url: str) -> Iterator[sessionmaker[Session]]:
    engine: Engine = init_database(sqlite_url)
    yield make_session_factory(engine)
    engine.dispose()


@pytest.fixture
def app(sqlite_url: str) -> Iterator[FastAPI]:
    yield create_app(
        Settings(environment="test", log_level="INFO", database_url=sqlite_url)
    )


@pytest.fixture
def client(
    app: FastAPI, session_factory: sessionmaker[Session]
) -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        app.state.session_factory = session_factory
        yield test_client


Write ONLY the plan (the three sections). No prose outside them.