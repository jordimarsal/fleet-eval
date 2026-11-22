FILES
src/seekandemploy/cli.py
src/seekandemploy/repository.py
src/seekandemploy/models.py
tests/test_applications_cli.py

TASKS
T1: Add CLI argument parsing for `--stale DAYS` and incompatibility check with `--all`
    depends_on: (none)
    refs: R4
T2: Implement logic to calculate "stale" days based on the last event (max of `applied_at` and latest event)
    depends_on: T1
    refs: R1, R3
T3: Filter applications to exclude closed states (rejected, withdrawn) and implement sorting by age descending
    depends_on: T2
    refs: R1, R4
T4: Format output rows with visible days and append the stale/live summary count line
    depends_on: T3
    refs: R1, R2
T5: Ensure no side effects (no new events, no snapshot regeneration, no `report:` lines)
    depends_on: T4
    refs: R5
T6: Write integration tests for `apply list --stale` covering filtering, counting, and error cases
    depends_on: T5
    refs: R1, R2, R4, R5

GATES
- Run `pytest tests/test_applications_cli.py -v` to verify CLI behavior and edge cases.
- Manually run `python -m seekandemploy cli apply list --stale 7` on a test database to verify output format and counts.
- Verify that `--stale` combined with `--all` returns exit code 2 with an error message.
- Confirm that no database writes or file modifications occur during the command execution (audit via logging or filesystem monitoring).