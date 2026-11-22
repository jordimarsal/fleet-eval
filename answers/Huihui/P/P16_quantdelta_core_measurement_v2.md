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
T5: Update Scorer port signature
    depends_on: (none)
    refs: R1
T6: Export new types from core package
    depends_on: T1, T3, T4, T5
    refs: R7
T7: Write unit tests for new models and validation rules
    depends_on: T1, T2, T3, T4, T5, T6
    refs: R8
T8: Create ADR-008 documentation
    depends_on: T4
    refs: R6

GATES
1. Run `pytest tests/unit/core/test_models.py` to verify all model validations pass
2. Run `pytest tests/unit/core/test_public_api.py` to confirm public API surface matches expected exports
3. Verify backward compatibility by parsing a pre-feature Report JSON without KL fields
4. Test round-trip serialization of new Report with KL fields using `to_json`/`from_json`
5. Confirm `RunRecord`, `to_jsonl`, and `parse_jsonl` remain unchanged via existing test suite
6. Validate that all invalid values raise `InvalidDataError` with correct field names
7. Check import boundary: no httpx, I/O, or adapter vocabulary in core module