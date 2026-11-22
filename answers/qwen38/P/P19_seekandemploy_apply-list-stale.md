FILES
src/seekandemploy/cli.py
tests/test_applications_cli.py

TASKS
T1: Implement --stale flag and validation logic in CLI
    depends_on: (none)
    refs: R4
T2: Implement stale application query and filtering logic
    depends_on: T1
    refs: R1, R3, R4
T3: Implement output formatting with counts and days visible
    depends_on: T2
    refs: R1, R2
T4: Add tests for stale listing behavior
    depends_on: T3
    refs: R1, R2, R3, R4, R5

GATES
- Run `pytest tests/test_applications_cli.py -v` to ensure all new and existing CLI tests pass.
- Verify that `apply list --stale 7 --all` returns exit code 2 and an error message.
- Verify that `apply list --stale 7` lists only open applications older than 7 days based on last event, sorted by age descending.
- Verify that closed applications are excluded from both the list and the total count N.
- Verify that the footer displays correct `stale: X of N` and `live: Y` counts.
- Verify that no database mutations occur (no new events, no snapshot regeneration).