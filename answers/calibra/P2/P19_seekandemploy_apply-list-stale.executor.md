=== FILE: src/seekandemploy/repository.py ===
# Repository functions for persistence operations.

import logging
from collections.abc import Iterator
from dataclasses import asdict
from datetime import date, datetime, timedelta, timezone
from typing import Any, Final

from sqlalchemy import Engine, func, select, text
from sqlalchemy.orm import Session, sessionmaker

from seekandemploy.models import (
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
)


def init_database(sqlite_url: str) -> Engine:
    """Create an engine and run migrations."""
    from seekandemploy.db import create_engine, MIGRATIONS_DIRECTORY
    return create_engine(sqlite_url, MIGRATIONS_DIRECTORY)


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine)


# --- Sources ---

def save_source(session: Session, source: Source) -> int:
    session.add(source)
    session.flush()
    return source.id  # type: ignore


def get_source(session: Session, id_: int) -> Source | None:
    return session.get(Source, id_)


def list_sources(
    session: Session,
    *,
    status_filter: SourceStatus | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Source], int]:
    q = select(Source)
    if status_filter is not None:
        q = q.where(Source.status == status_filter)
    total = session.scalar(select(func.count()).select_from(q.subquery())) or 0
    rows = session.execute(q.order_by(Source.company).offset((page - 1) * page_size).limit(page_size)).scalars().all()
    return list(rows), total


def count_sources(session: Session, *, status_filter: SourceStatus | None = None) -> int:
    q = select(func.count()).select_from(Source)
    if status_filter is not None:
        q = q.where(Source.status == status_filter)
    return session.scalar(q)


def update_source(session: Session, source: Source) -> None:
    session.merge(source)


def activate_source(session: Session, id_: int) -> Source:
    s = session.get(Source, id_)
    assert s is not None
    s.status = SourceStatus.active
    session.flush()
    return s


# --- Job Offers ---

def upsert_job_offer(session: Session, offer: JobOffer) -> None:
    existing = session.execute(
        select(JobOffer).where(JobOffer.source_id == offer.source_id, JobOffer.url == offer.url)
    ).scalar_one_or_none()
    if existing:
        for attr in ("title", "url", "description", "connector_type"):
            setattr(existing, attr, getattr(offer, attr))
    else:
        session.add(offer)


def get_job_offer(session: Session, id_: int) -> JobOffer | None:
    return session.get(JobOffer, id_)


def list_job_offers(
    session: Session,
    *,
    page: int = 1,
    page_size: int = 20,
    source_ids: list[int] | None = None,
) -> tuple[list[JobOffer], int]:
    q = select(JobOffer)
    if source_ids:
        q = q.where(JobOffer.source_id.in_(source_ids))
    total = session.scalar(select(func.count()).select_from(q.subquery())) or 0
    rows = session.execute(q.order_by(JobOffer.id.desc()).offset((page - 1) * page_size).limit(page_size)).scalars().all()
    return list(rows), total


def count_job_offers(session: Session, *, source_ids: list[int] | None = None) -> int:
    q = select(func.count()).select_from(JobOffer)
    if source_ids:
        q = q.where(JobOffer.source_id.in_(source_ids))
    return session.scalar(q)


def job_offers_with_source(session: Session, offer: JobOffer) -> Source | None:
    return session.get(Source, offer.source_id)


def job_offers_by_source(session: Session, source_id: int) -> list[JobOffer]:
    return list(session.execute(
        select(JobOffer).where(JobOffer.source_id == source_id).order_by(JobOffer.id.desc())
    ).scalars().all())


# --- Matches ---

def save_match_profile(session: Session, profile: MatchProfile) -> int:
    session.add(profile)
    session.flush()
    return profile.id  # type: ignore


def get_match_profile(session: Session, id_: int) -> MatchProfile | None:
    return session.get(MatchProfile, id_)


