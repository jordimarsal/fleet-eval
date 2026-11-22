FILES
src/seekandemploy/settings.py
src/seekandemploy/models.py
src/seekandemploy/repository.py
src/seekandemploy/event_log.py
src/seekandemploy/tracker_service.py
src/seekandemploy/snapshot.py
src/seekandemploy/cli.py
src/seekandemploy/applications_report.py
src/seekandemploy/web/routes_applications.py
src/seekandemploy/web/templates/partials/listing.html
src/seekandemploy/web/catalogs.py
tests/test_applications_cli.py
tests/test_applications_report.py
tests/test_snapshot.py

TASKS
T1: Define STALE_DAYS constant and stale days calculation logic
    depends_on: (none)
    refs: R5
T2: Implement write-off event handling and staleness clock preservation
    depends_on: T1
    refs: R4, R3
T3: Update CLI `apply list` to support `--stale` flag and count stale applications
    depends_on: T2
    refs: R2, R5
T4: Implement applications report generation with stale counting
    depends_on: T3
    refs: R2, R5
T5: Render application rows in HTML with `stale` class and highlighted days
    depends_on: T4
    refs: R1
T6: Display `written off` chip for applications with write-off notes
    depends_on: T2
    refs: R3
T7: Add bilingual catalog entries for stale and written-off UI text
    depends_on: T5
    refs: R1, R3
T8: Write tests for CLI stale filtering, report counting, and HTML rendering
    depends_on: T6
    refs: R1, R2, R3, R4, R5

GATES
- Run `pytest tests/test_applications_cli.py tests/test_applications_report.py tests/test_snapshot.py` to verify CLI and report logic.
- Verify `apply list --stale 21` output matches the Active section header counts in `applications.html`.
- Confirm that applications with write-off notes display the `written off` chip and that their staleness clock is not reset.
- Check that `STALE_DAYS` is a single shared constant used across CLI, report, and HTML filter.
- Validate that open applications with more than `STALE_DAYS` days of silence process activity are marked with the `stale` CSS class and highlighted days.