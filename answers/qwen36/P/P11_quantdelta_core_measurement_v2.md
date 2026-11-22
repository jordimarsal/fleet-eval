FILES
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/serialization.py
src/quantdelta/__init__.py
docs/decisions/additive-kl-fields.md
tests/unit/core/test_models.py
tests/unit/core/test_public_api.py
tests/unit/core/test_serialization.py

TASKS
T1: Define `TokenAlternative` and `TokenLogprob` frozen value types with validation
    depends_on: (none)
    refs: R2, R8
T2: Add optional `logprobs` field to `TaskOutput`
    depends_on: T1
    refs: R3, R8
T3: Define `TaskKL` frozen type with validation
    depends_on: T1
    refs: R4, R8
T4: Update `Report` model with additive KL fields and all-or-nothing invariant
    depends_on: T3
    refs: R5, R8
T5: Change `Scorer.score` signature from `(self, record)` to keyword-only `(self, *, task, output)`
    depends_on: (none)
    refs: R1, R7, R8
T6: Update serialization — keep version "1", add KL fields to `to_json`/`from_json`, ensure round-trip and old-report compatibility
    depends_on: T4
    refs: R6, R8
T7: Export new types from `quantdelta.core.__init__` and pin public API snapshot
    depends_on: T1, T3, T4, T5
    refs: R7, R8
T8: Write tests covering every invalid-value rule, old-report compat, new round-trip, port signature, and exports
    depends_on: T7
    refs: R8

GATES
- All unit tests pass (`pytest tests/unit/core`) including the full suite of InvalidDataError cases for each field.
- Old Report JSON without KL fields parses successfully via `from_json`.
- New Report with KL fields round-trips through `to_json` / `from_json` unchanged.
- Unknown fields in serialized data are still rejected.
- `RunRecord`, `to_jsonl`, and `parse_jsonl` remain functionally unchanged.
- Public API snapshot matches the pinned exports; no runtime dependencies added (no httpx, I/O, or adapter vocabulary).
- ADR-008 written documenting additive policy and its relationship to ADR-001 and R12.