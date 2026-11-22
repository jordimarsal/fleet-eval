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
R1: WHEN `JobConnector.map_offer` raises `ValueError` for one payload during `sync_source`, the system shall skip that payload and continue mapping the remaining payloads.

R2: WHEN `sync_source` finishes, the system shall persist exactly one `JobOffer` per successfully mapped payload through `upsert_job_offer`.

R3: The system shall not mark a source as failed when its only mapping failures are per-payload `ValueError` exceptions.

R4: The system shall expose the number of payloads skipped by per-payload `ValueError` in `SyncResult` through a `skipped` field.

R5: The system shall expose the number of payloads skipped by per-payload `ValueError` in one attempted source through a `SourceRun.skipped` field.

R6: The system shall expose the total number of payloads skipped across a collection run through a `CollectionResult.skipped` property.

R7: WHEN `sync_source` returns without raising for a source, the system shall set the source status to `active`, including when every payload was skipped.

R8: WHEN the `api_url` derivation of a connector raises `ValueError`, the system shall propagate the `ValueError` out of `sync_source`.

R9: WHEN the validation of a `GenericApiConfig` or a `GenericHtmlConfig` raises `ValueError`, the system shall propagate the `ValueError` out of `sync_source`.

R10: WHEN `JobConnector.parse` raises `ValueError`, the system shall propagate the `ValueError` out of `sync_source`.

R11: WHEN the transport raises `ConnectorError`, the system shall propagate the `ConnectorError` out of `sync_source`.

R12: WHEN `sync_source` raises `ValueError` or `ConnectorError`, the system shall set the source status to `error`.

R13: WHEN `sync_source` raises `ValueError` or `ConnectorError`, the system shall roll back every uncommitted `JobOffer` change of that source.

R14: WHEN `sync_source` skips at least one payload, the system shall log one warning that names the source and reports the skipped count, using `%s` placeholders.

