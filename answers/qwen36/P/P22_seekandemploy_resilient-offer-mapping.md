FILES
src/seekandemploy/collection.py
src/seekandemploy/connectors/base.py
src/seekandemploy/connectors/sync.py
tests/test_collection.py
tests/test_connectors_sync.py

TASKS
T1: Add `skipped` field to `SourceRun` dataclass in collection module
    depends_on: (none)
    refs: R5
T2: Add `skipped` property to `CollectionResult` that sums per-source skipped counts
    depends_on: T1
    refs: R6
T3: Modify `sync_source` to catch `ValueError` from `JobConnector.map_offer`, skip payload, increment counter, and continue
    depends_on: (none)
    refs: R1
T4: Wire up `skipped` count into `SourceRun` construction within `sync_source`
    depends_on: T3
    refs: R5
T5: Propagate `ValueError` from api_url derivation, config validation, parse, and transport errors out of `sync_source`
    depends_on: (none)
    refs: R8, R9, R10, R11
T6: Set source status to `active` when `sync_source` returns normally (including all-skipped case), else set to `error`
    depends_on: T5
    refs: R7, R12
T7: Roll back uncommitted `JobOffer` changes on `ValueError` or `ConnectorError` during `sync_source`
    depends_on: T5
    refs: R13
T8: Persist exactly one `JobOffer` per successfully mapped payload via `upsert_job_offer` in `sync_source`
    depends_on: T3
    refs: R2
T9: Log a warning naming the source and reporting skipped count using `%s` placeholders when at least one payload is skipped
    depends_on: T4
    refs: R14
T10: Write tests verifying skip behavior, status transitions, rollback, upsert counts, logging, and error propagation
    depends_on: T1, T2, T3, T4, T5, T6, T7, T8, T9
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14

GATES
- All unit tests pass (pytest) including new tests for skip logic, status handling, rollback, and error propagation.
- Integration test with real connector fixtures confirms that mapping failures do not mark source as failed and offers are persisted correctly.
- Logging verification: emitted warning contains source name and skipped count formatted with `%s`.
- Database state check after simulated failure: no partial JobOffer records remain; source status is `error`.
- CollectionResult.skipped property returns correct aggregate across multiple sources.