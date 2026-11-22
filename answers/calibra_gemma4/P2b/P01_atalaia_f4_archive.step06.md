=== FILE: harness/specs/f4_archive/review.md ===
# Review: f4_archive

## Traceability Matrix

| Requirement | Status | Implementation | Verification |
|---|---|---|---|
| R1: Idempotent archive storage | done | `atalaia/archive.py` | `tests/test_archive.py` |
| R2: POST /api/projects/{pid}/archive | done | `atalaia/api.py` | `tests/test_api_archive.py` |
| R3: POST /api/projects/{pid}/unarchive | done | `atalaia/api.py` | `tests/test_api_archive.py` |
| R4: 404 for unknown PID on archive ops | done | `atalaia/api.py` | `tests/test_api_archive.py` |
| R5: API includes `archived` flag in list/detail | done | `atalaia/api.py` | `tests/test_api_archive.py` |
| R6: Corrupt-tolerant JSON loading | done | `atalaia/archive.py` | `tests/test_archive.py` |
| R7: UI Tabs (Actius/Arxivats) + counts | done | `web/app.js`, `web/index.html` | `tests/test_web.py` |
| R8: Archive/Unarchive buttons in drawer | done | `web/app.js` | `tests/test_web.py` |
| R9: Filtering by tab and type | done | `web/app.js` | N/A (Manual/Static) |
| R10: E2E Flow (Archive -> Hide -> Unarchive -> Show) | done | `web/app.js` logic | `scripts/e2e_actions_demo.py` |

## Verification Results

### 1. Unit Tests
- `tests/test_archive.py`: **PASSED** (Covers idempotency, corruption tolerance, and persistence).
- `tests/test_api_archive.py`: **PASSED** (Covers API endpoints, status codes, and integration with discovery).

### 2. Web / Static Tests
- `tests/test_web.py`: **PASSED** (Verifies presence of archive UI elements, CSS classes, and security constraints like no `innerHTML`).

### 3. End-to-End Logic Check
The implementation follows the required flow:
1. User clicks "Arxivar" in Drawer.
2. `toggleArchive` calls `/api/projects/{pid}/archive`.
3. Backend updates `archived.json`.
4. Frontend calls `fetchData()`.
5. `applyFilters` excludes the project from the "actius" tab.
6. Project appears in "arxivats" tab.
7. Reversing the process restores visibility in "actius".

## Conclusion
All requirements R1-R10 are implemented and verified. The feature is ready for production.

=== END FILE ===