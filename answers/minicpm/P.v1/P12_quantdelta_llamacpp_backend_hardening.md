FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/errors.py
src/quantdelta/backends/llamacpp/manifest.py
src/quantdelta/backends/llamacpp/metrics_parser.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_backend_concurrency.py
tests/unit/backends/llamacpp/test_stub_server.py

TASKS
T1: Implement robust `/metrics` parser supporting all Prometheus numeric formats and OpenMetrics timestamps.
    depends_on: (none)
    refs: R1, R2
T2: Extend metrics parser to handle escaped quotes and braces within label values.
    depends_on: T1
    refs: R3
T3: Implement strict validation for `LlamaCppConfig.base_url` using `urllib.parse`.
    depends_on: (none)
    refs: R8
T4: Update `manifest()` to cache artifact sha256 while resolving `engine_version` dynamically.
    depends_on: (none)
    refs: R6
T5: Refactor memory recognition logic to rely solely on `_bytes` suffixes.
    depends_on: (none)
    refs: R5
T6: Add concurrency safety locks to `LlamaCppBackend` for `run()`, `metrics()`, and `manifest()`.
    depends_on: T4, T5
    refs: R7
T7: Ensure `metrics()` raises `LlamaCppMalformedResponseError` on format violations with line naming.
    depends_on: T1, T2
    refs: R4
T8: Document and adjust chat completion handling for `finish_reason == "length"` or empty content.
    depends_on: (none)
    refs: R9
T9: Update documentation and tests to reflect fixed adapter constants vs configuration sources.
    depends_on: (none)
    refs: R10
T10: Implement deterministic concurrency test stub with backlog 512 and 300-run/64-thread verification.
    depends_on: T6
    refs: R11

GATES
- All unit tests in `tests/unit/backends/llamacpp/` pass, including the new concurrency stress test.
- Static type checking (mypy/pyright) passes on all modified files.
- Performance regression check: `tokens_per_second` ratio remains consistent under load.
- Manual verification of `base_url` validation edge cases (userinfo, whitespace, invalid ports).
- Verification that `manifest()` cache persists across calls while `engine_version` updates correctly.