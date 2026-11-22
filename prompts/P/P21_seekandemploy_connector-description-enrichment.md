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
R1: QUAN el connector de Workable sincronitza una font, EL SISTEMA HA DE persistir una descripció no buida per a cada oferta publicada el shortcode de la qual aparegui al payload d'enriquiment v1.

R2: EL SISTEMA HA DE fer com a màxim **una** petició d'enriquiment per font i cicle de Workable, independentment del nombre d'ofertes de la font.

R3: QUAN la petició d'enriquiment d'una font de Workable falla, EL SISTEMA HA DE completar el cicle amb el llistat intacte (descripcions NULL), registrar un warning i no avortar la resta de fonts.

R4: QUAN el connector de SmartRecruiters sincronitza una oferta, EL SISTEMA HA DE persistir la descripció extreta de `jobAd.sections.jobDescription.text` del detall del posting.

R5: QUAN el detall d'una oferta de SmartRecruiters falla, EL SISTEMA HA DE desar l'oferta sense descripció, registrar un warning i continuar amb la resta d'ofertes de la font.

R6: EL SISTEMA HA DE no introduir al catàleg cap oferta que el llistat autoritatiu de Workable no reporti (les ofertes tancades del payload v1 no han d'arribar a `job_offer`).

--- FEATURE TITLE ---
feat(connectors): real descriptions for workable and smartrecruiters

--- REPOSITORY FILE TREE (before implementation, truncated) ---
.dockerignore
.env.example
.gitattributes
.gitignore
.opencode/agent/implementer.md
.opencode/agent/leader.md
.opencode/agent/reviewer.md
.opencode/agent/spec-author.md
AGENTS.md
Dockerfile
HARNESS.md
Makefile
README.md
alembic.ini
applications.html
applications.jsonl
compose.yaml
dashboard.yaml
docs/architecture.md
docs/conventions.md
docs/sonarqube-protocol.md
docs/specs.md
docs/verification.md
harness/CHECKPOINTS.md
harness/feature_list.json
harness/init.sh
harness/logs/score-confidence/batch-1.log
harness/logs/score-confidence/batch-2.log
harness/logs/score-confidence/batch-3.log
harness/logs/title-only-exclusions/batch-1.log
harness/progress/current.md
harness/progress/history.md
harness/progress/impl_application_tracking.md
harness/progress/impl_batch-source-activation.md
harness/progress/impl_collection-scheduler.md
harness/progress/impl_connector-framework.md
harness/progress/impl_core-models-persistence.md
harness/progress/impl_cv-profile-generation.md
harness/progress/impl_event-log.md
harness/progress/impl_generic-html-audit.md
harness/progress/impl_generic-html-selector-inference.md
harness/progress/impl_laya-server-start.md
harness/progress/impl_laya-typed-scoring.md
harness/progress/impl_matching-engine.md
harness/progress/impl_modality-unknown-recovery.md
harness/progress/impl_offers_to_apply.md
harness/progress/impl_project-skeleton.md
harness/progress/impl_resilient-offer-mapping.md
harness/progress/impl_score-confidence.md
harness/progress/impl_scoring-on-matching.md
harness/progress/impl_scoring-pending-count.md
harness/progress/impl_scoring-progress.md
harness/progress/impl_source-audit-persistence.md
harness/progress/impl_sources-table-controls.md
harness/progress/impl_telegram-alerts.md
harness/progress/impl_title-only-exclusions.md
harness/progress/impl_vendor-source-presets.md
harness/progress/impl_web-dashboard.md
harness/progress/impl_web-source-activation.md
harness/progress/review_batch-source-activation.md
harness/progress/review_collection-scheduler.md
harness/progress/review_connector-framework.md
harness/progress/review_core-models-persistence.md
harness/progress/review_cv-profile-generation.md
harness/progress/review_event-log.md
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
harness/progress/spec_event-log.md
harness/sonar.env.example
harness/specs/application-tracking/design.md
harness/specs/application-tracking/requirements.md
harness/specs/application-tracking/tasks.md
harness/specs/apply-notes-edit/APPROVAL.md
harness/specs/apply-notes-edit/design.md
harness/specs/apply-notes-edit/requirements.md
harness/specs/apply-notes-edit/tasks.md
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
harness/specs/event-log/design.md
harness/specs/event-log/requirements.md
harness/specs/event-log/tasks.md
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
harness/specs/offers_to_apply/design.md
harness/specs/offers_to_apply/requirements.md
harness/specs/offers_to_apply/tasks.md
harness/specs/project-skeleton/design.md
harness/specs/project-skeleton/requirements.md
harness/specs/project-skeleton/tasks.md
harness/specs/resilient-offer-mapping/design.md
harness/specs/resilient-offer-mapping/requirements.md
harness/specs/resilient-offer-mapping/tasks.md
harness/specs/score-confidence/APPROVAL.md
harness/specs/score-confidence/design.md
harness/specs/score-confidence/requirements.md
harness/specs/score-confidence/tasks.md
harness/specs/score-confidence/traceability.txt
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
harness/specs/title-only-exclusions/APPROVAL.md
harness/specs/title-only-exclusions/design.md
harness/specs/title-only-exclusions/requirements.md
harness/specs/title-only-exclusions/tasks.md
harness/specs/tracker-skill/APPROVAL.md
harness/specs/tracker-skill/design.md
harness/specs/tracker-skill/requirements.md
harness/specs/tracker-skill/tasks.md
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
harness/tools/check-traceability.py
harness/tools/commit-msg
harness/tools/commit.sh
harness/tools/sonar-review.sh
harness/tools/validate-feature-list.py
opencode.json
pyproject.toml
skills/README.md
skills/install.sh
skills/seekandemploy/SKILL.md
sonar-project.properties
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
src/seekandemploy/event_log.py
src/seekandemploy/extraction/__init__.py
src/seekandemploy/extraction/files.py
src/seekandemploy/extraction/heuristic.py
src/seekandemploy/extraction/llm.py
src/seekandemploy/extraction/models.py
src/seekandemploy/extraction/skills.py
src/seekandemploy/health.py
src/seekandemploy/identity.py
src/seekandemploy/laya/__init__.py
src/seekandemploy/laya/answers.py
src/seekandemploy/laya/client.py
src/seekandemploy/laya/questions.py
src/seekandemploy/laya_server_launcher.py
src/seekandemploy/laya_server_state.py
src/seekandemploy/legacy_export.py
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
src/seekandemploy/migrations/versions/0008_event_log_identity.py
src/seekandemploy/migrations/versions/0009_match_score_confidence.py
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
src/seekandemploy/snapshot.py
src/seekandemploy/tracker_service.py
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
tests/test_event_log.py
tests/test_extraction_files.py
tests/test_extraction_heuristic.py
tests/test_extraction_llm.py
tests/test_extraction_models.py
tests/test_extraction_skills.py
tests/test_gitattributes.py
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
tests/test_migration_0008.py
tests/test_migration_0009.py
tests/test_models.py
tests/test_offer_add.py
tests/test_profile_generation.py
tests/test_project.py
tests/test_remote_es.py

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- src/seekandemploy/web/catalogs.py (first 60 lines of 34265 bytes) ---
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
--- src/seekandemploy/web/routes_sources.py (first 60 lines of 33850 bytes) ---
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
--- src/seekandemploy/repository.py (first 60 lines of 30929 bytes) ---
"""Persistence functions for the domain models: session-first, flush-not-commit.

Every function takes a `Session` as its first argument, mutates or reads,
flushes, and returns; transaction control stays with the caller. Constraint
violations surface as `sqlalchemy.exc.IntegrityError` from the flush.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime
import re
from typing import Any, Final

from sqlalchemy import exists, func, or_, select
from sqlalchemy.orm import Session

from seekandemploy.models import (
    DEFAULT_SALARY_CURRENCY,
    MANUAL_CONNECTOR as models_MANUAL_CONNECTOR,
    Application,
    ApplicationEvent,
    ApplicationEventKind,
    ApplicationStatus,
    ConnectorType,
    JobOffer,
    Match,
    MatchProfile,
    Modality,
    Source,
    SourceStatus,
    TrackerMeta,
)

__all__ = [
    "activate_source",
    "add_application_event",
    "applications_by_id_prefix",
    "browse_job_offers",
    "browse_sources",
    "count_audited_sources",
    "count_job_offers",
    "count_match_profiles",
    "count_matches",
    "count_sources",
    "count_unscored_matches",
    "delete_application",
    "delete_match_profile",
    "delete_matches_for_profile",
    "find_match_profile",
    "get_application",
    "get_job_offer",
    "get_match",
    "get_match_profile",
    "get_or_create_manual_source",
    "get_tracker_meta",
    "normalize_url",
    "pending_manual_offers",
    "get_source",
    "job_offers_by_source",
    "job_offers_with_source",
--- tests/test_collection.py (first 60 lines of 24445 bytes) ---
"""Tests for the collection runner over a fake transport and a temp database."""

import json
from collections.abc import Iterator, Mapping
from datetime import date, datetime, timedelta, timezone
from typing import Any, Final

import pytest
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session, sessionmaker

from seekandemploy.collection import (
    CollectionResult,
    RunOutcome,
    SourceRun,
    run_collection,
    run_collection_for_source,
)
from seekandemploy.connectors.base import ConnectorError, HttpTransport
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.models import ConnectorType, JobOffer, Source, SourceStatus

FIXED_NOW: Final[datetime] = datetime(2026, 9, 4, 12, 0, 0, tzinfo=timezone.utc)
EXPECTED_RUN_TIME: Final[datetime] = datetime(2026, 9, 4, 12, 0, 0)
EXPECTED_TODAY: Final[date] = date(2026, 9, 4)
NON_UTC_NOW: Final[datetime] = datetime(
    2026, 3, 1, 23, 30, 0, tzinfo=timezone(timedelta(hours=2))
)
EXPECTED_NON_UTC_RUN_TIME: Final[datetime] = datetime(2026, 3, 1, 21, 30, 0)

ACME_API_URL: Final[str] = "https://api.lever.co/v0/postings/acme?mode=json"
GLOBEX_API_URL: Final[str] = "https://api.lever.co/v0/postings/globex?mode=json"
INOVA_API_URL: Final[str] = "https://api.lever.co/v0/postings/inova?mode=json"

REMOTE_OFFER: Final[dict[str, Any]] = {
    "id": "aa11-bb22",
    "text": "Remote Backend Engineer",
    "createdAt": 1787765871354,
    "hostedUrl": "https://jobs.lever.co/acme/aa11-bb22",
    "workplaceType": "remote",
    "categories": {"location": "Barcelona, Spain"},
    "salaryRange": {
        "min": 30000,
        "max": 50000,
        "currency": "EUR",
        "interval": "per-year-salary",
    },
}
HYBRID_OFFER: Final[dict[str, Any]] = {
    "id": "cc33-dd44",
    "text": "Hybrid Product Manager",
    "createdAt": 1787136040111,
    "hostedUrl": "https://jobs.lever.co/acme/cc33-dd44",
    "workplaceType": "hybrid",
    "categories": {"location": "Madrid, Spain"},
}
UNMODAL_OFFER: Final[dict[str, Any]] = {
    "id": "x1",
    "text": "Office Manager",
    "createdAt": 1787765871354,
--- src/seekandemploy/tracker_service.py (first 60 lines of 24305 bytes) ---
"""The tracker's coordinator: the event log on the front, SQLite as its cache.

Every mutation is validated, resolved, appended to `applications.jsonl`
(locked + fsynced), applied to SQLite through the same reducer the replay
uses, and committed together with the log fingerprint, so a crash can only
leave the log ahead of the cache — never the other way around. Any read or
write first passes `ensure_fresh`, which rebuilds the cache whenever the
log hash disagrees with `tracker_meta`. File I/O lives in
`event_log.ApplicationLog`; the repository stays session-first and
flush-not-commit, and the service owns the transaction boundary.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import cast
import uuid

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session, selectinload

from seekandemploy.event_log import (
    EMPTY_LOG_SHA256,
    ApplicationLog,
    LogEntry,
    LogEventType,
    LogFingerprint,
    LogFormatError,
)
from seekandemploy.identity import seeded_applied_uuid
from seekandemploy.legacy_export import plan_export
from seekandemploy.models import (
    Application,
    ApplicationEvent,
    ApplicationEventKind,
    ApplicationStatus,
    JobOffer,
)
from seekandemploy.repository import (
    add_application_event,
    applications_by_id_prefix,
    delete_application,
    get_application,
    get_job_offer,
    get_tracker_meta,
    normalize_url,
    save_application,
    set_tracker_meta,
)
from seekandemploy.snapshot import write_applications_snapshot

LOG_SHA256_KEY: str = "log_sha256"
LOG_LINES_KEY: str = "log_lines"
REBUILT_AT_KEY: str = "rebuilt_at"

__all__ = [
    "AmbiguousApplicationPrefix",
    "ApplicationNotFound",
    "ExportResult",
--- tests/test_audit.py (first 60 lines of 23660 bytes) ---
"""Tests for the audit engine: constants, transport seam, classifier, coordinator."""

from collections.abc import Callable, Iterator
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from typing import Final

import httpx
import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from seekandemploy.audit import (
    DEFAULT_AUDIT_CONNECTORS,
    HREF_ATTRIBUTE_PATTERN,
    MIN_JOB_LINKS,
    is_job_link,
    AuditProgressObserver,
    AuditReport,
    AuditResult,
    AuditVerdict,
    HttpxAuditTransport,
    HttpResponse,
    classify_page,
    count_unique_job_links,
    run_audit,
)
from seekandemploy.connectors.base import ConnectorError
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.models import ConnectorType, Source, SourceStatus
from seekandemploy.repository import save_source

LISTING_URL: Final[str] = "https://jobs.example/listing"
RUN_TIME: Final[datetime] = datetime(2026, 9, 6, 12, 0, 0, tzinfo=timezone.utc)
NAIVE_RUN_TIME: Final[datetime] = datetime(2026, 9, 6, 12, 0, 0)


def _job_links(count: int) -> str:
    """HTML carrying `count` distinct job-link anchors."""
    return "".join(f'<a href="/jobs/{index}">Job {index}</a>' for index in range(count))


def test_audit_verdict_members_are_pinned() -> None:
    assert [verdict.value for verdict in AuditVerdict] == [
        "unreachable",
        "blocked",
        "js_rendered",
        "parseable",
    ]


def test_default_audit_connectors_are_the_three_generic_families() -> None:
    assert DEFAULT_AUDIT_CONNECTORS == frozenset(
        {
            ConnectorType.generic_html,
            ConnectorType.teamtailor,
            ConnectorType.factorial,
        }
    )

--- src/seekandemploy/web/models.py (first 60 lines of 22767 bytes) ---
"""Typed view DTOs, page-size constant, and profile form parsing.

Every route passes exactly one frozen DTO of this module to `render`. The
only shapes that ever reach the ORM are the domain models built from
`ProfileValues`, the validated output of `parse_profile_input`.
"""

import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Final, Mapping, Self

from seekandemploy.audit import AuditVerdict
from seekandemploy.batch_activation import BatchOutcome
from seekandemploy.extraction import ExtractionMethod
from seekandemploy.laya_server_state import FailureKind, ServerPhase
from seekandemploy.models import ConnectorType, Modality, SourceStatus
from seekandemploy.web.query import OfferQuery, SourcesQuery
from seekandemploy.web.sorting import ColumnSort, SortState

PAGE_SIZE: Final[int] = 25

ACTIVATABLE_CONNECTORS: Final[frozenset[ConnectorType]] = frozenset(
    {
        ConnectorType.generic_html,
        ConnectorType.teamtailor,
        ConnectorType.factorial,
    }
)

MULTI_VALUE_SEPARATORS: Final[tuple[str, ...]] = (",", "\n")

REVIEW_FIELD_NAMES: Final[tuple[str, ...]] = (
    "name",
    "keywords",
    "excluded_keywords",
    "excluded_companies",
    "modality",
    "location",
    "salary_min",
    "max_offer_age_days",
)
REVIEW_INDEX_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^(?:" + "|".join(REVIEW_FIELD_NAMES) + r")_(\d+)$"
)

__all__ = [
    "ACTIVATABLE_CONNECTORS",
    "PAGE_SIZE",
    "AuditFeedbackFragment",
    "AuditReportFragment",
    "AuditRow",
    "BatchConfirmFragment",
    "BatchReportFragment",
    "BatchRow",
    "ConfigureFormInput",
    "ConfigurePage",
    "DashboardOverview",
    "ErrorPage",
    "FormError",
--- tests/test_batch_activation.py (first 60 lines of 22238 bytes) ---
"""Tests for the batch activation coordinator: candidates, run, and report."""

from collections.abc import Iterator, Mapping
from dataclasses import FrozenInstanceError
from datetime import date
from pathlib import Path
from typing import Any, Final, Literal

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from seekandemploy.audit import AuditVerdict
from seekandemploy.batch_activation import (
    BATCH_ACTIVATABLE_CONNECTORS,
    BATCH_SKIP_INVALID_CONFIG,
    BATCH_SKIP_MISSING,
    BATCH_SKIP_NO_CONFIG,
    BATCH_SKIP_NO_OFFERS,
    BATCH_SKIP_UNREACHABLE,
    BatchCandidate,
    BatchOutcome,
    BatchProgressObserver,
    BatchReport,
    BatchResult,
    list_batch_candidates,
    run_batch_activation,
)
from seekandemploy.connectors.base import ConnectorError
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.models import ConnectorType, Source, SourceStatus
from seekandemploy.repository import get_source, save_source

FIXED_TODAY: Final[date] = date(2026, 9, 1)
LISTING_CONFIG: Final[dict[str, Any]] = {
    "list_selector": "li",
    "title_selector": "a",
    "link_selector": "a",
}
LISTING_HTML: Final[str] = (
    "<ul>"
    '<li><a href="/jobs/a">Engineer A</a></li>'
    '<li><a href="/jobs/b">Engineer B</a></li>'
    '<li><a href="/jobs/c">Engineer C</a></li>'
    "</ul>"
)


@pytest.fixture
def session_factory(sqlite_url: str) -> Iterator[sessionmaker[Session]]:
    engine: Engine = init_database(sqlite_url)
    yield make_session_factory(engine)
    engine.dispose()


def _seed_source(
    session_factory: sessionmaker[Session],
    company: str,
    connector: ConnectorType = ConnectorType.generic_html,
    *,

Write ONLY the plan (the three sections). No prose outside them.