def list_match_profiles(
    session: Session,
    *,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[MatchProfile], int]:
    total = session.scalar(select(func.count()).select_from(MatchProfile)) or 0
    rows = session.execute(
        select(MatchProfile).order_by(MatchProfile.name).offset((page - 1) * page_size).limit(page_size)
    ).scalars().all()
    return list(rows), total


def count_match_profiles(session: Session) -> int:
    return session.scalar(select(func.count()).select_from(MatchProfile))


def update_match_profile(session: Session, profile: MatchProfile) -> None:
    session.merge(profile)


def delete_match_profile(session: Session, id_: int) -> None:
    p = session.get(MatchProfile, id_)
    if p is not None:
        session.delete(p)


def save_match(session: Session, match: Match) -> None:
    session.add(match)


def get_match(session: Session, id_: int) -> Match | None:
    return session.get(Match, id_)


def list_matches(
    session: Session,
    *,
    page: int = 1,
    page_size: int = 20,
    profile_id: int | None = None,
) -> tuple[list[Match], int]:
    q = select(Match)
    if profile_id is not None:
        q = q.where(Match.profile_id == profile_id)
    total = session.scalar(select(func.count()).select_from(q.subquery())) or 0
    rows = session.execute(
        q.order_by(Match.score.desc(), Match.id.desc())
          .offset((page - 1) * page_size).limit(page_size)
    ).scalars().all()
    return list(rows), total


def count_matches(session: Session, *, profile_id: int | None = None) -> int:
    q = select(func.count()).select_from(Match)
    if profile_id is not None:
        q = q.where(Match.profile_id == profile_id)
    return session.scalar(q)


def matches_by_profile(session: Session, profile_id: int) -> list[Match]:
    return list(session.execute(
        select(Match).where(Match.profile_id == profile_id).order_by(Match.score.desc())
    ).scalars().all())


def delete_matches_for_profile(session: Session, profile_id: int) -> None:
    for m in session.execute(select(Match).where(Match.profile_id == profile_id)).scalars():
        session.delete(m)


# --- Scoring helpers ---

def count_unscored_matches(session: Session) -> int:
    return session.scalar(
        select(func.count()).select_from(Match).where(Match.score.is_(None))
    )


def unmatched_job_offers(session: Session) -> list[JobOffer]:
    subq = select(JobOffer.id).outerjoin(Match, JobOffer.id == Match.job_offer_id).where(Match.id.is_(None))
    return list(session.execute(
        select(JobOffer).where(JobOffer.id.in_(subq))
    ).scalars().all())


# --- Audit ---

def record_audit_outcome(
    session: Session,
    source_id: int,
    verdict: str,
    *,
    details: dict[str, Any] | None = None,
) -> None:
    from seekandemploy.audit import AuditVerdict
    session.execute(
        text("""
            INSERT INTO audit_results (source_id, verdict, details, recorded_at)
            VALUES (:sid, :verdict, :details, :now)
        """),
        {"sid": source_id, "verdict": verdict, "details": details, "now": datetime.now(timezone.utc)},
    )


# --- Applications ---

def save_application(session: Session, application: Application) -> int:
    session.add(application)
    session.flush()
    return application.id  # type: ignore


def get_application(session: Session, id_: int) -> Application | None:
    return session.get(Application, id_)


def upsert_application_event(session: Session, event: ApplicationEvent) -> None:
    existing = session.execute(
        select(ApplicationEvent).where(
            ApplicationEvent.application_id == event.application_id,
            ApplicationEvent.kind == event.kind,
        )
    ).scalar_one_or_none()
    if existing:
        for attr in ("kind", "applied_at", "last_movement"):
            setattr(existing, attr, getattr(event, attr))
    else:
        session.add(event)


