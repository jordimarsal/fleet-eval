FILES
web/app.js
web/styles.css

TASKS
T1: Derive enrichment state from payload fields
    depends_on: (none)
    refs: R1, R2, R3, R12
T2: Build and render enrichment marker in updateRow
    depends_on: T1
    refs: R4, R9
T3: Style marker per enrichment state using palette tokens only
    depends_on: T2
    refs: R5, R6, R7, R8, R10, R11

GATES
- `test_page_has_no_external_network_dependencies` passes
- `test_scripts_use_safe_sinks_only` passes
- `test_enrichment_state_coloring` passes (all ACs exercised via unit tests on the derivation logic and DOM output)
- Visual regression check against design.md § D4 contrast ratios for all three states on both card backgrounds
- Manual verification that no new CSS variable is added to :root and no hex literals appear in web/styles.css rules introduced by this feature
- Verify `rowSignature` still carries exactly `artist`, `has_cover`, `enriched_at` with no additions