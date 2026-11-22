FILES
src/quantdelta/core/__init__.py
src/quantdelta/core/errors.py
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
docs/decisions/adr-008-additive-policy.md
tests/unit/core/test_models.py
tests/unit/core/test_public_api.py
tests/unit/core/test_serialization.py

TASKS
T1: Implement new frozen value types `TokenAlternative`, `TokenLogprob`, and `TaskKL` in `models.py` with strict validation logic for tokens, logprobs, masses, and divergence.
    depends_on: (none)
    refs: R2, R4, R8
T2: Update `TaskOutput` to include optional `logprobs` field and update `Report` to include additive KL fields with all-or-nothing validation logic.
    depends_on: T1
    refs: R3, R5, R8
T3: Refactor `Scorer` port signature in `ports.py` to use keyword-only arguments and the new `score(*, task: Task, output: TaskOutput, metric: str) -> Score` pattern.
    depends_on: T2
    refs: R1
T4: Update `quantdelta.core` exports and pin public API snapshot including new types and updated `Scorer`.
    depends_on: T3
    refs: R7
T5: Ensure serialization compatibility: verify `SCHEMA_VERSION` remains `"1"`, implement round-trip for new `Report` fields, and ensure backward compatibility for old reports.
    depends_on: T2
    refs: R6
T6: Document the additive policy in ADR-008.
    depends_on: T5
    refs: R6
T7: Implement comprehensive test suite covering all validation rules (InvalidDataError), serialization round-trips, and the new Scorer signature.
    depends_on: T1, T2, T3, T4, T5
    refs: R1, R2, R3, R4, R5, R6, R7, R8

GATES
- All unit tests in `tests/unit/core/` pass, specifically verifying `InvalidDataError` messages and field names.
- Serialization round-trip check: `Report` with KL data must match exactly after `to_json`/`from_json`.
- Backward compatibility check: Old JSON reports without KL fields must parse successfully into `Report` objects.
- Public API snapshot check: Verify `quantdelta.core.__all__` contains all required new types and updated signatures.
- Import boundary check: Ensure no new runtime dependencies were added to `quantdelta.core`.