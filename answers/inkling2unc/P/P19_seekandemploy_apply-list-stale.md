FILES
src/seekandemploy/repository.py
src/seekandemploy/applications_report.py
src/seekandemploy/cli.py
tests/test_applications_report.py
tests/test_applications_cli.py

TASKS
T1: Add stale-listing query support in the repository
    depends_on: (none)
    refs: R1, R3, R4
T2: Build the --stale listing view and summary counts in applications_report
    depends_on: T1
    refs: R1, R2, R3, R4
T3: Wire `apply list --stale DAYS` into the CLI with --all incompatibility
    depends_on: T2
    refs: R1, R2, R4, R5
T4: Cover the feature with unit and CLI tests
    depends_on: T3
    refs: R1, R2, R3, R4, R5

Details:
T1 — Extend `repository.py` with a read-only helper that returns open applications (status not rejected/withdrawn) whose last movement (max of applied_at and latest event timestamp from ApplicationEvent / tracker cache) is older than DAYS days, ordered by staleness descending with visible day count per row; also return N = number of open applications and live count Y (open apps within DAYS or unknown? No — define precisely: live = open apps NOT stale, i.e. last movement <= DAYS). Read via Session + select/flush only; no snapshot write, no event append, no replay trigger. Reuse existing ApplicationEvent query pattern already used elsewhere in repository.
T2 — In `applications_report.py` add the stale listing builder: filter open apps to those exceeding DAYS since last movement, sort oldest first... wait — requirements say "ordenades per antiguitat descendent" = sorted by age DESCENDING (oldest first). Each row shows app identifier + company/job + days since last move. Append closing line exactly `stale: X of N open applications (> DAYS days since the last event)` and `live: Y` on separate lines. Do NOT emit any `report:` line; do NOT call write_applications_snapshot or ensure_fresh-triggering paths here.
T3 — In `cli.py` extend the `apply list` command parser with optional `--stale DAYS` (integer, required-positive). Validate incompatibility with `--all`: print error message naming both flags and exit(2). When --stale is set, run read-only path against SQLite session directly (not through tracker_service ensure_fresh which may rewrite cache/snapshot), render rows from the T1/T2 view, then the summary lines, then return without mutation. Keep existing no-flag output unchanged.
T4 — Tests in tests/test_applications_report.py and tests/test_applications_cli.py: stale threshold ordering (recent note resets clock → not listed), exclusions of rejected/withdrawn from X and from N denominator, descending staleness order, exact summary wording incl. live count, exit 2 + message for --stale paired with --all, zero-mutation test (snapshot file bytes/hash and log fingerprint unchanged after invocation).

GATES
- pytest targeted: tests/test_applications_cli.py tests/test_applications_report.py tests/test_repository* (or repository coverage in test suite as present) green
- Full unit suite: pytest -q (excluding integration tests that need network/live services) green
- CLI smoke: a prepared temp database shows correct row order, counts, `live: Y` line; repeated runs byte-identical stdout; applications.html snapshot bytes and applications.jsonl + tracker_meta unchanged after run (R5 verification)
- ruff / project lint (make targets per repo conventions) clean on changed files
- Manual review checklist against R1–R5 before opening the PR