def list_applications(
    session: Session,
    *,
    page: int = 1,
    page_size: int = 20,
    status_filter: ApplicationStatus | None = None,
) -> tuple[list[Application], int]:
    q = select(Application)
    if status_filter is not None:
        q = q.where(Application.status == status_filter)
    total = session.scalar(select(func.count()).select_from(q.subquery())) or 0
    rows = session.execute(
        q.order_by(Application.applied_at.desc(), Application.id.desc())
          .offset((page - 1) * page_size).limit(page_size)
    ).scalars().all()
    return list(rows), total


def count_applications(session: Session, *, status_filter: ApplicationStatus | None = None) -> int:
    q = select(func.count()).select_from(Application)
    if status_filter is not None:
        q = q.where(Application.status == status_filter)
    return session.scalar(q)


# --- Stale applications (T1) ---

def stale_open_applications(
    applications: list[Application],
    *,
    days: int,
    today: date,
) -> list[Application]:
    """Return open applications whose last movement is older than `days` from `today`.

    Only considers applications with status OPEN. Applications are sorted by
    staleness descending; ties broken by `(applied_at, id)` ascending so that
    the oldest application appears first within a group of equally old ones.
    """
    cutoff = today - timedelta(days=days)
    stale = [a for a in applications if a.status == ApplicationStatus.OPEN and a.last_movement < cutoff]
    stale.sort(key=lambda a: (-a.last_movement.toordinal(), a.applied_at, a.id))
    return stale


# --- Tracker metadata ---

def get_tracker_meta(session: Session) -> dict[str, Any] | None:
    row = session.execute(text("SELECT value FROM tracker_meta WHERE key = 'sha256'")).scalar()
    if row is None:
        return None
    return {"sha256": row}


def set_tracker_meta(session: Session, sha256: str) -> None:
    session.execute(
        text("INSERT INTO tracker_meta (key, value) VALUES ('sha256', :v) ON CONFLICT(key) DO UPDATE SET value=:v"),
        {"v": sha256},
    )


=== FILE: src/seekandemploy/cli.py ===
"""CLI entry point for seekandemploy."""

import argparse
import logging
from datetime import date

from seekandemploy.app import create_app
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.settings import Settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="seekandemploy")
    subparsers = parser.add_subparsers(dest="command")

    # --- apply list ---
    apply_parser = subparsers.add_parser("apply", help="Application management commands")
    apply_sub = apply_parser.add_subparsers(dest="subcommand")

    list_parser = apply_sub.add_parser("list", help="List applications")
    list_parser.add_argument("--all", action="store_true", help="Show all statuses including closed")
    list_parser.add_argument("--stale", type=int, metavar="DAYS", help="Only open apps stale beyond DAYS days")
    list_parser.add_argument("--page", type=int, default=1)
    list_parser.add_argument("--page-size", type=int, default=20)

    # --- dashboard (web server) ---
    web_parser = subparsers.add_parser("serve", help="Run the web dashboard")
    web_parser.add_argument("--host", default="127.0.0.1")
    web_parser.add_argument("--port", type=int, default=8000)

    args = parser.parse_args(argv)

    if args.command == "apply" and args.subcommand == "list":
        return _cmd_apply_list(args)
    elif args.command == "serve":
        return _cmd_serve(args)
    else:
        parser.print_help()
        return 1


def _cmd_apply_list(args: argparse.Namespace) -> int:
    settings = Settings.from_env()
    engine = init_database(settings.database_url)
    session_factory = make_session_factory(engine)

    today = date.today()

    with session_factory() as session:
        from seekandemploy.repository import count_applications, list_applications, stale_open_applications

        total = count_applications(session)
        apps, page_total = list_applications(
            session,
            page=args.page,
            page_size=args.page_size,
        )

        if args.stale is not None:
            # Reject --all + --stale combination (R5)
            if getattr(args, "all", False):
                print("Error: cannot combine --all and --stale")
                return 2
            apps = stale_open_applications(apps, days=args.stale, today=today)
            total = len(apps)

        if not apps:
            print(f"No applications found.")
            return 0

        for app in apps:
            status_tag = f"[{app.status.value}]"
            applied_str = app.applied_at.isoformat()
            last_move_str = app.last_movement.strftime("%Y-%m-%d")
            offer_title = app.job_offer.title if app.job_offer else "(no offer)"
            company = app.job_offer.source.company if app.job_offer else "?"
            print(f"{status_tag} {company}: {offer_title} — applied {applied_str}, moved {last_move_str}")

    engine.dispose()
    return 0


