FILES
src/seekandemploy/settings.py
src/seekandemploy/models.py
src/seekandemploy/repository.py
src/seekandemploy/snapshot.py
src/seekandemploy/cli.py
src/seekandemploy/web/routes_applications.py
src/seekandemploy/web/templates/partials/listing.html
src/seekandemploy/web/static/styles.css
src/seekandemploy/web/catalogs.py
tests/test_snapshot_stale.py
tests/test_cli_apply_list_stale.py
tests/test_web_routes_applications_stale.py

TASKS
T1: Add STALE_DAYS constant and stale_days_since_process function
    depends_on: (none)
    refs: R5
T2: Update ApplicationEventKind to exclude write-off notes from process activity
    depends_on: T1
    refs: R4
T3: Modify snapshot rendering to mark rows with stale class and highlight days
    depends_on: T2
    refs: R1, R5
T4: Implement `apply list --stale 21` CLI subcommand using shared stale logic
    depends_on: T1
    refs: R2, R5
T5: Add "written off" chip to application row in HTML template
    depends_on: T2
    refs: R3
T6: Update Active section header to show N live · M stale >21d counts
    depends_on: T4
    refs: R2
T7: Add translations for stale-related strings to catalogs
    depends_on: (none)
    refs: R3, R5
T8: Write unit tests for stale computation, CLI output, and HTML rendering
    depends_on: T3, T4, T5
    refs: R1, R2, R3, R4

GATES
- pytest runs clean on all new test files plus existing applications/CLI/snapshot suites
- `make lint` passes on modified source files
- `apply list --stale 21` against fixture data produces correct count matching the HTML stale tally
- Snapshot rendered from a log with write-off notes does not reset staleness clock; rows with >STALE_DAYS silence get class="stale" and day highlight
- Row for an application whose last event is a write-off note shows the "written off" chip
- STALE_DAYS referenced only once in settings.py; stale_days_since_process called by snapshot, CLI, and web route