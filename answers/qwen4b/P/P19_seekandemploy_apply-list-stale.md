FILES
src/seekandemploy/cli.py
src/seekandemploy/repository.py
harness/specs/application-tracking/tasks.md
harness/specs/application-tracking/requirements.md

TASKS
T1: Implement --stale DAYS flag parsing and validation
    depends_on: (none)
    refs: R1, R3, R4
T2: Compute stale applications based on last event timestamp
    depends_on: T1
    refs: R1, R3, R5
T3: Generate output with live/stale counts and application list
    depends_on: T2
    refs: R1, R2, R5
T4: Enforce exclusion of rejected/withdrawn applications
    depends_on: T3
    refs: R4, R5
T5: Add compatibility check between --stale and --all flags
    depends_on: T4
    refs: R4

GATES
- Verify that `apply list --stale DAYS` lists only open applications with more than DAYS days since last event (R1)
- Confirm that the output includes correct stale/live counts (`stale: X of N open applications`, `live: Y`) (R2)
- Validate that the rellotge resets upon new events (e.g., note) (R3)
- Ensure no mutations occur in state or logs (R5)
- Test that rejected/withdrawn apps are excluded from both list and count (R4)
- Confirm error is raised when --stale and --all are used together (R4)