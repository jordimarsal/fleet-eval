FILES
src/seekandemploy/connectors/smartrecruiters.py
src/seekandemploy/connectors/workable.py
src/seekandemploy/collection.py
tests/test_connectors_smartrecruiters.py
tests/test_connectors_workable.py
tests/test_collection.py

TASKS
T1: Update Workable connector to handle enrichment payload and single-request logic
    depends_on: (none)
    refs: R1, R2, R3, R6
T2: Update SmartRecruiters connector to extract job description from posting detail
    depends_on: (none)
    refs: R4, R5
T3: Update collection runner to persist descriptions and handle partial failures gracefully
    depends_on: T1, T2
    refs: R1, R3, R4, R5

GATES
- Unit tests for Workable connector verify that only one enrichment request is made per cycle (R2).
- Unit tests for Workable connector verify that closed offers in payload v1 are not persisted (R6).
- Unit tests for SmartRecruiters connector verify correct extraction of `jobAd.sections.jobDescription.text` (R4).
- Integration tests verify that a failed Workable enrichment results in NULL descriptions but continues the cycle (R3).
- Integration tests verify that a failed SmartRecruiters detail fetch results in an offer without description but continues the cycle (R5).
- End-to-end test verifies that non-empty descriptions are correctly stored in the database for both connectors (R1).