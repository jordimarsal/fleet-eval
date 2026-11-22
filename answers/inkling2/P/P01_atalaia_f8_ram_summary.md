FILES
src/atalaia/api.py
web/app.js
web/index.html
tests/test_api_ram.py
tests/test_web_static.py (or new test for summary display)

TASKS
T1: Add /api/system endpoint reading MemAvailable from /proc/meminfo directly
    depends_on: (none)
    refs: R1, R2, R5
T2: Add unit tests for the system summary endpoint (valid read, missing/malformed meminfo returns null)
    depends_on: T1
    refs: R1, R2, R5
T3: Render sum of ram_mb over up entries plus free RAM in top bar, refreshed each poll, using — for unavailable values
    depends_on: T1
    refs: R3, R4
T4: Add UI/web verification coverage for summary rendering and placeholder behavior
    depends_on: T3
    refs: R3, R4

GATES
pytest tests/test_api_ram.py -v
pytest tests/test_web.py tests/test_web_static.py -v
pytest tests/test_api.py tests/test_scanner.py -v (no regressions)
manual check: GET /api/system with valid /proc/meminfo returns numeric free_ram_mb; simulated missing/malformed file returns null and still 200