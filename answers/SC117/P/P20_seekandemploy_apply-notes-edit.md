FILES
src/seekandemploy/cli.py
tests/test_applications_cli.py

TASKS
T1: Implement `--set` and `--clear` CLI argument parsing for `apply notes`
    depends_on: (none)
    refs: R8
T2: Implement application lookup and existence validation in `apply notes` command
    depends_on: T1
    refs: R1, R2, R7
T3: Implement persistence of `notes` field (SET text / CLEAR NULL)
    depends_on: T2
    refs: R1, R2
T4: Ensure `apply notes` does not trigger event logging or status changes
    depends_on: T3
    refs: R5, R6
T5: Implement stdout reporting format and HTML snapshot regeneration
    depends_on: T4
    refs: R3, R4
T6: Write tests for `apply notes` CLI behavior
    depends_on: T5
    refs: R1, R2, R3, R4, R5, R6, R7, R8

GATES
- Run `pytest tests/test_applications_cli.py -v` to verify all new test cases pass.
- Verify exit code 1 on missing ID (R7).
- Verify exit code 2 on invalid flag combinations (R8).
- Verify stdout output matches `[<id>] <status> <company> - <title>` followed by `report: <path>` (R3).
- Verify `applications.html` is regenerated/updated after successful edit (R4).
- Verify no new rows in `application_event` table after edit (R5).
- Verify application core fields remain unchanged after edit (R6).