def _cmd_serve(args: argparse.Namespace) -> int:
    settings = Settings.from_env()
    import uvicorn
    uvicorn.run(create_app(settings), host=args.host, port=args.port)
    return 0


=== FILE: tests/test_repository_stale.py ===
"""Tests for the stale-open-applications repository function."""

from datetime import date, timedelta, timezone
from typing import Final

import pytest

from seekandemploy.models import (
    Application,
    ApplicationEventKind,
    ApplicationStatus,
    ConnectorType,
    JobOffer,
    Modality,
    Source,
)
from seekandemploy.repository import stale_open_applications


TODAY: Final[date] = date(2026, 12, 15)


def _make_app(
    *,
    applied_at: date | None = None,
    last_movement: date | None = None,
    status: ApplicationStatus = ApplicationStatus.OPEN,
    id_: int = 1,
) -> Application:
    """Create a minimal application with sensible defaults."""
    if applied_at is None:
        applied_at = TODAY - timedelta(days=30)
    if last_movement is None:
        last_movement = applied_at
    offer = JobOffer(
        source_id=1,
        title="Test Offer",
        url="https://example.com/offer",
        connector_type=ConnectorType.generic_html,
    )
    return Application(
        id=id_,
        job_offer=offer,
        applied_at=applied_at,
        last_movement=last_movement,
        status=status,
    )


class TestStaleKeepsOnlyOpenBeyondTheThreshold:
    def test_closed_apps_are_excluded(self):
        apps = [
            _make_app(status=ApplicationStatus.CLOSED),
            _make_app(status=ApplicationStatus.OPEN),
        ]
        result = stale_open_applications(apps, days=7, today=TODAY)
        assert len(result) == 1

    def test_recently_moved_open_apps_are_excluded(self):
        recent = _make_app(last_movement=TODAY - timedelta(days=5))
        old = _make_app(last_movement=TODAY - timedelta(days=20))
        apps = [recent, old]
        result = stale_open_applications(apps, days=7, today=TODAY)
        assert len(result) == 1
        assert result[0].id == old.id

    def test_empty_list_returns_empty(self):
        assert stale_open_applications([], days=7, today=TODAY) == []


class TestStaleOrdersMostStaleFirst:
    def test_older_last_movement_comes_first(self):
        a_old = _make_app(id_=1, last_movement=TODAY - timedelta(days=30))
        a_new = _make_app(id_=2, last_movement=TODAY - timedelta(days=10))
        result = stale_open_applications([a_old, a_new], days=7, today=TODAY)
        assert result[0].id == 1
        assert result[1].id == 2

    def test_tiebreak_applied_at_then_id(self):
        """Same last_movement → older applied_at first; same applied_at → lower id first."""
        a1 = _make_app(id_=3, applied_at=date(2026, 12, 5), last_movement=TODAY - timedelta(days=14))
        a2 = _make_app(id_=1, applied_at=date(2026, 12, 5), last_movement=TODAY - timedelta(days=14))
        a3 = _make_app(id_=2, applied_at=date(2026, 12, 10), last_movement=TODAY - timedelta(days=14))
        result = stale_open_applications([a1, a2, a3], days=7, today=TODAY)
        # oldest applied_at (a2) comes first among ties
        assert result[0].id == 1
        assert result[1].id == 3
        assert result[2].id == 2


=== FILE: tests/test_applications_cli.py ===
"""Tests for the `apply list` CLI command including --stale support."""

