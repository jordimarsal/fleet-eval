FILES
src/seekandemploy/cli.py
src/seekandemploy/repository.py
src/seekandemploy/applications_report.py
tests/test_applications_cli.py
harness/CHECKPOINTS.md
harness/feature_list.json

TASKS
T1: Add `apply notes` command parser and validate exactly-one-of flags
    depends_on: (none)
    refs: R8
T2: Implement notes edit persistence path (set text / clear to NULL) and locate application with error handling
    depends_on: T1
    refs: R1, R2, R7
T3: Emit tracker-glance stdout line and guarantee no event row or field mutation on success
    depends_on: T2
    refs: R3, R5, R6
T4: Regenerate static HTML snapshot at --out (default applications.html) after a successful edit
    depends_on: T3
    refs: R4
T5: Cover the scenario in CLI tests (success set, success clear, both flags usage error exit 2, neither flag exit 2, missing id stderr + exit 1 + untouched snapshot, output format, snapshot regeneration, no events/no field changes)
    depends_on: T4
    refs: R1, R2, R3, R4, R5, R6, R7, R8

GATES
pytest tests/test_applications_cli.py -v
pytest tests/test_applications_report.py -v
pytest tests/test_applications_api.py tests/test_repository.py -v
pytest -q (full suite)
verify `apply notes` with --set, --clear, both flags, neither flag, unknown id against a scratch database including snapshot file existence before/after
confirm failures leave applications.html untouched and do not add application_event rows