FILES
report.py
html_report.py
benchmarks/test_bench_html.py
tests/test_html_report.py

TASKS
T1: Split pool rows into live and retired sets; sort dimension lists best→worst per metric direction
    depends_on: (none)
    refs: R5, R7, R8
T2: Build Board pane content from live rows only (KPI strip + Recommendations after it + "Weighted global" ordering preserved in source order, Recommendations before Weighted global) and omit retired styling/badge in Board
    depends_on: T1
    refs: R5, R6, R8
T3: Add Retired pane rendering with gray styling, "retired" badge, record-only statement, no KPI strip or Recommendations, same correctly sorted dimension lists
    depends_on: T1
    refs: R4, R7, R8, R9
T4: Emit tab bar (Board / Retired panes) present only when retired rows exist; single visible pane via pure CSS default to Board with no JS dependency
    depends_on: T2, T3
    refs: R1, R2, R3, R12
T5: Update header chips — models chip showing `N models (+M retired)` when retired rows exist else single total; task sets chip linking only to set blocks rendered in the Board pane, naming signature text never link for retired-only signatures
    depends_on: T2
    refs: R10, R11
T6: Keep report self-contained — inline styles/markup only, at most the existing single inline script, verify two-pane switching works without JavaScript
    depends_on: T4
    refs: R12
T7: Extend HTML tests and benchmark/report tests covering both panes, ordering, counts, chip links, absence of tab bar when no retired rows
    depends_on: T4, T5
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

GATES
- python -m pytest tests/test_html_report.py benchmarks/test_bench_html.py -q passes
- Full test suite (tests/ + benchmarks/) green on changed code paths
- Built report HTML verified with JS disabled / markup inspection: exactly one visible pane (Board) by default, tab bar absent when zero retired rows, Retired pane has no KPI strip or Recommendations section
- Rendered output contains no external resources beyond existing inline script; every per-dimension list sorted ascending for latency and descending otherwise in both panes
- models chip shows split counts only when retired rows exist (and matches header totals against live+retired row count)
- task sets chip: every link resolves to an element present in the Board pane; retired-only signatures rendered as text