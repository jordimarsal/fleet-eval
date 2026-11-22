FILES
src/quantdelta/core/models.py
tests/unit/core/test_models.py

TASKS
T1: Add model field notes and fleet link to RunRecord
    depends_on: (none)
    refs: R7
T2: Ensure schema_version is present in RunRecord for round-trip stability
    depends_on: T1
    refs: R3, R4, R12
T3: Verify frozen state of new fields in RunRecord
    depends_on: T1
    refs: R1
T4: Validate invalid data handling for new fields
    depends_on: T1
    refs: R2
T5: Confirm public API surface includes new attributes via snapshot test
    depends_on: T1
    refs: R11
T6: Check import boundary and vocabulary constraints for new code
    depends_on: T1
    refs: R5, R6

GATES
- `pytest tests/unit/core/test_models.py` passes all existing and new tests.
- `pytest tests/unit/core/test_public_api.py` confirms no regression in exported symbols.
- `pytest tests/unit/core/test_serialization.py` confirms lossless JSON/JSONL round-trips with the new fields.
- `pytest tests/unit/core/test_import_boundary.py` confirms no forbidden modules or vocabulary introduced.