FILES
src/seekandemploy/repository.py
src/seekandemploy/scoring/views.py
src/seekandemploy/web/catalogs.py
src/seekandemploy/web/templates/partials/scoring_progress.html
tests/test_repository.py
tests/test_web_scoring_progress.py

TASKS
T1: Implement `count_unscored_matches` in repository
    depends_on: (none)
    refs: R1, R2
T2: Add idle localization strings to catalogs
    depends_on: (none)
    refs: R13, R14, R15, R16
T3: Update scoring progress view logic for idle states
    depends_on: T1
    refs: R5, R6, R7, R8, R9, R10, R11, R12
T4: Render updated fragment template
    depends_on: T3
    refs: R3, R5, R6, R7, R8, R9
T5: Verify schema stability and run tests
    depends_on: T4
    refs: R17

GATES
- Unit test `test_count_unscored_matches` passes for 0 and N rows.
- Integration test verifies HTML output contains `<progress>` only when running.
- Integration test verifies localized text matches catalog keys and placeholders.
- Database migration check confirms no new migrations generated.