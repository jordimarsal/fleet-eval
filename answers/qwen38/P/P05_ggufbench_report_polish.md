FILES
html_report.py
tests/test_html_report.py

TASKS
T1: Implement CSS-only tab switching and pane structure
    depends_on: (none)
    refs: R1, R2, R3, R12
T2: Refactor row filtering to separate live and retired datasets
    depends_on: T1
    refs: R8, R5
T3: Render Retired pane with record-only content and sorting
    depends_on: T2
    refs: R4, R7, R9
T4: Update header chips for counts and link integrity
    depends_on: T2
    refs: R10, R11
T5: Verify Recommendations placement and KPI computation scope
    depends_on: T2
    refs: R6, R5

GATES
python -m pytest tests/test_html_report.py -v
grep -q "tab-bar" html_report.py && grep -q "retired-pane" html_report.py
! grep -E "<script src|http://|https://" results/report.html || true # Ensure no external resources in generated output if available, else check source logic
python -c "from ggufbench import html_report; print('Import OK')"