FILES
src/atalaia/detectors.py
src/atalaia/api.py
web/app.js
tests/test_api_ram.py

TASKS
T1: Implement direct `/proc/meminfo` reader in detectors
    depends_on: (none)
    refs: R1, R2, R5
T2: Add `GET /api/system` endpoint to API
    depends_on: T1
    refs: R1, R2
T3: Update UI top bar to calculate and display total RAM sum + free RAM
    depends_on: T2
    refs: R3, R4
T4: Add unit tests for RAM detection and API endpoint
    depends_on: T2
    refs: R1, R2

GATES
- Verify `GET /api/system` returns correct `free_ram_mb` from a mocked `/proc/meminfo`.
- Verify `GET /api/system` returns `null` when `/proc/meminfo` is missing or unreadable.
- Verify UI displays `—` when the API returns `null`.
- Verify UI correctly sums `ram_mb` of all "up" projects and adds the system free RAM.
- Verify no subprocess calls are made during the system RAM read.
- Run `harness/tools/check-traceability.py` to ensure all requirements are covered.