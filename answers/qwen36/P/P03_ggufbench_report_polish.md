FILES
html_report.py
tests/test_html_report.py

TASKS
T1: Add CSS-only tab bar for Board/Retired panes with default visibility of Board
    depends_on: (none)
    refs: R1, R2, R3, R8, R9, R12
T2: Compute KPI strip from live rows only; exclude retired models from headline figures
    depends_on: T1
    refs: R5
T3: Place Recommendations section after KPI strip and before "Weighted global"
    depends_on: T2
    refs: R6
T4: Sort per-dimension lists descending for higher-is-better scores and ascending for latency in both panes
    depends_on: T1
    refs: R7
T5: Render Retired pane without Recommendations section and without KPI strip
    depends_on: T1
    refs: R4
T6: Update header "models" chip to show separate counts when retired rows exist
    depends_on: (none)
    refs: R10
T7: Make "task sets" chip link only to blocks rendered in the Board pane; render retired-only signatures as plain text
    depends_on: T1
    refs: R11

GATES
- `python -m pytest tests/test_html_report.py` passes all existing + new assertions
- Open report with zero retired rows: no tab bar renders, board content visible, single total count in header
- Open report with mixed pool: tab bar shows two tabs, Board is active by default, Retired tab shows record-only notice, no recommendations/KPI inside Retired
- Verify KPI figures match live rows only (cross-check against raw data)
- Verify every dimension list is correctly sorted (higher-is-better desc, latency asc) in both panes
- Verify header chip format matches spec (`N models (+M retired)` vs `N models`)
- Verify task-set links resolve only within Board pane; retired-only signatures are plain text
- Disable JavaScript and toggle between panes via CSS-only mechanism — both states reachable