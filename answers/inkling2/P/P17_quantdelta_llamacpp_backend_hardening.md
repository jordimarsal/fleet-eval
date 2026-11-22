FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/manifest.py
tests/unit/backends/llamacpp/conftest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_run.py
tests/unit/backends/llamacpp/test_concurrency.py (new)
docs/decisions/llamacpp-backend-command-semantics.md

TASKS
T1: Harden /metrics parser and failure routing
    depends_on: (none)
    refs: R1, R2, R3, R4
T2: Restrict memory recognition to `_bytes` samples
    depends_on: T1
    refs: R5
T3: Cache manifest artifact hash; re-resolve engine_version per call
    depends_on: (none)
    refs: R6
T4: Serialize state mutation under a lock in the backend
    depends_on: T3
    refs: R7
T5: Validate base_url in LlamaCppConfig
    depends_on: (none)
    refs: R8
T6: Record finish_reason == "length" or empty content as success
    depends_on: (none)
    refs: R9
T7: Document amended scope and truncation handling in adapter design
    depends_on: T6
    refs: R10
T8: Backlog hardening plus 300-run / 64-thread offline concurrency test
    depends_on: T4
    refs: R11

GATES
- pytest tests/unit/backends/llamacpp -q passes offline with no network access (stub server only).
- Concurrency suite (new test file) passes repeatedly and deterministically across multiple runs without sleeps or timing assumptions; asserts zero lost updates and exact tokens_per_second ratio.
- Parser gate: fixtures covering decimal, scientific, leading '+', NaN, +Inf, -Inf samples, decimal OpenMetrics timestamps, braced label values and escaped quotes all parse; malformed lines raise LlamaCppMalformedResponseError naming the line.
- Manifest gate: repeated manifest() calls perform at most one artifact hash while engine_version reflects an observed fingerprint after the first call.
- Config gate: URLs with non-http(s) schemes, missing host, out-of-range ports, whitespace, query/fragment, userinfo are rejected; valid URLs are normalized (lowercased scheme, stripped trailing slash) with path prefix preserved.
- Run gate: finish_reason == "length" and empty content cases produce success records with token counts and error=None; frozen core contract unchanged (core package diff is empty).
- Style/type checks from repo tooling (e.g. ruff/mypy per AGENTS.md / pyproject.toml) pass on changed files.