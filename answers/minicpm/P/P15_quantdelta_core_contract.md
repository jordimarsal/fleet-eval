FILES
docs/fleet.md
src/quantdelta/core/models.py
tests/unit/core/test_models.py

TASKS
T1: Add model field notes and fleet link to documentation
    depends_on: (none)
    refs: R6
T2: Update RunRecord model to include optional model_notes and fleet_link fields
    depends_on: T1
    refs: R7, R11, R12
T3: Update serialization logic to handle new fields in RunRecord
    depends_on: T2
    refs: R3, R4, R12
T4: Add tests for new fields in RunRecord (construction, serialization, public API)
    depends_on: T3
    refs: R1, R2, R3, R4, R11

GATES
- All unit tests pass (pytest)
- Import boundary test passes (no forbidden modules loaded)
- Serialization round-trip test passes for RunRecord with new fields
- Public API snapshot test updated and passing
- No engine-specific vocabulary (gguf, llama, kv cache) in core sources