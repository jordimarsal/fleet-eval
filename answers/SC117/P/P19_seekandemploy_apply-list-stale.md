FILES
src/seekandemploy/cli.py
tests/test_applications_cli.py

TASKS
T1: Implement CLI argument parsing and validation for `--stale DAYS`
    depends_on: (none)
    refs: R4
T2: Implement stale application query logic in repository layer
    depends_on: T1
    refs: R1, R3
T3: Implement CLI output formatting and summary counts
    depends_on: T2
    refs: R1, R2
T4: Add unit tests for CLI flag incompatibility and stale filtering
    depends_on: T3
    refs: R1, R2, R3, R4, R5

GATES
- Run `pytest tests/test_applications_cli.py -v` to verify all new tests pass.
- Verify `--stale` is incompatible with `--all` (exit 2).
- Verify `apply list --stale 0` lists only open applications older than 0 days.
- Verify that a recent event resets the "last movement" timestamp correctly.
- Verify no mutations occur during the command execution (no new events, no snapshot regeneration).