--- FEATURE TITLE ---
feat(resilient-offer-mapping): skip unmappable offers instead of failing a source

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
compose.yaml
docs/architecture.md
docs/conventions.md
docs/specs.md
docs/verification.md
harness/CHECKPOINTS.md
harness/feature_list.json
harness/init.sh
harness/progress/current.md
harness/progress/history.md
harness/progress/impl_collection-scheduler.md
harness/progress/impl_connector-framework.md
harness/progress/impl_core-models-persistence.md
harness/progress/impl_matching-engine.md
harness/progress/impl_project-skeleton.md
harness/progress/impl_telegram-alerts.md
harness/progress/impl_web-dashboard.md
harness/progress/review_collection-scheduler.md
harness/progress/review_connector-framework.md
harness/progress/review_core-models-persistence.md
harness/progress/review_matching-engine.md
harness/progress/review_project-skeleton.md
harness/progress/review_telegram-alerts.md
harness/progress/review_web-dashboard.md
harness/specs/collection-scheduler/design.md
harness/specs/collection-scheduler/requirements.md
harness/specs/collection-scheduler/tasks.md
harness/specs/connector-framework/design.md
harness/specs/connector-framework/requirements.md
harness/specs/connector-framework/tasks.md
harness/specs/core-models-persistence/design.md
harness/specs/core-models-persistence/requirements.md
harness/specs/core-models-persistence/tasks.md
harness/specs/llm-scoring/APPROVAL.md
harness/specs/llm-scoring/design.md
harness/specs/llm-scoring/requirements.md
harness/specs/llm-scoring/tasks.md
harness/specs/llm-scoring/verification.md
harness/specs/matching-engine/design.md
harness/specs/matching-engine/requirements.md
harness/specs/matching-engine/tasks.md
harness/specs/project-skeleton/design.md
harness/specs/project-skeleton/requirements.md
harness/specs/project-skeleton/tasks.md
harness/specs/telegram-alerts/design.md
harness/specs/telegram-alerts/requirements.md
harness/specs/telegram-alerts/tasks.md
harness/specs/web-dashboard/audit-1-usability-findings.md
harness/specs/web-dashboard/audit-2-visual-a11y-findings.md
harness/specs/web-dashboard/audit-3-copy-findings.md
harness/specs/web-dashboard/design.md
harness/specs/web-dashboard/requirements.md
harness/specs/web-dashboard/tasks.md
pyproject.toml
src/seekandemploy/__init__.py
src/seekandemploy/alerts.py
src/seekandemploy/app.py
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
src/seekandemploy/connectors/recruitee.py
src/seekandemploy/connectors/registry.py
src/seekandemploy/connectors/remote_es.py
src/seekandemploy/connectors/smartrecruiters.py
src/seekandemploy/connectors/sync.py
src/seekandemploy/connectors/workable.py
src/seekandemploy/db.py
src/seekandemploy/health.py
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
src/seekandemploy/models.py
src/seekandemploy/repository.py
src/seekandemploy/scheduler.py
src/seekandemploy/score.py
src/seekandemploy/scoring/__init__.py
src/seekandemploy/scoring/prompt.py
src/seekandemploy/scoring/response.py
src/seekandemploy/scoring/scorer.py
src/seekandemploy/scoring/verdict.py
src/seekandemploy/scoring/views.py
src/seekandemploy/scoring_runner.py
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
src/seekandemploy/web/routes_dashboard.py
src/seekandemploy/web/routes_matches.py
src/seekandemploy/web/routes_matching.py
src/seekandemploy/web/routes_offers.py
src/seekandemploy/web/routes_profiles.py
src/seekandemploy/web/routes_sources.py
src/seekandemploy/web/sorting.py
src/seekandemploy/web/static/PROVENANCE.md
src/seekandemploy/web/static/htmx.min.js
src/seekandemploy/web/static/styles.css
src/seekandemploy/web/templates/base.html
src/seekandemploy/web/templates/dashboard.html
src/seekandemploy/web/templates/error.html
src/seekandemploy/web/templates/matches.html
src/seekandemploy/web/templates/offers.html
src/seekandemploy/web/templates/partials/listing.html
src/seekandemploy/web/templates/partials/profile_fields.html
src/seekandemploy/web/templates/partials/profile_summary.html
src/seekandemploy/web/templates/partials/sources_fragment.html
src/seekandemploy/web/templates/partials/sources_table.html
src/seekandemploy/web/templates/probe.html
src/seekandemploy/web/templates/profile_delete.html
src/seekandemploy/web/templates/profile_form.html
src/seekandemploy/web/templates/profiles.html
src/seekandemploy/web/templates/sources.html
tests/conftest.py
tests/fixtures/ashby/docplanner_job_board.json
tests/fixtures/bamboohr/jobandtalent_careers.json
tests/fixtures/greenhouse/affirm_jobs.json
tests/fixtures/lever/contentsquare_postings.json
tests/fixtures/personio/holidaypirates.xml
tests/fixtures/recruitee/sequra_offers.json
tests/fixtures/remote_es/readme_slice.md
tests/fixtures/smartrecruiters/ecovadis_postings.json
tests/fixtures/workable/kahoot_jobs.json
tests/integration/__init__.py
tests/integration/test_docker.py
tests/integration/test_scoring_live.py
tests/test_alerts.py
tests/test_app.py
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
tests/test_connectors_recruitee.py
tests/test_connectors_registry.py
tests/test_connectors_smartrecruiters.py
tests/test_connectors_sync.py
tests/test_connectors_workable.py
tests/test_db.py
tests/test_health.py
tests/test_integration_connectors.py
tests/test_logging_setup.py
tests/test_matching.py
tests/test_matching_runner.py
tests/test_models.py
tests/test_project.py
tests/test_remote_es.py
tests/test_repository.py
tests/test_scheduler.py
tests/test_score_cli.py
tests/test_scoring_prompt.py
tests/test_scoring_response.py
tests/test_scoring_runner.py
tests/test_scoring_scorer.py
tests/test_scoring_verdict.py
tests/test_settings.py
tests/test_web_dashboard.py
tests/test_web_errors.py
tests/test_web_i18n.py
tests/test_web_layout.py
tests/test_web_matches.py
tests/test_web_models.py
tests/test_web_offers.py
tests/test_web_profiles.py
tests/test_web_sorting.py
tests/test_web_sources.py
tests/test_web_triggers.py

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- tests/test_repository.py (first 60 lines of 27525 bytes) ---
"""Tests for the persistence repository functions."""

