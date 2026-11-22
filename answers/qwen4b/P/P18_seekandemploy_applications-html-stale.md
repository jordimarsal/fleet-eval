FILES
src/seekandemploy/web/templates/partials/sources_table.html
src/seekandemploy/web/routes_applications.py
src/seekandemploy/tracker_service.py
src/seekandemploy/event_log.py
harness/specs/apply-list-stale/design.md
harness/specs/apply-list-stale/requirements.md
harness/specs/apply-list-stale/tasks.md

TASKS
T1: Implement stale days calculation and apply to applications list
    depends_on: (none)
    refs: R1, R5
T2: Update header counter logic for active/stale applications
    depends_on: T1
    refs: R2
T3: Add write-off chip display in application row
    depends_on: T1
    refs: R3
T4: Ensure write-off events do not reset staleness timer
    depends_on: T3
    refs: R4, R5

GATES
- Verify that every application row with more than STALE_DAYS of silence shows `stale` class
- Confirm header displays N live · M stale >21d matching CLI output from `apply list --stale 21`
- Validate that write-off chips appear correctly when last event is a write-off note
- Check that staleness rellotge persists after write-off events
- Ensure all components (HTML, CLI, filter) use the same STALE_DAYS constant and stale-days function