FILES
src/atalaia/api.py
web/app.js
tests/test_api_ram.py
harness/progress/impl_f8_ram_summary.md

TASKS
T1: Implement GET /api/system endpoint with direct file read of /proc/meminfo
    depends_on: (none)
    refs: R1, R2, R5
T2: Update UI top bar to display sum of up RAM and free RAM from system API
    depends_on: T1
    refs: R3, R4
T3: Add tests for new endpoint and update traceability documentation
    depends_on: T1, T2
    refs: R1, R2, R3, R4, R5

GATES
- Run `pytest tests/test_api_ram.py` to verify backend logic for `/api/system`.
- Verify that `GET /api/system` returns correct JSON structure (`free_ram_mb`) when `/proc/meminfo` exists.
- Mock or simulate missing/malformed `/proc/meminfo` to ensure `free_ram_mb` is null and request succeeds (R2).
- Confirm no subprocess calls are made in the new code path (R5).
- Manually inspect `web/app.js` changes to ensure the top bar updates on poll and handles null values by displaying "—" (R3, R4).