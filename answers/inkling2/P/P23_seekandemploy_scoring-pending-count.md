FILES
src/seekandemploy/repository.py
src/seekandemploy/web/catalogs.py
src/seekandemploy/web/routes_scoring.py
src/seekandemploy/web/templates/partials/scoring_progress.html
tests/test_repository.py
tests/test_web_scoring_progress.py

TASKS
T1: Add `count_unscored_matches` to the repository
    depends_on: (none)
    refs: R1, R2, R17
T2: Define localized pending/up-to-date scoring strings in both catalogs
    depends_on: (none)
    refs: R13, R14, R16
T3: Render the idle fragment from database state and snapshot rules
    depends_on: T1, T2
    refs: R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R15
GATES
uv run pytest tests/test_repository.py -k count_unscored_matches -v; uv run pytest tests/test_web_scoring_progress.py -v; uv run pytest tests/test_web_i18n.py tests/test_scoring_progress*.py -v; uv run pytest -q