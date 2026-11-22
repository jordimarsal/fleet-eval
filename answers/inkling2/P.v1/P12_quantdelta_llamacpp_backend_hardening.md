FILES
src/quantdelta/backends/llamacpp/metrics.py
src/quantdelta/backends/llamacpp/manifest.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/backend.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_run.py
tests/unit/backends/llamacpp/test_boundary.py
tests/unit/backends/llamacpp/conftest.py
tests/unit/backends/llamacpp/test_concurrency.py
docs/decisions/llamacpp-parser-cache-and-concurrency.md

TASKS
T1: metrics /metrics parser rewrite (R1, R2, R3, R4)
    depends_on: (none)
    refs: R1, R2, R3, R4
T2: memory recognition restricted to `*_bytes` samples (R5)
    depends_on: (none)
    refs: R5
T3: stricter base_url validation in LlamaCppConfig (R8)
    depends_on: (none)
    refs: R8
T4: manifest sha256 cache with per-call engine_version resolution (R6)
    depends_on: (none)
    refs: R6
T5: lock instance state and guarantee at most one hash across concurrent calls (R7)
    depends_on: T1, T2, T3, T4
    refs: R7
T6: record finish_reason=length or empty content as success; document task interaction (R9)
    depends_on: T5
    refs: R9
T7: adapter design doc for amended scope and truncation handling, plus constants/config boundary tests (R10)
    depends_on: T3, T6
    refs: R9, R10
T8: stub backlog of >=512 and deterministic offline concurrency stress test (R11)
    depends_on: T5, T6
    refs: R11

GATES
- `python -m pytest` entire suite runs fully offline (no network access required by fixtures or marks).
- Parser gates: decimal, scientific notation, leading `+`, `NaN`, `+Inf`, `-Inf` samples accepted (R1); OpenMetrics integer/decimal sample timestamp accepted (R2); label values with braces inside quotes and escaped quote sequences parse correctly (R3); malformed lines raise `LlamaCppMalformedResponseError` naming the line (R4).
- Memory recognition gate: only names ending in `_bytes` are recognized as GiB memory samples; strings such as `memory_pool_count` and `process_memory_kib` yield no measurement even though they contain "memory"; non-finite and negative samples are not recognized.
- Manifest gate: repeated manifest calls do not re-hash the artifact, while engine_version changes after a later observed system fingerprint differ from earlier calls; concurrent manifest calls compute the hash exactly once.
- Config gate: valid http/https URLs pass case-insensitively (normalized to lowercase scheme); missing hostname, bad port range, whitespace, query/fragment, or userinfo all fail validation; path prefixes preserved and trailing slashes stripped.
- Concurrency gates: test_backend run plus new 300-run x64-thread concurrency test proves zero lost updates on successful-run counters and a consistent tokens_per_second ratio between fastest and slowest requests, under repeated execution offline, fully deterministic outcomes.
- run() success recording gate: finish_reason == "length" and empty content cases both count as successful runs with token counts recorded and error=None.