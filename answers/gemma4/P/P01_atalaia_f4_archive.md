FILES
src/atalaia/models.py
src/atalaia/api.py
src/atalaia/actions.py
web/app.js
web/index.html
web/style.css
tests/test_archive.py

TASKS
T1: Implement Archive Persistence Logic
    depends_on: (none)
    refs: R1, R6, R10
T2: Update Models and API Payloads
    depends_on: T1
    refs: R5
T3: Implement Archive/Unarchive API Endpoints
    depends_on: T2
    refs: R2, R3, R4
T4: Update UI Tabs and Filtering logic
    depends_on: T3
    refs: R7, R9
T5: Add Archive Actions to UI Detail Drawer
    depends_on: T4
    refs: R8

GATES
- Run `pytest tests/test_archive.py` to verify persistence, error handling (R4), and idempotency (R2, R3).
- Verify that the state file is created in the user's state directory and survives a simulated restart.
- Verify via browser inspection that project payloads contain the `archived` boolean.
- Manual verification of UI tab switching and action button visibility in the detail drawer.
- Run `harness/tools/check-traceability.py --feature f4_archive` to ensure all requirements are mapped.