FILES
src/atalaia/api.py
web/app.js
tests/test_api_ram.py

TASKS
T1: Implement `/api/system` endpoint to return `free_ram_mb` from `/proc/meminfo`
    depends_on: (none)
    refs: R1, R5
T2: Handle missing or malformed `/proc/meminfo` gracefully in API
    depends_on: T1
    refs: R2
T3: Update UI top bar to display sum of `ram_mb` for `up` entries and free RAM
    depends_on: T1
    refs: R3
T4: Implement UI fallback display (`—`) when values are unavailable
    depends_on: T3
    refs: R4

GATES
- Run `pytest tests/test_api_ram.py` to verify API endpoint behavior and error handling.
- Verify `GET /api/system` returns correct `free_ram_mb` value from `/proc/meminfo`.
- Verify `GET /api/system` returns `null` for `free_ram_mb` when `/proc/meminfo` is missing/malformed.
- Inspect UI top bar to confirm it displays the sum of `ram_mb` for `up` containers plus free RAM.
- Confirm UI displays `—` when any required value is unavailable.
- Ensure no Docker or subprocess calls are used in the system summary read logic.