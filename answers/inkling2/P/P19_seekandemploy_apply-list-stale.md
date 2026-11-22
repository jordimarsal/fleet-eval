FILES
src/seekandemploy/cli.py
src/seekandemploy/repository.py
src/seekandemploy/applications_report.py
tests/test_applications_cli.py
tests/test_applications_report.py

TASKS
T1: Add read-side last-movement query for open applications
    depends_on: (none)
    refs: R1, R3, R4
T2: Wire `apply list --stale DAYS` flag with --all incompatibility and non-mutating behavior
    depends_on: T1
    refs: R1, R4, R5
T3: Render rows with visible age, sort by staleness, and print the summary count lines (stale + live)
    depends_on: T2
    refs: R1, R2, R3, R5

GATES
- Focused tests pass: pytest tests/test_applications_cli.py tests/test_applications_report.py -q
- Full suite passes: pytest -q
- A live dry run of `quan apply list --stale N` shows only open applications older than N days from their latest movement, sorted oldest first, with per-row day counts and a final `stale: X of N open applications (> DAYS days since the last event)` / `live: Y` footer; no new events, snapshot regeneration, or `report:` line appears in any output
- Passing test proves an application with a recent note event is excluded as stale even if applied long ago; rejected/withdrawn applications never appear and are excluded from the totals
- `--stale 7 --all` exits with code 2 and an error message