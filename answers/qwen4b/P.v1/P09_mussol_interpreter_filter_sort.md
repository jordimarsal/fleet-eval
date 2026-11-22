FILES  
src/mussol/library/store.py  
src/mussol/library/library_record.py  
harness/specs/interpreter_filter_sort/design.md  
harness/specs/interpreter_filter_sort/requirements.md  
harness/specs/interpreter_filter_sort/tasks.md  

TASKS  
T1: Implement interpreter resolution from audio tags using metadata catalog  
    depends_on: (none)  
    refs: R1, R2  
T2: Add interpreter filtering capability to library panel UI  
    depends_on: T1  
    refs: R3  
T3: Implement sorting by title, interpreter, or date added with direction control  
    depends_on: T1  
    refs: R4  
T4: Ensure filter and sort state persists across polling refreshes  
    depends_on: T2, T3  
    refs: R5  

GATES  
- Verify that every library record includes an interpreter via traceability check (run `harness/tools/check-traceability.py`)  
- Confirm that `/library` API responses include interpreter field in all records  
- Validate that filtering and sorting work as expected in frontend panel and persist after refresh  
- Run full integration test suite for library panel functionality (`tests/test_library_panel.py`)  
- Confirm no data loss during polling cycles through manual refresh testing