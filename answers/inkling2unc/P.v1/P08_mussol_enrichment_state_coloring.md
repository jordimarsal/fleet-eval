FILES
web/app.js
web/styles.css
tests/test_web.py

TASKS
T1: Add enrichment-state derivation helper
    depends_on: (none)
    refs: R1, R2, R3, R12

T2: Build the state marker inside updateRow with words and titles
    depends_on: T1
    refs: R4, R8, R9

T3: Add three-state marker styling using palette tokens only
    depends_on: T2
    refs: R5, R6, R7, R11

T4: Preserve enrich action behaviour by enrichment state
    depends_on: T1
    refs: R10, R12

T5: Extend panel tests for state derivation, rendering and refresh reconciliation
    depends_on: T2, T3, T4
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

GATES
node --check web/app.js; grep for album or date in web/app.js must return nothing; confirm LibraryDto/LibraryRecord/library_records fields unchanged (git diff shows no changes outside listed files); run pytest tests/test_web.py -v (including test_page_has_no_external_network_dependencies and test_scripts_use_safe_sinks_only if present there) and the full suite pytest -q to confirm AC-related checks stay green; manual check that buildRow builds no marker, updateRow builds exactly one from its updated item, marker text is untagged/partial/tagged with title naming missing fields for partial, complete uses var(--color-accent), partial uses var(--color-muted) with var(--color-destructive) border, none uses var(--color-muted) with no border/background, enrichButton label/request/position unchanged and no state-based disable/dim/hide