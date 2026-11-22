FILES
src/atalaia/api.py
src/atalaia/detectors.py
web/app.js
tests/test_api_ram.py
tests/test_detectors.py

TASKS
T1: Implement `/api/system` endpoint to return `free_ram_mb` from `/proc/meminfo`
    depends_on: (none)
    refs: R1, R5
T2: Handle missing or malformed `/proc/meminfo` gracefully in the API
    depends_on: T1
    refs: R2
T3: Update UI top bar to display sum of `ram_mb` for `up` entries plus system free RAM
    depends_on: T1
    refs: R3
T4: Ensure UI displays `—` when any value is unavailable
    depends_on: T3
    refs: R4

GATES
- Run `pytest tests/test_api_ram.py` to verify the `/api/system` endpoint returns correct `free_ram_mb` and handles errors.
- Run `pytest tests/test_detectors.py` to verify helper functions for reading memory info.
- Manually verify the UI top bar updates with the correct RAM summary on poll.
- Run `harness/tools/check-traceability.py --feature f6_ram` to ensure all requirements (R1-R4) are traced to tasks and tests.