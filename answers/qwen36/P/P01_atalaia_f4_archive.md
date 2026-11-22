FILES
src/atalaia/archive.py
src/atalaia/api.py
web/app.js
web/index.html
web/style.css
tests/test_archive.py
tests/test_api.py
tests/test_web.py
harness/specs/f4_archive/tasks.md
harness/specs/f4_archive/design.md
harness/specs/f4_archive/requirements.md
harness/specs/f4_archive/review.md
harness/specs/f4_archive/APPROVAL
harness/progress/current.md
harness/progress/history.md

TASKS
T1: Create archive persistence module
    depends_on: (none)
    refs: R1, R6, R10
T2: Add archive state to project model and status payload
    depends_on: T1
    refs: R5
T3: Implement POST /api/projects/{id}/archive endpoint
    depends_on: T2
    refs: R2, R4
T4: Implement POST /api/projects/{id}/unarchive endpoint
    depends_on: T2
    refs: R3, R4
T5: Wire archive endpoints into FastAPI router
    depends_on: T3, T4
    refs: R2, R3
T6: Update list/detail API responses to include archived field
    depends_on: T2
    refs: R5
T7: Add archived tab and filter logic to web/app.js
    depends_on: T6
    refs: R7, R9
T8: Add arxivar/desarxivar buttons in detail drawer
    depends_on: T7
    refs: R8
T9: Style tabs and action buttons in web/style.css
    depends_on: T8
    refs: R7, R8
T10: Write unit tests for archive module
    depends_on: T1
    refs: R1, R6
T11: Write integration tests for archive/unarchive endpoints
    depends_on: T5
    refs: R2, R3, R4
T12: Write UI tests for tab filtering and actions
    depends_on: T9
    refs: R7, R8, R9

GATES
- harness/tools/check-traceability.py --feature f4_archive passes (all R1–R10 covered)
- pytest -q runs clean on tests/test_archive.py, tests/test_api.py, tests/test_web.py
- curl POST /api/projects/{id}/archive returns 202; repeated call also 202
- curl POST /api/projects/{id}/unarchive returns 202; repeated call also 202
- curl to unknown id returns 404 for both endpoints
- GET list/detail includes "archived": true/false per project
- Missing/malformed state file does not crash server
- UI shows two tabs with correct counts; archived projects hidden from actius, non-archived hidden from arxivats
- Detail drawer shows arxivar/desarxivar buttons as appropriate
- After refresh, tab assignment reflects new archive state immediately
- No files inside scanned project trees are modified