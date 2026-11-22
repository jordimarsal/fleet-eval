FILES
src/seekandemploy/cli.py
src/seekandemploy/repository.py
tests/test_applications_cli.py

TASKS
T1: Implement repository logic for stale application filtering and counting
    depends_on: (none)
    refs: R1, R2, R3, R4
T2: Update CLI to support `--stale DAYS` argument and handle incompatibility with `--all`
    depends_on: T1
    refs: R1, R4, R5
T3: Add unit tests for stale listing logic, including event-based clock reset and exclusion of closed applications
    depends_on: T2
    refs: R1, R2, R3, R4

GATES
- Verify `apply list --stale X` correctly calculates age based on the latest `ApplicationEvent` timestamp or `applied_at`.
- Verify `apply list --stale X` excludes applications with status `rejected` or `withdrawn`.
- Verify `apply list --stale X` fails with exit code 2 when combined with `--all`.
- Verify the summary line format: `stale: X of N open applications (> DAYS days since the last event) and live: Y`.
- Verify no side effects (no new events, no snapshot changes, no `report:` output) occur during a stale list command.