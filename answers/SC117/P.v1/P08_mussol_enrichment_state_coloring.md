FILES
web/app.js
web/styles.css

TASKS
T1: Implement enrichment state derivation logic in `web/app.js`
    depends_on: (none)
    refs: R1, R2, R3
T2: Add CSS tokens and styles for the three enrichment states in `web/styles.css`
    depends_on: T1
    refs: R5, R6, R7, R11
T3: Update `updateRow` to render the enrichment marker based on derived state in `web/app.js`
    depends_on: T1, T2
    refs: R4, R8, R9, R10
T4: Verify no external dependencies or new palette tokens introduced in `web/app.js` and `web/styles.css`
    depends_on: T3
    refs: R11, R12

GATES
- Run `test_page_has_no_external_network_dependencies`
- Run `test_scripts_use_safe_sinks_only`
- Visual inspection of markers against `--color-card` and `--color-primary` backgrounds for AA contrast compliance per `design.md` § D4
- Verify `rowSignature` contains only `artist`, `has_cover`, `enriched_at`
- Verify `buildRow` does not create a marker element