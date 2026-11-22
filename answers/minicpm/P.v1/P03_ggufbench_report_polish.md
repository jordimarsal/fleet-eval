FILES
html_report.py
report.py
tests/test_html_report.py
tests/test_report.py

TASKS
T1: Implement tab bar logic and pane switching with pure CSS
    depends_on: (none)
    refs: R1, R12
T2: Implement default visibility of Board pane and conditional tab bar rendering
    depends_on: T1
    refs: R2, R3
T3: Implement Retired pane content filtering and messaging
    depends_on: T1
    refs: R4, R8, R9
T4: Implement KPI strip computation restricted to live rows
    depends_on: (none)
    refs: R5
T5: Implement Recommendations section placement
    depends_on: T4
    refs: R6
T6: Implement sorting logic for per-dimension lists in both panes
    depends_on: (none)
    refs: R7
T7: Implement header "models" chip logic for separate counts
    depends_on: (none)
    refs: R10
T8: Implement "task sets" chip linking logic restricted to Board pane
    depends_on: T1
    refs: R11

GATES
- Verify that with only live rows, the report renders without a tab bar (R3).
- Verify that with retired rows, the tab bar appears with "Board" and "Retired" panes (R1).
- Verify that the Board pane is visible by default on load without JavaScript (R2).
- Verify that the Retired pane excludes the Recommendations section and KPI strip (R4).
- Verify that KPI metrics are calculated exclusively from live rows (R5).
- Verify that the Recommendations section is positioned between the KPI strip and "Weighted global" section (R6).
- Verify that all per-dimension lists are sorted correctly (best to worst) in both panes (R7).
- Verify that the Board pane does not display any retired rows (R8).
- Verify that the Retired pane displays the required record-only message (R9).
- Verify that the header chip shows separate counts when retired rows exist (e.g., `18 models (+16 retired)`) (R10).
- Verify that task set links only point to blocks in the Board pane (R11).
- Verify that pane switching works with JavaScript disabled using pure CSS (R12).