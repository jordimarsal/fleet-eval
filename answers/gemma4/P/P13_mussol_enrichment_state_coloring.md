FILES
web/styles.css
web/app.js

TASKS
T1: Implement enrichment state derivation logic in frontend
    depends_on: (none)
    refs: R1, R2, R3, R12
T2: Add CSS rules for enrichment marker states and accessibility
    depends_on: (none)
    refs: R5, R6, R7, R11
T3: Update `updateRow` to construct and render the enrichment marker
    depends_on: T1, T2
    refs: R4, R8, R9, R10
T4: Verify row signature and rebuild logic
    depends_on: T3
    refs: R9

GATES
- Run `test_page_has_no_external_network_dependencies` to ensure no new network calls.
- Run `test_scripts_use_safe_sinks_only` to ensure security compliance.
- Manual visual verification of AA contrast ratios for all 3 states against `--color-card` and `--color-primary`.
- Verify that `enrichButton` remains functional and unchanged in state `none`.
- Verify that changing `artist`, `has_cover`, or `enriched_at` via a poll triggers a marker update.