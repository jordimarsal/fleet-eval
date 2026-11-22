FILES
html_report.py
tests/test_html_report.py

TASKS
T1: Update report data structures to separate live and retired rows
    depends_on: (none)
    refs: R1, R3, R8
T2: Implement KPI strip calculation using only live rows
    depends_on: T1
    refs: R5
T3: Implement Recommendations section placement logic
    depends_on: T1
    refs: R4, R6
T4: Implement sorting logic for all dimension lists (descending vs ascending)
    depends_on: T1
    refs: R7
T5: Implement CSS-only tab bar and pane switching mechanism
    depends_on: T1
    refs: R1, R2, R12
T6: Implement header chip logic for model counts (split vs single)
    depends_on: T1
    refs: R10
T7: Implement task set link safety (text-only for retired signatures)
    depends_on: T1
    refs: R11
T8: Add Retired pane content (record notice and specific exclusions)
    depends_on: T1
    refs: R4, R9
T9: Finalize HTML template with integrated styles and structure
    depends_on: T5, T6, T7, T8
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

GATES
- Verify report renders a single pane when no retired rows exist.
- Verify report renders two switchable panes via CSS (no JS required) when retired rows exist.
- Verify KPI strip values match CLI output using only live models.
- Verify "Board" pane contains zero retired rows.
- Verify "Retired" pane contains the record-only disclaimer and lacks Recommendations/KPIs.
- Verify all dimension lists are correctly sorted (latency ascending, others descending).
- Verify model count chip displays `X models (+Y retired)` format correctly.
- Verify task set links in the Retired pane are plain text if they don't exist in Board.