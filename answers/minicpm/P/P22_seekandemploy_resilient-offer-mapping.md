FILES
src/seekandemploy/collection.py
src/seekandemploy/connectors/sync.py
src/seekandemploy/models.py
tests/test_collection.py
tests/test_connectors_sync.py

TASKS
T1: Update `CollectionResult`, `SourceRun`, and `SyncResult` models to include `skipped` fields.
    depends_on: (none)
    refs: R4, R5, R6
T2: Modify `sync_source` to wrap `JobConnector.map_offer` calls in try/except for `ValueError`, skipping failed payloads and counting them.
    depends_on: T1
    refs: R1
T3: Ensure `upsert_job_offer` is called exactly once per successfully mapped payload in `sync_source`.
    depends_on: T1, T2
    refs: R2
T4: Update source status logic in `sync_source` to set status to `active` even if all payloads were skipped, unless a critical error occurs.
    depends_on: T2
    refs: R3, R7
T5: Propagate `ValueError` from `api_url` derivation, config validation, and `parse` methods out of `sync_source`.
    depends_on: (none)
    refs: R8, R9, R10
T6: Propagate `ConnectorError` from the transport layer out of `sync_source`.
    depends_on: (none)
    refs: R11
T7: Implement error handling in `sync_source` to set source status to `error` and rollback uncommitted `JobOffer` changes on `ValueError` or `ConnectorError`.
    depends_on: T2
    refs: R12, R13
T8: Add logging warning when payloads are skipped, naming the source and reporting the count.
    depends_on: T2
    refs: R14
T9: Write/update tests to verify skipping behavior, status updates, error propagation, and result counting.
    depends_on: T1, T2, T3, T4, T5, T6, T7, T8
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14

GATES
- All unit tests in `tests/test_collection.py` and `tests/test_connectors_sync.py` pass.
- Integration test verifying that a source with only mapping failures remains `active` passes.
- Integration test verifying that `SyncResult`, `SourceRun`, and `CollectionResult` correctly report `skipped` counts passes.
- Manual review of error propagation paths for `api_url`, config validation, and `parse` methods.