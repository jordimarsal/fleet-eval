FILES
src/atalaia/memory.py
src/atalaia/api.py
web/app.js
web/index.html
tests/test_memory.py
tests/test_api_system.py
tests/test_web_summary.py

TASKS
T1: Add direct /proc/meminfo reader and GET /api/system endpoint
    depends_on: (none)
    refs: R1, R2, R5
T2: Render total up-entry RAM and free RAM in the UI top bar on every poll
    depends_on: T1
    refs: R3, R4
T3: Add tests for meminfo parsing, system endpoint degradation, and top-bar rendering
    depends_on: T1, T2
    refs: R1, R2, R3, R4, R5

GATES
pytest -q (full suite, including new tests)
python harness/tools/check-traceability.py --feature f8_ram_summary (or --all if feature not registered yet) — all requirements covered with done status
manual smoke of GET /api/system against a healthy system and an unreadable/malformed /proc/meminfo (free_ram_mb null, request still succeeds)
UI check that top bar shows summed ram_mb of `up` entries + free RAM after each poll cycle, showing — when any value is unavailable