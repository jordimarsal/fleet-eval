FILES
html_report.py
tests/test_html_report.py

TASKS
T1: Split pool into live vs retired rows and build the two-pane tab bar
    depends_on: (none)
    refs: R1, R2, R3, R8, R12
T2: Compute KPIs from live rows only; insert Recommendations between KPI strip and "Weighted global"; make Retired pane a record without KPI/Recommendations + notice
    depends_on: T1
    refs: R4, R5, R6, R9
T3: Sort every per-dimension list best→worst (code/agent/tools/gen t/s/prompt t/s desc, speed ms asc) including Retired pane lists
    depends_on: T1
    refs: R7
T4: Header chips — models chip dual counts with retired present; task sets chip links board blocks only, text for retired-only signatures
    depends_on: T1
    refs: R10, R11

GATES
python3 -m unittest tests.test_html_report -v (all new pane/sorting/chip cases green)
python3 -m unittest discover -s tests (full suite regression; especially test_report.py and test_run_cli.py)
Render smoke check on a pool containing live+retired rows: single <script> retained, zero external src/href resources, Board pane visible by default with no JS needed to reach it, invariants: at most one <style> block, CSS contains the pure-CSS :checked toggle pattern, tab bar absent entirely when no retired rows exist, retired rows never appear in Board pane or KPI strip/Recommendations, Recommendations appears after KPI strip and before "Weighted global", retired listings sorted best→worst, header shows `<n> models (+<m> retired)` while without retired rows keeps single total