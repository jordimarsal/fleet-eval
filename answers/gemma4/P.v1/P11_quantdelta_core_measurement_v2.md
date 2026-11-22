FILES
src/quantdelta/core/errors.py
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/__init__.py
docs/decisions/adr-008-additive-schema-policy.md
tests/unit/core/test_models.py
tests/unit/core/test_serialization.py
tests/unit/core/test_public_api.py

TASKS
T1: Implement new frozen value types `TokenAlternative`, `TokenLogprob`, and `TaskKL` with strict validation logic in `models.py`.
    depends_on: (none)
    refs: R2, R4, R8
T2: Update `TaskOutput` to include optional `logprobs` field and update `Report` with additive KL fields and cross-field validation logic.
    depends_on: T1
    refs: R3, R5, R8
T3: Refactor `Scorer` port signature in `ports.py` to use keyword-only arguments and the new task/output pattern.
    depends_on: T2
    refs: R1
T4: Update `core/__init__.py` for public exports and ensure no new runtime dependencies are introduced.
    depends_on: T3
    refs: R7
T5: Implement serialization round-trip tests and backward compatibility checks for `Report` in `serialization.py`.
    depends_on: T2
    refs: R6, R8
T6: Create ADR-008 documenting the additive schema policy.
    depends_on: T5
    refs: R6
T7: Finalize unit tests covering all `InvalidDataError` cases, public API snapshots, and import boundaries.
    depends_on: T4, T5
    refs: R7, R8

GATES
- All `tests/unit/core/*` pass, specifically verifying `InvalidDataError` field names.
- `to_json`/`from_json` round-trip for `Report` with KL fields is identity-preserving.
- Old `Report` JSON (without KL) parses successfully into `Report` models using defaults.
- `quantdelta.core` contains no imports from `httpx` or other non-core libraries.
- Public API snapshot matches expected exported members (`TokenAlternative`, `TokenLogprob`, `TaskKL`, and updated `Scorer`).