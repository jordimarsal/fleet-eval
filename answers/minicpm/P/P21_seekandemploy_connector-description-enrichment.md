FILES
src/seekandemploy/connectors/workable.py
src/seekandemploy/connectors/smartrecruiters.py
src/seekandemploy/repository.py
src/seekandemploy/models.py
tests/test_connectors_workable.py
tests/test_connectors_smartrecruiters.py

TASKS
T1: Implement Workable enrichment payload handling and persistence
    depends_on: (none)
    refs: R1, R2, R6
T2: Implement Workable failure resilience and warning logging
    depends_on: T1
    refs: R3
T3: Implement SmartRecruiters description extraction from job detail
    depends_on: (none)
    refs: R4
T4: Implement SmartRecruiters failure resilience and partial save
    depends_on: T3
    refs: R5

GATES
- Verify that Workable syncs persist non-empty descriptions for offers present in the v1 enrichment payload shortcode.
- Verify that only one enrichment request is made per source per Workable cycle, regardless of offer count.
- Verify that Workable enrichment failures log a warning and complete the cycle with NULL descriptions without aborting other sources.
- Verify that SmartRecruiters offers persist the description from `jobAd.sections.jobDescription.text`.
- Verify that SmartRecruiters detail fetch failures save the offer without a description, log a warning, and continue processing other offers.
- Verify that no offers are added to the catalog if they are not reported by the authoritative Workable list payload (closed offers excluded).