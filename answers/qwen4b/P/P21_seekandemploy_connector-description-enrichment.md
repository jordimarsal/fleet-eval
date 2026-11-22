FILES
src/seekandemploy/connectors/workable.py
src/seekandemploy/connectors/smartrecruiters.py
src/seekandemploy/extraction/__init__.py
src/seekandemploy/models.py
tests/test_connectors_workable.py
tests/test_connectors_smartrecruiters.py

TASKS
T1: Implement Workable connector to extract and persist job descriptions from enriquiment v1 payload
    depends_on: (none)
    refs: R1, R3
T2: Implement SmartRecruiters connector to extract description from `jobAd.sections.jobDescription.text`
    depends_on: (none)
    refs: R4, R5
T3: Ensure Workable connector limits enriquiment requests per source and cycle
    depends_on: T1
    refs: R2
T4: Handle failed Workable enrichment requests by preserving existing offers with NULL descriptions
    depends_on: T1
    refs: R3
T5: Handle failed SmartRecruiters job details by saving offer with NULL description and logging warning
    depends_on: T2
    refs: R5
T6: Validate that only active, non-closed offers from Workable payload are persisted in job_offer table
    depends_on: T1
    refs: R6

GATES
- Verify that all Workable and SmartRecruiters job descriptions are correctly extracted and stored in the database via integration test coverage.
- Confirm that no more than one enrichment request is made per source and cycle using a mock environment.
- Validate failure resilience: ensure that partial failures do not block processing of other sources or offers.
- Check that closed/offered jobs from Workable are excluded from `job_offer` persistence.
- Ensure audit logs contain warnings for failed enrichment attempts.