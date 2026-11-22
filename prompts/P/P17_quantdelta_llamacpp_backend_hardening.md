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
R1: The `/metrics` parser shall accept every numeric sample value legal in the Prometheus text format: decimal, scientific notation, a leading `+`, and the special tokens `NaN`, `+Inf` and `-Inf`.

R2: The `/metrics` parser shall accept an optional sample timestamp written as an integer or a decimal number (OpenMetrics).

R3: The `/metrics` parser shall accept label values that contain braces inside quotes, and escaped quotes inside label values.

R4: When a `/metrics` line still violates the exposition format, `metrics()` shall raise `LlamaCppMalformedResponseError` naming the offending line, as in R16 of feature 2.

R5: Memory recognition shall use only sample names ending in `_bytes`. The `"memory"` substring heuristic is removed: `memory_pool_count` or `process_memory_kib` never become a GiB value. Non-finite and negative samples remain unrecognized (feature 2, R14).

R6: `manifest()` shall cache the artifact sha256 across calls, but shall resolve `engine_version` on every call from the configuration pin or the most recent observed `system_fingerprint`. Repeated calls shall not re-hash the artifact and shall reflect a fingerprint observed after the first call. This supersedes the object-identity reading of R25 in feature 2; the closed feature 2 spec is not edited.

R7: A `LlamaCppBackend` instance shall be safe for concurrent `run()`, `metrics()` and `manifest()` calls from multiple threads: successful-run counters, the fingerprint and the artifact hash cache are updated under a lock, and concurrent `manifest()` calls compute the hash once. HTTP requests are never performed while holding the lock.

R8: `LlamaCppConfig` shall validate `base_url` with `urllib.parse`: scheme `http` or `https` case-insensitively and normalized to lower case, a non-empty hostname, an optional port in 1–65535, no whitespace, no query/fragment, and no userinfo (credentials). Path prefixes are preserved; trailing slashes are stripped.

R9: A chat completion with `finish_reason == "length"` or empty `content` shall be recorded as a success with its token counts and `error=None`. Truncation handling is the runner/scorer's responsibility and shall be documented in the adapter design; the frozen core contract is not changed.

R10: The amended R29 scope shall be documented and tested: the host, port, model identifier and file location come only from configuration, while the HTTP route suffixes and the sampling defaults are fixed adapter constants. This supersedes the literal wording of R29 in feature 2; the closed feature 2 spec is not edited.

R11: The test stub shall use a listen backlog of at least 512 and the suite shall include a 300-run, 64-thread concurrency test proving zero lost updates and an exact `tokens_per_second` ratio. The test runs offline and deterministically.

--- FEATURE TITLE ---
fix(llamacpp): harden the parser, manifest cache and concurrency

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
docs/decisions/llamacpp-backend-command-semantics.md
docs/decisions/llamacpp-backend-error-routing.md
docs/fleet.md
docs/gauntlet-protocol.md
docs/model-field-notes.md
docs/specs.md
docs/verification.md
opencode.json
pyproject.toml
src/quantdelta/__init__.py
src/quantdelta/backends/__init__.py
src/quantdelta/backends/llamacpp/__init__.py
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/errors.py
src/quantdelta/backends/llamacpp/manifest.py
src/quantdelta/core/__init__.py
src/quantdelta/core/errors.py
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/serialization.py
tests/test_smoke.py
tests/unit/backends/llamacpp/conftest.py
tests/unit/backends/llamacpp/test_backend.py
tests/unit/backends/llamacpp/test_boundary.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_llamacpp_errors.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_run.py
tests/unit/backends/llamacpp/test_stub_server.py
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
--- src/quantdelta/backends/llamacpp/backend.py (first 60 lines of 11152 bytes) ---
"""Adapter connecting to an externally started llama.cpp server."""

from __future__ import annotations

import math
import re
import time
from importlib.metadata import version as _package_version

import httpx

from quantdelta.backends.llamacpp.config import LlamaCppConfig
from quantdelta.backends.llamacpp.errors import (
    LlamaCppConfigError,
    LlamaCppHttpError,
    LlamaCppMalformedResponseError,
    LlamaCppTimeoutError,
    LlamaCppUnreachableError,
)
from quantdelta.backends.llamacpp.manifest import ReproManifest, build_command, hash_gguf
from quantdelta.core.models import ResourceMetrics, Task, TaskOutput

_GIB = 2**30

# One Prometheus exposition sample line: <name> [<labels>] <value> [<timestamp>].
# Values must be finite numbers; NaN/Inf are rejected on purpose so a bad probe
# can never poison the peak-memory maximum.
_SAMPLE_LINE_RE = re.compile(
    r"^(?P<name>[A-Za-z_:][A-Za-z0-9_:]*)"
    r"(?:\{[^{}]*\})?"
    r"[ \t]+"
    r"(?P<value>-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
    r"(?:[ \t]+(?P<timestamp>\d+))?$"
)


