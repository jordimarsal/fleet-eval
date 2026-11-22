FILES
src/mussol/library/library_record.py
src/mussol/api/dtos.py
src/mussol/api/app.py
web/app.js
web/styles.css
tests/test_library_record.py
tests/test_api.py
harness/specs/interpreter_filter_sort/tasks.md

TASKS
T1: Implement interpreter resolution logic in LibraryRecord
    depends_on: (none)
    refs: R1
T2: Expose interpreter field in API DTO and endpoint
    depends_on: T1
    refs: R2
T3: Add interpreter filter state and query parameter handling
    depends_on: T2
    refs: R3, R5
T4: Add sorting state and query parameter handling for title, interpreter, date
    depends_on: T2
    refs: R4, R5
T5: Update Web UI to display interpreter and render filter/sort controls
    depends_on: T3, T4
    refs: R2, R3, R4
T6: Verify persistence of filter/sort state across polling refreshes
    depends_on: T5
    refs: R5
T7: Run traceability check and update task documentation
    depends_on: T6
    refs: R1, R2, R3, R4, R5

GATES
- Unit tests pass for `LibraryRecord` interpreter resolution priority (catalogue > tags > title).
- Integration test verifies `GET /library` response includes the resolved interpreter.
- E2E/Integration test confirms filtering by interpreter text works via API query params.
- E2E/Integration test confirms sorting by title, interpreter, or date (asc/desc) works via API query params.
- Verification that filter/sort parameters are preserved in URL/query string during polling updates.
- `harness/tools/check-traceability.py` reports 100% requirement coverage.