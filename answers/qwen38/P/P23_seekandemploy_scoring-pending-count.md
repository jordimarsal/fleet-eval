FILES
src/seekandemploy/repository.py
src/seekandemploy/web/routes_scoring.py
src/seekandemploy/web/catalogs.py
tests/test_repository.py
tests/test_web_scoring_progress.py

TASKS
T1: Implement `count_unscored_matches` in repository
    depends_on: (none)
    refs: R1, R2
T2: Add localized strings for pending and up-to-date states
    depends_on: (none)
    refs: R13, R14, R16
T3: Update scoring progress fragment logic to derive idle state from DB
    depends_on: T1, T2
    refs: R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R15
T4: Write tests for repository function
    depends_on: T1
    refs: R1, R2
T5: Write tests for updated scoring progress fragment
    depends_on: T3
    refs: R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R15

GATES
- Run unit tests for `repository.count_unscored_matches` to verify signature and count accuracy.
- Run integration/web tests for `/scoring/progress` to verify HTML output for running, idle-pending, and idle-up-to-date states in both English and Spanish.
- Verify that no database migrations are added or modified.