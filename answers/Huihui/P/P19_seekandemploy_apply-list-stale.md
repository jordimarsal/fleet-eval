FILES
src/seekandemploy/cli.py
tests/test_applications_cli.py

TASKS
T1: Implement --stale flag and validation logic in CLI
    depends_on: (none)
    refs: R4
T2: Implement stale application query and sorting logic
    depends_on: T1
    refs: R1, R3
T3: Implement output formatting with counts and days
    depends_on: T2
    refs: R1, R2
T4: Add unit tests for stale listing behavior
    depends_on: T3
    refs: R1, R2, R3, R4, R5

GATES
- Run `pytest tests/test_applications_cli.py -v` to ensure all new and existing CLI tests pass.
- Verify that `apply list --stale 7` outputs only open applications older than 7 days based on last event.
- Verify that `apply list --stale 7 --all` exits with code 2 and prints an error message.
- Verify that closed applications are excluded from the count N and the list.
- Verify that no new events or snapshots are written during execution.