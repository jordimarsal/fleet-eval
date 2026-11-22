FILES
html_report.py
tests/test_html_report.py

TASKS
T1: Implement CSS-only tab switching for Board/Retired panes
    depends_on: (none)
    refs: R1, R3, R12
T2: Update HTML structure to include Retired pane and conditional Tab Bar
    depends_on: T1
    refs: R1, R3, R8, R9
T3: Implement default visibility of Board pane on load
    depends_on: T2
    refs: R2
T4: Filter KPI strip computation to live rows only
    depends_on: (none)
    refs: R5
T5: Filter Recommendations section to live rows only
    depends_on: (none)
    refs: R6
T6: Exclude Recommendations and KPI from Retired pane rendering
    depends_on: T2
    refs: R4
T7: Ensure descending/ascending sort order in all per-dimension lists including Retired
    depends_on: (none)
    refs: R7
T8: Update header "models" chip logic for dual count display
    depends_on: (none)
    refs: R10
T9: Update "task sets" chip logic to link only to Board pane blocks
    depends_on: (none)
    refs: R11

GATES
- Verify CSS-only tab switching works with JavaScript disabled (R12).
- Confirm Board pane is visible by default without JS (R2).
- Check that Tab Bar is absent when no retired rows exist (R3).
- Validate that Retired pane contains no Recommendations or KPIs (R4).
- Verify KPI metrics are calculated exclusively from live rows (R5).
- Confirm Recommendations appear between KPI strip and Weighted global (R6).
- Ensure all dimension lists (code, agent, tools, speed, gen, prompt) are sorted correctly (best-to-worst) in both panes (R7).
- Confirm Board pane excludes retired rows entirely (R8).
- Verify Retired pane displays the specific record-only statement (R9).
- Check header chip shows separate counts when retired rows exist (R10).
- Verify task set links point only to visible Board blocks (R11).