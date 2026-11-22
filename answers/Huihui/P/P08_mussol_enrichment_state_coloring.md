FILES
web/app.js
web/styles.css
tests/test_web.py
harness/progress/impl_enrichment_state_coloring.md

TASKS
T1: Implement enrichment state derivation logic in web/app.js
    depends_on: (none)
    refs: R1, R2, R3, R12
T2: Implement enrichment marker rendering and updateRow integration
    depends_on: T1
    refs: R4, R5, R6, R7, R8, R9, R10
T3: Add CSS rules for enrichment markers using existing tokens
    depends_on: T2
    refs: R5, R6, R7, R11
T4: Write unit tests for state derivation and DOM rendering
    depends_on: T2
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12
T5: Update progress documentation
    depends_on: T4
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

GATES
- Run `pytest tests/test_web.py` to verify new unit tests pass.
- Run `pytest tests/` to ensure no regressions in existing test suite.
- Verify `web/app.js` does not contain the strings "album" or "date".
- Verify `web/styles.css` contains no hex color literals (e.g., #fff) in the newly added rules.
- Verify `rowSignature` function in `web/app.js` includes `artist`, `has_cover`, and `enriched_at`.
- Manually inspect `updateRow` in `web/app.js` to confirm marker construction is present and `buildRow` does not construct a marker.