FILES
src/seekandemploy/connectors/sync.py
src/seekandemploy/collection.py
tests/test_connectors_sync.py
tests/test_collection.py

TASKS
T1: Update SyncResult dataclass to include skipped field
    depends_on: (none)
    refs: R4
T2: Implement resilient mapping logic in sync_source
    depends_on: T1
    refs: R1, R2, R3, R7, R8, R9, R10, R11, R14
T3: Update SourceRun and CollectionResult to expose skipped counts
    depends_on: T2
    refs: R5, R6
T4: Add tests for resilient mapping behavior
    depends_on: T2, T3
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14

GATES
- Run `pytest tests/test_connectors_sync.py -v` to verify all sync source behaviors including error handling and skip counting.
- Run `pytest tests/test_collection.py -v` to verify collection result aggregation of skipped payloads.
- Verify that no new linter errors are introduced by running the project's standard linting tools on modified files.