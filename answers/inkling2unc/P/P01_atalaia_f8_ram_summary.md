FILES
src/atalaia/system.py
src/atalaia/api.py
web/app.js
tests/test_system.py

TASKS
T1: Add direct /proc/meminfo reader for free RAM
    depends_on: (none)
    refs: R1, R2, R5
T2: Expose GET /api/system returning free_ram_mb
    depends_on: T1
    refs: R1, R2
T3: Show sum of up-entry ram_mb and free RAM in the top bar, refreshed each poll with em dash fallback
    depends_on: T2
    refs: R3, R4
T4: Verification coverage for system endpoint and UI summary
    depends_on: T2, T3
    refs: R1, R2, R3, R4

GATES
- pytest tests/test_system.py plus existing api/web suites — all pass
- curl GET /api/system returns JSON with free_ram_mb in MB; missing/malformed /proc/meminfo yields null without erroring the request
- no Docker or subprocess calls on the /api/system path (code inspection/grep)
- UI smoke check: after poll, top bar shows summed up-container ram_mb and free RAM, refreshed per poll, showing "—" when a value is unavailable