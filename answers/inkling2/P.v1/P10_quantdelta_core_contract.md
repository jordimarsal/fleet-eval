FILES
src/quantdelta/core/errors.py
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/serialization.py
src/quantdelta/core/__init__.py
tests/unit/core/test_errors.py
tests/unit/core/test_models.py
tests/unit/core/test_public_api.py
tests/unit/core/test_serialization.py
tests/unit/core/test_import_boundary.py

TASKS
T1: Add neutral error and validation helpers
    depends_on: (none)
    refs: R2, R6, R12
T2: Define frozen Task, Score, TaskDelta, RunRecord, Report types
    depends_on: T1
    refs: R1, R2, R6, R7, R11, R12
T3: Define Scorer and Backend ports with record-driven signatures only
    depends_on: T2
    refs: R8, R9, R10, R6
T4: Implement JSON roundtrip serialization with stable schema versioning
    depends_on: T2
    refs: R3, R12, R6
T5: Implement JSONL reader/writer preserving records unchanged
    depends_on: T4
    refs: R4, R12
T6: Build reports from run records using injected scoring without I/O
    depends_on: T3, T4
    refs: R8, R9
T7: Pin public field names and import boundary in tests
    depends_on: T2, T3, T6
    refs: R5, R6, R11

GATES
python -m pytest tests/unit/core -q
verify quantdelta.core import has no httpx, subprocess, numpy or typer loaded by the targeted import test
run engine/file-format vocabulary audit across src/quantdelta/core for gguf, llama and kv cache tokens in identifiers, fields, docstrings, comments and error text
confirm serialized RunRecord/Report output includes a non-empty stable schema_version and produces equal instances after parsing through each path separately
confirm parsed JSONL lines reconstruct all input records with identical attribute values
review final diff against approved requirements before marking feature complete