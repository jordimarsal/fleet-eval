FILES
src/seekandemploy/connectors/workable.py
src/seekandemploy/connectors/smartrecruiters.py
src/seekandemploy/repository.py
tests/test_connectors_workable.py
tests/test_connectors_smartrecruiters.py

TASKS
T1: Add enrichment endpoint and batch logic to Workable connector
    depends_on: (none)
    refs: R2
T2: Persist enriched descriptions in Workable sync cycle
    depends_on: T1
    refs: R1
T3: Handle Workable enrichment failure gracefully
    depends_on: T2
    refs: R3
T4: Filter closed offers from Workable payload before persistence
    depends_on: T2
    refs: R6
T5: Implement SmartRecruiters description extraction from job detail
    depends_on: (none)
    refs: R4
T6: Handle SmartRecruiters detail fetch failure gracefully
    depends_on: T5
    refs: R5
T7: Run integration tests for Workable and SmartRecruiters connectors
    depends_on: T3, T6
    refs: R1, R2, R3, R4, R5, R6

GATES
- Unit tests pass for `test_connectors_workable` and `test_connectors_smartrecruiters`.
- Integration test verifies that a single HTTP request is made per Workable source cycle.
- Integration test verifies that failed enrichment results in NULL description but successful save.
- Integration test verifies that SmartRecruiters offers with failed details are saved without description.
- Database schema migration includes `description` column on `job_offer` table.