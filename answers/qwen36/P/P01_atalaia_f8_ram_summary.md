FILES
src/atalaia/system.py
src/atalaia/api.py
web/app.js
tests/test_api_system.py
harness/specs/f8_ram/tasks.md

TASKS
T1: Implement system.py module with get_free_ram_mb() function that reads /proc/meminfo and parses MemAvailable, returning None on missing or malformed data.
    depends_on: (none)
    refs: R1, R2, R5
T2: Add GET /api/system endpoint to api.py that calls get_free_ram_mb() from system.py and returns JSON with free_ram_mb field.
    depends_on: T1
    refs: R1, R2
T3: Update web/app.js poll handler to fetch /api/system each cycle, accumulate ram_mb for all up entries, display sum plus free RAM in top bar, using — when any value is unavailable.
    depends_on: T1
    refs: R3, R4
T4: Write unit tests in test_api_system.py covering successful read, missing file, malformed file, and null return behavior.
    depends_on: T1
    refs: R1, R2
T5: Record tasks.md entry under harness/specs/f8_ram/tasks.md documenting the implementation plan and task dependencies.
    depends_on: (none)
    refs: R1, R2, R3, R4, R5

GATES
- pytest tests/test_api_system.py passes (all 4 scenarios covered)
- curl -s http://localhost/api/system returns valid JSON with numeric or null free_ram_mb
- UI renders correct sum of up-entry ram_mb + free RAM after poll cycle
- UI shows — when either free_ram_mb or any ram_mb is null/missing
- No subprocess calls or Docker invocations present in src/atalaia/system.py