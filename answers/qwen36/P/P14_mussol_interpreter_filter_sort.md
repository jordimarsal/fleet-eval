FILES
src/mussol/library/library_record.py
src/mussol/api/dtos.py
src/mussol/api/app.py
web/app.js
tests/test_library_store.py
tests/test_api.py
harness/specs/interpreter_filter_sort/tasks.md

TASKS
T1: Add `artist` field to LibraryRecord and persist it in store
    depends_on: (none)
    refs: R1, R2
T2: Implement interpreter resolution logic (catalogue → tags → title pattern)
    depends_on: T1
    refs: R1
T3: Wire interpreter into GET /library response DTO
    depends_on: T2
    refs: R2
T4: Add interpreter filter input to web panel
    depends_on: (none)
    refs: R3
T5: Add sort controls (title, interpreter, date added; asc/desc) to web panel
    depends_on: (none)
    refs: R4
T6: Persist filter + sort state across polling refreshes
    depends_on: T4, T5
    refs: R5
T7: Update traceability table and verify all requirements covered
    depends_on: T6
    refs: R1, R2, R3, R4, R5

GATES
- harness/tools/check-traceability.py confirms every requirement has at least one task ref
- pytest tests/test_library_store.py passes (artist round-trip, persistence)
- pytest tests/test_api.py passes (GET /library includes artist field)
- Manual browser test: filter by interpreter text query works
- Manual browser test: sort by title/interpreter/date with direction toggles correctly
- Manual browser test: after 3+ polling cycles, filter and sort selections are preserved