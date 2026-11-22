FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/errors.py
src/quantdelta/backends/llamacpp/manifest.py
tests/unit/backends/llamacpp/test_backend.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_stub_server.py

TASKS
T1: Harden /metrics parser to accept all Prometheus numeric values and OpenMetrics timestamps
    depends_on: (none)
    refs: R1, R2
T2: Extend label-value parsing in _SAMPLE_LINE_RE to handle braces inside quotes and escaped quotes
    depends_on: T1
    refs: R3
T3: Raise LlamaCppMalformedResponseError with offending line on parse failure
    depends_on: T2
    refs: R4
T4: Rewrite memory recognition logic to use only `_bytes` suffixes; remove "memory" substring heuristic
    depends_on: T3
    refs: R5
T5: Implement manifest() caching of artifact sha256 while resolving engine_version fresh each call
    depends_on: (none)
    refs: R6
T6: Add threading lock around successful-run counters, fingerprint, and artifact hash cache in LlamaCppBackend
    depends_on: T5
    refs: R7
T7: Validate base_url in LlamaCppConfig using urllib.parse with the specified constraints
    depends_on: (none)
    refs: R8
T8: Document truncation handling responsibility for finish_reason == "length" or empty content
    depends_on: (none)
    refs: R9
T9: Update docstrings/constants to document amended R29 scope (host/port/model from config, route/sampling as constants)
    depends_on: T8
    refs: R10
T10: Write concurrency test stub with backlog >= 512 and 300-run/64-thread suite verifying zero lost updates and exact tokens_per_second ratio
    depends_on: T6
    refs: R11

GATES
- `pytest tests/unit/backends/llamacpp/test_metrics.py` passes all new parser tests including NaN/+Inf/-Inf, scientific notation, decimal timestamps, quoted braces, escaped quotes, and malformed-line error naming.
- `pytest tests/unit/backends/llamacpp/test_config.py` validates base_url constraints (scheme normalization, hostname required, port range, no whitespace/query/fragment/userinfo, trailing-slash stripping).
- `pytest tests/unit/backends/llamacpp/test_manifest.py` confirms sha256 cache is reused across calls while engine_version reflects the latest system_fingerprint observed after first call.
- `pytest tests/unit/backends/llamacpp/test_backend.py -k memory` verifies only `_bytes`-ending samples are recognized; `memory_pool_count` and `process_memory_kib` remain unrecognized.
- `pytest tests/unit/backends/llamacpp/test_stub_server.py` runs the 300-run, 64-thread concurrency test offline with backlog ≥ 512, asserting zero lost updates and exact tokens_per_second ratio.
- `python -c "from quantdelta.backends.llamacpp import LlamaCppBackend"` imports cleanly and docstrings for R9/R10 are present in the module.