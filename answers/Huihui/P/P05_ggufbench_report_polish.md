FILES
html_report.py
tests/test_html_report.py

TASKS
T1: Implement CSS-only tabbed interface structure
    depends_on: (none)
    refs: R1, R2, R3, R8, R9, R12
T2: Refactor data partitioning and KPI/Recommendations logic
    depends_on: T1
    refs: R4, R5, R6, R7
T3: Update header chips and task set link resolution
    depends_on: T2
    refs: R10, R11
T4: Add unit tests for retired pane behavior and self-containment
    depends_on: T3
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

GATES
- Run `python -m pytest tests/test_html_report.py` to verify all new and existing report rendering tests pass.
- Execute a manual smoke test by generating the report with a pool containing both live and retired rows; verify that the Board pane is visible by default without JavaScript, that the Retired pane contains no Recommendations or KPI strip, and that the "models" chip displays separate counts.
- Verify that when the pool contains only live rows, no tab bar or Retired pane markup is present in the generated HTML.
- Confirm that per-dimension lists are correctly sorted (descending for scores/throughputs, ascending for latency) in both panes.
- Validate that the "task sets" chip links only to blocks present in the Board pane, rendering signatures exclusive to retired rows as plain text.