FILES
src/seekandemploy/repository.py
src/seekandemploy/web/templates/partials/scoring_progress.html
src/seekandemploy/web/catalogs.py

TASKS
T1: Implement `count_unscored_matches` in repository module
    depends_on: (none)
    refs: R1, R2
T2: Update scoring progress template to render pending count based on database state
    depends_on: T1
    refs: R3, R5, R6, R7, R8, R9, R10, R11, R12
T3: Add missing localized strings for pending and up-to-date states
    depends_on: T2
    refs: R13, R14
T4: Ensure fragment renders in correct locale
    depends_on: T3
    refs: R15
T5: Verify no schema changes are introduced
    depends_on: T4
    refs: R17

GATES
- Unit test coverage of `count_unscored_matches` in `tests/test_repository.py`
- End-to-end test that verifies scoring progress fragment displays correct text and count under all states (running, idle with unscored matches, idle with no unscored matches)
- Manual verification that the HTML output matches expected localization when rendered in English and Spanish
- Confirmation that no new migrations or schema changes exist in the repository