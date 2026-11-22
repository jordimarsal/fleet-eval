FILES
src/seekandemploy/settings.py
src/seekandemploy/models.py
src/seekandemploy/repository.py
src/seekandemploy/event_log.py
src/seekandemploy/cli.py
src/seekandemploy/snapshot.py
src/seekandemploy/web/routes_applications.py
src/seekandemploy/web/catalogs.py
src/seekandemploy/web/templates/partials/listing.html
tests/test_applications_cli.py
tests/test_snapshot.py

TASKS
T1: Define STALE_DAYS constant and shared staleness logic
    depends_on: (none)
    refs: R5
T2: Update event log reducer to ignore write-off notes for process activity
    depends_on: T1
    refs: R4
T3: Implement CLI `apply list --stale` command using shared logic
    depends_on: T1
    refs: R5
T4: Add `written_off` chip rendering in HTML template
    depends_on: T2
    refs: R3
T5: Implement stale row styling and day highlighting in HTML template
    depends_on: T1, T2
    refs: R1
T6: Implement Active section header counter with live/stale split
    depends_on: T3, T5
    refs: R2
T7: Write unit tests for staleness calculation and CLI output
    depends_on: T3
    refs: R5
T8: Write integration tests for snapshot rendering and write-off handling
    depends_on: T4, T5
    refs: R1, R3

GATES
- Run `pytest tests/test_applications_cli.py -k stale` to verify CLI output matches expected format.
- Verify `STALE_DAYS` is defined once in settings and imported consistently by CLI, Snapshot, and Web modules.
- Confirm that adding a write-off note does not reset the last process event timestamp in the database.
- Render the applications HTML page and inspect source to ensure `.stale` class is present on rows exceeding threshold.
- Check Active section header text contains correct counts of live vs stale applications (>21 days).