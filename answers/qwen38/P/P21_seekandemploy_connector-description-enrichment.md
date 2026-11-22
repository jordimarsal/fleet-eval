FILES
src/seekandemploy/connectors/workable.py
src/seekandemploy/connectors/smartrecruiters.py
tests/test_connectors_workable.py
tests/test_connectors_smartrecruiters.py
tests/fixtures/workable/kahoot_jobs.json
tests/fixtures/smartrecruiters/ecovadis_postings.json

TASKS
T1: Implement Workable enrichment logic and description persistence
    depends_on: (none)
    refs: R1, R2, R3, R6
T2: Implement SmartRecruiters detail fetching and error handling
    depends_on: (none)
    refs: R4, R5
T3: Update test fixtures and add unit tests for new behaviors
    depends_on: T1, T2
    refs: R1, R2, R3, R4, R5, R6

GATES
- Run `pytest tests/test_connectors_workable.py` to verify Workable enrichment, single-request constraint, failure resilience, and closed-offer exclusion.
- Run `pytest tests/test_connectors_smartrecruiters.py` to verify SmartRecruiters description extraction and failure resilience.
- Run full test suite (`pytest`) to ensure no regressions in other connectors or collection logic.