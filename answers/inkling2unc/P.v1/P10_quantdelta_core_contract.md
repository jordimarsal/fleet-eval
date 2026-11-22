FILES
src/quantdelta/core/errors.py
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/serialization.py
src/quantdelta/core/schema.py
src/quantdelta/core/__init__.py
tests/unit/core/test_errors.py
tests/unit/core/test_models.py
tests/unit/core/test_import_boundary.py
tests/unit/core/test_public_api.py
tests/unit/core/test_serialization.py

TASKS
T1: Establish the shared core vocabulary and validated-error contract
    depends_on: (none)
    refs: R2, R6
T2: Implement frozen Task, Score and TaskDelta with validated construction and no mutable runtime state
    depends_on: T1
    refs: R1, R5
T3: Expand immutable RunRecord fields for subject identity, backend name/version, command, seed, timestamps, side-scoped per-task scores and resource metrics
    depends_on: T2
    refs: R7, R11
T4: Define Scorer and Backend ports using record data only; exclude concrete backends and engine vocabulary from public names
    depends_on: T1
    refs: R9, R10, R6
T5: Add stable schema constants and JSON serialization round-trip behavior for every model, including JSONL write and read reconstruction
    depends_on: T3
    refs: R3, R4, R12
T6: Build Reports purely from provided records via injected scorers or local aggregate rules, without network access, disk I/O or storage fallback reads
    depends_on: T4
    refs: R8
T7: Publish a narrow core API surface, pin field names in the snapshot test, and verify imports stay within lightweight standard dependencies
    depends_on: T5
    refs: R11, R5

GATES
- Run `pytest -q tests/unit/core tests/test_smoke.py` and confirm all frozen model, validation, import boundary, public-api and serialization expectations pass.
- Inspect each migrated error message and public symbol under `src/quantdelta/core/` to confirm no engine/file-format wording appears anywhere outside allowed filenames by reviewer annotation.
- Assert in isolation that importing `quantdelta.core` does not leave httpx, subprocess, numpy or typer present in sys.modules.
- Execute report aggregation using a fixture record set while filesystem operations are disabled; it must complete successfully for every Scorer implementation used by the suite.
- Verify JSON round-trip produces equal instances with unchanged attribute values across Task/Score/TaskDelta/RunRecord/Report edges and forward stable schema versions from previously generated JSONL records into new parsing logic.