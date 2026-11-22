FILES
src/seekandemploy/repository.py
src/seekandemploy/web/catalogs.py
src/seekandemploy/web/routes_scoring.py
src/seekandemploy/scoring/views.py
src/seekandemploy/scoring_progress.py
src/seekandemploy/web/templates/partials/scoring_progress.html
tests/test_repository.py
tests/test_web_scoring_progress.py

TASKS
T1: Add count_unscored_matches to the repository
    depends_on: (none)
    refs: R1, R2

T2: Extend both catalogs with localized pending/up-to-date strings
    depends_on: T1
    refs: R13, R14, R16

T3: Make the scoring fragment derive the idle state from the database
    depends_on: T1, T2
    refs: R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R15

T4: Cover the change and verify schema stability
    depends_on: T1, T2, T3
    refs: R17

GATES
- Run targeted tests: pytest tests/test_repository.py tests/test_web_scoring_progress.py -q; then full suite pytest -q
- Verify no migration or schema files added (git status / alembic heads unchanged for src/seekandemploy/migrations)
- Confirm EN and ES catalogs have identical key sets and that scoring_progress_pending carries {pending} in both languages
- Lint/format per repo conventions (Makefile checks) before closing