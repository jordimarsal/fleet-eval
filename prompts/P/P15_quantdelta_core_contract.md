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

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- tests/unit/core/test_models.py (first 60 lines of 20517 bytes) ---
import math
import types
from datetime import UTC, datetime, timedelta, timezone
from typing import Any, cast

import pytest
from pydantic import ValidationError

from quantdelta.core import InvalidDataError
from quantdelta.core.models import (
    SCHEMA_VERSION,
    JsonValue,
    Report,
    ResourceMetrics,
    RunRecord,
    Score,
    Task,
    TaskDelta,
    TaskOutput,
)


def test_task_constructs_with_required_fields() -> None:
    task = Task(id="t1", name="Addition", prompt="Solve 2 + 2")

    assert task.id == "t1"
    assert task.name == "Addition"
    assert task.prompt == "Solve 2 + 2"


def test_task_optional_fields_have_defaults() -> None:
    task = Task(id="t1", name="Addition", prompt="p")

    assert task.description == ""
    assert task.tags == ()
    assert task.payload == {}


def test_payload_accepts_nested_json_values_and_is_a_read_only_view() -> None:
    payload: dict[str, JsonValue] = {
        "difficulty": "easy",
        "limits": {"max_tokens": 64},
        "allowed_operators": ["+", "-"],
        "ratio": 0.5,
        "flagged": True,
        "note": None,
    }
    task = Task(id="t1", name="n", prompt="p", payload=payload)

    assert isinstance(task.payload, types.MappingProxyType)
    assert task.payload["limits"] == {"max_tokens": 64}


def test_payload_item_mutation_raises_type_error() -> None:
    task = Task(id="t1", name="n", prompt="p", payload={"k": 1})

    # The static type already forbids assignment; the cast reaches the runtime view.
    with pytest.raises(TypeError):
        cast(dict[str, JsonValue], task.payload)["other"] = 2

--- src/quantdelta/core/models.py (first 60 lines of 11563 bytes) ---
"""Frozen domain value objects of the shared measurement contract."""

from __future__ import annotations

import math
import re
import types
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_serializer,
    field_validator,
    model_validator,
)

from quantdelta.core.errors import InvalidDataError

type JsonValue = bool | int | float | str | list[JsonValue] | dict[str, JsonValue] | None

SCHEMA_VERSION = "1"


def _to_invalid_data_error(error: ValidationError) -> InvalidDataError:
    first = error.errors(include_url=False)[0]
    loc = first.get("loc") or ()
    field = str(loc[0]) if loc else "<root>"
    message = str(first.get("msg", ""))
    return InvalidDataError(field=field, reason=message.removeprefix("Value error, "))


class ContractModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", validate_default=True)

    def __init__(self, /, **data: object) -> None:
        try:
            super().__init__(**data)
        except ValidationError as caught:
            raise _to_invalid_data_error(caught) from caught


class Task(ContractModel):
    id: str
    name: str
    description: str = ""
    prompt: str
    tags: tuple[str, ...] = ()
    payload: Mapping[str, JsonValue] = {}

    @field_validator("id", "name", "prompt")
    @classmethod
    def _non_empty(cls, value: str) -> str:
        if value:
            return value
        msg = "must not be empty"
--- tests/unit/core/test_public_api.py (first 60 lines of 8386 bytes) ---
"""Public API checks for quantdelta.core: exports, protocol surfaces and snapshot pins."""

from __future__ import annotations

import inspect
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import get_type_hints

import pytest

import quantdelta.core as core
from quantdelta.core import (
    SCHEMA_VERSION,
    Backend,
    ContractModel,
    CoreError,
    InvalidDataError,
    Report,
    ResourceMetrics,
    RunRecord,
    Score,
    Scorer,
    Task,
    TaskDelta,
    TaskOutput,
    from_json,
    parse_jsonl,
    to_json,
    to_jsonl,
)

EXPECTED_PUBLIC_SURFACE = [
    "SCHEMA_VERSION",
    "Backend",
    "ContractModel",
    "CoreError",
    "InvalidDataError",
    "Report",
    "ResourceMetrics",
    "RunRecord",
    "Score",
    "Scorer",
    "Task",
    "TaskDelta",
    "TaskOutput",
    "from_json",
    "parse_jsonl",
    "to_json",
    "to_jsonl",
]


