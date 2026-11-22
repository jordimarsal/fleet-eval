FILES
src/seekandemploy/cli.py
tests/test_apply_notes_cli.py

TASKS
T1: Add `notes` column to Application model and migration
    depends_on: (none)
    refs: R1, R2
T2: Implement `--set <text>` / `--clear` CLI subcommand in cli.py
    depends_on: T1
    refs: R1, R2, R7, R8
T3: Wire up notes edit handler that updates DB without touching other fields or event table
    depends_on: T2
    refs: R5, R6
T4: Emit tracker-glance line + report path on success; regenerate HTML snapshot at --out
    depends_on: T3
    refs: R3, R4
T5: Write integration tests covering set, clear, not-found error, usage-error, no-event-append, no-field-alter, html regeneration
    depends_on: T4
    refs: R1, R2, R3, R4, R5, R6, R7, R8

GATES
- `pytest -x tests/test_apply_notes_cli.py` passes all assertions (set, clear, not-found stderr+exit 1, both/neither flags exit 2, stdout format matches `[<id>] <status> <company> - <title>\nreport: <path>`, HTML file regenerated and contains updated application row).
- `alembic upgrade head` succeeds with the new migration.
- Manual smoke: `seekandemploy apply notes 1 --set "interview scheduled"` prints correct line and regenerates `applications.html`; `seekandemploy apply notes 999 --set x` exits 1 with stderr message; `seekandemploy apply notes 1 --set a --clear b` exits 2.