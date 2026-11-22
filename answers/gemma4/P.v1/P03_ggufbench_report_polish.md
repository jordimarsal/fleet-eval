FILES
report.py
tests/test_report.py

TASKS
T1: Update data models and KPI logic to filter live rows
    depends_on: (none)
    refs: R5, R8
T2: Implement sorting logic for all dimension lists (descending vs ascending)
    depends_on: T1
    refs: R7
T3: Update header chips to show separate counts for live and retired models
    depends_on: T1
    refs: R10
T4: Refactor report generation to support dual panes with CSS-only switching
    depends_on: T2
    refs: R1, R2, R3, R12
T5: Implement Retired pane content restrictions and disclaimer
    depends_on: T4
    refs: R4, R9
T6: Fix task set links to ensure they only link to visible Board blocks
    depends_on: T4
    refs: R11
T7: Finalize layout ordering (KPI -> Recommendations -> Weighted Global)
    depends_on: T1, T4
    refs: R6

GATES
- Verify that the "Board" pane is visible by default when JS is disabled.
- Verify that the "Retired" pane contains no KPI strip or Recommendations section.
- Verify that KPIs are calculated strictly from non-retired rows.
- Verify that all dimension lists (latency, throughput, etc.) are correctly sorted in both panes.
- Verify that the model count chip displays `X models (+Y retired)` only when retired rows exist.
- Verify that task set links in the Retired pane are plain text if the target block is in the Board pane.
- Run `tests/test_report.py` to ensure data integrity across live/retired splits.