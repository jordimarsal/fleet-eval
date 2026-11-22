FILES
src/seekandemploy/repository.py
src/seekandemploy/web/routes_scoring.py
src/seekandemploy/web/templates/partials/scoring_progress.html
src/seekandemploy/web/catalogs.py
tests/test_repository.py
tests/test_web_scoring_progress.py

TASKS
T1: Add count_unscored_matches to repository
    depends_on: (none)
    refs: R1, R2
T2: Update scoring progress route logic for idle state
    depends_on: T1
    refs: R3, R4, R5, R6, R7, R8, R9, R10, R11, R12
T3: Update scoring progress template for idle rendering
    depends_on: T2
    refs: R3, R5, R6, R7, R8, R9, R11, R12
T4: Define localized strings in catalogs
    depends_on: (none)
    refs: R13, R14, R15, R16
T5: Implement tests for repository and web fragment
    depends_on: T1, T2, T3, T4
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17

GATES
- Run `pytest tests/test_repository.py -v` to verify `count_unscored_matches` implementation.
- Run `pytest tests/test_web_scoring_progress.py -v` to verify fragment rendering logic for running, idle, and absent states.
- Verify that no new migration files are created in `src/seekandemploy/migrations/versions/`.
- Manually inspect `src/seekandemploy/web/catalogs.py` to ensure `scoring_progress_pending` and `scoring_progress_up_to_date` exist in both EN and ES with correct placeholders.