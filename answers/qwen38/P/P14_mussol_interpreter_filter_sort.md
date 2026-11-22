FILES
src/mussol/library/store.py
src/mussol/api/app.py
web/app.js
tests/test_library_store.py
tests/test_api.py
harness/specs/interpreter_filter_sort/APPROVAL
harness/specs/interpreter_filter_sort/design.md
harness/specs/interpreter_filter_sort/tasks.md

TASKS
T1: Implement interpreter resolution logic in LibraryStore
    depends_on: (none)
    refs: R1
T2: Expose interpreter in GET /library API response
    depends_on: T1
    refs: R2
T3: Implement frontend filtering and sorting with state persistence
    depends_on: T2
    refs: R3, R4, R5
T4: Update documentation and traceability artifacts
    depends_on: T3
    refs: R1, R2, R3, R4, R5

GATES
- Run `python -m pytest tests/test_library_store.py` to verify R1 resolution logic (catalogue -> tags -> title pattern).
- Run `python -m pytest tests/test_api.py` to verify R2 (API payload includes interpreter) and ensure no regression in existing endpoints.
- Manually verify or run integration check for R3/R4/R5: Confirm that `web/app.js` maintains `activeArtistQuery`, `sortKey`, and `sortDirection` across polling cycles and correctly filters/sorts the DOM elements.
- Execute `harness/tools/check-traceability.py` to confirm all requirements R1-R5 are mapped to implemented tasks/files.