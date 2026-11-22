FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/manifest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_run.py
tests/unit/backends/llamacpp/conftest.py
docs/architecture.md

TASKS
T1: Harden Prometheus parser for numeric and label edge cases
    depends_on: (none)
    refs: R1, R2, R3, R4
T2: Refactor memory recognition to strict `_bytes` suffix
    depends_on: T1
    refs: R5
T3: Implement `base_url` validation in `LlamaCppConfig`
    depends_on: (none)
    refs: R8
T4: Update `run()` logic for truncation handling
    depends_on: (none)
    refs: R9
T5: Implement manifest caching with dynamic fingerprint resolution
    depends_on: (none)
    refs: R6
T6: Add thread-safety locks to `LlamaCppBackend`
    depends_on: T5
    refs: R7
T7: Document adapter scope and update tests for concurrency
    depends_on: T6
    refs: R10, R11

GATES
- Run unit tests for metrics parsing (`test_metrics.py`) covering scientific notation, special tokens, timestamps, and escaped labels.
- Verify memory recognition ignores non-`_bytes` metrics and handles negative/non-finite values correctly.
- Execute configuration validation tests ensuring `base_url` normalization and rejection of invalid schemes/ports/userinfo.
- Confirm `manifest()` caches SHA256 but updates `engine_version` on subsequent calls without re-hashing.
- Run the 300-run, 64-thread concurrency test against a stub server with backlog >= 512 to verify zero lost updates and exact TPS ratio.
- Validate that `finish_reason == "length"` or empty content results in success status with correct token counts.