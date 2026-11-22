FILES
src/mussol/library/library_record.py
src/mussol/api/dtos.py
src/mussol/api/app.py
web/app.js
tests/test_library_store.py
tests/test_api.py

TASKS
T1: Persist interpreter in LibraryRecord and Store
    depends_on: (none)
    refs: R1, R2
T2: Expose interpreter in API DTOs and Endpoint
    depends_on: T1
    refs: R2
T3: Implement frontend filtering by interpreter
    depends_on: T2
    refs: R3
T4: Implement frontend sorting by title/interpreter/date
    depends_on: T3
    refs: R4
T5: Ensure filter/sort state survives polling refreshes
    depends_on: T4
    refs: R5
T6: Update tests for store persistence and API response
    depends_on: T1
    refs: R1, R2
T7: Update tests for frontend logic
    depends_on: T5
    refs: R3, R4, R5

GATES
- harness/tools/check-traceability.py verifies all requirements are covered by tasks.
- pytest runs full test suite including new tests for library record enrichment and API endpoints.
- Manual verification of web app: load library, check artist display, apply filters, change sort order, refresh page to verify state persistence.