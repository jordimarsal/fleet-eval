FILES
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/__init__.py
src/quantdelta/core/serialization.py
tests/unit/core/test_models.py
tests/unit/core/test_public_api.py
tests/unit/core/test_serialization.py
docs/decisions/adr-008.md

TASKS
T1: Implement `TokenAlternative` and `TokenLogprob` frozen value types
    depends_on: (none)
    refs: R2
T2: Update `TaskOutput` to carry optional `logprobs`
    depends_on: T1
    refs: R3
T3: Implement `TaskKL` frozen value type with validation
    depends_on: T1
    refs: R4
T4: Update `Report` model to support additive KL fields
    depends_on: T3
    refs: R5
T5: Update `Scorer` port signature to `score(*, task: Task, output: TaskOutput) -> Score`
    depends_on: (none)
    refs: R1
T6: Ensure serialization schema version "1" compatibility and round-trip
    depends_on: T4
    refs: R6
T7: Pin public API exports and verify import boundary constraints
    depends_on: T1, T3, T4, T5
    refs: R7
T8: Add comprehensive tests for all validation rules and edge cases
    depends_on: T1, T2, T3, T4, T5, T6, T7
    refs: R8

GATES
- All unit tests pass, including coverage for every invalid value rule in R8.
- Public API snapshot test passes with new exports (`TokenAlternative`, `TokenLogprob`, `TaskKL`) and updated `Scorer` signature.
- Serialization round-trip test passes for old reports (without KL fields) and new reports (with KL fields).
- Import boundary test confirms no runtime dependencies on httpx, I/O, or adapter vocabulary.
- ADR-008 document created/updated reflecting the additive policy.