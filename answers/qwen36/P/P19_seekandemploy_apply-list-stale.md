FILES
src/seekandemploy/cli.py
src/seekandemploy/web/catalogs.py
tests/test_applications_cli.py

TASKS
T1: Add `--stale DAYS` CLI flag and mutual-exclusion with `--all`
    depends_on: (none)
    refs: R4
T2: Implement stale-application query logic (open-only, last-event-based age, descending sort)
    depends_on: T1
    refs: R1, R3
T3: Wire output formatting — table rows + summary line with counts
    depends_on: T2
    refs: R1, R2
T4: Ensure zero mutation semantics (no event creation, no snapshot regeneration, no report lines)
    depends_on: T2
    refs: R5
T5: Add bilingual catalog entries for stale-count labels
    depends_on: T1
    refs: R2
T6: Write integration tests covering open/closed filtering, last-event reset, days calculation, error on --all/--stale combo, and immutability
    depends_on: T5
    refs: R1, R2, R3, R4, R5

GATES
- `pytest tests/test_applications_cli.py -v` passes all new test cases.
- Manual smoke test: `python -m seekandemploy.cli apply list --stale 7` produces a table of only open applications sorted by staleness descending, followed by the exact summary format (`stale: X of N open applications (> DAYS days since the last event)` and `live: Y`).
- Verify that running `--stale 7 --all` exits with code 2 and an error message.
- Confirm no new events are written to `applications.jsonl`, no snapshot is regenerated, and no `report:` line appears in stdout.