from collections.abc import Iterator
from datetime import date

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
)
from seekandemploy.repository import (
    browse_job_offers,
    count_job_offers,
    count_match_profiles,
    count_matches,
    count_sources,
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
    factory = make_session_factory(engine)
    with factory() as session:
        yield session
    engine.dispose()


def _save_source(
--- tests/test_web_triggers.py (first 60 lines of 25431 bytes) ---
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
from seekandemploy.scheduler import COLLECTION_JOB_ID, COLLECT_NOW_JOB_PREFIX
from seekandemploy.settings import Settings

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
                connector=ConnectorType.greenhouse,
                url=f"https://{company}.example",
                status=status,
            ),
        )
--- tests/test_scheduler.py (first 60 lines of 24145 bytes) ---
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
from seekandemploy.collection import CollectionResult, RunOutcome
from seekandemploy.connectors.base import HttpTransport, HttpxTransport
from seekandemploy.db import init_database, make_session_factory
from apscheduler.jobstores.base import ConflictingIdError
from seekandemploy.matching_runner import MatchingResult
from seekandemploy.scoring_runner import ScoringProfileRun, ScoringResult

from seekandemploy.scheduler import (
    COLLECT_NOW_DELAY_SECONDS,
    COLLECT_NOW_JOB_PREFIX,
    COLLECTION_JOB_ID,
    build_collection_scheduler,
    collect_source_job,
    run_cycle,
    schedule_collect_now,
)
from seekandemploy.settings import Settings


def _settings(sqlite_url: str) -> Settings:
    """Build deterministic default settings for one scheduler or lifespan test."""
    return Settings(environment="test", log_level="INFO", database_url=sqlite_url)


@pytest.fixture
def session_factory(sqlite_url: str) -> Iterator[sessionmaker[Session]]:
    """Yield a session factory over a freshly migrated temporary database."""
    engine: Engine = init_database(sqlite_url)
    yield make_session_factory(engine)
    engine.dispose()


def test_build_collection_scheduler_returns_a_stopped_scheduler(
    session_factory: sessionmaker[Session], sqlite_url: str
) -> None:
    scheduler = build_collection_scheduler(session_factory, _settings(sqlite_url))

    assert isinstance(scheduler, AsyncIOScheduler)
    assert scheduler.running is False


