FILES
src/seekandemploy/applications_report.py
src/seekandemploy/web/routes_applications.py
src/seekandemploy/web/templates/partials/listing.html
tests/test_applications_report.py
tests/test_applications_api.py

TASKS
T1: Implement shared staleness logic and report generation
    depends_on: (none)
    refs: R1, R2, R4, R5
T2: Update web routes to use new report data
    depends_on: T1
    refs: R1, R2, R3
T3: Update HTML template for stale styling and chips
    depends_on: T2
    refs: R1, R3
T4: Add tests for report logic and API integration
    depends_on: T1, T2
    refs: R1, R2, R3, R4, R5

GATES
- Run `pytest tests/test_applications_report.py` to verify staleness calculation, constant sharing, and write-off exclusion logic.
- Run `pytest tests/test_applications_api.py` to ensure the web route returns correct counts and row data including stale flags and written-off chips.
- Verify that `STALE_DAYS` is defined once in `applications_report.py` (or a shared constants module if preferred, but here we assume it's centralized in the report module or imported from settings/models as per existing patterns) and used by both the CLI filter logic (if applicable/modified) and the HTML report generator.
- Manually inspect generated HTML snippet (via test fixture or local run) to confirm `class="stale"` is applied to rows > STALE_DAYS old and "written off" chip appears on relevant rows.