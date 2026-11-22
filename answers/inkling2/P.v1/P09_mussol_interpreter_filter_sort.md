FILES
src/mussol/library/library_record.py
src/mussol/library/store.py
src/mussol/metadata/tagger.py
src/mussol/metadata/catalog.py
src/mussol/api/dtos.py
src/mussol/api/app.py
web/index.html
web/styles.css
web/app.js
tests/test_library_record.py
tests/test_library_store.py
tests/test_api.py
tests/test_web.py
harness/specs/interpreter_filter_sort/tasks.md (traceability table)

TASKS
T1: Persist interpreter on library records via catalogue > embedded tags > title pattern resolution order
    depends_on: (none)
    refs: R1
T2: Expose interpreter on GET /library and render it on each card
    depends_on: T1
    refs: R2
T3: Add text-query filter by interpreter in the panel, applied over polled data
    depends_on: T2
    refs: R3, R5
T4: Add sorting by title, interpreter or date added with asc/desc direction in the panel, applied over polled data
    depends_on: T3
    refs: R4, R5
T5: Update traceability table for feature harness/specs/interpreter_filter_sort so every requirement has implementation coverage noted
    depends_on: T4
    refs: R1, R2, R3, R4, R5

GATES
- python -m pytest tests/test_library_record.py tests/test_library_store.py tests/test_tagger.py tests/test_catalog.py tests/test_api.py tests/test_web.py (all green)
- python -m pytest (full suite, all green)
- tests/test_quality_gates.py and any repo lint/type checks via pyproject (e.g. uv run pytest / ruff if configured) pass
- python harness/tools/check-traceability.py for harness/specs/interpreter_filter_sort (every requirement mapped to a task/implementation) passes
- Manual smoke check of GET /library payload includes interpreter per item (via test fixtures or API response dump)