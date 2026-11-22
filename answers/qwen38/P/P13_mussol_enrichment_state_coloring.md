FILES
web/app.js
web/styles.css
tests/test_web.py

TASKS
T1: Implement enrichment state derivation logic in frontend
    depends_on: (none)
    refs: R1, R2, R3, R12
T2: Add CSS classes for enrichment marker states
    depends_on: T1
    refs: R5, R6, R7, R8, R11
T3: Integrate marker rendering into updateRow and ensure buildRow exclusion
    depends_on: T2
    refs: R4, R9, R10
T4: Update tests to verify new behavior and constraints
    depends_on: T3
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

GATES
- Run `pytest tests/test_web.py` to ensure all static frontend checks pass, including token usage, safety sinks, and specific enrichment badge assertions.
- Verify that no hex color literals are introduced in `web/styles.css` or `web/app.js`.
- Confirm that `rowSignature` in `web/app.js` includes `artist`, `has_cover`, and `enriched_at`.
- Ensure `buildRow` does not create the enrichment marker.
- Check that `updateRow` creates the marker based on derived state.