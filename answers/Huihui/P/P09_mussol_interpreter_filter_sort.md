FILES
harness/specs/interpreter_filter_sort/APPROVAL
harness/specs/interpreter_filter_sort/design.md
harness/specs/interpreter_filter_sort/requirements.md
harness/specs/interpreter_filter_sort/tasks.md
src/mussol/library/library_record.py
src/mussol/api/dtos.py
src/mussol/api/app.py
web/app.js
web/index.html
tests/test_library_record.py
tests/test_api.py
tests/test_web.py

TASKS
T1: Persist interpreter resolution logic in LibraryRecord
    depends_on: (none)
    refs: R1
T2: Expose interpreter in API DTO and GET /library response
    depends_on: T1
    refs: R2
T3: Implement frontend card display for interpreter
    depends_on: T2
    refs: R2
T4: Implement frontend filtering by interpreter text query
    depends_on: T3
    refs: R3, R5
T5: Implement frontend sorting by title, interpreter, or date added
    depends_on: T3
    refs: R4, R5
T6: Update specification documentation and traceability
    depends_on: T1, T2, T3, T4, T5
    refs: R1, R2, R3, R4, R5

GATES
- Run `python -m pytest tests/test_library_record.py` to verify R1 persistence logic.
- Run `python -m pytest tests/test_api.py` to verify R2 API exposure.
- Run `python -m pytest tests/test_web.py` to verify R2-R5 frontend behaviors (filtering, sorting, state persistence).
- Execute `harness/tools/check-traceability.py` to ensure all requirements are mapped to tasks and files.