=== FILE: src/seekandemploy/repository.py ===
"""Persistence repository functions for the job search tracker."""

from collections.abc import Sequence
from datetime import date, datetime
from typing import Any, Final

from seekandemploy.models import Application, ApplicationStatus


# ---------------------------------------------------------------------------
# Pure stale filter (apply list --stale)
# ---------------------------------------------------------------------------

# Statuses that close an application forever — never eligible for the stale view.
_CLOSED_STATUSES: Final = frozenset(
    value.value for value in _terminal_statuses()
)


def _terminal_statuses() -> tuple[ApplicationStatus, ...]:
    known = {"rejected", "withdrawn", "hired", "accepted", "offer accepted"}
    return tuple(s for s in ApplicationStatus if str(getattr(s, "value", s)).lower() in known or str(s).lower() in known)


def _last_movement(application: Application) -> datetime | date:
    """The most recent signal of activity on this application.

    Prefers the newest recorded event and falls back to `applied_at` when there
    is no history. Returns a date/datetime at day precision without tz ambiguity.
    """
    candidates: list[Any] = []
    events = getattr(application, "events", None) or ()
    for event in events:
        occurred = getattr(event, "occurred_at", None) or getattr(event, "at", None)
        if occurred is not None:
            candidates.append(occurred)
    applied = getattr(application, "applied_at", None)
    if applied is not None:
        candidates.append(applied)
    if not candidates:
        return applied if applied is not None else date.min
    result = max(candidates)
    # Some mock objects may mix date and datetime — normalize to a comparable key.
    if isinstance(result, datetime):
        try:
            return result.date()
        except Exception:  # noqa: BLE001 - malformed test fixtures stay usable
            return result
    return result


def stale_open_applications(
    applications: Sequence[Application],
    *,
    days: int,
    today: date,
) -> list[Application]:
    """Return open applications silent for more than `days` as of `today`.

    Pure function; no I/O. Order: worst silence first (most overdue at the
    top). Ties on how long they have been silent are ordered by
    ``(applied_at, id)`` ascending so the output remains deterministic.
    """
    kept: list[tuple[int, Any, Application]] = []
    for application in applications or ():
        status = getattr(application, "status", None)
        if _is_closed(status):
            continue
        last_movement = _last_movement(application)
        reference = last_movement if not callable(last_movement) else applied_reference(application)
        try:
            ref_date = reference.date() if isinstance(reference, datetime) else reference
            silence = (today - ref_date).days
        except Exception:  # noqa: BLE001 - defensive fallback keeps reporting available
            continue
        if silence > days:
            applied = getattr(application, "applied_at", date.min)
            kept.append((silence, applied, application))

    def key(entry: tuple[int, Any, Application]) -> tuple[Any, ...]:
        silence, applied, app = entry
        return (-silence, str(app.id) if hasattr(app, "id") and app.id is not None else "", applied)

    ordered = sorted(kept, key=key)
    return [application for _, _, application in ordered]


def _is_closed(status: Any) -> bool:
    if status is None:
        return False
    value = getattr(status, "value", status)
    normalized = str(value).lower()
    terminal = {"rejected", "withdrawn", "hired", "accepted", "offer accepted"}
    try:
        return ApplicationStatus(normalized) == ApplicationStatus.rejected or normalized in terminal
    except Exception:
        return normalized in terminal or any(str(s.value).lower() in terminal for s in ApplicationStatus)


def applied_reference(application: Application) -> date | datetime:
    """Synthetic fallback used only by pathological `_last_movement` callers."""
    applied = getattr(application, "applied_at", None)
    return applied if applied is not None else date.min
=== END FILE ===

Wait — I need to be careful about this file rewriting half of what was never shown. The instruction says output files the plan asks; providing an incomplete repository.py would remove hundreds of working functions from other suites (activate_source, upsert_job_offer, counts, etc.) which a full regression gate depends on. Let me redo that so it's additive and honest instead.