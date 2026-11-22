FILES
src/atalaia/archive.py
src/atalaia/api.py
web/index.html
web/app.js
web/style.css
tests/test_archive.py
tests/test_api_archive.py

TASKS
T1: Persist archived id set in a state file with tolerant load
    depends_on: (none)
    refs: R1, R6, R10
T2: Add archive/unarchive endpoints and `archived` flag in list/detail payloads
    depends_on: T1
    refs: R2, R3, R4, R5
T3: Implement actius/arxivats tabs with counts and detail-drawer arxivar/desarxivar actions
    depends_on: T2
    refs: R7, R8, R9
T4: Cover persistence, endpoint behavior, and regression scenarios with tests
    depends_on: T2
    refs: R1, R2, R3, R4, R5, R6, R10

GATES
Run full test suite (pytest) including new archive tests; run ./harness/init.sh; verify requirements traceability for f4 with check-traceability.py once progress tables are updated; confirm no writes into scanned project trees (state only under XDG/user state dir or configured override); spot-check the UI in browser/static smoke test (list + detail contain tabs, counts, archive/unarchive buttons) and that missing/malformed state file yields empty set without errors.