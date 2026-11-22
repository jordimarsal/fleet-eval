FILES
src/quantdelta/core/models.py
tests/unit/core/test_models.py
tests/unit/core/test_serialization.py
docs/fleet.md

TASKS
T1: Add schema_version field to RunRecord and Report models to ensure backward compatibility
    depends_on: (none)
    refs: R1, R12, R3, R4
T2: Implement frozen value type enforcement for all core domain types using pydantic's frozen=True config
    depends_on: T1
    refs: R1, R2, R7
T3: Ensure RunRecord round-trip serialization with lossless JSON and JSONL parsing
    depends_on: T2
    refs: R3, R4
T4: Verify that Report construction from RunRecords does not require external I/O or network access
    depends_on: T3
    refs: R8
T5: Define Scorer port with dependency on record contents only
    depends_on: T2
    refs: R9
T6: Define Backend port with minimal execution interface and no engine-specific methods
    depends_on: T2
    refs: R10
T7: Pin public API surface via snapshot test to enforce stable field names
    depends_on: T6
    refs: R11
T8: Validate import boundary excludes forbidden modules and vocabulary
    depends_on: T7
    refs: R5, R6

GATES
- All unit tests in tests/unit/core/test_models.py pass (R1, R2, R7)
- Round-trip serialization of RunRecord and Report passes in tests/unit/core/test_serialization.py (R3, R4)
- Import boundary test passes without loading forbidden modules (R5) and contains no engine-specific terms (R6)
- Public API surface matches pinned snapshot in tests/unit/core/test_public_api.py (R11)
- Report construction from RunRecords is fully self-contained (R8)
- Scorer and Backend ports are correctly defined and used in isolation (R9, R10)