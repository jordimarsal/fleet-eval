FILES
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/__init__.py
src/quantdelta/core/serialization.py
docs/decisions/adr-008-score-kl-additive-policy.md
tests/unit/core/test_models.py
tests/unit/core/test_public_api.py
tests/unit/core/test_serialization.py

TASKS
T1: Add TokenAlternative, TokenLogprob and TaskKL value types with validation
    depends_on: (none)
    refs: R2, R4, R8
T2: Make scoring keyword-only, score one output per call; keep metric attribute and drop record parameter
    depends_on: (none)
    refs: R1, R7
T3: Add optional logprobs tuple to TaskOutput (None = not requested, empty = requested but no tokens)
    depends_on: T1
    refs: R3
T4: Add additive KL fields to Report with all-or-nothing invariants and cross-field checks
    depends_on: T1
    refs: R5, R8
T5: Wire new exports into quantdelta.core __all__, keep schema version "1", confirm old-report parse and new round-trip through serialization while unknown fields stay rejected
    depends_on: T3, T4
    refs: R6, R7, R8
T6: Pin the public API surface and Scorer signature in snapshot tests
    depends_on: T2, T5
    refs: R7
T7: Update or extend core unit tests covering every invalid value, compatibility, round-trip, port signature and exports
    depends_on: T1, T2, T3, T4, T5
    refs: R1, R2, R3, R4, R5, R6, R7, R8
T8: Record the additive policy and its relationship with ADR-001 and R12 in ADR-008
    depends_on: (none)
    refs: R6

GATES
pytest on tests/unit (full suite must pass; no network/backend regressions)
Public API snapshot test passes proving TokenAlternative, TokenLogprob, TaskKL exported and Scorer pinned at the new signature
Core import boundary check still green (no httpx or I/O imports from quantdelta.core)
Serialization checks green: old Report JSON parses with defaults, new Report with KL fields round-trips unchanged, unknown fields rejected, RunRecord/to_jsonl/parse_jsonl untouched
Error coverage verified: each R8 rule raises InvalidDataError naming the offending field (or <root> only when no single field applies)