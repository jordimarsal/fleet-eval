FILES
web/app.js
web/styles.css
tests/test_web.py

TASKS
T1: Implement enrichment state derivation logic in JavaScript
    depends_on: (none)
    refs: R1, R2, R3
T2: Implement enrichment marker rendering in updateRow
    depends_on: T1
    refs: R4, R9
T3: Apply state-specific styling to the enrichment marker
    depends_on: T2
    refs: R5, R6, R7
T4: Add textual state label and tooltip to the marker
    depends_on: T3
    refs: R8
T5: Ensure enrich action remains unchanged for 'none' state
    depends_on: T4
    refs: R10
T6: Verify no external dependencies or new color tokens are introduced
    depends_on: T5
    refs: R11
T7: Update tests to cover all enrichment state scenarios
    depends_on: T1
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R12

GATES
- Run `test_page_has_no_external_network_dependencies` to ensure no network dependencies.
- Run `test_scripts_use_safe_sinks_only` to ensure security safety.
- Run `tests/test_web.py` to verify frontend behavior and CSS rules.
- Run `tests/test_download_service.py` to ensure backend integration points remain valid.
- Verify that `web/app.js` does not reference `album` or `date`.
- Verify that `:root` in `web/styles.css` has no new color tokens added.