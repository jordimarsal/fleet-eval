FILES  
src/quantdelta/core/models.py  
src/quantdelta/core/ports.py  
src/quantdelta/core/serialization.py  
docs/fleet.md  

TASKS  
T1: Implement frozen value types for Task, Score, TaskDelta, RunRecord, and Report  
    depends_on: (none)  
    refs: R1, R7, R11  
T2: Add validation logic to raise InvalidDataError on invalid field construction  
    depends_on: T1  
    refs: R2  
T3: Ensure RunRecord round-trip serialization preserves attribute values  
    depends_on: T1  
    refs: R3, R4, R12  
T4: Define Backend port with minimal required methods for task execution and resource reporting  
    depends_on: T1  
    refs: R10, R6  
T5: Define Scorer port to abstract scoring from backend implementation  
    depends_on: T1  
    refs: R9  
T6: Update documentation with model field notes and fleet link  
    depends_on: T1  
    refs: R7, R8, R12  

GATES  
- All unit tests in test_models.py, test_serialization.py, and test_import_boundary.py pass.  
- Round-trip JSONL deserialization of RunRecords produces identical instances as input.  
- No imports of httpx, subprocess, numpy, or typer are detected in quantdelta.core module.  
- Public API fields in Task, Score, TaskDelta, RunRecord, and Report match pinned snapshot in docs/decisions/core-contract-data-model-pydantic.md.  
- System passes import boundary check (no engine-specific names or dependencies).