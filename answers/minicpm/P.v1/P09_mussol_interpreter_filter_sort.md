FILES
src/mussol/library/library_record.py
src/mussol/api/dtos.py
src/mussol/api/app.py
web/app.js
web/index.html
web/styles.css
tests/test_library_record.py
tests/test_api.py
tests/test_web.py

TASKS
T1: Implement interpreter resolution logic in LibraryRecord
    depends_on: (none)
    refs: R1
T2: Update API DTOs and Endpoint to expose interpreter
    depends_on: T1
    refs: R2
T3: Implement interpreter filtering UI component
    depends_on: T2
    refs: R3
T4: Implement sorting UI component and backend support
    depends_on: T3
    refs: R4
T5: Ensure filtering and sorting state persists across polling refreshes
    depends_on: T4
    refs: R5

GATES
- Run `harness/tools/check-traceability.py` to verify all requirements (R1-R5) are mapped to tasks.
- Execute unit tests for `test_library_record.py` to validate interpreter resolution order (Catalog -> Tags -> Title).
- Execute integration tests for `test_api.py` to confirm `GET /library` returns interpreter data.
- Execute end-to-end tests for `test_web.py` to verify filtering and sorting UI behavior and state persistence.
- Run manual verification of the library panel UI to ensure card display and control interactions match requirements.