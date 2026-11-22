FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/manifest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_manifest.py

TASKS
T1: Enhance /metrics parser to accept scientific notation and leading + in values
    depends_on: (none)
    refs: R1, R3
T2: Add optional timestamp parsing support for OpenMetrics format
    depends_on: T1
    refs: R2
T3: Update label value parsing to handle braces inside quotes and escaped quotes
    depends_on: T1
    refs: R3
T4: Implement strict validation of memory sample names ending in _bytes
    depends_on: T1
    refs: R5
T5: Refactor manifest() to cache artifact sha256 across calls and resolve engine_version from config or system_fingerprint
    depends_on: T4
    refs: R6
T6: Ensure LlamaCppBackend is thread-safe with proper locking around run(), metrics(), and manifest()
    depends_on: T5
    refs: R7
T7: Validate base_url in LlamaCppConfig using urllib.parse with scheme, hostname, port, and path constraints
    depends_on: T6
    refs: R8
T8: Record success for finish_reason == "length" or empty content with token counts
    depends_on: T6
    refs: R9
T9: Document and test fixed adapter constants for host, port, model ID, file location, and sampling defaults
    depends_on: T7
    refs: R10
T10: Add 300-run, 64-thread concurrency test with listen backlog >= 512 to verify zero lost updates and exact tokens_per_second ratio
    depends_on: T9
    refs: R11

GATES
- All parser tests pass for numeric values (decimal, scientific, leading +) and special tokens (NaN, ±Inf)
- Label value parsing correctly handles braces inside quotes and escaped quotes
- Memory recognition only accepts samples ending in _bytes; no false positives on memory_pool_count or process_memory_kib
- Manifest() returns consistent sha256 across calls and uses correct engine_version resolution logic
- Threaded concurrency test completes without data loss or race conditions
- Base URL validation passes all required constraints (scheme, hostname, port, path)
- Success recording for length-truncated responses is accurate and matches expected behavior
- Test suite includes full coverage of all requirements via unit and integration tests