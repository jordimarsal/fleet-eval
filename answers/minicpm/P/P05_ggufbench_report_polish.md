FILES
html_report.py
tests/test_html_report.py

TASKS
T1: Implement tab bar UI with Board/Retired panes
    depends_on: (none)
    refs: R1, R2, R3, R12
T2: Filter Board pane to exclude retired rows
    depends_on: T1
    refs: R8
T3: Populate Retired pane with record-only content
    depends_on: T1
    refs: R4, R9
T4: Compute KPI strip from live rows only
    depends_on: T1
    refs: R5
T5: Position Recommendations section correctly
    depends_on: T4
    refs: R6
T6: Implement descending/ascending sort for per-dimension lists
    depends_on: T1
    refs: R7
T7: Update header "models" chip to show separate counts when retired rows exist
    depends_on: T1
    refs: R10
T8: Update "task sets" chip to link only to Board pane blocks
    depends_on: T1
    refs: R11

GATES
- Run `python -m pytest tests/test_html_report.py` to verify HTML generation and self-contained constraint (no external resources, max 1 inline script).
- Verify tab bar renders with two panes (Board/Retired) when pool contains both live and retired rows.
- Verify Board pane is visible by default on report open.
- Verify no tab bar or Retired pane renders when pool has zero retired rows.
- Verify Retired pane lacks Recommendations section and KPI strip.
- Verify KPI strip values are derived exclusively from live rows.
- Verify Recommendations section appears between KPI strip and "Weighted global" section.
- Verify all per-dimension lists (code, agent, tools, speed) are sorted correctly (descending for scores/throughput, ascending for latency) in both panes.
- Verify Board pane does not render any retired rows.
- Verify Retired pane includes the "record only" statement.
- Verify header "models" chip format switches between single total and `X models (+Y retired)` based on retired row presence.
- Verify "task sets" chip links only to blocks in Board pane, never to retired-only signatures.
- Verify pane switching works with JavaScript disabled (pure CSS implementation).