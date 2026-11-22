ROLE: implementation planner. A feature has been approved. You get the
approved requirements and the repository file tree BEFORE implementation.
Write the implementation plan with EXACTLY these three sections:

FILES
<repo-relative path of every file you would create or modify, one per line>

TASKS
T1: <short title>
    depends_on: (none)
    refs: R1, R2
T2: <short title>
    depends_on: T1
    refs: R3
(... ordered so dependencies come first; every requirement must be covered
 by the refs of at least one task)

GATES
<the verification gates you would run before closing the feature>

--- APPROVED REQUIREMENTS ---
R1: The system shall expose Task, Score, TaskDelta, RunRecord and Report as frozen value types whose attributes cannot be reassigned after creation.

R2: When a domain type is constructed with invalid data, the system shall raise an InvalidDataError naming the offending field.

R3: When a RunRecord is serialized to JSON and parsed back, the system shall produce an equal instance with identical attribute values.

R4: When RunRecords are written as JSONL lines and read back, the system shall reconstruct every record unchanged.

R5: The system shall not load httpx, subprocess, numpy or typer into sys.modules when quantdelta.core is imported.

R6: The system shall not use engine or file-format vocabulary such as gguf, llama or kv cache in any name, field or error message under src/quantdelta/core/.

R7: Each RunRecord shall carry the identity of the model or agent under test, the backend name and version, the exact command, the seed, timestamps, per-task scores for that side only, and resource metrics.

R8: When a Report is built from RunRecords, the system shall complete without network access or disk access.

R9: The system shall define the Scorer port so that scoring depends only on record contents and never on a concrete backend implementation.

R10: The system shall define the Backend port with exactly the methods a runner needs to execute tasks and report resources, and no engine-specific method.

R11: The system shall expose stable public field names for Task, Score, TaskDelta, RunRecord and Report as pinned by a snapshot test.

R12: Every serialized RunRecord and Report shall carry a schema_version field with a stable value so old JSONL files remain readable after format changes.

--- FEATURE TITLE ---
docs: add the model field notes and the fleet link

--- REPOSITORY FILE TREE (before implementation) ---
.gitignore
.opencode/agent/implementer.md
.opencode/agent/leader.md
.opencode/agent/reviewer.md
.opencode/agent/spec-author.md
AGENTS.md
HARNESS.md
README.md
docs/architecture.md
docs/clarity-style.md
docs/conventions.md
docs/decisions/core-contract-data-model-pydantic.md
docs/decisions/core-contract-shared-core-boundary.md
docs/fleet.md
docs/gauntlet-protocol.md
docs/specs.md
docs/verification.md
opencode.json
pyproject.toml
src/quantdelta/__init__.py
src/quantdelta/core/__init__.py
src/quantdelta/core/errors.py
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/serialization.py
tests/test_smoke.py
tests/unit/core/test_errors.py
tests/unit/core/test_import_boundary.py
tests/unit/core/test_models.py
tests/unit/core/test_public_api.py
tests/unit/core/test_serialization.py

Write ONLY the plan (the three sections). No prose outside them.