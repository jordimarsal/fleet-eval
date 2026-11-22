FILES
src/seekandemploy/connectors/sync.py
src/seekandemploy/collection.py
tests/test_connectors_sync.py
tests/test_collection.py

TASKS
T1: Skip unmappable payloads inside the mapping loop
    depends_on: (none)
    refs: R1
T2: Persist one JobOffer per mapped payload and expose skipped on SyncResult
    depends_on: T1
    refs: R2, R4
T3: Propagate non-per-payload failures from sync_source and roll back on them
    depends_on: T2
    refs: R8, R9, R10, R11, R12, R13
T4: Keep skip-only outcomes successful, active, and log the warning
    depends_on: T2
    refs: R3, R7, R14
T5: Carry skipped counts through SourceRun and CollectionResult
    depends_on: T2
    refs: R5, R6
T6: Extend the connector and collection test suites for every requirement
    depends_on: T3, T4, T5
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14

GATES
pytest tests/test_connectors_sync.py -v
pytest tests/test_collection.py -v
ruff check src/seekandemploy/connectors/sync.py src/seekandemploy/collection.py tests/test_connectors_sync.py tests/test_collection.py
python -m pytest tests/ -q (full suite; must stay green)