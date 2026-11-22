FILES
src/seekandemploy/connectors/sync.py
src/seekandemploy/collection.py
tests/test_connectors_sync.py
tests/test_collection.py

TASKS
T1: make sync_source resilient to per-payload map_offer failures and propagate hard errors with correct status/rollback handling
    depends_on: (none)
    refs: R1, R8, R9, R10, R11, R12, R13, R14
T2: expose skipped counts through SyncResult, SourceRun, and CollectionResult.skipped; keep active status when all payloads are skipped
    depends_on: T1
    refs: R2, R3, R4, R5, R6, R7
T3: add regression tests covering skip behavior, error propagation, rollback, logging, and aggregate counters
    depends_on: T1, T2
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14

GATES
pytest tests/test_connectors_sync.py tests/test_collection.py -v
pytest -q (full suite)
ruff check src tests / mypy or project lint command from Makefile if configured
confirm no source is marked failed after only per-payload ValueErrors and that every successful payload yields one upsert_job_offer