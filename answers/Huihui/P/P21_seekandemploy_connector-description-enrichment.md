FILES
src/seekandemploy/connectors/workable.py
src/seekandemploy/connectors/smartrecruiters.py
tests/test_connectors_workable.py
tests/test_connectors_smartrecruiters.py
tests/fixtures/workable/kahoot_jobs.json
tests/fixtures/smartrecruiters/ecovadis_postings.json

TASKS
T1: Implement Workable description enrichment and filtering
    depends_on: (none)
    refs: R1, R2, R3, R6
T2: Implement SmartRecruiters description extraction and error handling
    depends_on: (none)
    refs: R4, R5

GATES
- Run `pytest tests/test_connectors_workable.py -v` to verify Workable logic.
- Run `pytest tests/test_connectors_smartrecruiters.py -v` to verify SmartRecruiters logic.
- Verify that `job_offer.description` is populated for valid payloads in both connectors.
- Verify that closed offers from Workable are not persisted.
- Verify that a single HTTP request is made per source for Workable enrichment.
- Verify that warnings are logged when enrichment or detail fetching fails without aborting the cycle.