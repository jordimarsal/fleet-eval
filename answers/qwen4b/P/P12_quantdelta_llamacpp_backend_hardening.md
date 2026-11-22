FILES  
src/quantdelta/backends/llamacpp/metrics.py  
src/quantdelta/backends/llamacpp/manifest.py  
src/quantdelta/backends/llamacpp/backend.py  
tests/unit/backends/llamacpp/test_metrics.py  
tests/unit/backends/llamacpp/test_manifest.py  
docs/specs.md  

TASKS  
T1: Implement Prometheus text format numeric value parsing with support for decimal, scientific notation, leading +, and special tokens NaN, +Inf, -Inf  
    depends_on: (none)  
    refs: R1, R2, R3, R4  

T2: Add label value parsing to handle braces within quoted values and escaped quotes  
    depends_on: T1  
    refs: R3  

T3: Modify memory recognition logic to only accept sample names ending in _bytes; remove substring heuristic  
    depends_on: T1  
    refs: R5  

T4: Update manifest() to cache artifact sha256 across calls and resolve engine_version from config or system_fingerprint on each call  
    depends_on: T1  
    refs: R6  

T5: Ensure LlamaCppBackend is thread-safe for concurrent run(), metrics(), and manifest() calls via locking of shared state  
    depends_on: T4  
    refs: R7  

T6: Validate base_url in LlamaCppConfig using urllib.parse with scheme, hostname, port, and path constraints  
    depends_on: T1  
    refs: R8  

T7: Record chat completions with finish_reason == "length" or empty content as success with token counts  
    depends_on: T1  
    refs: R9  

T8: Document and test the fixed adapter constants scope: host, port, model ID, file location from config; route suffixes and sampling defaults are fixed  
    depends_on: T1  
    refs: R10  

T9: Add 300-run, 64-thread concurrency test with listen backlog ≥ 512 to verify zero lost updates and exact tokens_per_second ratio  
    depends_on: T1  
    refs: R11  

GATES  
- All parser edge cases (NaN, +Inf, -Inf, scientific notation) pass unit tests in test_metrics.py  
- Manifest caching behavior matches specification: hash cached across calls, engine_version re-resolved on first call  
- Thread safety verified via concurrent execution in a multi-threaded test suite (test_manifest.py, test_backend.py)  
- Base URL validation passes all schema constraints in test_config.py  
- Memory recognition correctly ignores non-_bytes sample names and negative/non-finite values  
- Concurrency test shows no data loss and correct tokens_per_second ratio under 64 threads  
- Documentation updated in docs/specs.md for R10 scope and R7 thread safety