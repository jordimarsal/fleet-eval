FILES
src/seekandemploy/cli.py
tests/test_applications_cli.py

TASKS
T1: Implement `apply notes` CLI command logic
    depends_on: (none)
    refs: R1, R2, R3, R4, R5, R6, R7, R8
T2: Add tests for `apply notes` CLI command
    depends_on: T1
    refs: R1, R2, R3, R4, R5, R6, R7, R8

GATES
- Run `pytest tests/test_applications_cli.py -v` to ensure all new and existing application CLI tests pass.
- Verify that `python -m seekandemploy apply notes --help` displays correct usage including `--set` and `--clear`.
- Manually verify exit codes: 0 on success, 1 on not found, 2 on invalid flag combination.
- Confirm HTML snapshot regeneration occurs only on successful edits.