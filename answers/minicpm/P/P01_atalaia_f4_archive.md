FILES
src/atalaia/archive.py
src/atalaia/api.py
src/atalaia/models.py
web/app.js
web/index.html
web/style.css
tests/test_api_archive.py
tests/test_web_archive.py

TASKS
T1: Implement archive state persistence layer
    depends_on: (none)
    refs: R1, R6, R10
T2: Implement POST /api/projects/{id}/archive endpoint
    depends_on: T1
    refs: R2, R4
T3: Implement POST /api/projects/{id}/unarchive endpoint
    depends_on: T1
    refs: R3, R4
T4: Update project models and API payloads to include 'archived' boolean
    depends_on: T1
    refs: R5
T5: Update UI to show actius/arxivats tabs with filtered counts
    depends_on: T4
    refs: R7
T6: Add arxivar/desarxivar actions in project detail drawer
    depends_on: T5
    refs: R8
T7: Wire UI actions to API endpoints and refresh tab state
    depends_on: T2, T3, T6
    refs: R9
T8: Add tests for archive/unarchive API and UI behavior
    depends_on: T4, T7
    refs: R2, R3, R4, R5, R7, R8, R9

GATES
- Run `python -m pytest tests/test_api_archive.py tests/test_web_archive.py` to verify API and UI integration tests pass.
- Run `harness/tools/check-traceability.py --feature f4_archive` to ensure all requirements R1-R10 are traced to implemented tasks.
- Manually verify:
  - Archiving/unarchiving a project persists across server restarts (R1).
  - POST /api/projects/{id}/archive returns 202 and idempotently succeeds (R2).
  - POST /api/projects/{id}/unarchive returns 202 and idempotently succeeds (R3).
  - Unknown project ID returns 404 for both archive and unarchive (R4).
  - Project list and detail payloads include `archived: boolean` (R5).
  - Missing/malformed state file does not crash the system (R6).
  - UI shows "actius" and "arxivats" tabs with correct counts and filtering (R7).
  - Detail drawer shows "arxivar" for non-archived and "desarxivar" for archived projects (R8).
  - Tab assignment updates immediately after archive state change (R9).
  - No files inside scanned project trees are modified to store archive state (R10).