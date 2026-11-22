FILES  
docs/specs/report_polish/requirements.md  
html_report.py  

TASKS  
T1: Implement tab bar logic for board and retired panes  
    depends_on: (none)  
    refs: R1, R2, R3, R10  
T2: Configure Retired pane content exclusion rules  
    depends_on: T1  
    refs: R4, R9  
T3: Compute KPI strip from live rows only  
    depends_on: T1  
    refs: R5, R6  
T4: Order per-dimension lists by performance metrics  
    depends_on: T1  
    refs: R7  
T5: Ensure Board pane does not render retired rows  
    depends_on: T1  
    refs: R8  
T6: Update header "models" chip to show separate counts when retired rows exist  
    depends_on: T1  
    refs: R10  
T7: Restrict "task sets" chip links to active board blocks only  
    depends_on: T1  
    refs: R11  
T8: Validate report self-containment and pure CSS switching  
    depends_on: T1  
    refs: R12  

GATES  
- Verify tab bar renders correctly with both panes when retired rows exist (R1)  
- Confirm Board pane is visible by default without JavaScript (R2)  
- Validate no retired rows are shown in Board pane (R8)  
- Confirm Retired pane excludes Recommendations and KPI strip (R4)  
- Verify KPI strip uses only live row data (R5)  
- Check Recommendations section appears after KPI strip (R6)  
- Validate all dimension lists are sorted correctly (R7)  
- Confirm "models" chip shows correct count format (R10)  
- Ensure "task sets" chip links only to visible board blocks (R11)  
- Test that report works with JavaScript disabled (R12)