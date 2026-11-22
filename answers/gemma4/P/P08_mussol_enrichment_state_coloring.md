FILES
web/app.js
web/styles.css

TASKS
T1: Implement enrichment state derivation logic in frontend
    depends_on: (none)
    refs: R1, R2, R3, R12
T2: Implement marker rendering and styling in `updateRow`
    depends_on: T1
    refs: R4, R5, R6, R7, R8, R9, R10
T3: Add CSS rules for enrichment states using existing tokens
    depends_on: T1
    refs: R5, R6, R7, R11
T4: Verify accessibility and constraints
    depends_on: T2, T3
    refs: R5, R6, R8, R11, R12

GATES
- Run `test_page_has_no_external_network_dependencies` to ensure no new network calls.
- Run `test_scripts_use_safe_sinks_only` to ensure security compliance.
- Manual visual verification of all three states (`untagged`, `partial`, `tagged`) against `design.md` contrast ratios on both `--color-card` and `--color-primary` backgrounds.
- Verify that the `enrichButton` remains functional and unchanged in state `none`.
- Verify that adding/removing `artist`, `has_cover`, or `enriched_at` triggers a UI update via `updateRow`.