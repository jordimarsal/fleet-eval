FILES
src/seekandemploy/applications_report.py
src/seekandemploy/cli.py
src/seekandemploy/repository.py
src/seekandemploy/tracker_service.py
src/seekandemploy/web/routes_applications.py
src/seekandemploy/web/static/styles.css
tests/test_applications_report.py
tests/test_applications_cli.py
tests/test_applications_api.py

TASKS
T1: Introduce shared STALE_DAYS constant and single process-silence helper
    depends_on: (none)
    refs: R5, R4
T2: Wire report, CLI filter and web header to the shared constant/helper; exclude write-off notes from staleness clock
    depends_on: T1
    refs: R2, R4, R5
T3: Render stale rows with highlighted days in applications HTML snapshot and active header counts
    depends_on: T2
    refs: R1, R2
T4: Show "written off" chip when last application event is a write-off note
    depends_on: T2
    refs: R3
T5: Cover all behaviors with unit tests (stale row markup, header counts, written-off chip, write-off exclusion, shared constant usage)
    depends_on: T3, T4
    refs: R1, R2, R3, R4, R5

GATES
python -m pytest tests/test_applications_report.py tests/test_applications_cli.py tests/test_applications_api.py tests/test_applications_models.py tests/test_event_log.py -q
CLI cross-check: `apply list --stale 21` output counts match the Active section header count printed by the dashboard/HTML render for the same fixture data
Repository/render check: no duplicate STALE threshold literal remains outside the single constant module; grep confirms report/CLI/web import it rather than redefining
Traceability validation of feature spec artifacts (harness tooling) and existing full test suite green before closing