FILES
harness/specs/interpreter_filter_sort/design.md
harness/specs/interpreter_filter_sort/requirements.md
harness/specs/interpreter_filter_sort/tasks.md
src/mussol/library/library_record.py
src/mussol/library/store.py
src/mussol/api/app.py
web/app.js

TASKS
T1: Implement interpreter resolution from audio tags and title pattern
    depends_on: (none)
    refs: R1
T2: Update library record store to persist interpreter field
    depends_on: T1
    refs: R1, R5
T3: Add interpreter filtering in library panel UI
    depends_on: T2
    refs: R3
T4: Implement sorting by title, interpreter, or date added with direction control
    depends_on: T2
    refs: R4
T5: Ensure filtering and sorting state persists across polling refreshes
    depends_on: T3, T4
    refs: R3, R4, R5

GATES
- Verify that each library record contains an interpreter resolved per R1
- Confirm that `GET /library` responses include interpreter field per R2
- Validate that text-based interpreter filter works as expected per R3
- Test that sorting options (title, interpreter, date) work with ascending/descending directions per R4
- Confirm that filter and sort states are retained during polling via browser dev tools or API inspection per R5
- Run traceability check using harness/tools/scan.py to ensure all requirements are covered in tasks