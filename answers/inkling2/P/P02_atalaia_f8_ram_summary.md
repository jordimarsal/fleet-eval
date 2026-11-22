FILES
src/atalaia/sysmem.py
src/atalaia/api.py
web/app.js
web/index.html
tests/test_sysmem.py
tests/test_api_system.py
tests/test_web.py

TASKS
T1: Implement direct /proc/meminfo reader
    depends_on: (none)
    refs: R1, R2, R5

T2: Add GET /api/system returning free_ram_mb
    depends_on: T1
    refs: R1, R2

T3: Render sum of up ram_mb + free RAM in top bar with unavailable handling
    depends_on: T2
    refs: R3, R4

GATES
python -m pytest (full suite incl. new test_sysmem.py, test_api_system.py, web tests) — all green
bash harness/tools/check-traceability.py --all (or --feature f8_ram_summary once registered) — no gaps for R1–R5
manual smoke: start the API, curl /api/system (and simulate missing/malformed /proc/meminfo where actionable) and confirm 200 JSON with float MB or null; verify top bar shows summed up RAM + free RAM on each poll, "—" when a value is absent
confirm no Docker/subprocess calls are used by the system summary path (static inspection of src/atalaia/sysmem.py and api.py route)
ruff/lint (if configured) clean