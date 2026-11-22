FILES
web/app.js
web/styles.css
tests/test_web.py

TASKS
T1: Implement enrichment state derivation logic in JavaScript
    depends_on: (none)
    refs: R1, R2, R3
T2: Render enrichment marker in library cards
    depends_on: T1
    refs: R4
T3: Apply colour styling based on enrichment state
    depends_on: T2
    refs: R5, R6, R7
T4: Add textual state label and tooltip to marker
    depends_on: T3
    refs: R8
T5: Ensure marker updates on payload poll changes
    depends_on: T1
    refs: R9
T6: Verify no changes to enrich action for `none` state
    depends_on: T2
    refs: R10
T7: Validate palette constraints and external dependencies
    depends_on: T3
    refs: R11
T8: Confirm enrichment state independence from album/date
    depends_on: T1
    refs: R12

GATES
- Run `test_web.py` to verify state derivation and marker rendering.
- Run `test_page_has_no_external_network_dependencies` to ensure no network dependencies.
- Run `test_scripts_use_safe_sinks_only` to ensure security compliance.
- Visual inspection of `--color-card` and `--color-primary` backgrounds for contrast compliance (R5.2, R6.2).
- Verify `web/app.js` does not reference `album` or `date` (R12.1).