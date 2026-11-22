FILES
src/seekandemploy/repository.py
src/seekandemploy/scoring/views.py
src/seekandemploy/web/catalogs.py
src/seekandemploy/web/templates/partials/scoring_progress.html
tests/test_repository.py
tests/test_web_scoring_progress.py

TASKS
T1: Add `count_unscored_matches` to repository
    depends_on: (none)
    refs: R1, R2
T2: Wire `count_unscored_matches` into scoring views
    depends_on: T1
    refs: R3, R4, R5, R6, R7, R8, R9, R10, R11, R12
T3: Define idle i18n strings in both catalogs
    depends_on: (none)
    refs: R13, R14, R15, R16
T4: Update scoring-progress template for idle state
    depends_on: T2, T3
    refs: R3, R5, R6, R7, R8, R9, R10, R11, R12
T5: Add tests for `count_unscored_matches`
    depends_on: T1
    refs: R2
T6: Add integration tests for idle fragment rendering
    depends_on: T4
    refs: R5, R6, R7, R8, R9, R10, R11, R12

GATES
- Unit test suite passes (`pytest -q`) including new tests in T5 and T6.
- `alembic check` confirms no pending migrations (R17).
- Manual verification of `GET /scoring/progress`:
  - Running snapshot present → `<progress>` with correct value/max; no pending count query logged.
  - Snapshot absent + unscored matches > 0 → localized pending text with count; no `<progress>`.
  - Snapshot absent + unscored matches == 0 → localized up-to-date text; no `<progress>`.
  - Snapshot running=False + unscored matches > 0 → localized pending text with count + last-pass summary on same line.
  - Snapshot running=False + unscored matches == 0 → localized up-to-date text + last-pass summary on same line.
  - Locale switch between en/es yields correct catalog strings (R13–R14).