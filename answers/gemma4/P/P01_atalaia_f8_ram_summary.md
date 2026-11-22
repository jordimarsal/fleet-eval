FILES
src/atalaia/api.py
web/app.js
tests/test_api_ram.py

TASKS
T1: Implement system RAM retrieval logic in API
    depends_on: (none)
    refs: R1, R2, R5
T2: Add GET /api/system endpoint to API
    depends_on: T1
    refs: R1, R2
T3: Update UI top bar to calculate and display total RAM sum
    depends_on: T2
    refs: R3, R4
T4: Add unit tests for RAM retrieval and API endpoint
    depends_on: T2
    refs: R1, R2, R5

GATES
- Verify `GET /api/system` returns correct MB value from a mocked `/proc/meminfo`.
- Verify `GET /api/system` returns `null` when `/proc/meminfo` is missing or unreadable.
- Verify UI displays `—` when API returns `null` or container RAM data is missing.
- Verify UI correctly sums `up` container RAM + free system RAM.
- Confirm no subprocess or Docker calls are used in the RAM reading logic.