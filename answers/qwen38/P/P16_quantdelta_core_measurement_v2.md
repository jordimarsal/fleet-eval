FILES
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/__init__.py
tests/unit/core/test_models.py
tests/unit/core/test_public_api.py
docs/decisions/additive-kl-reporting.md

TASKS
T1: Define TokenAlternative and TokenLogprob value types
    depends_on: (none)
    refs: R2
T2: Add logprobs field to TaskOutput
    depends_on: T1
    refs: R3
T3: Define TaskKL value type
    depends_on: (none)
    refs: R4
T4: Update Report with KL fields and validation
    depends_on: T3
    refs: R5
T5: Refactor Scorer port signature
    depends_on: (none)
    refs: R1
T6: Update public API exports
    depends_on: T1, T3, T5
    refs: R7
T7: Write unit tests for new models and validation rules
    depends_on: T1, T2, T3, T4
    refs: R8
T8: Update serialization tests for round-trip compatibility
    depends_on: T4
    refs: R6
T9: Document ADR-008 additive policy
    depends_on: T4
    refs: R6

GATES
pytest tests/unit/core/test_models.py -v
pytest tests/unit/core/test_public_api.py -v
pytest tests/unit/core/test_serialization.py -v
python -m mypy src/quantdelta/core --strict