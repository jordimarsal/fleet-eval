FILES
src/mussol/api/dtos.py
src/mussol/api/app.py
src/mussol/library/library_record.py
src/mussol/library/store.py
web/app.js
web/index.html
tests/test_library_record.py
tests/test_library_store.py
tests/test_api.py

TASKS
T1: Implement interpreter resolution logic in LibraryRecord
    depends_on: (none)
    refs: R1
T2: Update LibraryStore to persist and query by artist/interpreter
    depends_on: T1
    refs: R1
T3: Update API DTOs and endpoints to include interpreter and support filtering/sorting
    depends_on: T2
    refs: R2, R3, R4
T4: Update Web Frontend to display interpreter, add filter input, and sort controls
    depends_on: T3
    refs: R2, R3, R4
T5: Ensure UI state (filter/sort) is preserved during polling refreshes
    depends_on: T4
    refs: R5

GATES
- Verify `GET /library` returns the correct `artist` field for records with varying metadata sources (Catalogue > Tags > Title).
- Verify `GET /library?artist=...&sort_by=...&direction=...` correctly filters and orders results via SQL.
- Verify frontend UI maintains text input in the filter box and active sort selection after a DOM refresh from polling.
- Run `harness/tools/check-traceability.py` to ensure all requirements are mapped.