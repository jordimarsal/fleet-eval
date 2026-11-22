FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/errors.py
src/quantdelta/backends/llamacpp/manifest.py
docs/architecture.md
tests/unit/backends/llamacpp/test_backend.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_run.py
tests/unit/backends/llamacpp/test_stub_server.py

TASKS
T1: Update LlamaCppConfig with strict URL validation
    depends_on: (none)
    refs: R8
T2: Enhance metrics parser for Prometheus/OpenMetrics compliance and error reporting
    depends_on: (none)
    refs: R1, R2, R3, R4
T3: Refactor memory recognition logic in backend
    depends_on: T2
    refs: R5
T4: Implement thread-safe manifest caching and engine version resolution
    depends_on: (none)
    refs: R6, R7
T5: Update chat completion success criteria and documentation
    depends_on: (none)
    refs: R9, R10
T6: Implement high-concurrency stress test and stub server hardening
    depends_on: T1, T4, T5
    refs: R11
T7: Finalize adapter design documentation regarding truncation
    depends_on: T5
    refs: R9

GATES
- Unit tests for `LlamaCppConfig` pass all URL edge cases (R8).
- Metrics parser unit tests cover scientific notation, special tokens, timestamps, and escaped quotes (R1, R2, R3, R4).
- Memory recognition tests verify only `_bytes` suffix is used and non-finite values are ignored (R5).
- Manifest cache tests verify single hash computation and dynamic engine versioning (R6).
- Concurrency test passes 300 runs with 64 threads showing zero lost updates and exact TPS ratio (R7, R11).
- Stub server test verifies listen backlog of 512 (R11).
- Documentation updated to reflect amended R29 scope and truncation responsibilities (R9, R10).