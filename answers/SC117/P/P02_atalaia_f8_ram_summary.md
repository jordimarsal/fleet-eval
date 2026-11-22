FILES
src/atalaia/detectors.py
src/atalaia/api.py
web/app.js
tests/test_detectors.py
tests/test_api_ram.py

TASKS
T1: Implement direct /proc/meminfo reader
    depends_on: (none)
    refs: R5
T2: Add free_ram_mb to system endpoint
    depends_on: T1
    refs: R1, R2
T3: Update UI top bar with RAM summary and null handling
    depends_on: T2
    refs: R3, R4

GATES
- check-traceability.py --feature f8_ram_summary verifies all R1-R5 are covered.
- pytest tests/test_detectors.py::test_read_meminfo_direct and tests/test_api_ram.py verify backend logic including malformed file fallback.
- Manual browser verification of web/index.html confirms top bar displays "—" when data is missing and sums RAM correctly on poll.