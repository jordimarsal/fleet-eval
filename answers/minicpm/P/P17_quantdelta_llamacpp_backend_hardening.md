FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/manifest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_backend.py
tests/unit/backends/llamacpp/test_stub_server.py

TASKS
T1: Harden `/metrics` parser to accept all Prometheus numeric formats and OpenMetrics timestamps
    depends_on: (none)
    refs: R1, R2
T2: Update `/metrics` parser to handle escaped quotes and braces in label values
    depends_on: T1
    refs: R3
T3: Enforce `LlamaCppMalformedResponseError` on any remaining exposition format violations
    depends_on: T2
    refs: R4
T4: Refactor memory recognition logic to use only `_bytes` suffix heuristic
    depends_on: (none)
    refs: R5
T5: Implement `manifest()` caching for artifact sha256 while resolving `engine_version` dynamically
    depends_on: (none)
    refs: R6
T6: Add thread-safety locks to `LlamaCppBackend` for concurrent `run()`, `metrics()`, and `manifest()` calls
    depends_on: T5
    refs: R7
T7: Validate `base_url` in `LlamaCppConfig` using `urllib.parse` with strict rules
    depends_on: (none)
    refs: R8
T8: Update chat completion handling to record `length` finish_reason and empty content as success
    depends_on: (none)
    refs: R9
T9: Document and test the amended R29 scope regarding configuration vs. adapter constants
    depends_on: (none)
    refs: R10
T10: Implement concurrency test stub with backlog 512 and 300-run/64-thread deterministic test
    depends_on: T6
    refs: R11

GATES
- Run `pytest tests/unit/backends/llamacpp/test_metrics.py` to verify parser improvements (R1-R4).
- Run `pytest tests/unit/backends/llamacpp/test_config.py` to verify `base_url` validation (R8).
- Run `pytest tests/unit/backends/llamacpp/test_manifest.py` to verify caching and fingerprint logic (R6).
- Run `pytest tests/unit/backends/llamacpp/test_backend.py` to verify thread-safety and memory recognition (R5, R7).
- Run `pytest tests/unit/backends/llamacpp/test_stub_server.py` and new concurrency test to verify zero lost updates and tokens_per_second ratio (R11).
- Verify that `finish_reason == "length"` cases are recorded as successes in integration/smoke tests (R9).
- Confirm documentation updates for R29 scope and adapter design (R10).