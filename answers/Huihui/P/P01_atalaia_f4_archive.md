FILES
src/atalaia/archive.py
src/atalaia/api.py
web/app.js
tests/test_archive.py
tests/test_api_archive.py
tests/test_web_static.py

TASKS
T1: Implement archive state persistence module
    depends_on: (none)
    refs: R1, R6
T2: Add archive/unarchive API endpoints and payload enrichment
    depends_on: T1
    refs: R2, R3, R4, R5
T3: Update UI for tabs, counts, and actions
    depends_on: T2
    refs: R7, R8, R9
T4: Verify no modification of scanned project trees
    depends_on: T1
    refs: R10

GATES
- Run `python -m pytest tests/test_archive.py` to verify persistence logic and malformed file handling.
- Run `python -m pytest tests/test_api_archive.py` to verify endpoint status codes (202, 404) and idempotency.
- Run `python -m pytest tests/test_api_detail.py` to ensure `archived` boolean is present in payloads.
- Run `python -m pytest tests/test_web_static.py` to verify UI tab rendering and action visibility logic.
- Execute `harness/tools/check-traceability.py --feature f4_archive` to confirm all requirements are mapped to tasks/tests.