def _parse_exposition_samples(text: str) -> tuple[tuple[str, float], ...]:
    """Parse Prometheus text exposition into (metric name, value) samples."""
    samples: list[tuple[str, float]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = _SAMPLE_LINE_RE.match(line)
        if match is None:
            raise LlamaCppMalformedResponseError(f"invalid exposition line: {line}")
        samples.append((match["name"], float(match["value"])))
    return tuple(samples)


def _response_detail(response: httpx.Response) -> str:
    """Server-provided failure detail, falling back to the HTTP reason phrase."""
    try:
        payload = response.json()
    except ValueError:
        return response.reason_phrase
    if isinstance(payload, dict):
        error = payload.get("error")
        if isinstance(error, str) and error:
            return error
--- tests/unit/backends/llamacpp/test_metrics.py (first 60 lines of 9919 bytes) ---
"""Tests of LlamaCppBackend.metrics(): tokens/s aggregation and /metrics parsing."""

from __future__ import annotations

import math
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest

import quantdelta.backends.llamacpp.backend as backend_module
from quantdelta.backends.llamacpp.backend import LlamaCppBackend
from quantdelta.backends.llamacpp.config import LlamaCppConfig
from quantdelta.backends.llamacpp.errors import (
    LlamaCppHttpError,
    LlamaCppMalformedResponseError,
    LlamaCppTimeoutError,
    LlamaCppUnreachableError,
)
from quantdelta.core.models import Task

CHAT_PATH = "/v1/chat/completions"
METRICS_PATH = "/metrics"


def canned_response() -> dict[str, Any]:
    return {
        "id": "chatcmpl-stub",
        "object": "chat.completion",
        "created": 1750000000,
        "model": "stub-model",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": "hello from stub"},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 42, "completion_tokens": 7, "total_tokens": 49},
        "system_fingerprint": "fp-b8c3d2e1",
    }


@pytest.fixture()
def backend(
    stub_server: Any, make_backend: Callable[..., LlamaCppConfig]
) -> Iterator[LlamaCppBackend]:
    stub_server.register(CHAT_PATH, body=canned_response())
    instance = LlamaCppBackend(make_backend())
    try:
        yield instance
    finally:
        instance.close()


def make_task() -> Task:
    return Task(id="task-1", name="greeting", prompt="Say hello")


--- tests/unit/backends/llamacpp/test_run.py (first 60 lines of 9356 bytes) ---
"""Success-path tests of LlamaCppBackend.run(): request shape and TaskOutput."""

from __future__ import annotations

import math
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest

from quantdelta.backends.llamacpp.backend import LlamaCppBackend
from quantdelta.backends.llamacpp.config import LlamaCppConfig
from quantdelta.core.models import Task

CHAT_PATH = "/v1/chat/completions"


def canned_response() -> dict[str, Any]:
    return {
        "id": "chatcmpl-stub",
        "object": "chat.completion",
        "created": 1750000000,
        "model": "stub-model",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": "hello from stub"},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 42, "completion_tokens": 7, "total_tokens": 49},
        "system_fingerprint": "fp-b8c3d2e1",
    }


@pytest.fixture()
def backend(
    stub_server: Any, make_backend: Callable[..., LlamaCppConfig]
) -> Iterator[LlamaCppBackend]:
    stub_server.register(CHAT_PATH, body=canned_response())
    instance = LlamaCppBackend(make_backend())
    try:
        yield instance
    finally:
        instance.close()


def make_task() -> Task:
    return Task(id="task-1", name="greeting", prompt="Say hello")


def test_run_posts_exact_request_body_without_seed(
    backend: LlamaCppBackend, stub_server: Any
) -> None:
    task = make_task()

    backend.run(task=task, seed=None)

    (request,) = stub_server.requests
--- tests/unit/backends/llamacpp/test_manifest.py (first 60 lines of 9073 bytes) ---
import hashlib
import re
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any

import pytest

from quantdelta.backends.llamacpp.backend import LlamaCppBackend
from quantdelta.backends.llamacpp.config import LlamaCppConfig
from quantdelta.backends.llamacpp.errors import LlamaCppConfigError
from quantdelta.backends.llamacpp.manifest import ReproManifest, build_command, hash_gguf
from quantdelta.core.models import Task


def _existing_gguf(tmp_path: Path) -> Path:
    gguf = tmp_path / "model.gguf"
    gguf.write_bytes(b"gguf-magic-bytes")
    return gguf


def _config_kwargs(gguf: Path, **overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "base_url": "http://127.0.0.1:8080",
        "model_id": "test-model",
        "gguf_path": gguf,
        "timeout_s": 5.0,
    }
    base.update(overrides)
    return base


def test_hash_gguf_matches_one_shot_digest_on_a_file_larger_than_one_chunk(
    tmp_path: Path,
) -> None:
    size = 3 * 1024 * 1024 + 7  # larger than the 1 MiB streaming chunk
    payload = (b"quantdelta-gguf-streaming-payload-" * ((size // 32) + 1))[:size]
    gguf = tmp_path / "large.gguf"
    gguf.write_bytes(payload)

    digest = hash_gguf(gguf)

    assert digest == hashlib.sha256(payload).hexdigest()
    assert re.fullmatch(r"[0-9a-f]{64}", digest)


def test_hash_gguf_is_deterministic_across_calls(tmp_path: Path) -> None:
    gguf = _existing_gguf(tmp_path)

    assert hash_gguf(gguf) == hash_gguf(gguf)


def test_build_command_pins_the_argv_shape_for_default_sampling(tmp_path: Path) -> None:
    config = LlamaCppConfig(**_config_kwargs(_existing_gguf(tmp_path)))

    command = build_command(config)

    assert command == (
        "POST",
        "http://127.0.0.1:8080/v1/chat/completions",
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

Write ONLY the plan (the three sections). No prose outside them.