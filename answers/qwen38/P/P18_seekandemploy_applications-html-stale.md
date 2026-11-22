FILES
src/seekandemploy/applications_report.py
src/seekandemploy/web/routes_applications.py
src/seekandemploy/web/catalogs.py
tests/test_applications_report.py
tests/test_applications_api.py

TASKS
T1: Define shared staleness logic and constants
    depends_on: (none)
    refs: R5
T2: Implement stale row marking in HTML report
    depends_on: T1
    refs: R1
T3: Update Active section header counts
    depends_on: T1
    refs: R2
T4: Add written-off chip to rows
    depends_on: T1
    refs: R3
T5: Ensure write-offs do not reset process silence clock
    depends_on: T1
    refs: R4
T6: Update i18n catalogs for new UI elements
    depends_on: T1
    refs: R1, R2, R3
T7: Write tests for report generation and API endpoints
    depends_on: T2, T3, T4, T5
    refs: R1, R2, R3, R4, R5

GATES
- Run `pytest tests/test_applications_report.py` to verify report logic.
- Run `pytest tests/test_applications_api.py` to verify web route behavior.
- Verify that `STALE_DAYS` is defined once and imported by both CLI and Web modules.
- Confirm that the "Active" header count matches the output of `apply list --stale 21`.