FILES
src/seekandemploy/connectors/workable.py
src/seekandemploy/connectors/smartrecruiters.py
src/seekandemploy/models.py
src/seekandemploy/repository.py
tests/test_connectors_workable.py
tests/test_connectors_smartrecruiters.py

TASKS
T1: Add `description` column to JobOffer model and migration
    depends_on: (none)
    refs: R1, R4
T2: Workable enricher — single API call per source cycle for descriptions
    depends_on: T1
    refs: R1, R2
T3: SmartRecruiters enricher — fetch job description from posting detail
    depends_on: T1
    refs: R4
T4: Workable resilience — fail gracefully on enrichment failure
    depends_on: T2
    refs: R3
T5: SmartRecruiters resilience — fail gracefully on detail fetch failure
    depends_on: T3
    refs: R5
T6: Workable filter — exclude closed offers not in authoritative listing
    depends_on: T1
    refs: R6

GATES
- pytest tests/test_connectors_workable.py::test_enrichment_single_call_per_source_cycle
- pytest tests/test_connectors_workable.py::test_failed_enrichment_preserves_listing_with_null_descriptions_and_warning
- pytest tests/test_connectors_workable.py::test_closed_offers_excluded_from_catalog
- pytest tests/test_connectors_smartrecruiters.py::test_description_extracted_from_jobAd_sections_jobDescription_text
- pytest tests/test_connectors_smartrecruiters.py::test_failed_detail_fetch_saves_offer_without_description_and_continues
- pytest tests/test_connectors_workable.py::test_non_empty_description_persisted_for_published_offers
- pytest tests/test_connectors_smartrecruiters.py::test_description_persisted_when_present