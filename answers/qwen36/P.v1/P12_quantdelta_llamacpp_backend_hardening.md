FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/errors.py
src/quantdelta/backends/llamacpp/manifest.py
src/quantdelta/backends/llamacpp/metrics_parser.py
tests/unit/backends/llamacpp/test_backend.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_stub_server.py

TASKS
T1: Add `LlamaCppMalformedResponseError` to errors module
    depends_on: (none)
    refs: R4
T2: Implement `/metrics` parser in new metrics_parser module
    depends_on: T1
    refs: R1, R2, R3
T3: Wire parser into `backend.metrics()` with error raising on violation
    depends_on: T2
    refs: R4
T4: Update memory recognition logic to use `_bytes` suffix only
    depends_on: (none)
    refs: R5
T5: Refactor `manifest()` to cache artifact sha256 and resolve engine_version dynamically
    depends_on: (none)
    refs: R6
T6: Add threading lock around shared state in `LlamaCppBackend` for run/metrics/manifest
    depends_on: T5
    refs: R7
T7: Validate `base_url` in `LlamaCppConfig.__init__` using urllib.parse
    depends_on: (none)
    refs: R8
T8: Document truncation handling responsibility in adapter design docs
    depends_on: (none)
    refs: R9
T9: Document amended R29 scope in architecture or decisions docs
    depends_on: (none)
    refs: R10
T10: Write concurrency test stub with backlog >= 512 and 300-run / 64-thread suite
    depends_on: T6, T7
    refs: R11

GATES
- Unit tests pass for metrics parser covering decimal, scientific notation, +Inf, -Inf, NaN, optional timestamps, quoted braces, escaped quotes.
- Malformed line raises LlamaCppMalformedResponseError with offending line content.
- Memory recognition only matches `_bytes` suffix; memory_pool_count and process_memory_kib are not treated as GiB.
- manifest() returns same sha256 across calls without re-hashing; engine_version updates when system_fingerprint changes after first call.
- Concurrent run/metrics/manifest from multiple threads produce correct counters and no lost updates under lock.
- HTTP requests never occur while holding the lock.
- Config validation rejects invalid base_url schemes, empty hostnames, out-of-range ports, whitespace, query/fragment, userinfo; preserves path prefixes and strips trailing slashes.
- Truncation handling documented in adapter design docs.
- Amended R29 scope documented in architecture or decisions docs.
- Concurrency test runs offline deterministically with backlog >= 512, 300 runs, 64 threads, zero lost updates, exact tokens_per_second ratio.