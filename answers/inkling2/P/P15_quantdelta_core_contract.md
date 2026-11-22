FILES
docs/model-field-notes.md
docs/fleet.md
docs/specs.md
src/quantdelta/core/models.py
src/quantdelta/core/serialization.py
tests/unit/core/test_public_api.py
tests/unit/core/test_serialization.py
tests/unit/core/test_import_boundary.py
tests/unit/core/test_report_no_io.py

TASKS
T1: Verify frozen value types and InvalidDataError behavior
    depends_on: (none)
    refs: R1, R2
T2: Confirm RunRecord JSON/JSONL round-trip losslessness and schema_version stamping
    depends_on: T1
    refs: R3, R4, R12
T3: Confirm the no-network/no-disk Report construction constraint
    depends_on: T1
    refs: R8
T4: Audit RunRecord identity fields against the contract
    depends_on: T1
    refs: R7
T5: Pin public field names with a snapshot test
    depends_on: T1
    refs: R11
T6: Check port surfaces for scoring separation and backend minimalism
    depends_on: T1
    refs: R9, R10
T7: Verify import boundary and engine-vocabulary rules still hold
    depends_on: T3
    refs: R5, R6
T8: Write model field notes documenting Task, Score, TaskDelta, RunRecord and Report contracts
    depends_on: T2, T4, T5
    refs: R1, R3, R4, R7, R11, R12
T9: Add fleet link from the core docs to fleet documentation
    depends_on: T8
    refs: R7, R8
GATES
python -m pytest tests/unit/core tests/test_smoke.py -q (full unit suite green)
python -m pytest tests/unit/core/test_import_boundary.py tests/unit/core/test_serialization.py tests/unit/core/test_public_api.py tests/unit/core/test_report_no_io.py -q (focused gates after edits)
grep check that src/quantdelta/core introduces no gguf|llama|kv-cache vocabulary in identifiers, fields or messages, and that quantdelta.core imports do not load httpx/subprocess/numpy/typer (subprocess child-module isolation test passing)
confirmation diff shows every approved requirement R1–R12 either unchanged at runtime or deliberately documented with its contract source in the notes; public API snapshot still matches; schema_version stable for backward JSONL compatibility