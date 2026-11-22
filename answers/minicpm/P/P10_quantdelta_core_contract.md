FILES
src/quantdelta/core/models.py
src/quantdelta/core/serialization.py
src/quantdelta/core/ports.py
src/quantdelta/core/errors.py
tests/unit/core/test_models.py
tests/unit/core/test_serialization.py
tests/unit/core/test_public_api.py

TASKS
T1: Define frozen value types (Task, Score, TaskDelta, RunRecord, Report) with immutable attributes.
    depends_on: (none)
    refs: R1, R11
T2: Implement validation logic to raise InvalidDataError with field names for invalid construction data.
    depends_on: T1
    refs: R2
T3: Implement JSON and JSONL serialization/deserialization for RunRecord ensuring round-trip equality.
    depends_on: T1
    refs: R3, R4, R12
T4: Enforce import boundaries to prevent loading httpx, subprocess, numpy, or typer on core import.
    depends_on: (none)
    refs: R5
T5: Audit and refactor code to remove engine/file-format vocabulary (gguf, llama, kv cache) from core.
    depends_on: T1
    refs: R6
T6: Extend RunRecord schema to include model identity, backend name/version, command, seed, timestamps, per-task scores, and resource metrics.
    depends_on: T1
    refs: R7
T7: Ensure Report generation from RunRecords operates without network or disk access.
    depends_on: T1
    refs: R8
T8: Define Scorer port to depend only on record contents, decoupled from backend implementation.
    depends_on: T1
    refs: R9
T9: Define Backend port with exactly the methods needed for task execution and resource reporting.
    depends_on: T1
    refs: R10
T10: Update snapshot tests to pin stable public field names for all core value types.
    depends_on: T1
    refs: R11

GATES
- All unit tests in tests/unit/core/ pass, including import boundary checks.
- Round-trip serialization tests (JSON and JSONL) verify identical instance reconstruction.
- Static analysis confirms no forbidden imports (httpx, subprocess, numpy, typer) in quantdelta.core.
- Code search confirms absence of "gguf", "llama", and "kv cache" in src/quantdelta/core/.
- Report generation test verifies no network or disk I/O occurs during construction.
- Snapshot tests pass for public API field names.