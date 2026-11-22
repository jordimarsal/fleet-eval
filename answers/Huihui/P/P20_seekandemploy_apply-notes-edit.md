FILES
src/seekandemploy/cli.py
tests/test_applications_cli.py

TASKS
T1: Implement `apply notes` CLI command logic and argument parsing
    depends_on: (none)
    refs: R1, R2, R3, R4, R5, R6, R7, R8
T2: Add unit tests for `apply notes` functionality
    depends_on: T1
    refs: R1, R2, R3, R4, R5, R6, R7, R8

GATES
- Run `pytest tests/test_applications_cli.py -v` to ensure all new tests pass.
- Verify that running `python -m seekandemploy apply notes <id> --set "text"` updates the database correctly without appending to `application_event`.
- Verify that running `python -m seekandemploy apply notes <id> --clear` sets notes to NULL in the database.
- Confirm that stdout matches the tracker-glance format `[<id>] <status> <company> - <title>` followed by `report: <path>`.
- Confirm that `applications.html` is regenerated with updated content.
- Confirm that exit code is 1 and stderr contains `error: application <id> not found` when ID does not exist.
- Confirm that exit code is 2 when both or neither of `--set`/`--clear` are provided.