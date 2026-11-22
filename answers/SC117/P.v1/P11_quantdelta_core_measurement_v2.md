FILES
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/serialization.py
src/quantdelta/core/__init__.py
docs/decisions/additive-kl-report-policy.md
tests/unit/core/test_models.py
tests/unit/core/test_serialization.py
tests/unit/core/test_ports.py
tests/unit/core/test_public_api.py

TASKS
T1: Implement TokenAlternative and TokenLogprob value types
    depends_on: (none)
    refs: R2, R8
T2: Update TaskOutput to include optional logprobs
    depends_on: T1
    refs: R3, R8
T3: Implement TaskKL frozen value type
    depends_on: (none)
    refs: R4, R8
T4: Update Report model with KL fields and validation logic
    depends_on: T3
    refs: R5, R8
T5: Modify Scorer port signature and implementation
    depends_on: (none)
    refs: R1, R7
T6: Update serialization schema and round-trip logic
    depends_on: T2, T4
    refs: R6, R8
T7: Export new types from core package and update public API snapshot
    depends_on: T1, T3, T4, T5
    refs: R7
T8: Add ADR for additive policy
    depends_on: (none)
    refs: R6
T9: Write comprehensive tests for all new models, ports, and serialization
    depends_on: T1, T2, T3, T4, T5, T6, T7
    refs: R8

GATES
- Unit tests pass for all new validation rules in TokenAlternative, TokenLogprob, TaskKL, and Report.
- Serialization round-trip test passes for old reports (no KL) and new reports (with KL).
- Scorer port signature matches the keyword-only definition.
- Public API exports are correct and pinned.
- No new runtime dependencies introduced.
- Import boundary test confirms no httpx/I/O/adapter vocabulary leaks into core.