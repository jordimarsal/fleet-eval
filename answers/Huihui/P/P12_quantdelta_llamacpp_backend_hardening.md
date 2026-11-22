FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/manifest.py
src/quantdelta/backends/llamacpp/errors.py
tests/unit/backends/llamacpp/conftest.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_backend.py
tests/unit/backends/llamacpp/test_run.py
docs/architecture.md

TASKS
T1: Harden LlamaCppConfig validation for base_url
    depends_on: (none)
    refs: R8, R10
T2: Enhance metrics parser to support full Prometheus numeric and label syntax
    depends_on: (none)
    refs: R1, R2, R3, R4
T3: Update memory recognition logic to strict _bytes suffix matching
    depends_on: T2
    refs: R5
T4: Implement thread-safe manifest caching with fingerprint resolution
    depends_on: (none)
    refs: R6
T5: Refactor backend concurrency controls for run/metrics/manifest
    depends_on: T4
    refs: R7
T6: Adjust chat completion success recording for truncation
    depends_on: (none)
    refs: R9
T7: Update test stubs and add high-concurrency verification suite
    depends_on: T5, T6
    refs: R11
T8: Document adapter scope and design decisions
    depends_on: T1, T6
    refs: R10

GATES
- Run `pytest tests/unit/backends/llamacpp/test_config.py` to verify URL parsing edge cases.
- Run `pytest tests/unit/backends/llamacpp/test_metrics.py` to ensure all numeric formats and label escaping are parsed correctly without raising errors.
- Run `pytest tests/unit/backends/llamacpp/test_manifest.py` to confirm sha256 is cached while engine_version updates dynamically.
- Run `pytest tests/unit/backends/llamacpp/test_backend.py -k "concurrent"` to execute the 300-run, 64-thread stress test verifying zero lost updates and exact TPS ratio.
- Run full unit test suite `pytest tests/unit` to ensure no regressions in core contracts or other backend components.