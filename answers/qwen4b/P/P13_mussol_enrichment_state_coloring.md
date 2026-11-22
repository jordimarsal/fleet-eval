FILES
src/mussol/library/library_record.py
web/app.js
web/styles.css

TASKS
T1: Implement enrichment state derivation logic for library records
    depends_on: (none)
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12
T2: Update row rendering to include enrichment marker based on derived state
    depends_on: T1
    refs: R4, R5, R6, R7, R8
T3: Ensure no new tokens or network dependencies are introduced
    depends_on: T1, T2
    refs: R11
T4: Verify poll-based state updates trigger correct marker rebuilds
    depends_on: T2
    refs: R9

GATES
- verify_enrichment_state_derivation_correctly_handles_all_cases
- verify_marker_rendering_matches_specified_colors_and_text
- verify_no_new_tokens_or_network_dependencies_introduced
- verify_enrichment_state_does_not_depend_on_album_or_date
- verify_enrich_button_stays_unchanged_in_none_state
- verify_contrast_ratios_meet_wcag_aa_requirements