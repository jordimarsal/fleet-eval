FILES
src/mussol/library/library_record.py
src/mussol/library/store.py
src/mussol/api/dtos.py
src/mussol/api/app.py
web/app.js
web/index.html

TASKS
T1: Implement interpreter resolution logic in LibraryRecord
    depends_on: (none)
    refs: R1
T2: Update LibraryStore to support filtering and sorting
    depends_on: T1
    refs: R4
T3: Update API DTOs and endpoints to include interpreter and query parameters
    depends_on: T2
    refs: R2, R4
T4: Update Web Frontend UI for filter/sort controls and card display
    depends_on: T3
    refs: R2, R3, R4
T5: Implement state persistence for filters/sorting during polling
    depends_on: T4
    refs: R5

GATES
- Unit tests for `LibraryRecord` resolution priority (Catalogue > Tags > Title pattern).
- Integration tests for `GET /library` with `interpreter`, `sort_by`, and `order` query parameters.
- Manual verification that UI filter/sort inputs persist after a simulated polling refresh.
- Traceability check using `harness/tools/check-traceability.py`.