FILES
src/seekandemploy/connectors/sync.py
src/seekandemploy/collection.py
tests/test_connectors_sync.py
tests/test_collection.py

TASKS
T1: Update `sync_source` to handle per-payload mapping errors
    depends_on: (none)
    refs: R1, R2, R3, R4, R7, R8, R9, R10, R11, R12, R13, R14
T2: Expose skipped counts in collection results
    depends_on: T1
    refs: R5, R6
T3: Implement verification tests for resilient mapping and result exposure
    depends_on: T1, T2
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14

GATES
- Run unit tests for `sync_source` verifying that `ValueError` from `map_offer` skips payloads without failing the source, while other `ValueError`s propagate.
- Verify that `SyncResult.skipped` correctly reflects the number of skipped payloads.
- Confirm that `SourceRun.skipped` and `CollectionResult.skipped` aggregate skipped counts accurately across sources.
- Ensure that when all payloads are skipped, the source status is set to `active`.
- Validate that `ConnectorError` and specific `ValueError`s (api_url derivation, config validation, parse) propagate out of `sync_source` and mark the source as `error`, rolling back changes.
- Check logging output for warnings with correct placeholders when payloads are skipped.