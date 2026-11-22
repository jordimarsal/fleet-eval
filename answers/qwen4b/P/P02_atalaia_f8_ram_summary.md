FILES
src/atalaia/detectors.py
web/app.js

TASKS
T1: Implement direct reading of /proc/meminfo to extract free_ram_mb
    depends_on: (none)
    refs: R1, R2, R5
T2: Update API endpoint to serve free_ram_mb from /proc/meminfo directly
    depends_on: T1
    refs: R1, R2, R5
T3: Modify UI summary rendering to aggregate up entries and include free RAM
    depends_on: T2
    refs: R3, R4
T4: Ensure missing or malformed /proc/meminfo returns null without error
    depends_on: T1
    refs: R2, R4

GATES
- Verify that GET /api/system returns correct free_ram_mb value when /proc/meminfo is present and valid (test: test_api_ram.py)
- Confirm that GET /api/system returns null for free_ram_mb when /proc/meminfo is missing or malformed (test: test_api_ram.py)
- Validate that UI top bar displays sum of up entries and free RAM on poll (manual test with web app)
- Confirm that any unavailable value in UI renders as "—" (test: test_web.py)