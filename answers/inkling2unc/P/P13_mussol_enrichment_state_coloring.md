FILES
web/app.js
web/styles.css
tests/test_web.py

TASKS
T1: Add pure enrichment-state derivation helper
    depends_on: (none)
    refs: R1, R2, R3, R12
T2: Render the state marker inside updateRow only
    depends_on: T1
    refs: R4, R8, R9, R10, R11, R12
T3: Add palette-token-only marker styles for complete / partial / none
    depends_on: T2
    refs: R5, R6, R7, R11
T4: Extend static frontend tests and verify gates
    depends_on: T1, T2, T3
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

GATES
Run pytest on tests/test_web.py plus the full test suite (pytest -q) with existing static checks; confirm test_scripts_use_safe_sinks_only and test_page_has_no_external_network_dependencies stay green; confirm web/app.js mentions no `album` or `date`, that web/styles.css adds no hex literals and no new :root tokens, and that the library schema/DTOs are untouched; run repo scanners (harness tools as configured in docs/verification.md) before closing the feature.