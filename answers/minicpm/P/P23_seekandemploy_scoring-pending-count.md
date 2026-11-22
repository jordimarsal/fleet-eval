FILES
src/seekandemploy/repository.py
src/seekandemploy/scoring/progress.py
src/seekandemploy/scoring/views.py
src/seekandemploy/web/catalogs.py
src/seekandemploy/web/templates/partials/scoring_progress.html
tests/test_repository.py
tests/test_scoring_progress.py
tests/test_web_scoring_progress.py

TASKS
T1: Implement `count_unscored_matches` in repository
    depends_on: (none)
    refs: R1, R2
T2: Update scoring progress logic to use DB count when idle
    depends_on: T1
    refs: R5, R6, R7, R8, R10
T3: Prevent unscored-match count query when running
    depends_on: T1
    refs: R4
T4: Update scoring progress fragment HTML for running state
    depends_on: (none)
    refs: R3
T5: Update scoring progress fragment HTML for idle state (no progress element)
    depends_on: (none)
    refs: R11
T6: Add localized strings for pending and up-to-date states
    depends_on: (none)
    refs: R13, R14, R16
T7: Implement last-pass summary rendering when running=False
    depends_on: T1
    refs: R9, R12
T8: Ensure locale resolution for idle fragment
    depends_on: (none)
    refs: R15
T9: Verify no schema migrations are added
    depends_on: (none)
    refs: R17

GATES
- Run `alembic check` to confirm no pending migrations or schema changes.
- Run `pytest tests/test_repository.py -k count_unscored_matches` to verify R1/R2.
- Run `pytest tests/test_scoring_progress.py` to verify running/idle state logic (R3-R11).
- Run `pytest tests/test_web_scoring_progress.py` to verify HTML output and localization (R13-R15).
- Run `pytest tests/test_web_catalogs.py` to verify new/existing translation keys (R13, R16).
- Confirm no new files in `src/seekandemploy/migrations/versions/` related to this feature.