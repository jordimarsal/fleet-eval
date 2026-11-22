FILES
src/quantdelta/core/models.py
tests/unit/core/test_models.py
tests/unit/core/test_public_api.py
docs/decisions/core-contract-data-model-pydantic.md

TASKS
T1: Define TokenAlternative and TokenLogprob types with validation rules
    depends_on: (none)
    refs: R2, R3
T2: Add TaskKL type with field constraints and validation
    depends_on: T1
    refs: R4, R5
T3: Extend TaskOutput to include optional logprobs field
    depends_on: T1
    refs: R3
T4: Update Report model to carry kl_divergence, task_kl, and kl_method fields
    depends_on: T2
    refs: R5, R6
T5: Modify Scorer port signature to be keyword-only and remove record parameter
    depends_on: T4
    refs: R1, R7
T6: Validate all new value types and report fields against invalid data rules
    depends_on: T1, T2, T3, T4
    refs: R8

GATES
- All new Pydantic models pass schema validation with both old and new Report formats
- Round-trip serialization of a full Report with KL fields matches input exactly
- Scorer function signature is correctly documented and tested in unit tests
- Invalid data inputs raise `InvalidDataError` with precise field names as required by R8
- Public API snapshot confirms inclusion of TokenAlternative, TokenLogprob, TaskKL, and updated Scorer signature
- Unit tests cover every validation rule (empty tokens, positive log-probabilities, duplicate alternatives, out-of-range masses, missing task_id, etc.)