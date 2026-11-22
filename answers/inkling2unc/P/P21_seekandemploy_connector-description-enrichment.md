FILES
src/seekandemploy/connectors/workable.py
src/seekandemploy/connectors/smartrecruiters.py
src/seekandemploy/collection.py
src/seekandemploy/collect.py
tests/test_connectors_workable.py
tests/test_connectors_smartrecruiters.py
tests/test_collection.py
tests/fixtures/workable/kahoot_jobs.json
tests/fixtures/smartrecruiters/ecovadis_postings.json

TASKS
T1: Workable enrichment — one request per source/cycle, map shortcodes to descriptions, persist non-empty description per published offer; exclude closed offers not in listing or absent from authoritative payload (never enter job_offer)
    depends_on: (none)
    refs: R1, R2, R6
T2: Workable failure handling — on enrichment HTTP error complete cycle with intact listing, NULL descriptions, log warning, continue remaining sources
    depends_on: T1
    refs: R3
T3: SmartRecruiters detail fetch — extract jobAd.sections.jobDescription.text and persist on the saved offer
    depends_on: (none)
    refs: R4
T4: SmartRecruiters failure tolerance — failed detail leaves offer without description, logs warning, continues with the rest of the source's offers
    depends_on: T3
    refs: R5
T5: Extend fixtures and unit tests for both connectors covering success path, failure path, single-request guarantee, closed-offer exclusion, and cross-source persistence behavior
    depends_on: T2, T4
    refs: R1, R2, R3, R4, R5, R6

GATES
1. python -m pytest tests/test_connectors_workable.py tests/test_connectors_smartrecruiters.py tests/test_collection.py -q — all pass (new + regression)
2. Full suite: python -m pytest tests/ -q excluding live integration tests (integration requires env) — no failures, including existing Workable/SmartRecruiters connector and collection-runner coverage
3. Verify at runtime count: mock transport records exactly one enrichment HTTP request per Workable source per cycle; enrichments-run against fixture set twice shows descriptions persisted only for shortcodes reported in listing payload v1 and job_offer rows contain no closed/unlisted offers
4. Log capture check: simulated SmartRecruiters/Workable detail or enrichment failure produces a warning record naming the affected offer/source while sibling offers still persist with their data intact
5. ruff / line-length and repo lint gate (if configured via Makefile targets) clean on modified files