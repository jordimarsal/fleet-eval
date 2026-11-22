FILES
html_report.py
report.py

TASKS
T1: Implement tab bar logic based on retired rows presence
    depends_on: (none)
    refs: R1, R3, R10
T2: Configure Board pane rendering with default visibility
    depends_on: T1
    refs: R1, R2
T3: Exclude Recommendations and KPI strip from Retired pane
    depends_on: T1
    refs: R4, R5
T4: Ensure KPI strip computes only from live rows
    depends_on: T3
    refs: R5
T5: Order per-dimension lists by performance metrics
    depends_on: T1
    refs: R7
T6: Prevent Board pane from rendering retired rows
    depends_on: T1
    refs: R8
T7: Add retired record status text to Retired pane
    depends_on: T1
    refs: R9
T8: Update header "models" chip count display for retired rows
    depends_on: T1
    refs: R10
T9: Restrict "task sets" chip links to Board pane only
    depends_on: T1
    refs: R11
T10: Verify self-contained report with pure CSS tab switching
    depends_on: T1
    refs: R12

GATES
- Visual inspection of report output showing correct tab behavior (Board visible by default)
- Manual validation that Retired pane lacks Recommendations and KPI strip
- Verification that KPI values derive solely from live rows in test data
- Confirmation that all dimension lists are sorted correctly (best to worst) 
- Check that retired models appear grayed out and labeled as records
- Validation that the "models" header shows both live and retired counts when applicable
- Test that task set links only exist in Board pane, not in Retired pane
- Confirm no external resources or JavaScript required for tab switching