def test_core_all_matches_the_public_surface() -> None:
    assert core.__all__ == EXPECTED_PUBLIC_SURFACE


def test_every_exported_name_is_importable_from_the_package_root() -> None:
    exported = {name: getattr(core, name) for name in EXPECTED_PUBLIC_SURFACE}
--- tests/unit/core/test_serialization.py (first 60 lines of 7616 bytes) ---
"""Lossless JSON and JSONL round-trip checks for the core value types."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

import pytest

from quantdelta.core import InvalidDataError
from quantdelta.core.models import (
    ContractModel,
    Report,
    ResourceMetrics,
    RunRecord,
    Score,
    Task,
    TaskDelta,
    TaskOutput,
)
from quantdelta.core.serialization import (
    SCHEMA_VERSION,
    from_json,
    parse_jsonl,
    to_json,
    to_jsonl,
)


def _task() -> Task:
    return Task(
        id="t1",
        name="Addition",
        description="warm-up task",
        prompt="Solve 2 + 2",
        tags=("math", "easy"),
        payload={
            "difficulty": "easy",
            "limits": {"max_tokens": 64},
            "allowed_operators": ["+", "-"],
            "ratio": 0.5,
            "flagged": True,
            "note": None,
        },
    )


def _score() -> Score:
    return Score(value=0.95, metric="accuracy", n_samples=10)


def _delta() -> TaskDelta:
    return TaskDelta(
        task_id="t1",
        reference=Score(value=0.8, metric="accuracy", n_samples=4),
        variant=Score(value=0.75, metric="accuracy", n_samples=4),
        delta=-0.05,
        ci_lower=-0.12,
        ci_upper=0.02,
    )
--- src/quantdelta/core/serialization.py (first 60 lines of 3297 bytes) ---
"""Lossless JSON codecs for the shared measurement contract."""

from __future__ import annotations

import json
from collections.abc import Iterable

from pydantic import ValidationError

from quantdelta.core.errors import InvalidDataError
from quantdelta.core.models import SCHEMA_VERSION as SCHEMA_VERSION
from quantdelta.core.models import ContractModel, RunRecord, _to_invalid_data_error


def to_json(value: ContractModel) -> str:
    """Serialize one value object into a single canonical JSON document."""
    return value.model_dump_json()


def from_json[T: ContractModel](text: str | bytes, *, model: type[T]) -> T:
    """Parse one JSON document into ``model``.

    Malformed documents and validation failures surface as InvalidDataError;
    records carrying an unsupported schema_version are rejected outright.
    """
    try:
        document = json.loads(text)
    except json.JSONDecodeError as caught:
        raise InvalidDataError(field="<root>", reason=f"invalid JSON: {caught.msg}") from caught
    try:
        parsed = model.model_validate(document)
    except ValidationError as caught:
        raise _to_invalid_data_error(caught) from caught
    _reject_unsupported_schema_version(parsed)
    return parsed


def _reject_unsupported_schema_version(instance: ContractModel, *, context: str = "") -> None:
    version: object = getattr(instance, "schema_version", None)
    if not isinstance(version, str) or version == SCHEMA_VERSION:
        return
    reason = f"unsupported schema_version '{version}' (expected '{SCHEMA_VERSION}')"
    if context:
        reason = f"{context}{reason}"
    raise InvalidDataError(field="schema_version", reason=reason)


def to_jsonl(records: Iterable[RunRecord]) -> str:
    """Serialize records as JSON Lines: one document per line, trailing newline."""
    return "".join(f"{record.model_dump_json()}\n" for record in records)


def parse_jsonl(text: str) -> tuple[RunRecord, ...]:
    """Parse JSON Lines into RunRecords.

    Blank lines are skipped; malformed or invalid lines raise InvalidDataError
    naming the offending field and carrying their 1-based line number.
    """
    records: list[RunRecord] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
--- tests/unit/core/test_import_boundary.py (first 57 lines of 1782 bytes) ---
"""Import-boundary checks for quantdelta.core (R5: module loading, R6: vocabulary)."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

