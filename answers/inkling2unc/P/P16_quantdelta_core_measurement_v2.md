FILES
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/__init__.py
src/quantdelta/core/serialization.py
docs/decisions/additive-kl-policy.md
tests/unit/core/test_models.py
tests/unit/core/test_serialization.py
tests/unit/core/test_public_api.py
tests/unit/core/test_ports.py

TASKS
T1: Implement TokenAlternative and TokenLogprob frozen types with log-probability/token validators
    depends_on: (none)
    refs: R2, R7, R8
T2: Implement TaskKL frozen type with id, divergence, reference_mass and variant_mass validators
    depends_on: (none)
    refs: R4, R7, R8
T3: Add optional logprobs tuple to TaskOutput (None vs empty distinction preserved)
    depends_on: T1
    refs: R3, R8
T4: Extend Report with kl_divergence / task_kl / kl_method additive fields plus all-or-nothing invariants (unique ids present in deltas, mean within 1e-9 of arithmetic average)
    depends_on: T2
    refs: R5, R8
T5: Change the Scorer port to keyword-only score(*, task, output) -> Score; keep metric: str attribute; leave aggregation outside core
    depends_on: (none)
    refs: R1, R7, R8
T6: Preserve schema version "1": accept pre-feature JSON without KL fields via defaults, round-trip new reports unchanged, reject unknown fields, keep RunRecord/to_jsonl/parse_jsonl untouched
    depends_on: T4, T3
    refs: R6, R8
T7: Export TokenAlternative, TokenLogprob and TaskKL from quantdelta.core; pin them, the new Scorer signature, and defaults in the public API snapshot; confirm no runtime dependency and import boundary
    depends_on: T1, T2, T5
    refs: R7, R8
T8: Add ADR-008 recording the additive policy and its relationship with ADR-001 and R12
    depends_on: T6
    refs: R6
T9: Extend unit tests covering every invalid value (NaN/Inf/positive log-probabilities, empty tokens, duplicate alternative tokens, masses out of [0,1], negative/non-finite divergence, duplicate TaskKL ids, id absent from deltas, mean mismatch, partial KL set), old-report compatibility, new round-trip, port signature and exports
    depends_on: T3, T4, T6, T7
    refs: R1, R2, R3, R4, R5, R6, R7, R8

GATES
- pytest for core units: python -m pytest tests/unit/core — all pass, including new validation cases and serialization compatibility/round-trip tests
- Public API snapshot test passes: __all__/export list matches exactly (TokenAlternative, TokenLogprob, TaskKL added; no extras), importable from package root, scorer pinned to keyword-only score(*, task, output) -> Score
- Import boundary check: quantdelta.core imports nothing from httpx or adapter code; ruff/lint and type checks clean on changed files
- Manual review: schema version remains "1", RunRecord format unchanged, additive fields preserve None/empty distinction in behavior, docs/ADR updated with no conflicting claims