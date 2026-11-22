FILES
src/seekandemploy/repository.py
src/seekandemploy/web/catalogs.py
src/seekandemploy/web/templates/partials/scoring_progress.html
tests/test_repository.py
tests/test_web_scoring_progress.py

TASKS
T1: Implement `count_unscored_matches` in repository
    depends_on: (none)
    refs: R1, R2, R17
T2: Update translation catalogs with new scoring progress strings
    depends_on: T1
    refs: R13, R14, R16
T3: Refactor scoring progress fragment logic and template
    depends_on: T2
    refs: R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R15
T4: Add unit tests for repository count function
    depends_on: T1
    refs: R1, R2
T5: Add integration tests for scoring progress fragment states
    depends_on: T3
    refs: R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R15

GATES
- Verify `count_unscored_matches` returns correct integer based on NULL scores in `Match` table.
- Verify no database migrations are generated or required.
- Verify HTML output of `GET /scoring/progress` matches all state requirements:
    - Running (with snapshot): `<progress>` present, no unscored query executed.
    - Idle (no snapshot): No `<progress>`, shows "up-to-date" if 0 unscored, shows "pending {n}" if n > 0.
    - Idle (with snapshot, running=False): Shows summary appended to pending/up-to-date text.
    - Idle (snapshot absent): No last-pass summary shown.
- Verify localization works for English and Spanish for all new strings.
- Verify the idle fragment respects the request locale.