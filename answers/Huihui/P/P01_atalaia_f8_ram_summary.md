FILES
src/atalaia/system_info.py
src/atalaia/api.py
web/app.js
tests/test_system_info.py
tests/test_api_system.py

TASKS
T1: Implement system info module for /proc/meminfo parsing
    depends_on: (none)
    refs: R1, R2, R5
T2: Integrate GET /api/system endpoint into API router
    depends_on: T1
    refs: R1, R2
T3: Update UI top bar to display RAM summary and handle nulls
    depends_on: T2
    refs: R3, R4
T4: Write unit tests for system info parsing and API integration
    depends_on: T1, T2
    refs: R1, R2, R5

GATES
- Run `pytest tests/test_system_info.py` to verify MemAvailable parsing, MB conversion, and malformed file handling.
- Run `pytest tests/test_api_system.py` to verify `GET /api/system` returns correct JSON structure with `free_ram_mb`.
- Run `pytest` full suite to ensure no regressions in existing features.
- Manual verification of UI top bar displaying sum of up containers' RAM + free RAM, and showing `—` when values are unavailable.