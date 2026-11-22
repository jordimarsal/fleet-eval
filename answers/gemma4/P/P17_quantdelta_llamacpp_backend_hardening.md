FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/manifest.py
tests/unit/backends/llamacpp/test_backend.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_run.py
tests/unit/backends/llamacpp/test_stub_server.py

TASKS
T1: Update metrics parser regex and logic for Prometheus compliance
    depends_on: (none)
    refs: R1, R2, R3, R4
T2: Refactor memory recognition heuristic to use suffix-only matching
    depends_on: T1
    refs: R5
T3: Implement thread-safe manifest caching with dynamic engine version resolution
    depends_on: (none)
    refs: R6, R7
T4: Harden LlamaCppConfig URL validation using urllib.parse
    depends_on: (none)
    refs: R8
T5: Adjust chat completion success criteria for length/empty content cases
    depends_on: (none)
    refs: R9
T6: Document and test adapter scope constraints (host/port/model from config only)
    depends_on: T4
    refs: R10
T7: Enhance test stub backlog and implement high-concurrency stress test
    depends_on: T3, T5
    refs: R11

GATES
- Unit tests for `_parse_exposition_samples` covering all numeric formats (scientific, NaN, Inf), timestamps, and complex label strings.
- Unit tests for `LlamaCppConfig` validating various malformed and valid URLs.
- Unit tests for `manifest()` verifying artifact hash is cached while `engine_version` updates dynamically.
- Concurrency test passing: 300 runs across 64 threads with zero lost updates and exact token math.
- Verification that memory recognition fails on non-`_bytes` suffixes.