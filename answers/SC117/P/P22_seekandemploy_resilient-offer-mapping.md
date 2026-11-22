FILES
src/seekandemploy/collection.py
src/seekandemploy/connectors/base.py
src/seekandemploy/connectors/sync.py
tests/test_collection.py

TASKS
T1: Add `skipped` field to `SourceRun` model
    depends_on: (none)
    refs: R5
T2: Add `skipped` property to `CollectionResult` model
    depends_on: T1
    refs: R6
T3: Implement per-payload error handling in `sync_source`
    depends_on: (none)
    refs: R1, R8, R9, R10, R11
T4: Update `upsert_job_offer` logic and transaction rollback behavior
    depends_on: T3
    refs: R2, R13
T5: Update source status logic in collection runner
    depends_on: T3
    refs: R3, R7, R12
T6: Add warning logging for skipped payloads
    depends_on: T3
    refs: R14
T7: Wire up `skipped` counts from connector sync to `SourceRun`
    depends_on: T4, T5, T6
    refs: R4, R5
T8: Write unit tests for resilient mapping and status updates
    depends_on: T7
    refs: R1, R2, R3, R4, R5, R7, R8, R9, R10, R11, R12, R13, R14

GATES
- Unit tests pass (`pytest tests/test_collection.py tests/test_connectors_sync.py`) covering all requirements.
- Integration test verifies that a source with mixed valid/invalid payloads ends as `active` with correct skip count.
- Integration test verifies that a source with only invalid payloads (ValueError) ends as `active`.
- Integration test verifies that a source with transport/config errors ends as `error`.
- Log output verification confirms the specific warning message format when skips occur.