FILES
src/seekandemploy/collection.py
src/seekandemploy/connectors/sync.py
src/seekandemploy/web/catalogs.py
tests/test_collect.py
tests/test_connectors_sync.py

TASKS
T1: Update Result models to include `skipped` fields
    depends_on: (none)
    refs: R4, R5, R6
T2: Implement error handling in `JobConnector.sync_source` to skip `ValueError` during mapping
    depends_on: T1
    refs: R1, R2, R3, R7, R14
T3: Implement error propagation for critical `ValueError` and `ConnectorError` types
    depends_on: T2
    refs: R8, R9, R10, R11, R12, R13
T4: Integrate skipped count into `SyncResult`, `SourceRun`, and `CollectionResult`
    depends_on: T1, T2
    refs: R4, R5, R6
T5: Add translation keys for skipped payload warnings
    depends_on: T4
    refs: R14
T6: Add unit and integration tests for resilient mapping and error propagation
    depends_on: T3
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14

GATES
- Verify that a single `ValueError` in `map_offer` does not stop the sync loop.
- Verify that `upsert_job_offer` is called exactly once per successful map.
- Verify that `api_url` derivation errors or `parse` errors propagate and set source to `error`.
- Verify that `ConnectorError` propagates and triggers database rollback/source error status.
- Verify that `skipped` counts are correctly aggregated from `SyncResult` -> `SourceRun` -> `CollectionResult`.
- Verify that a source with only skipped payloads remains `active`.
- Verify that a warning log is emitted when payloads are skipped.