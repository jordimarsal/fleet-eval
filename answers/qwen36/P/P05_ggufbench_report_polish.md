FILES
html_report.py
tests/test_html_report.py

TASKS
T1: Add CSS-only tab bar and two-pane layout to report HTML
    depends_on: (none)
    refs: R1, R2, R3, R8, R9, R12
T2: Split pool into live/retired subsets; render Board pane from live only
    depends_on: T1
    refs: R1, R3, R8
T3: Render Retired pane with record-only text; exclude Recommendations + KPI strip
    depends_on: T2
    refs: R4, R9
T4: Compute KPI strip from live rows only
    depends_on: T2
    refs: R5
T5: Insert Recommendations section after KPI strip, before Weighted global
    depends_on: T4
    refs: R6
T6: Sort all per-dimension lists descending for higher-is-better, ascending for latency (both panes)
    depends_on: T2
    refs: R7
T7: Update header "models" chip — dual count when retired exist, single otherwise
    depends_on: T2
    refs: R10
T8: Fix task-set links in Board pane; retire signatures as plain text
    depends_on: T2
    refs: R11

GATES
- `python -m pytest tests/test_html_report.py` passes (all existing tests still green plus new tab-bar / retired-pane assertions).
- Open generated report.html offline (no network): verify two tabs appear when pool has retired rows, default to Board, switch works without JS.
- Verify self-contained contract: `<script src>` absent, no external URLs, at most one inline script tag.
- Spot-check that Retired pane contains no Recommendations section and no KPI strip values.
- Confirm KPI strip figures match only live-row computations (cross-reference with report._scores output).
- Check sorting within every dimension list is correct direction (higher-is-better desc, latency asc) in both panes.
- Validate header chip format: `N models (+M retired)` when retired > 0, plain `N models` otherwise.
- Verify all task-set links point to blocks visible in the Board pane; retired-only signatures are rendered as text, not links.