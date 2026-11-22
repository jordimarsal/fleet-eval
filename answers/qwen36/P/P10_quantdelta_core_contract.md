FILES
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/serialization.py
src/quantdelta/core/errors.py
src/quantdelta/core/__init__.py
tests/unit/core/test_models.py
tests/unit/core/test_serialization.py
tests/unit/core/test_public_api.py
tests/unit/core/test_import_boundary.py
tests/unit/core/test_errors.py

TASKS
T1: Define frozen value types Task, Score, TaskDelta, RunRecord and Report with immutable attributes.
    depends_on: (none)
    refs: R1, R7, R11
T2: Implement InvalidDataError that names the offending field on domain construction failures.
    depends_on: T1
    refs: R2
T3: Add schema_version to every serialized RunRecord and Report so old JSONL files remain readable after format changes.
    depends_on: T1
    refs: R12
T4: Implement RunRecord serialization/deserialization via JSON round-trip preserving all fields including schema_version.
    depends_on: T3
    refs: R3, R4, R7, R12
T5: Implement JSONL line-based write/read for RunRecords preserving order and content.
    depends_on: T4
    refs: R4
T6: Verify quantdelta.core imports without loading httpx, subprocess, numpy or typer into sys.modules.
    depends_on: T1
    refs: R5
T7: Audit src/quantdelta/core/ for engine/file-format vocabulary (gguf, llama, kv cache) in names, fields and error messages.
    depends_on: T1, T2
    refs: R6
T8: Build Report from RunRecords using only record contents; verify no network or disk access occurs during report creation.
    depends_on: T1, T4
    refs: R8
T9: Define Scorer port that accepts record contents and returns scores without depending on a concrete backend implementation.
    depends_on: T1
    refs: R9
T10: Define Backend port with exactly the methods needed by a runner to execute tasks and report resources, excluding engine-specific methods.
    depends_on: T1
    refs: R10
T11: Pin public field names of Task, Score, TaskDelta, RunRecord and Report via snapshot test.
    depends_on: T1
    refs: R11

GATES
- pytest tests/unit/core/test_models.py passes (frozen types, invalid data errors, schema_version present)
- pytest tests/unit/core/test_serialization.py passes (JSON round-trip equality, JSONL line reconstruction)
- pytest tests/unit/core/test_import_boundary.py passes (no httpx/subprocess/numpy/typer loaded)
- grep -rE 'gguf|llama|kv.cache' src/quantdelta/core/ returns zero matches
- pytest tests/unit/core/test_public_api.py passes (snapshot test for pinned field names)
- smoke test importing quantdelta.core completes without side effects