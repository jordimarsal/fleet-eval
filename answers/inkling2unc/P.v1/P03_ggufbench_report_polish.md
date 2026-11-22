FILES
html_report.py
report.py
tests/test_html_report.py
tests/test_report.py
benchmarks/test_bench_report.py

TASKS
T1: Split pool into live vs retired rows and compute KPIs from live rows only
    depends_on: (none)
    refs: R5

T2: Render Board and Retired panes as a pure-CSS tab bar (no JS dependency, Board default visible)
    depends_on: T1
    refs: R1, R2, R3, R8, R12

T3: Sort every per-dimension list by direction (higher-is-better descending, latency ascending, incl. Retired pane)
    depends_on: T2
    refs: R7

T4: Place Recommendations after KPI strip and before "Weighted global"; filter task sets chips to Board blocks only, naming signature as text when it exists solely among retired rows
    depends_on: T2
    refs: R6, R11

T5: Header chip counts, retired-pane record note, and exclusion of recommendations/KPI strip in the Retired pane
    depends_on: T3, T4
    refs: R9, R10, R4

T6: Add regression tests for all approved requirements and run existing suite
    depends_on: T5
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

GATES
pytest -q tests/test_html_report.py tests/test_report.py benchmarks/test_bench_report.py
pytest -q
Render a sample pool containing both live and retired rows; verify manually that the tab bar switches without JavaScript (Board default visible), Board contains no retired row, Retired shows no KPI strip or Recommendations section and carries the record-only note, per-dimension lists are sorted correctly in both panes, header shows `N models (+M retired)` with single total when retired=0, task sets chips link only to rendered Board blocks, and document remains self-contained.