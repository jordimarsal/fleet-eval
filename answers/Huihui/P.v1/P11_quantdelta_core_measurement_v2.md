FILES
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/serialization.py
src/quantdelta/core/__init__.py
docs/decisions/additive-kl-reporting.md
tests/unit/core/test_models.py
tests/unit/core/test_ports.py
tests/unit/core/test_serialization.py
tests/unit/core/test_public_api.py

TASKS
T1: Define TokenAlternative and TokenLogprob value types
    depends_on: (none)
    refs: R2, R8
T2: Add logprobs field to TaskOutput
    depends_on: T1
    refs: R3, R8
T3: Define TaskKL type with validation
    depends_on: (none)
    refs: R4, R8
T4: Update Report model with KL fields and invariants
    depends_on: T3
    refs: R5, R8
T5: Refactor Scorer port signature
    depends_on: (none)
    refs: R1, R7
T6: Update serialization for new types and Report
    depends_on: T2, T4
    refs: R6, R8
T7: Export new types from core package
    depends_on: T1, T3, T5
    refs: R7
T8: Write ADR-008 documentation
    depends_on: T6
    refs: R6
T9: Implement unit tests for models and validation
    depends_on: T1, T2, T3, T4
    refs: R2, R3, R4, R5, R8
T10: Implement unit tests for ports and public API
    depends_on: T5, T7
    refs: R1, R7, R8
T11: Implement serialization round-trip and compatibility tests
    depends_on: T6
    refs: R6, R8

GATES
1. Run `pytest tests/unit/core/` to ensure all model, port, and serialization tests pass.
2. Verify that `python -c "from quantdelta.core import TokenAlternative, TokenLogprob, TaskKL"` succeeds without importing httpx or I/O modules (import boundary check).
3. Execute a manual JSONL round-trip test: serialize a Report with KL fields, deserialize it, and assert equality; also parse an old-format JSON string missing KL fields to verify defaults are applied correctly.
4. Confirm that the `Scorer` protocol signature matches `score(*, task: Task, output: TaskOutput) -> Score` via introspection in the test suite.
5. Validate that no new runtime dependencies were added to `pyproject.toml`.