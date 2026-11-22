FILES
src/seekandemploy/applications_report.py
src/seekandemploy/cli.py
src/seekandemploy/snapshot.py
src/seekandemploy/settings.py
src/seekandemploy/event_log.py
src/seekandemploy/tracker_service.py
src/seekandemploy/web/routes_applications.py
src/seekandemploy/web/models.py
src/seekandemploy/web/catalogs.py
tests/test_applications_report.py
tests/test_applications_cli.py
tests/test_applications_api.py

TASKS
T1: Add shared process-silence helper + STALE_DAYS constant; make write-off notes not reset the clock
    depends_on: (none)
    refs: R4, R5
T2: Wire CLI `apply list --stale` to the shared helper/threshold
    depends_on: T1
    refs: R2, R5
T3: Mark stale rows in applications.html snapshot render and Active section header
    depends_on: T1
    refs: R1, R2
T4: Show written off chip on rows whose last event is a write-off note
    depends_on: T1
    refs: R3
T5: Tests for staleness rules, counts, chips, and snapshot rendering; full verification gates
    depends_on: T2, T3, T4
    refs: R1, R2, R3, R4, R5

GATES
pytest tests/test_applications_report.py tests/test_applications_cli.py tests/test_applications_api.py -q
python -m pytest tests/ -k "application or stale" -q
Run the snapshot renderer against fixture data confirming open >STALE_DAYS rows carry class `stale` with highlighted days and the Active header count matches `apply list --stale <STALE_DAYS>` output (same constant)
Confirm a row ending in a write-off note shows the `written off` chip and does not reset process recency after such a note
Full suite: python -m pytest -q (or repo's documented test command from HARNESS.md / docs/verification.md)