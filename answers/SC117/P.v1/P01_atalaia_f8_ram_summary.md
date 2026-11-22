FILES
src/atalaia/system.py
src/atalaia/api.py
web/app.js
tests/test_system.py
tests/test_api.py

TASKS
T1: Implement direct /proc/meminfo reader for free RAM
    depends_on: (none)
    refs: R1, R5
T2: Add error handling for missing/malformed /proc/meminfo
    depends_on: T1
    refs: R2
T3: Expose free_ram_mb endpoint in API
    depends_on: T2
    refs: R1, R2
T4: Update UI to fetch and display system summary (free RAM + up entries sum)
    depends_on: T3
    refs: R3
T5: Implement fallback display logic ('—') for unavailable values
    depends_on: T4
    refs: R4
T6: Write unit tests for system module and API endpoint
    depends_on: T3
    refs: R1, R2, R5
T7: Write integration/e2e verification for UI rendering
    depends_on: T5
    refs: R3, R4

GATES
- Unit tests pass for `src/atalaia/system.py` covering valid, invalid, and missing `/proc/meminfo`.
- API test verifies `GET /api/system` returns correct JSON structure with `free_ram_mb`.
- Static analysis confirms no Docker or subprocess calls in the new system reading logic.
- Visual inspection or snapshot test of `web/app.js` output confirms `—` is displayed when data is null/undefined.
- End-to-end check that the top bar sums `ram_mb` from active entries and adds free RAM correctly on poll.