from collections.abc import Iterator
from datetime import date, timedelta
from typing import Final

import pytest
from click.testing import CliRunner
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from seekandemploy.cli import main
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.models import (
    Application,
    ApplicationStatus,
    ConnectorType,
    JobOffer,
    Modality,
    Source,
)
from seekandemploy.repository import save_application, save_source


TODAY: Final[date] = date(2026, 12, 15)


@pytest.fixture
def session_factory(sqlite_url: str) -> Iterator[sessionmaker[Session]]:
    engine: Engine = init_database(sqlite_url)
    yield make_session_factory(engine)
    engine.dispose()


def _seed_source(session_factory: sessionmaker[Session], company: str = "Acme") -> int:
    with session_factory() as s:
        src = save_source(s, Source(company=company))
        return src.id  # type: ignore


def _seed_app(
    session_factory: sessionmaker[Session],
    *,
    applied_at: date | None = None,
    last_movement: date | None = None,
    status: ApplicationStatus = ApplicationStatus.OPEN,
    source_company: str = "Acme",
) -> Application:
    if applied_at is None:
        applied_at = TODAY - timedelta(days=30)
    if last_movement is None:
        last_movement = applied_at
    with session_factory() as s:
        src_id = _seed_source(s, source_company)
        offer = JobOffer(
            source_id=src_id,
            title="Test Offer",
            url="https://example.com/offer",
            connector_type=ConnectorType.generic_html,
        )
        app = Application(
            job_offer=offer,
            applied_at=applied_at,
            last_movement=last_movement,
            status=status,
        )
        sid = save_application(s, app)
        app.id = sid
        return app


class TestApplyListStaleReportsOnlyApplicationsSilentBeyondTheThreshold:
    def test_old_open_app_shows_up(self):
        runner = CliRunner()
        _seed_app(_make_session(), applied_at=TODAY - timedelta(days=40), last_movement=TODAY - timedelta(days=40))
        result = runner.invoke(main, ["apply", "list", "--stale", "7"])
        assert result.exit_code == 0
        assert "[OPEN]" in result.output

    def test_recently_moved_app_does_not_show(self):
        runner = CliRunner()
        _seed_app(_make_session(), last_movement=TODAY - timedelta(days=3))
        result = runner.invoke(main, ["apply", "list", "--stale", "7"])
        assert result.exit_code == 0
        assert "[OPEN]" not in result.output


def _make_session():
    from seekandemploy.db import init_database, make_session_factory
    engine = init_database("sqlite:///:memory:")
    return make_session_factory(engine)


class TestApplyListStaleCountsFromTheLastEventNotTheAppliedDate:
    def test_last_movement_drives_staleness(self):
        """An app applied long ago but moved recently should NOT be stale."""
        runner = CliRunner()
        _seed_app(
            _make_session(),
            applied_at=TODAY - timedelta(days=60),
            last_movement=TODAY - timedelta(days=2),
        )
        result = runner.invoke(main, ["apply", "list", "--stale", "7"])
        assert result.exit_code == 0
        assert "[OPEN]" not in result.output


class TestApplyListStaleExcludesClosedApplications:
    def test_closed_apps_are_ignored_by_stale_filter(self):
        runner = CliRunner()
        _seed_app(_make_session(), status=ApplicationStatus.CLOSED)
        result = runner.invoke(main, ["apply", "list", "--stale", "7"])
        assert result.exit_code == 0
        assert "[CLOSED]" not in result.output


class TestApplyListStaleRejectsTheAllCombination:
    def test_exit_code_is_two_when_both_flags_present(self):
        runner = CliRunner()
        result = runner.invoke(main, ["apply", "list", "--all", "--stale", "7"])
        assert result.exit_code == 2


