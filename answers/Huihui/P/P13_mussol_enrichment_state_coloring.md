FILES
web/app.js
web/styles.css
tests/test_web.py

TASKS
T1: Implement enrichment state derivation logic in web/app.js
    depends_on: (none)
    refs: R1, R2, R3, R12
T2: Implement enrichment marker construction and rendering in updateRow
    depends_on: T1
    refs: R4, R8, R9, R10
T3: Define CSS styles for enrichment markers in web/styles.css
    depends_on: T2
    refs: R5, R6, R7, R11
T4: Add static frontend tests for enrichment markers
    depends_on: T2, T3
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

GATES
- Run `pytest tests/test_web.py` to verify all new and existing frontend tests pass.
- Verify that `test_page_has_no_external_network_dependencies` and `test_scripts_use_safe_sinks_only` remain green.
- Manually inspect `web/app.js` to ensure `rowSignature` includes `artist`, `has_cover`, and `enriched_at`.
- Confirm no hex color literals are introduced in the new CSS rules.