FILES
src/quantdelta/core/models.py
src/quantdelta/core/__init__.py
docs/decisions/additive-kl-fields.md
tests/unit/core/test_models.py
tests/unit/core/test_public_api.py
tests/unit/core/test_serialization.py
tests/unit/core/test_errors.py

TASKS
T1: Add TokenAlternative and TokenLogprob frozen value types to core.models
    depends_on: (none)
    refs: R2
T2: Add logprobs field to TaskOutput
    depends_on: T1
    refs: R3
T3: Add TaskKL frozen type to core.models
    depends_on: T1
    refs: R4
T4: Update Report with additive KL fields and all-or-nothing validation
    depends_on: T3
    refs: R5
T5: Change Scorer port signature from record-based to task+output scoring
    depends_on: (none)
    refs: R1
T6: Wire serialization round-trip for new Report fields; preserve old-report compatibility
    depends_on: T4
    refs: R6
T7: Pin public API snapshot with new exports and updated Scorer signature
    depends_on: T1, T3, T5
    refs: R7
T8: Write comprehensive error-validation tests covering every InvalidDataError rule
    depends_on: T1, T2, T3, T4, T5
    refs: R8

GATES
- `pytest tests/unit/core/test_models.py` passes (all model validators, frozen semantics, defaults)
- `pytest tests/unit/core/test_public_api.py` passes (new types exported, Scorer signature pinned, no extra imports)
- `pytest tests/unit/core/test_serialization.py` passes (old report parses with defaults, new report round-trips unchanged, unknown fields rejected)
- `pytest tests/unit/core/test_errors.py` passes (every invalid-value rule covered by a dedicated test raising InvalidDataError with correct field name)
- `python -m quantdelta.core --verify-import-boundary` confirms no httpx/I/O/adapter vocabulary leaks into core