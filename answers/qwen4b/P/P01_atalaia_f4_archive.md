FILES
harness/specs/f4_archive/APPROVAL
harness/specs/f4_archive/design.md
harness/specs/f4_archive/requirements.md
harness/specs/f4_archive/review.md
harness/specs/f4_archive/tasks.md
src/atalaia/actions.py
src/atalaia/api.py
src/atalaia/models.py
src/atalaia/detail.py
tests/test_api_actions.py
tests/test_api_detail.py
web/app.js
web/style.css

TASKS
T1: Implement archive/unarchive API endpoints with id validation and state persistence
    depends_on: (none)
    refs: R1, R2, R3, R4
T2: Update project model to include archived status and modify detail payload
    depends_on: T1
    refs: R5, R6
T3: Modify UI to show tabs for active and archived projects with proper filtering
    depends_on: T2
    refs: R7, R8
T4: Ensure UI reflects state changes immediately after refresh
    depends_on: T3
    refs: R9
T5: Validate state file handling on startup and during server restarts
    depends_on: T2
    refs: R1, R6
T6: Verify no modifications are made to scanned project trees when storing archive state
    depends_on: T1
    refs: R10

GATES
- Requirement traceability check via harness/tools/check-traceability.py
- Security audit via harness/tools/audit-security.sh
- Feature list validity via harness/tools/validate-feature-list.py
- End-to-end test coverage in tests/test_api_actions.py and tests/test_api_detail.py