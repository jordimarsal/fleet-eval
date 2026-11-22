FILES
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/manifest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/conftest.py
tests/unit/backends/llamacpp/test_run.py
docs/architecture.md

TASKS
T1: Harden Prometheus parser for numeric and label edge cases
    depends_on: (none)
    refs: R1, R2, R3, R4
T2: Refactor memory recognition to strict `_bytes` suffix matching
    depends_on: T1
    refs: R5
T3: Implement thread-safe manifest caching with lazy fingerprint resolution
    depends_on: (none)
    refs: R6
T4: Enforce URL validation in LlamaCppConfig
    depends_on: (none)
    refs: R8
T5: Update run logic for truncation handling and concurrency safety
    depends_on: T3
    refs: R7, R9
T6: Document scope boundaries and adapter constants
    depends_on: (none)
    refs: R10
T7: Expand test suite for concurrency, stub server limits, and new behaviors
    depends_on: T1, T2, T3, T4, T5
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11

GATES
- `pytest tests/unit/backends/llamacpp/test_metrics.py -v` passes all parser edge case tests.
- `pytest tests/unit/backends/llamacpp/test_config.py -v` validates URL parsing rules.
- `pytest tests/unit/backends/llamacpp/test_manifest.py -v` confirms cache behavior and fingerprint updates.
- `pytest tests/unit/backends/llamacpp/test_run.py -v` verifies success recording for truncated responses.
- `pytest tests/unit/backends/llamacpp/conftest.py::test_concurrency_300_runs_64_threads -v` proves zero lost updates and exact TPS ratio.
- `ruff check src/quantdelta/backends/llamacpp/` reports no linting errors.