FILES
html_report.py
report.py
benchmarks/test_bench_report.py
harness/progress/current.md

TASKS
T1: Implement CSS-only tab bar and pane structure in HTML report
    depends_on: (none)
    refs: R1, R2, R3, R12
T2: Refactor data processing to separate live and retired rows with correct sorting
    depends_on: T1
    refs: R5, R7, R8
T3: Update header chips for model counts and task set links
    depends_on: T2
    refs: R10, R11
T4: Adjust Retired pane content (remove KPIs/Recs, add record notice)
    depends_on: T2
    refs: R4, R9
T5: Update tests for new report structure and behavior
    depends_on: T1, T2, T3, T4
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12
T6: Update progress documentation
    depends_on: T5
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

GATES
- Run `python -m pytest benchmarks/test_bench_report.py` to verify all report rendering tests pass.
- Verify HTML output contains tab bar only when retired rows exist; otherwise no tab bar or retired pane is present.
- Confirm Board pane is visible by default without JavaScript execution.
- Check that KPI strip values are computed exclusively from live rows.
- Validate sorting order in all per-dimension lists (descending for scores/throughputs, ascending for latency) in both panes.
- Ensure Retired pane does not contain Recommendations section or KPI strip.
- Verify header "models" chip displays separate counts when retired rows exist, single total otherwise.
- Confirm "task sets" chip links only to blocks rendered in the Board pane; signatures exclusive to retired rows appear as text.
- Test with JavaScript disabled to ensure panes remain switchable via pure CSS.
- Verify report remains self-contained with no external resources and at most one inline script.