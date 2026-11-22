FILES
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/serialization.py
src/quantdelta/core/__init__.py
docs/decisions/additive-kl-and-logprob-fields.md
tests/unit/core/test_models.py
tests/unit/core/test_serialization.py
tests/unit/core/test_public_api.py
tests/unit/core/test_import_boundary.py

TASKS
T1: Add TokenAlternative, TokenLogprob and TaskKL frozen value types with validation
    depends_on: (none)
    refs: R2, R4, R8
T2: Change Scorer port signature to keyword-only score(*, task: Task, output: TaskOutput) -> Score
    depends_on: (none)
    refs: R1, R7, R8
T3: Carry optional logprobs on TaskOutput and export new types from quantdelta.core; pin public API snapshot
    depends_on: T1, T2
    refs: R3, R7, R8
T4: Extend Report with all-or-nothing KL fields and additive schema/version handling in serialization
    depends_on: T1
    refs: R5, R6, R8
T5: Write ADR-008 recording the additive policy and its relationship with ADR-001 and R12
    depends_on: T4
    refs: R6
T6: Expand core unit tests for validators, port signature, old/new report compatibility and JSONL stability
    depends_on: T3, T4, T5
    refs: R1, R2, R3, R4, R5, R6, R7, R8

GATES
- pytest tests/unit/core -q (models, serialization, port/public-api, import boundary)
- python -c "import quantdelta.core as c; assert not hasattr(c, 'httpx')" / existing test_import_boundary passes with no runtime dependency added to pyproject.toml
- ruff check and format on changed files if configured by CI/HARNESS.md
- verify frozen types validate NaN/Inf/positive log-probs, empty tokens, duplicate alternative tokens, masses outside [0,1], negative/non-finite KL divergence, duplicate TaskKL ids, missing deltas id, mean mismatch beyond 1e-9, partial KL field sets; confirm unknown fields still rejected, RunRecord/to_jsonl/parse_jsonl unchanged, version stays "1"