def test_build_collection_scheduler_configures_the_interval_trigger(
    session_factory: sessionmaker[Session], sqlite_url: str
--- tests/test_web_profiles.py (first 60 lines of 20655 bytes) ---
"""Tests for the profiles view: list, create/edit forms, validation, 404s."""

from collections.abc import Iterator
from typing import Final

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from seekandemploy.app import create_app
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.models import MatchProfile, Modality
from seekandemploy.repository import get_match_profile, save_match_profile
from seekandemploy.settings import Settings

SUBMIT_HEADERS: Final[dict[str, str]] = {
    "content-type": "application/x-www-form-urlencoded"
}


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


def _seed_profile(
    session_factory: sessionmaker[Session],
    name: str = "python-remote",
    *,
    keywords: list[str] | None = None,
    modality: str | None = "remote",
    location: str | None = "Barcelona",
    salary_min: int | None = 30000,
    max_age: int | None = 30,
) -> int:
    """Persist one profile with representative criteria and return its id."""
    with session_factory() as session:
        profile = save_match_profile(
            session,
            MatchProfile(
                name=name,
                keywords=keywords if keywords is not None else ["python", "fastapi"],
                excluded_keywords=["php"],
                excluded_companies=["Acme"],
                modality=modality,
                location=location,
                salary_min=salary_min,
                max_offer_age_days=max_age,
            ),
        )
--- tests/test_web_offers.py (first 60 lines of 18995 bytes) ---
"""Tests for the offers browse view: filters, rows, errors, and rendering."""

from collections.abc import Iterator
from datetime import date
from typing import Final

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from seekandemploy.app import create_app
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.models import (
    ConnectorType,
    JobOffer,
    Match,
    MatchProfile,
    Modality,
    Source,
)
from seekandemploy.repository import (
    save_match_profile,
    save_source,
    upsert_job_offer,
    upsert_match,
)
from seekandemploy.settings import Settings
from seekandemploy.web.dependencies import get_today

DEFAULT_PUBLISHED: Final[date] = date(2026, 9, 3)


@pytest.fixture
def session_factory(sqlite_url: str) -> Iterator[sessionmaker[Session]]:
    engine: Engine = init_database(sqlite_url)
    yield make_session_factory(engine)
    engine.dispose()


@pytest.fixture
def app(sqlite_url: str) -> Iterator[FastAPI]:
    settings = Settings(environment="test", log_level="INFO", database_url=sqlite_url)
    yield create_app(settings)


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


def _seed_source(
    session_factory: sessionmaker[Session],
    company: str,
    connector: ConnectorType = ConnectorType.greenhouse,
) -> int:
    """Persist one source and return its id."""
    with session_factory() as session:
--- tests/test_collection.py (first 60 lines of 18707 bytes) ---
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
--- src/seekandemploy/web/catalogs.py (first 60 lines of 17270 bytes) ---
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
    "matching_done_banner": (
        "Matching run finished: {evaluated} offers evaluated, {created} new matches."
    ),
    "sources_by_status_heading": "Sources by status",
    "dashboard_empty_sources_intro": "No sources yet. Add them to the configuration; open the ",
    "dashboard_link_sources": "sources view",
    "dashboard_empty_sources_mid": " to start collecting offers. Then ",
    "dashboard_link_create_profile": "create a profile",
    "dashboard_empty_sources_end": " to match them.",
    "dashboard_empty_offers_intro": "No offers yet. Use “Collect now” on the ",
--- tests/test_matching_runner.py (first 60 lines of 16788 bytes) ---
"""Tests for the matching coordinator over temp SQLite migrated to head 0004."""

from collections.abc import Iterator
from datetime import date
from typing import Final

import pytest
from sqlalchemy import Engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from seekandemploy import matching_runner
from seekandemploy.collection import RunOutcome
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.matching import MatchCriteria, OfferView
from seekandemploy.matching_runner import NewMatch, ProfileRun, run_matching
from seekandemploy.models import (
    ConnectorType,
    JobOffer,
    Match,
    MatchProfile,
    Modality,
    Source,
    SourceStatus,
)

FIXED_TODAY: Final = date(2026, 9, 5)


@pytest.fixture
def engine(sqlite_url: str) -> Iterator[Engine]:
    database_engine = init_database(sqlite_url)
    yield database_engine
    database_engine.dispose()


@pytest.fixture
def session_factory(engine: Engine) -> sessionmaker[Session]:
    return make_session_factory(engine)


def _seed_source(session_factory: sessionmaker[Session], company: str = "Acme") -> int:
    """Insert one source and return its id."""
    with session_factory() as session:
        source = Source(
            company=company,
            connector=ConnectorType.lever,
            url=f"https://jobs.lever.co/{company.lower()}",
            status=SourceStatus.active,
        )
        session.add(source)
        session.commit()
        return int(source.id)


def _seed_offer(
    session_factory: sessionmaker[Session],
    source_id: int,
    external_id: str,
    *,

Write ONLY the plan (the three sections). No prose outside them.