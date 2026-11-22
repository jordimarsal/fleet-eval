FILES
src/mussol/metadata/interpreter.py
src/mussol/library/library_record.py
src/mussol/library/store.py
src/mussol/api/dtos.py
src/mussol/api/app.py
web/index.html
web/styles.css
web/app.js
tests/test_interpreter_resolver.py
tests/test_library_record.py
tests/test_api.py
tests/test_web.py
harness/specs/interpreter_filter_sort/traceability.md
harness/specs/interpreter_filter_sort/APPROVAL
docs/verification.md (only if gate list changed)

TASKS
T1: Add interpreter resolution helper (catalogue lookup → embedded tags → title pattern)
    depends_on: (none)
    refs: R1

T2: Persist resolved interpreter on the library record and expose it in GET /library DTO
    depends_on: T1
    refs: R1, R2

T3: Render interpreter on library cards
    depends_on: T2
    refs: R2

T4: Add interpreter text filter and sortable controls (title/interpreter/date added, asc/desc) to the panel
    depends_on: T3
    refs: R3, R4

T5: Keep filter/sort state across polling refreshes; backfill traceability table and R1 test coverage, mark feature close-out artifacts
    depends_on: T4
    refs: R5, R1

GATES
- pytest tests/test_interpreter_resolver.py tests/test_library_record.py tests/test_api.py tests/test_web.py -q
- full suite: python -m pytest (or project's configured test command) plus module boundary scan per HARNESS.md
- manual check that GET /library payload contains interpreter for each item
- UI smoke: type interpreter query and toggle sort directions, trigger refresh, confirm filters/sorting persist
- run check-traceability tool against the updated spec folder to confirm every requirement maps to code and tests before closing