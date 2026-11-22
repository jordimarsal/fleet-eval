FILES
src/seekandemploy/settings.py
src/seekandemploy/repository.py
src/seekandemploy/snapshot.py
src/seekandemploy/tracker_service.py
src/seekandemploy/web/catalogs.py
src/seekandemploy/web/templates/partials/listing.html
tests/test_applications_cli.py
tests/test_applications_models.py
tests/test_applications_report.py

TASKS
T1: Centralize STALE_DAYS and staleness logic
    depends_on: (none)
    refs: R5
T2: Update repository to filter process events for staleness calculation
    depends_on: T1
    refs: R4
T3: Implement write-off chip detection in application models/logic
    depends_on: T1
    refs: R3
T4: Update snapshot rendering to apply 'stale' class and highlight days
    depends_on: T2, T3
    refs: R1
T5: Update HTML template to show 'written off' chip
    depends_on: T3
    refs: R3
T6: Update web dashboard header to count live vs stale applications
    depends_on: T1
    refs: R2
T7: Add translation keys for staleness and write-off labels
    depends_on: T1
    refs: R1, R3
T8: Update CLI and Report logic to use centralized constant and function
    depends_on: T1
    refs: R2, R5

GATES
- Verify `STALE_DAYS` is defined only in `settings.py`.
- Run `apply list --stale 21` and compare counts with the HTML dashboard header.
- Confirm that adding a `write-off` note does NOT update the `last_process_event` timestamp.
- Verify that an application with a `write-off` event shows the `written off` chip in HTML.
- Ensure rows with > `STALE_DAYS` process silence have the CSS class `stale` and highlighted text.