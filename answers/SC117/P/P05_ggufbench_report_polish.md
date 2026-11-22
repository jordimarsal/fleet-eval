FILES
html_report.py
tests/test_html_report.py

TASKS
T1: Implement CSS-only tab bar and pane switching logic
    depends_on: (none)
    refs: R12
T2: Add conditional rendering of Tab Bar and Retired Pane based on pool state
    depends_on: T1
    refs: R1, R3
T3: Set Board pane as default visible view on load
    depends_on: T2
    refs: R2
T4: Filter Board content to exclude retired rows
    depends_on: T2
    refs: R8
T5: Exclude Recommendations section and KPI strip from Retired pane
    depends_on: T2
    refs: R4
T6: Compute KPI strip metrics using only live rows
    depends_on: T4
    refs: R5
T7: Ensure correct ordering (descending/ascending) in all per-dimension lists including Retired pane
    depends_on: T4
    refs: R7
T8: Update header "models" chip to show separate counts when retired rows exist
    depends_on: T2
    refs: R10
T9: Update task set links to only target blocks in the Board pane
    depends_on: T4
    refs: R11
T10: Add explanatory text to Retired pane stating models are a record only
    depends_on: T2
    refs: R9
T11: Position Recommendations section correctly relative to KPI strip and Weighted global
    depends_on: T6
    refs: R6
T12: Verify self-containment and CSS-only switching with JS disabled
    depends_on: T1
    refs: R12

GATES
- Run `python -m pytest tests/test_html_report.py` to ensure all existing HTML report tests pass.
- Generate an HTML report with a pool containing both live and retired models; verify the tab bar appears, defaults to Board, and clicking "Retired" shows only retired rows without KPIs/Recommendations.
- Generate an HTML report with only live models; verify no tab bar is rendered and the board displays normally.
- Inspect the generated HTML source to confirm no external resources (images, fonts, external scripts) are linked and that the inline script count remains <= 1.
- Disable JavaScript in a browser and open the report with mixed pool; verify tabs switch correctly using pure CSS (:target or similar mechanism).
- Verify the header chip text matches `N models (+M retired)` format when retired rows exist, and single total otherwise.