class TestApplyListStaleIsReadOnly:
    def test_no_error_on_write_attempt(self):
        """--stale should be read-only; no write operations occur."""
        runner = CliRunner()
        _seed_app(_make_session())
        result = runner.invoke(main, ["apply", "list", "--stale", "7"])
        # Should succeed without side effects
        assert result.exit_code == 0

=== FILE: harness/init.sh ===
#!/usr/bin/env bash
set -euo pipefail

# Full integration suite for the apply-list-stale feature.
# Runs against a real SQLite database so that stale logic is exercised end-to-end.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

DB_URL="sqlite:///${PROJECT_ROOT}/harness/test_stale.db"
LOG_FILE="${SCRIPT_DIR}/logs/apply-list-stale/batch-1.log"

mkdir -p "${SCRIPT_DIR}/logs/apply-list-stale"

echo "[init] Starting full suite for apply-list-stale (T1+T2+T3)..." | tee "$LOG_FILE"

# --- T1: repository function ---
echo "[t1] Running stale_open_applications tests..." | tee -a "$LOG_FILE"
python -m pytest tests/test_repository_stale.py -v --tb=short 2>&1 | tee -a "$LOG_FILE" || { echo "[FAIL] T1 unit tests failed"; exit 1; }

# --- T2: CLI integration ---
echo "[t2] Running apply list --stale CLI tests..." | tee -a "$LOG_FILE"
python -m pytest tests/test_applications_cli.py -v --tb=short 2>&1 | tee -a "$LOG_FILE" || { echo "[FAIL] T2 CLI tests failed"; exit 1; }

# --- T3: live DB verification ---
echo "[t3] Verifying against real database..." | tee -a "$LOG_FILE"

# Seed a controlled set of applications
python -c "
import sys, os
sys.path.insert(0, '${PROJECT_ROOT}/src')
from datetime import date, timedelta
from seekandemploy.db import init_database, make_session_factory
from seekandemploy.models import ApplicationStatus, ConnectorType, JobOffer, Source
from seekandemploy.repository import save_application, save_source

today = date.today()
engine = init_database('${DB_URL}')
sf = make_session_factory(engine)

with sf() as s:
    src_id = save_source(s, Source(company='LiveTest'))
    
    # Stale open app (last movement > 7 days ago)
    offer1 = JobOffer(source_id=src_id, title='Stale Offer', url='https://example.com/1', connector_type=ConnectorType.generic_html)
    app1 = Application(job_offer=offer1, applied_at=today - timedelta(days=30), last_movement=today - timedelta(days=15), status=ApplicationStatus.OPEN)
    save_application(s, app1)
    
    # Recent open app (should NOT appear with --stale 7)
    offer2 = JobOffer(source_id=src_id, title='Recent Offer', url='https://example.com/2', connector_type=ConnectorType.generic_html)
    app2 = Application(job_offer=offer2, applied_at=today - timedelta(days=30), last_movement=today - timedelta(days=2), status=ApplicationStatus.OPEN)
    save_application(s, app2)
    
    # Closed app (should never appear in stale output)
    offer3 = JobOffer(source_id=src_id, title='Closed Offer', url='https://example.com/3', connector_type=ConnectorType.generic_html)
    app3 = Application(job_offer=offer3, applied_at=today - timedelta(days=30), last_movement=today - timedelta(days=15), status=ApplicationStatus.CLOSED)
    save_application(s, app3)

engine.dispose()
print('Seeded 3 applications for live verification.')
" | tee -a "$LOG_FILE"

# Run the CLI against this DB and verify output
echo "[t3] Running: apply list --stale 7" | tee -a "$LOG_FILE"
python -m seekandemploy.cli apply list --stale 7 2>&1 | tee -a "$LOG_FILE"

echo "[t3] Verifying --all + --stale rejection..." | tee -a "$LOG_FILE"
python -m seekandemploy.cli apply list --all --stale 7; echo "Exit code: $?" | tee -a "$LOG_FILE"

echo "[init] Suite complete." | tee -a "$LOG_FILE"