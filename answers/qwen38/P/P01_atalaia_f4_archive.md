FILES
src/atalaia/archive.py
src/atalaia/api.py
web/app.js
web/index.html
tests/test_archive.py
tests/test_api_archive.py
tests/test_web_static.py

TASKS
T1: Implement archive state persistence module
    depends_on: (none)
    refs: R1, R6, R10
T2: Add archive/unarchive API endpoints and payload integration
    depends_on: T1
    refs: R2, R3, R4, R5
T3: Update UI for tabs and actions
    depends_on: T2
    refs: R7, R8, R9
T4: Write unit tests for archive logic and API
    depends_on: T1, T2
    refs: R1, R2, R3, R4, R5, R6, R10
T5: Verify UI static assets and traceability
    depends_on: T3, T4
    refs: R7, R8, R9

GATES
- Run `pytest` to ensure all new and existing tests pass.
- Execute `harness/tools/check-traceability.py --feature f4_archive` to verify requirement coverage.
- Manually verify that the state file is created in the user's state directory and not inside project trees.