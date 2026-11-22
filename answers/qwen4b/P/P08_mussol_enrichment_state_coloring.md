FILES  
src/mussol/library/library_record.py  
web/app.js  
web/styles.css  

TASKS  
T1: Implement enrichment state derivation logic in LibraryRecord  
    depends_on: (none)  
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R12  
T2: Update row rendering to display enrichment marker based on derived state  
    depends_on: T1  
    refs: R4, R5, R6, R7, R8, R9, R10  
T3: Ensure marker text and title meet accessibility requirements  
    depends_on: T2  
    refs: R8, R5, R6, R7  
T4: Verify no new colour tokens or network dependencies are introduced  
    depends_on: T1, T2, T3  
    refs: R11  
T5: Confirm enrichment state does not depend on album or date fields  
    depends_on: T1  
    refs: R12  

GATES  
- All ACs from R1–R12 are validated via unit tests in `tests/test_library_record.py` and `tests/test_web.js`  
- WCAG contrast ratios for all text and borders are verified against `design.md` § D4 using automated test suite  
- No new CSS variables or hex colours appear in `web/styles.css`  
- `test_page_has_no_external_network_dependencies` remains green  
- `test_scripts_use_safe_sinks_only` remains green  
- `rowSignature` includes only `artist`, `has_cover`, and `enriched_at` (verified in `web/app.js`)  
- Enrichment action button remains unchanged in UI (verified in `web/app.js`)