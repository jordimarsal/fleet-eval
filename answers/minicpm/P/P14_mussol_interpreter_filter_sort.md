FILES
src/mussol/library/library_record.py
src/mussol/api/dtos.py
src/mussol/api/app.py
web/app.js
web/index.html
tests/test_library_record.py
tests/test_api.py

TASKS
T1: Implement interpreter resolution logic in LibraryRecord
    depends_on: (none)
    refs: R1
T2: Persist and expose interpreter in API DTOs
    depends_on: T1
    refs: R2
T3: Add interpreter filter UI component to web panel
    depends_on: T2
    refs: R3
T4: Add sorting controls (title, interpreter, date) to web panel
    depends_on: T3
    refs: R4
T5: Ensure filter/sort state persists across polling refreshes
    depends_on: T4
    refs: R5

GATES
- Run `pytest tests/test_library_record.py` to verify interpreter resolution order (catalogue -> tags -> title pattern).
- Run `pytest tests/test_api.py` to verify `GET /library` responses include the interpreter field.
- Manual verification in browser: Confirm filter input exists and filters list by interpreter text.
- Manual verification in browser: Confirm sort controls exist and correctly sort by title, interpreter, and date added with asc/desc direction.
- Manual verification in browser: Apply filter/sort, wait for polling refresh, confirm state is preserved.
- Run `harness/tools/check-traceability.py` to ensure all requirements (R1-R5) are covered by tasks.