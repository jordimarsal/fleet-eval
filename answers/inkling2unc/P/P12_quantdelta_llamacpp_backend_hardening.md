FILES
src/quantdelta/backends/llamacpp/metrics.py
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/manifest.py
src/quantdelta/backends/llamacpp/errors.py
docs/decisions/llamacpp-backend-parser-hardening.md
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_run.py
tests/unit/backends/llamacpp/test_stub_server.py
tests/unit/backends/llamacpp/conftest.py

TASKS
T1: Metric line parser accepts numeric sample values and optional OpenMetrics timestamps; reject malformed lines with error naming the offending line
    depends_on: (none)
    refs: R1, R2, R4
T2: Config validation via urllib.parse for base_url
    depends_on: (none)
    refs: R8
T3: Memory recognition by `_bytes` suffix only; non-finite/negative remain unrecognized
    depends_on: T1
    refs: R5
T4: Manifest caching of artifact sha256 with per-call engine_version resolution from pin or latest fingerprint
    depends_on: (none)
    refs: R6
T5: Thread-safe backend: counters, fingerprint and hash cache under a lock; no HTTP while holding lock
    depends_on: T3, T4
    refs: R7
T6: Treat finish_reason "length" or empty content as success with token counts and error=None; document truncation handling in adapter design
    depends_on: T1
    refs: R9, R10
T7: Test stub listen backlog >= 512 and 300-run/64-thread concurrency test with zero lost updates and exact tokens_per_second ratio; record amended R29 scope doc and tests
    depends_on: T5
    refs: R11, R10
T8: Docs update for parser hardening, manifest cache semantics and amended R29 scope
    depends_on: T6, T7
    refs: R5, R9, R10

GATES
- pytest tests/unit/backends/llamacpp -q: all pass offline (including new metrics numeric/timestamp/malformed cases, config validation cases, manifest cache freshness case, 300-run 64-thread concurrency test)
- ruff check / python -m compileall on src and tests paths changed
- grep the codebase confirming no `"memory"` substring heuristic remains outside intentional legacy notes
- coverage sanity run over src/quantdelta/backends/llamacpp to confirm every requirement R1–R11 mapped to a passing test
- verify docs updated consistently with decision records (no stale statements that conflict with superseded readings of feature 2 specs)