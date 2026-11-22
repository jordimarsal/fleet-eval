FILES
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/serialization.py
src/quantdelta/core/__init__.py
tests/unit/core/test_models.py
tests/unit/core/test_serialization.py
tests/unit/core/test_public_api.py
docs/decisions/adr-008.md

TASKS
T1: Implement `TokenAlternative` and `TokenLogprob` value types
    depends_on: (none)
    refs: R2, R8
T2: Implement `TaskKL` value type
    depends_on: T1
    refs: R4, R8
T3: Update `TaskOutput` to carry optional `logprobs`
    depends_on: T1
    refs: R3, R8
T4: Update `Scorer` port signature to `score(*, task: Task, output: TaskOutput) -> Score`
    depends_on: T3
    refs: R1, R7, R8
T5: Implement `Report` type with additive KL fields and validation logic
    depends_on: T2, T3
    refs: R5, R8
T6: Update serialization to support new fields while maintaining backward compatibility
    depends_on: T3, T5
    refs: R6, R8
T7: Export new types from `quantdelta.core` and update public API snapshot
    depends_on: T1, T2, T4, T5
    refs: R7
T8: Add comprehensive tests for all new types, validation rules, and serialization round-trips
    depends_on: T1, T2, T3, T4, T5, T6, T7
    refs: R8

GATES
- All unit tests pass, including coverage for every invalid value case specified in R8.
- Public API snapshot test passes, confirming exports of `TokenAlternative`, `TokenLogprob`, `TaskKL`, and the updated `Scorer` signature.
- Serialization round-trip test passes for both old (no KL fields) and new (with KL fields) `Report` instances.
- Import boundary test passes, ensuring no new runtime dependencies (httpx, I/O, etc.) are introduced.
- ADR-008 document created and reviewed, documenting the additive policy.