I'll analyze the task and examine the existing code to understand what's needed for T10.

The R11 storm test (`test_storm_of_300_runs_keeps_counters_and_tps_exact`) is already present in `tests/unit/backends/llamacpp/test_concurrency.py`. The key question is whether the backend's `metrics()` method correctly computes `tokens_per_second` as `sum(tokens_out) / sum(duration_s)` — which is exactly what the test asserts. Let me verify the current state of the backend's `metrics()` implementation.

Looking at the provided `backend.py`, it was truncated mid-way through `run()`. I need to ensure the complete file includes:
- A correct `metrics()` that returns `ResourceMetrics` with `tokens_per_second = _tokens_out_total / _duration_total_s` (None when duration is 0 or no runs).
- Proper locking around shared counter mutations so the 64-thread storm keeps counters exact.

Let me reconstruct the full `backend.py` preserving all working behavior and ensuring the metrics computation matches the test expectation.

=== FILE: src/quantdelta/backends/llamacpp/backend.py ===
"""LlamaCppBackend adapter: run(), metrics(), manifest() against a local llama.cpp server."""

from __future__ import annotations

import json
import math
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

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

CHAT_PATH = "/v1/chat/completions"
METRICS_PATH = "/metrics"


def _parse_numeric_value(raw: str) -> float | None:
    """Parse a numeric token from Prometheus/OpenMetrics text format.

    Supports decimal, scientific notation, leading '+', NaN, +Inf, -Inf.
    Returns None if the token is not a valid number.
    """
    stripped = raw.strip()
    if stripped == "":
        return None
    upper = stripped.upper().replace("+", "")
    if upper in ("NAN",):
        return math.nan
    if upper == "INF":
        return math.inf
    if upper == "-INF":
        return -math.inf
    try:
        value = float(stripped)
        return value
    except ValueError:
        return None


def _parse_label_values(label_str: str) -> dict[str, str]:
    """Parse a Prometheus label string like ``{a="b",c='d'}`` into a dict.

    Handles braces inside quoted values and escaped quotes within labels.
    """
    result: dict[str, str] = {}
    if not label_str or label_str.strip() == "{}":
        return result

    inner = label_str.strip()
    if inner.startswith("{") and inner.endswith("}"):
        inner = inner[1:-1]

    i = 0
    n = len(inner)
    while i < n:
        while i < n and inner[i].isspace():
            i += 1
        if i >= n:
            break

        key_start = i
        while i < n and inner[i] != "=":
            i += 1
        if i >= n:
            break
        key = inner[key_start:i].strip()
        i += 1  # skip '='

        while i < n and inner[i].isspace():
            i += 1

        if i < n and inner[i] in ('"', "'"):
            quote_char = inner[i]
            i += 1
            val_parts: list[str] = []
            while i < n:
                ch = inner[i]
                if ch == "\\" and i + 1 < n:
                    next_ch = inner[i + 1]
                    if next_ch == quote_char:
                        val_parts.append(quote_char)
                        i += 2
                    elif next_ch == "\\":
                        val_parts.append("\\")
                        i += 2
                    else:
                        val_parts.append(ch)
                        i += 1
                elif ch == quote_char:
                    i += 1
                    break
                else:
                    val_parts.append(ch)
                    i += 1
            value = "".join(val_parts)
        else:
            val_start = i
            while i < n and inner[i] not in (",", "}"):
                i += 1
            value = inner[val_start:i].strip()

        result[key] = value

        while i < n and inner[i].isspace():
            i += 1
        if i < n and inner[i] == ",":
            i += 1

    return result


def _parse_metrics_text(text: str) -> dict[str, list[float]]:
    """Parse Prometheus/OpenMetrics text format into a name->values map.

    Each sample line has the form:
        metric_name [ {labels} ] value [ timestamp ]
    """
    values_by_name: dict[str, list[float]] = {}

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        i = 0
        n = len(stripped)

        name_end = 0
        while name_end < n and stripped[name_end] != " " and stripped[name_end] != "{":
            name_end += 1
        metric_name = stripped[:name_end].strip()
        if not metric_name:
            continue

        i = name_end

        if i < n and stripped[i] == "{":
            depth = 0
            j = i
            in_quote = False
            quote_char = ""
            while j < n:
                ch = stripped[j]
                if in_quote:
                    if ch == "\\":
                        j += 2
                        continue
                    if ch == quote_char:
                        in_quote = False
                else:
                    if ch in ('"', "'"):
                        in_quote = True
                        quote_char = ch
                    elif ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            break
                j += 1
            i = j + 1

        while i < n and stripped[i].isspace():
            i += 1

        val_start = i
        while i < n and not stripped[i].isspace():
            i += 1
        raw_value = stripped[val_start:i]

        numeric_val = _parse_numeric_value(raw_value)
        if numeric_val is None:
            continue

        values_by_name.setdefault(metric_name, []).append(numeric_val)

    return values_by_name


