FILES
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/__init__.py
tests/unit/core/test_models.py
tests/unit/core/test_public_api.py

TASKS
T1: Implement TokenAlternative and TokenLogprob value types
    depends_on: (none)
    refs: R2, R8
T2: Add logprobs field to TaskOutput
    depends_on: T1
    refs: R3, R8
T3: Implement TaskKL value type
    depends_on: (none)
    refs: R4, R8
T4: Update Report model with KL fields and validation logic
    depends_on: T3
    refs: R5, R6, R8
T5: Update Scorer port signature in ports.py
    depends_on: (none)
    refs: R1, R7
T6: Export new types from quantdelta.core and update public API snapshot
    depends_on: T1, T3, T5
    refs: R7, R8
T7: Write comprehensive unit tests for all new models and validations
    depends_on: T1, T2, T3, T4, T5, T6
    refs: R8

GATES
- Run `pytest tests/unit/core/` ensuring all new validators raise InvalidDataError correctly.
- Verify `quantdelta.core.__all__` includes `TokenAlternative`, `TokenLogprob`, `TaskKL`.
- Confirm `Scorer.score` signature matches the keyword-only requirement.
- Validate round-trip serialization of `Report` with and without KL fields.