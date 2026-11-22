FILES
src/quantdelta/core/ports.py
src/quantdelta/core/models.py
src/quantdelta/core/__init__.py
src/quantdelta/core/serialization.py
tests/unit/core/test_models.py
tests/unit/core/test_serialization.py
tests/unit/core/test_errors.py
tests/unit/core/test_public_api.py
docs/decisions/additive-report-kl-logprob-policy.md

TASKS
T1: Change the Scorer port signature
    depends_on: (none)
    refs: R1
T2: Add frozen TokenAlternative and TokenLogprob value types with validation
    depends_on: (none)
    refs: R2
T3: Add optional logprobs tuple to TaskOutput
    depends_on: T2
    refs: R3
T4: Add frozen TaskKL type with field validation
    depends_on: T2
    refs: R4
T5: Extend Report with additive KL fields, all-or-nothing invariant, uniqueness and mean-tolerance checks
    depends_on: T4
    refs: R5
T6: Keep schema version "1"; verify old-report compatibility, new round-trip, rejection of unknown fields, unchanged RunRecord JSONL path
    depends_on: T5
    refs: R6
T7: Export token probability types and TaskKL from quantdelta.core; pin public API snapshot and the changed Scorer signature
    depends_on: T2, T3, T4, T5
    refs: R7, R1
T8: Cover every invalid value and invariants across tests, including exports/signature gates
    depends_on: T7
    refs: R8, R2, R4, R5
T9: Record ADR for the additive KL/logprob policy and its relationship with ADR-001 and R12
    depends_on: T6
    refs: R6

GATES
- Full unit test suite (tests/unit) passes, including core model/serialization/public-api/errors coverage for the new fields and validation rules.
- Import boundary check still passes: no httpx or other runtime dependencies added to src/quantdelta/core; adapter vocabulary absent; pyproject dependency set unchanged.
- Public API snapshot test confirms TokenAlternative, TokenLogprob, TaskKL, and the pinned keyword-only non-RunRecord Scorer signature are exported as expected.
- Serialization compatibility checks pass: pre-feature Report JSON parses without KL fields using defaults; a full Report round-trips byte-semantically through to_json/from_json; unknown fields remain rejected; RunRecord and parse_jsonl behavior is unchanged.
- No reliance on aggregate aggregation outside core; replicate/aggregation logic remains outside core as before.