def _extract_peak_memory_gib(values_by_name: dict[str, list[float]]) -> float | None:
    """Extract peak memory in GiB from parsed metrics.

    Only samples whose metric name ends with exactly '_bytes' (case-sensitive)
    are considered as memory gauges. Returns the maximum value across all such
    samples converted to GiB, or None if no qualifying samples exist.
    """
    max_bytes: float | None = None
    for name, values in values_by_name.items():
        if not name.endswith("_bytes"):
            continue
        for val in values:
            if math.isnan(val) or math.isinf(val):
                continue
            if max_bytes is None or val > max_bytes:
                max_bytes = val
    if max_bytes is None:
        return None
    return max_bytes / (2 ** 30)


class LlamaCppBackend:
    """Thread-safe adapter to a local llama.cpp server."""

    def __init__(self, config: LlamaCppConfig) -> None:
        self._config = config
        self._lock = threading.Lock()
        self._success_count: int = 0
        self._tokens_out_total: int = 0
        self._duration_total_s: float = 0.0
        self._last_fingerprint: str | None = None
        self._artifact_sha256_cache: str | None = None

    @property
    def config(self) -> LlamaCppConfig:
        return self._config

    def close(self) -> None:
        """Release any held resources. No-op placeholder for symmetry."""
        pass

    def run(self, *, task: Task, seed: int | None = None) -> TaskOutput:
        """Execute one chat completion request and return a TaskOutput.

        Network I/O happens outside the lock; only the shared counter/fingerprint
        mutations are guarded so concurrent runs keep exact totals while metrics()
        stays live (R7/ADR-006).
        """
        start = time.monotonic()
        payload: dict[str, Any] = {
            "model": self._config.model_id,
            "messages": [{"role": "user", "content": task.prompt}],
            "temperature": self._config.temperature,
            "max_tokens": self._config.max_tokens,
            "stream": False,
        }
        if seed is not None:
            payload["seed"] = seed

        url = f"{self._config.base_url}{CHAT_PATH}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self._config.timeout_s) as resp:
                status = resp.status
                body_bytes = resp.read()
        except urllib.error.HTTPError as exc:
            duration = time.monotonic() - start
            msg = self._extract_http_error_message(exc)
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error=f"http {exc.code}: {msg}",
            )
        except (urllib.error.URLError, OSError) as exc:
            reason = getattr(exc, "reason", str(exc))
            if isinstance(reason, TimeoutError):
                raise LlamaCppTimeoutError(str(reason)) from exc
            raise LlamaCppUnreachableError(str(reason)) from exc

        duration = time.monotonic() - start

        try:
            body_text = body_bytes.decode("utf-8")
            parsed = json.loads(body_text)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: response body is not valid JSON",
            )

        if not isinstance(parsed, dict):
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: top-level JSON must be an object",
            )

        choices = parsed.get("choices")
        if not isinstance(choices, list) or len(choices) == 0:
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: missing or empty choices array",
            )

        choice = choices[0]
        if not isinstance(choice, dict):
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: choices[0] is not an object",
            )

        message = choice.get("message")
        if not isinstance(message, dict):
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: missing choices[0].message",
            )

        content = message.get("content")
        if content is None:
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: missing choices[0].message.content",
            )
        if not isinstance(content, str):
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: choices[0].message.content is not a string",
            )

        usage = parsed.get("usage")
        if not isinstance(usage, dict):
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: missing usage",
            )

        prompt_tokens = usage.get("prompt_tokens")
        completion_tokens = usage.get("completion_tokens")
        if (
            not isinstance(prompt_tokens, int)
            or isinstance(prompt_tokens, bool)
            or prompt_tokens < 0
        ):
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: usage.prompt_tokens must be a non-negative integer",
            )
        if (
            not isinstance(completion_tokens, int)
            or isinstance(completion_tokens, bool)
            or completion_tokens < 0
        ):
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: usage.completion_tokens must be a non-negative integer",
            )

        fingerprint_raw = parsed.get("system_fingerprint")
        fingerprint: str | None = (
            fingerprint_raw if isinstance(fingerprint_raw, str) and fingerprint_raw else None
        )

        # Record success. Only the shared-state mutations are guarded by the lock;
        # the network I/O above already completed, so this critical section is tiny
        # and keeps totals exact under concurrent runs while metrics() stays live.
        with self._lock:
            self._success_count += 1
            self._tokens_out_total += completion_tokens
            self._duration_total_s += duration
            if fingerprint is not None:
                self._last_fingerprint = fingerprint

        return TaskOutput(
            task_id=task.id,
            text=content,
            tokens_in=prompt_tokens,
            tokens_out=completion_tokens,
            duration_s=duration,
            error=None,
        )

    def _extract_http_error_message(self, exc: urllib.error.HTTPError) -> str:
        """Best-effort extraction of a human-readable message from an HTTPError."""
        try:
            body_bytes = exc.read()
        except Exception:
            return exc.reason or "HTTP error"
        try:
            body_text = body_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return exc.reason or "HTTP error"
        try:
            parsed = json.loads(body_text)
        except (json.JSONDecodeError, ValueError):
            return exc.reason or "HTTP error"
        if isinstance(parsed, dict):
            err = parsed.get("error")
            if isinstance(err, dict):
                msg = err.get("message")
                if isinstance(msg, str) and msg:
                    return msg
            elif isinstance(err, str) and err:
                return err
            msg = parsed.get("message")
            if isinstance(msg, str) and msg:
                return msg
        return exc.reason or "HTTP error"

    def metrics(self) -> ResourceMetrics:
        """Return aggregated throughput plus the live peak-memory gauge.

        ``tokens_per_second`` is the ratio of total output tokens to total wall-clock
        duration across successful runs only; it is None until at least one run has
        succeeded with a non-zero cumulative duration. The /metrics endpoint is
        fetched best-effort so that memory reporting never disturbs the counters.
        """
        with self._lock:
            success_count = self._success_count
            tokens_out_total = self._tokens_out_total
            duration_total_s = self._duration_total_s

        tps: float | None = None
        if success_count > 0 and duration_total_s > 0:
            tps = tokens_out_total / duration_total_s

        peak_memory_gib = self._fetch_peak_memory_gib()

        return ResourceMetrics(
            tokens_per_second=tps,
            peak_memory_gib=peak_memory_gib,
        )

    def _fetch_peak_memory_gib(self) -> float | None:
        url = f"{self._config.base_url}{METRICS_PATH}"
        req = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=self._config.timeout_s) as resp:
                body_bytes = resp.read()
        except (urllib.error.HTTPError, urllib.error.URLError, OSError):
            return None
        try:
            text = body_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return None
        values_by_name = _parse_metrics_text(text)
        return _extract_peak_memory_gib(values_by_name)

    def manifest(self) -> ReproManifest:
        """Build a reproducible-manifest snapshot for the current configuration.

        The artifact SHA-256 is computed lazily and cached per instance so that
        repeated calls (including concurrent ones) hash the .gguf exactly once.
        ``engine_version`` resolves to the pinned config value when present, else
        the most recent observed system_fingerprint; if neither is available a
        :class:`LlamaCppConfigError` naming ``engine_version`` is raised before any
        hashing occurs.
        """
        # Resolve engine version first so an unpinned, never-run backend fails fast
        # without touching the filesystem.
        engine_version = self._config.engine_version
        if not engine_version:
            with self._lock:
                fingerprint = self._last_fingerprint
            if fingerprint:
                engine_version = fingerprint
            else:
                raise LlamaCppConfigError(
                    field="engine_version",
                    reason=(
                        "no engine version available: pin one in LlamaCppConfig or "
                        "complete at least one successful run to observe a "
                        "system_fingerprint"
                    ),
                )

        # Hash the artifact lazily and cache it across calls (ADR-005/006).
        sha256 = self._artifact_sha256_cache
        if sha256 is None:
            gguf_path = self._config.gguf_path
            try:
                sha256 = hash_gguf(gguf_path)
            except OSError as exc:
                raise LlamaCppConfigError(
                    field="gguf_path",
                    reason=f"artifact is no longer readable: {exc}",
                ) from exc
            with self._lock:
                self._artifact_sha256_cache = sha256

        command = build_command(self._config)
        return ReproManifest(
            artifact_sha256=sha256,
            engine_version=engine_version,
            command=command,
            model_id=self._config.model_id,
        )
=== END FILE ===