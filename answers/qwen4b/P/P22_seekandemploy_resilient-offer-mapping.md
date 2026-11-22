FILES
src/seekandemploy/connectors/base.py
src/seekandemploy/connectors/sync.py
src/seekandemploy/collection.py
src/seekandemploy/repository.py
tests/test_collection.py
tests/test_connectors_base.py
tests/test_connectors_sync.py

TASKS
T1: Implement per-payload error handling in JobConnector.map_offer to skip invalid payloads and continue mapping
    depends_on: (none)
    refs: R1, R4, R5, R6
T2: Add skipped payload tracking to SourceRun and CollectionResult models and expose via properties
    depends_on: T1
    refs: R4, R5, R6, R7
T3: Update sync_source logic to set source status to active when all payloads are skipped
    depends_on: T2
    refs: R3, R7
T4: Propagate ValueError from api_url derivation in connector configuration
    depends_on: T1
    refs: R8
T5: Propagate ValueError from GenericApiConfig or GenericHtmlConfig validation
    depends_on: T1
    refs: R9
T6: Propagate ValueError from JobConnector.parse during offer parsing
    depends_on: T1
    refs: R10
T7: Propagate ConnectorError from transport layer
    depends_on: T1
    refs: R11
T8: Set source status to error on ValueError or ConnectorError in sync_source
    depends_on: T1
    refs: R12
T9: Roll back uncommitted JobOffer changes on sync_source failure
    depends_on: T8
    refs: R13
T10: Log warning for skipped payloads with source name and count
    depends_on: T1
    refs: R14

GATES
- Verify that `map_offer` skips payloads raising `ValueError` and continues processing others (R1)
- Confirm that exactly one `JobOffer` is persisted per successfully mapped payload via `upsert_job_offer` (R2)
- Validate that no source is marked as failed when only per-payload `ValueError`s occur (R3)
- Ensure `SyncResult.skipped`, `SourceRun.skipped`, and `CollectionResult.skipped` fields are correctly populated (R4, R5, R6)
- Test that source status becomes `active` after successful completion with all payloads skipped (R7)
- Confirm that `ValueError` and `ConnectorError` from configuration, parsing, or transport are properly propagated (R8–R11)
- Verify that source status transitions to `error` upon any `ValueError` or `ConnectorError` during `sync_source` (R12)
- Validate that all uncommitted `JobOffer` changes are rolled back on error (R13)
- Check that a warning log entry is generated for each source with skipped payload count (R14)