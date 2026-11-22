FILES
harness/specs/interpreter_filter_sort/tasks.md
src/mussol/library/library_record.py
src/mussol/api/dtos.py
src/mussol/api/app.py
web/app.js
web/styles.css
tests/test_library_record.py
tests/test_api.py
tests/test_web.py

TASKS
T1: Add interpreter field to LibraryRecord and resolve it from tags, catalogue lookup, or title pattern in that order
    depends_on: (none)
    refs: R1
T2: Expose interpreter on GET /library response DTO
    depends_on: T1
    refs: R2
T3: Wire interpreter into card rendering in web app
    depends_on: T2
    refs: R2
T4: Implement text-based filter by interpreter in library panel state
    depends_on: (none)
    refs: R3
T5: Implement sort controls for title, interpreter, date added with ascending/descending direction
    depends_on: (none)
    refs: R4
T6: Persist filter and sort state across polling refreshes
    depends_on: T4, T5
    refs: R5

GATES
- `python -m pytest tests/test_library_record.py` passes all new interpreter resolution cases (tags > catalogue > title fallback).
- `python -m pytest tests/test_api.py` verifies GET /library includes interpreter in every item.
- `python -m pytest tests/test_web.py` confirms card renders interpreter and filter/sort UI is present.
- Manual browser test: open `/library`, type an interpreter name to filter, toggle sort by each column and direction, reload page — filter and sort persist.