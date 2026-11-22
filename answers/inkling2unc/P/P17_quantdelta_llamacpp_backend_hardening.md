FILES
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/manifest.py
docs/decisions/llamacpp-backend-command-semantics.md
tests/unit/backends/llamacpp/conftest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_run.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_boundary.py
tests/unit/backends/llamacpp/test_concurrency.py

TASKS
T1: Validate base_url via urllib.parse (R8)
    depends_on: (none)
    refs: R8
T2: Harden /metrics parsing — numeric values, OpenMetrics timestamps, quoted label values with braces and escaped quotes; malformed lines name the offending line (R1–R4)
    depends_on: (none)
    refs: R1, R2, R3, R4
T3: Memory recognition by `_bytes` sample suffix only, preserving non-finite/negative rejection (R5)
    depends_on: T2
    refs: R5
T4: Manifest artifact sha256 cache across calls with per-call engine_version resolution (supersedes feature 2 object-identity reading of R25) (R6)
    depends_on: (none)
    refs: R6
T5: Record finish_reason == "length" or empty content as a success with token counts recorded (R9)
    depends_on: (none)
    refs: R9
T6: Make run()/metrics()/manifest() thread-safe with a single lock held for state updates only (no HTTP under lock); compute hash once across concurrent manifest() calls (R7)
    depends_on: T2, T3, T4, T5
    refs: R7
T7: Document and test amended R29 scope — host/port/identifier/location from configuration only, route suffixes and sampling defaults fixed constants; document the R9 truncation handling in the adapter design (superseding both closed spec wordings) (R10 plus documentation completion)
    depends_on: T1, T5, T6
    refs: R9, R10
T8: Set stub listen backlog >= 512 and add offline deterministic 300-run × 64-thread concurrency test proving zero lost updates and exact tokens_per_second ratio (R11)
    depends_on: T6, T7
    refs: R11

GATES
pytest tests/unit/core -q (unchanged core contract untouched by these changes).
pytest tests/unit/backends/llamacpp -q (parser cases incl. scientific notation, signed leading '+', NaN/±Inf, decimal timestamps, braces/escaped quotes in label values, ordering of malformed lines naming offender; config validation boundary matrix for http/https case-insensitivity, port range 1–65535, empty hostname, query/fragment/userinfo rejection, trailing-slash stripping, path preservation; manifest cache freshness after later fingerprint; run success on length/empty content; concurrent counter accuracy through the new 300 × 64 thread test).
Full unit suite pytest tests/unit -q green with no network access and deterministic output.
No `quantdelta` public or core surface change beyond what is listed above; verify via existing import-boundary, models, serialization and public-API gates without modifying them.