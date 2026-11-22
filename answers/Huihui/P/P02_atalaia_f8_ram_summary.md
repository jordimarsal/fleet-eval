FILES
src/atalaia/api.py
web/app.js
tests/test_api_ram.py
harness/specs/f8_ram_summary/tasks.md
harness/specs/f8_ram_summary/design.md
harness/specs/f8_ram_summary/review.md
harness/progress/impl_f8_ram_summary.md

TASKS
T1: Implement /api/system endpoint with direct file read
    depends_on: (none)
    refs: R1, R2, R5
T2: Update UI to display RAM summary and handle null values
    depends_on: T1
    refs: R3, R4
T3: Write unit tests for API and UI logic
    depends_on: T1, T2
    refs: R1, R2, R3, R4, R5
T4: Document implementation and traceability
    depends_on: T3
    refs: R1, R2, R3, R4, R5

GATES
- Run `pytest tests/test_api_ram.py` to verify backend logic for `/api/system`.
- Verify that `GET /api/system` returns correct `free_ram_mb` from `/proc/meminfo` on a Linux host.
- Simulate missing/malformed `/proc/meminfo` to ensure `free_ram_mb` is `null` and request succeeds.
- Manually inspect UI top bar to confirm it displays the sum of `ram_mb` for up entries plus free RAM.
- Confirm that unavailable values render as `—` in the UI.
- Ensure no subprocess calls are made during system summary read (code review or static analysis).