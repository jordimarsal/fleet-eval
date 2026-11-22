FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/manifest.py
src/quantdelta/backends/llamacpp/errors.py
docs/architecture.md
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_backend.py

TASKS
T1: Enhance `/metrics` parser to support full Prometheus numeric types and OpenMetrics timestamps
    depends_on: (none)
    refs: R1, R2
T2: Update `/metrics` parser to handle quoted braces and escaped quotes in label values
    depends_on: T1
    refs: R3
T3: Implement strict `_bytes` suffix recognition for memory metrics, removing substring heuristic
    depends_on: T1
    refs: R5
T4: Add `LlamaCppMalformedResponseError` raising logic with line identification for format violations
    depends_on: T2, T3
    refs: R4
T5: Refactor `manifest()` to cache artifact sha256 while resolving `engine_version` dynamically from config/fingerprint
    depends_on: (none)
    refs: R6
T6: Introduce thread-safe locking in `LlamaCppBackend` for concurrent access to counters, fingerprint, and hash cache
    depends_on: T5
    refs: R7
T7: Document truncation handling responsibility in adapter design docs
    depends_on: (none)
    refs: R9
T8: Document amended scope of configuration vs. fixed constants in architecture/docs
    depends_on: (none)
    refs: R10
T9: Create concurrency test stub with backlog 512 and run 300-run/64-thread deterministic suite
    depends_on: T6
    refs: R11

GATES
- Unit tests pass for parser edge cases (scientific notation, NaN/Inf, timestamps, quoted labels).
- Memory recognition unit tests confirm `_bytes` suffix matching and exclusion of heuristic matches.
- Malformed response error tests verify correct exception raising and line naming.
- Manifest cache tests verify sha256 is cached across calls but engine_version updates on subsequent calls.
- Concurrency stress test passes with zero lost updates and exact tokens_per_second ratio.
- Documentation review confirms R9 and R10 scopes are accurately described.