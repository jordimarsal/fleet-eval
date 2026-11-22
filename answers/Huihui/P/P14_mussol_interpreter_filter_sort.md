FILES
src/mussol/library/store.py
src/mussol/api/app.py
web/index.html
web/app.js
tests/test_library_store.py
tests/test_api.py
harness/specs/interpreter_filter_sort/APPROVAL

TASKS
T1: Implement interpreter resolution and persistence in LibraryStore
    depends_on: (none)
    refs: R1
T2: Expose interpreter in GET /library API response
    depends_on: T1
    refs: R2
T3: Add interpreter display to library card UI
    depends_on: T2
    refs: R2
T4: Implement frontend filtering by interpreter
    depends_on: T3
    refs: R3, R5
T5: Implement frontend sorting by title, interpreter, or date added
    depends_on: T4
    refs: R4, R5
T6: Verify traceability and approval status
    depends_on: T5
    refs: R1, R2, R3, R4, R5

GATES
- Run `python -m pytest tests/test_library_store.py` to verify interpreter persistence logic (R1).
- Run `python -m pytest tests/test_api.py` to verify `GET /library` includes interpreter field (R2).
- Manually inspect `web/index.html` and `web/app.js` to confirm filter input and sort controls exist and are wired to state variables that persist across polling cycles (R3, R4, R5).
- Execute `harness/tools/check-traceability.py` to ensure all requirements R1-R5 are mapped to implemented tasks/files.
- Confirm existence of `harness/specs/interpreter_filter_sort/APPROVAL`.