FILES
src/seekandemploy/connectors/workable.py
src/seekandemploy/connectors/smartrecruiters.py
tests/fixtures/workable/kahoot_jobs.json
tests/fixtures/smartrecruiters/ecovadis_postings.json
tests/test_connectors_workable.py
tests/test_connectors_smartrecruiters.py

TASKS
T1: Add enrichment request support + filtering in Workable connector — persist non-empty descriptions keyed off published shortcodes only; at most one enrichment call per source/cycle; skip closed offers from payload v1 (no `job_offer` entries)
    depends_on: (none)
    refs: R1, R2, R6
T2: Harden Workable enrichment failure handling — on enrichment request failure, still complete the cycle with all offers intact (descriptions NULL), log a warning, and do not abort remaining sources
    depends_on: T1
    refs: R3
T3: Persist SmartRecruiters description from jobAd.sections.jobDescription.text for synced postings
    depends_on: (none)
    refs: R4
T4: Handle SmartRecruiters posting detail failure — save the offer without description, log a warning, continue with remaining postings in the source
    depends_on: T3
    refs: R5
T5: Tests + fixtures covering both connectors' happy paths, enrichment limits, failures and degraded modes
    depends_on: T1, T2, T3, T4
    refs: R1, R2, R3, R4, R5, R6

GATES
pytest tests/test_connectors_workable.py tests/test_connectors_smartrecruiters.py -v
pytest tests/test_collection.py tests/test_collect.py tests/integration/ -k "workable or smartrecruiter" -v
ruff check src/seekandemploy/connectors/workable.py src/seekandemploy/connectors/smartrecruiters.py && ruff format --check src/seekandemploy/connectors/workable.py src/seekandemploy/connectors/smartrecruiters.py
full pytest suite green; confirm no closed Workable offers appear in job_offer for a cycled run