FORBIDDEN_MODULES = ("httpx", "subprocess", "numpy", "typer")
FORBIDDEN_VOCABULARY = re.compile(r"gguf|llama|kv[-_ ]?cache", re.IGNORECASE)


def _core_root() -> Path:
    return Path(__file__).resolve().parents[3] / "src" / "quantdelta" / "core"


def test_importing_core_loads_no_forbidden_modules() -> None:
    # The child interpreter must start clean; only its sys.modules matters (R5).
    code = "\n".join(
        [
            "import sys",
            "import quantdelta.core",
            f"forbidden = {list(FORBIDDEN_MODULES)}",
            "loaded = sorted(set(sys.modules) & set(forbidden))",
            "if loaded:",
            '    raise SystemExit("forbidden modules loaded: " + ", ".join(loaded))',
        ]
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        cwd=_core_root().parents[2],
    )

    assert result.returncode == 0, f"child failed:\n{result.stdout}\n{result.stderr}"


def _core_files() -> list[Path]:
    root = _core_root()
    files = [
        path
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    ]
    return sorted(files)


def test_core_sources_contain_no_engine_vocabulary() -> None:
    offenders: list[str] = []
    for path in _core_files():
        match = FORBIDDEN_VOCABULARY.search(path.read_text(encoding="utf-8"))
        if match is not None:
            offenders.append(f"{path.name}: '{match.group(0)}'")

    assert not offenders, "engine vocabulary under src/quantdelta/core/: " + "; ".join(offenders)
--- tests/unit/core/test_errors.py (first 58 lines of 1690 bytes) ---
from typing import Any

import pytest

from quantdelta.core import CoreError, InvalidDataError
from quantdelta.core.models import Score, Task


def test_invalid_data_error_exposes_field_and_reason() -> None:
    error = InvalidDataError(field="n_samples", reason="must be >= 0")

    assert error.field == "n_samples"
    assert error.reason == "must be >= 0"


def test_str_always_names_the_field_first() -> None:
    error = InvalidDataError(field="value", reason="must be finite")

    assert str(error) == "value: must be finite"


def test_root_field_is_named_in_message() -> None:
    error = InvalidDataError(field="<root>", reason="malformed document at line 3")

    assert "<root>" in str(error)
    assert "line 3" in str(error)


def test_invalid_data_error_is_a_core_error() -> None:
    with pytest.raises(CoreError):
        raise InvalidDataError(field="id", reason="empty")


def test_core_error_carries_a_plain_message() -> None:
    error = CoreError("contract violated")

    assert str(error) == "contract violated"


def test_missing_required_field_error_carries_its_reason() -> None:
    kwargs: dict[str, Any] = {"name": "Addition", "prompt": "Solve 2 + 2"}
    with pytest.raises(InvalidDataError) as excinfo:
        Task(**kwargs)

    error = excinfo.value
    assert error.field == "id"
    assert error.reason
    assert error.reason in str(error)


def test_failed_value_validator_error_carries_its_reason() -> None:
    with pytest.raises(InvalidDataError) as excinfo:
        Score(value=float("nan"), metric="accuracy", n_samples=1)

    error = excinfo.value
    assert error.field == "value"
    assert error.reason
    assert error.reason in str(error)
--- src/quantdelta/core/__init__.py (first 41 lines of 787 bytes) ---
"""Public API of quantdelta.core: value types, ports, errors and serializers."""

from quantdelta.core.errors import CoreError, InvalidDataError
from quantdelta.core.models import (
    ContractModel,
    Report,
    ResourceMetrics,
    RunRecord,
    Score,
    Task,
    TaskDelta,
    TaskOutput,
)
from quantdelta.core.ports import Backend, Scorer
from quantdelta.core.serialization import (
    SCHEMA_VERSION,
    from_json,
    parse_jsonl,
    to_json,
    to_jsonl,
)

__all__ = [
    "SCHEMA_VERSION",
    "Backend",
    "ContractModel",
    "CoreError",
    "InvalidDataError",
    "Report",
    "ResourceMetrics",
    "RunRecord",
    "Score",
    "Scorer",
    "Task",
    "TaskDelta",
    "TaskOutput",
    "from_json",
    "parse_jsonl",
    "to_json",
    "to_jsonl",
]

Write ONLY the plan (the three sections). No prose outside them.