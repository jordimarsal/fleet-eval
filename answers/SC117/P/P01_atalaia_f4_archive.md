FILES
src/atalaia/archive.py
src/atalaia/api.py
tests/test_archive.py
web/app.js
web/style.css

TASKS
T1: Implement archive state persistence layer
    depends_on: (none)
    refs: R1, R6, R10
T2: Implement API endpoints for archive/unarchive
    depends_on: T1
    refs: R2, R3, R4
T3: Update project models and API responses to include archived status
    depends_on: T1
    refs: R5
T4: Implement UI tab filtering logic based on archived status
    depends_on: T3
    refs: R7
T5: Implement UI actions (archive/unarchive buttons) in detail drawer
    depends_on: T2, T3
    refs: R8, R9
T6: Add tests for archive functionality
    depends_on: T1, T2, T3
    refs: R1, R2, R3, R4, R5, R6

GATES
- Run `python -m pytest tests/test_archive.py` to verify unit tests for persistence and API.
- Run `python -m pytest tests/test_api.py` and `tests/test_detail.py` to ensure existing functionality is not broken by the new `archived` field.
- Run `harness/tools/check-traceability.py --feature f4_archive` to verify all requirements are covered.
- Manual verification: Start server, POST archive request, check file existence under state dir, restart server, verify file persists, check UI tabs update correctly.