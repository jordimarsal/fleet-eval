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
R1: The `Scorer` port shall score one task output at a time: `score(*, task: Task, output: TaskOutput) -> Score`. The signature is keyword-only, references only core types, keeps the `metric: str` attribute, and replaces the `record: RunRecord` signature. The scorer returns one score per successful output; replicate aggregation stays outside the core.

R2: The core shall expose two frozen value types for next-token probabilities: `TokenAlternative` with `token: str` and `logprob: float`, and `TokenLogprob` with `token: str`, `logprob: float` and `top_logprobs: tuple[TokenAlternative, ...] = ()`. Both shall validate that the token is non-empty and the log-probability is finite and `<= 0`. `TokenLogprob` shall reject duplicate alternative token strings; the generated token may also appear in `top_logprobs`, and the order is preserved.

R3: `TaskOutput` shall carry an optional `logprobs: tuple[TokenLogprob, ...] | None = None`. `None` means log-probabilities were not requested; an empty tuple means they were requested but the engine returned no generated tokens. The field is additive and does not change `RunRecord` or the JSONL format.

R4: The core shall expose a frozen `TaskKL` type with `task_id: str`, `divergence: float`, `reference_mass: float` and `variant_mass: float`. `task_id` shall be non-empty, `divergence` finite and `>= 0`, and both masses finite in `[0, 1]`. The type carries the result of one KL estimate and the probability mass that the estimate retained on each side.

R5: `Report` shall carry three additive fields: `kl_divergence: float | None = None`, `task_kl: tuple[TaskKL, ...] = ()` and `kl_method: str | None = None`. They shall be all-or-nothing: either all absent/empty, or `task_kl` non-empty, `kl_divergence` finite and `>= 0`, and `kl_method` non-empty. `task_kl` task ids shall be unique and each shall exist in `deltas`; `kl_divergence` shall equal the arithmetic mean of the `TaskKL.divergence` values within an absolute tolerance of `1e-9`. A report with no KL fields shall remain valid.

R6: The serialized schema shall stay version `"1"`. A pre-feature `Report` JSON without the KL fields shall parse with the defaults; a new `Report` with KL fields shall round-trip through `to_json`/`from_json` unchanged; unknown fields shall still be rejected; `RunRecord`, `to_jsonl` and `parse_jsonl` shall be unchanged. ADR-008 shall record the additive policy and its relationship with ADR-001 and R12.

R7: `TokenAlternative`, `TokenLogprob` and `TaskKL` shall be exported from `quantdelta.core` and pinned by the public API snapshot; the `Scorer` signature change shall be pinned too. The core shall add no runtime dependency and shall keep its import boundary (no httpx, no I/O, no adapter vocabulary).

R8: Every invalid value shall raise `InvalidDataError` naming the offending field (or `<root>` only when no single field applies). At minimum: NaN/Inf/positive log-probabilities, empty tokens, duplicate alternative tokens, masses outside `[0, 1]`, negative or non-finite KL, duplicate `TaskKL` ids, a `TaskKL` id absent from `deltas`, a KL mean mismatch, and a partial KL field set. Tests shall cover each rule, the old-report compatibility, the new round-trip, the port signature and the public exports.

--- FEATURE TITLE ---
feat(core)!: score task outputs, carry logprobs and report KL

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
docs/decisions/llamacpp-backend-threading.md
docs/decisions/llamacpp-manifest-cache.md
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
tests/unit/backends/llamacpp/test_concurrency.py
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

--- src/quantdelta/backends/llamacpp/backend.py (first 60 lines of 13855 bytes) ---
"""Adapter connecting to an externally started llama.cpp server."""

from __future__ import annotations

import math
import re
import threading
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
# Accepted value tokens (feature 3 R1): decimal, scientific notation, a leading
# sign, and the special tokens NaN/+Inf/-Inf. Non-finite values parse fine and
# are skipped by the memory recognizer instead of being treated as malformed.
# Labels may contain braces inside quotes and escaped quotes (R3); timestamps
# may be integer or decimal OpenMetrics seconds (R2). Quoted/dotted metric
# names stay unsupported (documented non-goal).
_VALUE = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|NaN|[+-]Inf"
_LABELS = r'\{(?:[^"{}]|"(?:\\.|[^"\\])*")*\}'
_SAMPLE_LINE_RE = re.compile(
    rf"^(?P<name>[A-Za-z_:][A-Za-z0-9_:]*)(?:{_LABELS})?[ \t]+"
    rf"(?P<value>{_VALUE})(?:[ \t]+(?P<timestamp>[+-]?\d+(?:\.\d*)?))?$"
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
--- tests/unit/backends/llamacpp/test_metrics.py (first 60 lines of 13619 bytes) ---
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
--- tests/unit/backends/llamacpp/test_manifest.py (first 60 lines of 10951 bytes) ---
import hashlib
import re
from collections.abc import Callable
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
--- tests/unit/backends/llamacpp/test_run.py (first 60 lines of 10851 bytes) ---
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
--- tests/unit/backends/llamacpp/test_concurrency.py (first 60 lines of 8187 bytes) ---
"""Concurrency guarantees for LlamaCppBackend (feature 3 R7/R11, ADR-006).

One backend instance shared across threads: successful-run counters must stay
exact, metrics() must remain callable while runs are in flight, and concurrent
manifest() calls must compute the artifact hash exactly once. The R11 storm
additionally proves the stub's listen backlog absorbs a 64-way connection burst
and that tokens_per_second equals sum(tokens_out) / sum(duration_s).
"""

from __future__ import annotations

import hashlib
import math
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from quantdelta.backends.llamacpp.backend import LlamaCppBackend
from quantdelta.backends.llamacpp.config import LlamaCppConfig
from quantdelta.backends.llamacpp.manifest import hash_gguf
from quantdelta.core.models import Task, TaskOutput

CHAT_PATH = "/v1/chat/completions"

_STORM_THREADS = 64
_RUNS_PER_THREAD = 5
_TOKENS_OUT_PER_RUN = 7


def canned_response() -> dict[str, Any]:
    usage = {
        "prompt_tokens": 3,
        "completion_tokens": _TOKENS_OUT_PER_RUN,
        "total_tokens": 10,
    }
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
        "usage": usage,
        "system_fingerprint": "fp-concurrent",
    }


def make_task() -> Task:
    return Task(id="task-conc", name="greeting", prompt="Say hello")



Write ONLY the plan (the three sections). No prose outside them.