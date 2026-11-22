FILES
src/quantdelta/core/errors.py
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/serialization.py
src/quantdelta/core/__init__.py
docs/architecture.md
docs/fleet.md
tests/unit/core/test_errors.py
tests/unit/core/test_models.py
tests/unit/core/test_public_api.py
tests/unit/core/test_serialization.py
tests/unit/core/test_import_boundary.py

TASKS
T1: Add InvalidDataError / CoreError and wire failure conversion into every constructor path
    depends_on: (none)
    refs: R2
T2: Define the frozen ContractModel base plus Task, Score and TaskDelta with strict validation
    depends_on: T1
    refs: R1, R6
T3: Implement ResourceMetrics, RunRecord and Report with identity-bearing fields; pure in-memory report build from records
    depends_on: T2
    refs: R7, R8, R11
T4: Provide JSON codec/decoder pair with stable schema_version field handling
    depends_on: T3
    refs: R3, R12
T5: Provide JSONL writer and reader over RunRecords
    depends_on: T4
    refs: R4
T6: Define Scorer and Backend ports with exactly the runner methods needed
    depends_on: T3
    refs: R9, R10
T7: Wire public __init__ surface to match pinned names and export list
    depends_on: T2, T6
    refs: R11

GATES
pytest tests/unit/core -v
python -m pytest tests/unit/core/test_import_boundary.py::test_importing_core_loads_no_forbidden_modules (clean child subprocess, no httpx/subprocess/numpy/typer)
python -m pytest tests/unit/core/test_import_boundary.py::test_core_sources_contain_no_engine_vocabulary (R6 scan across all core files incl docs additions if any)
json round-trip / parse_jsonl smoke checks demonstrating R3 and R4 with identical attribute values after encode/decode for a Task set carrying Report attributes plus explicit schema_version check on R12
black --check or ruff and pyright/mypy pass on src/quantdelta/core as required by repo tooling, then repeat for test edits