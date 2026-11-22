FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/errors.py
src/quantdelta/backends/llamacpp/manifest.py
tests/unit/backends/llamacpp/test_backend.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_metrics.py
docs/architecture.md

TASKS
T1: Update metrics parser regex and logic for Prometheus/OpenMetrics compliance
    depends_on: (none)
    refs: R1, R2, R3, R4
T2: Refine memory recognition to use `_bytes` suffix heuristic only
    depends_on: T1
    refs: R5
T3: Implement manifest caching and dynamic fingerprint resolution
    depends_on: (none)
    refs: R6
T4: Add concurrency safety with locking in LlamaCppBackend
    depends_on: T3
    refs: R7
T5: Validate base_url in LlamaCppConfig using urllib.parse
    depends_on: (none)
    refs: R8
T6: Document truncation handling and adapter scope constants
    depends_on: (none)
    refs: R9, R10
T7: Create deterministic 300-run concurrency test stub
    depends_on: T4
    refs: R11

GATES
- Unit tests pass for all modified files (`pytest tests/unit/backends/llamacpp/`)
- New concurrency test (`test_stub_server.py` or similar) passes deterministically offline
- `metrics()` correctly parses scientific notation, Inf tokens, quoted braces, and timestamps
- `manifest()` returns cached hash on second call but updates fingerprint if observed
- `LlamaCppConfig` raises error on invalid URLs (whitespace, bad port, userinfo)
- Memory recognition ignores non-`_bytes` suffixes