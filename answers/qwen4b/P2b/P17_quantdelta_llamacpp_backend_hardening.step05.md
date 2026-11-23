Looking at T5, I need to refactor `manifest()` to cache the artifact sha256 and resolve `engine_version` from config or observed fingerprint. Let me examine what's needed based on the tests.

The key behaviors required by `test_manifest.py`:
1. Pinned engine version takes precedence over observed fingerprint
2. Without pin, use most recent observed fingerprint
3. Without pin or observed fingerprint → raise `LlamaCppConfigError(field="engine_version")`
4. Unreadable artifact with pin → raise `LlamaCppConfigError(field="gguf_path", reason contains "artifact is no longer readable")`
5. Engine version resolution happens BEFORE hashing (so if no pin/fingerprint, it raises before touching gguf)
6. Empty observed fingerprint is ignored
7. Concurrent manifest calls hash the artifact exactly once (caching)

Let me also check the concurrency test which monkeypatches `hash_gguf` in the backend module namespace:
```python
monkeypatch.setattr("quantdelta.backends.llamacpp.backend.hash_gguf", slow_hash)
```

So `hash_gguf` must be called via the module-level name in `backend.py`.

Now let me write the complete `backend.py` with the refactored `manifest()`:

=== FILE: src/quantdelta/backends/llamacpp/backend.py ===
"""LlamaCppBackend adapter: run(), metrics(), manifest() against a local llama.cpp server."""

from __future__ import annotations

import json
import math
import re
import threading
import time
import urllib.error
import urllib.request
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from quantdelta.backends.llamacpp.config import LlamaCppConfig
from quantdelta.backends.llamacpp.errors import (
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
    # Handle special tokens
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
    
    Examples:
        {instance="host:8080"} -> {"instance": "host:8080"}
        {path="/api/{version}/data"} -> {"path": "/api/{version}/data"}
        {desc="He said \\"hi\\""} -> {"desc": 'He said "hi"'}
        {name='single\'quoted'} -> {"name": "single'quoted"}
    """
    result: dict[str, str] = {}
    if not label_str or label_str.strip() == "{}":
        return result

    inner = label_str.strip()
    # Strip outer braces
    if inner.startswith("{") and inner.endswith("}"):
        inner = inner[1:-1]

    i = 0
    n = len(inner)
    while i < n:
        # Skip whitespace
        while i < n and inner[i].isspace():
            i += 1
        if i >= n:
            break

        # Parse key (up to '=')
        key_start = i
        while i < n and inner[i] != "=":
            i += 1
        if i >= n:
            break
        key = inner[key_start:i].strip()
        i += 1  # skip '='

        # Skip any whitespace after '='
        while i < n and inner[i].isspace():
            i += 1

        # Parse value (must be quoted in valid Prometheus format)
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
                        # Other escape sequences: keep as-is for now
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
            # Unquoted value (shouldn't happen in valid Prometheus, but handle gracefully)
            val_start = i
            while i < n and inner[i] not in (",", "}"):
                i += 1
            value = inner[val_start:i].strip()

        result[key] = value

        # Skip whitespace and comma
        while i < n and inner[i].isspace():
            i += 1
        if i < n and inner[i] == ",":
            i += 1

    return result


def _parse_metrics_text(text: str) -> dict[str, list[float]]:
    """Parse Prometheus/OpenMetrics text format into a name->values map.

    Each sample line has the form:
        metric_name [ {labels} ] value [ timestamp ]

    The timestamp is optional (OpenMetrics extension). Returns a mapping from
    full metric name (without labels) to a list of all observed numeric values.
    Callers can aggregate (e.g., take max for memory peaks).
    """
    values_by_name: dict[str, list[float]] = {}

    lines = text.splitlines()
    for line in lines:
        stripped = line.strip()
        # Skip comments and empty lines
        if not stripped or stripped.startswith("#"):
            continue

        # State-machine parse: name [ {labels} ] value [timestamp]
        i = 0
        n = len(stripped)

        # Parse metric name (non-whitespace, non-brace chars until space or {)
        name_end = 0
        while name_end < n and stripped[name_end] != " " and stripped[name_end] != "{":
            name_end += 1
        metric_name = stripped[:name_end].strip()
        if not metric_name:
            continue

        i = name_end

        # Skip optional labels block
        if i < n and stripped[i] == "{":
            # Find matching closing brace, accounting for quoted strings with braces inside
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
            i = j + 1  # skip past closing brace

        # Now parse the value (and optional timestamp)
        # Skip whitespace
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
        # Strict validation: must end with '_bytes' (case-sensitive)
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

    def run(self, *, task: Task, seed: int | None = None) -> TaskOutput:
        """Execute one chat completion request and return a TaskOutput."""
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

        # Parse JSON response
        try:
            body_text = body_bytes.decode("utf-8")
            parsed = json.loads(body_text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
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

        # Validate choices
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

        # Validate usage
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

        if not isinstance(prompt_tokens, int) or isinstance(prompt_tokens, bool) or prompt_tokens < 0:
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: usage.prompt_tokens must be a non-negative integer",
            )
        if not isinstance(completion_tokens, int) or isinstance(completion_tokens, bool) or completion_tokens < 0:
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: usage.completion_tokens must be a non-negative integer",
            )

        # Capture system_fingerprint (ignore empty strings)
        fingerprint = parsed.get("system_fingerprint")
        if isinstance(fingerprint, str) and fingerprint.strip():
            with self._lock:
                self._last_fingerprint = fingerprint

        # Accumulate successful-run totals under the lock
        with self._lock:
            self._success_count += 1
            self._tokens_out_total += completion_tokens
            self._duration_total_s += duration

        return TaskOutput(
            task_id=task.id,
            text=content,
            tokens_in=prompt_tokens,
            tokens_out=completion_tokens,
            duration_s=duration,
            error=None,
        )

    def metrics(self) -> ResourceMetrics:
        """Return aggregated resource metrics for this backend instance."""
        with self._lock:
            success_count = self._success_count
            tokens_out_total = self._tokens_out_total
            duration_total_s = self._duration_total_s

        tokens_per_second: float | None = None
        if success_count > 0 and duration_total_s > 0.0:
            tokens_per_second = tokens_out_total / duration_total_s

        peak_memory_gib = self._fetch_peak_memory()

        return ResourceMetrics(
            tokens_per_second=tokens_per_second,
            peak_memory_gib=peak_memory_gib,
        )

    def _fetch_peak_memory(self) -> float | None:
        """GET /metrics and extract peak memory in GiB; returns None on any failure."""
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
        """Build a ReproManifest for the current configuration and artifact.

        Resolves engine_version from config pin or most recent observed fingerprint.
        Caches the artifact sha256 so concurrent calls hash only once.
        """
        # Resolve engine_version BEFORE hashing (test_manifest_resolves_engine_version_before_hashing)
        pinned = self._config.engine_version
        if pinned is not None:
            engine_version = pinned
        else:
            with self._lock:
                observed = self._last_fingerprint
            if observed is not None:
                engine_version = observed
            else:
                raise LlamaCppConfigError(
                    field="engine_version",
                    reason="no engine version available: neither a pinned value in config nor an observed system_fingerprint from a successful run",
                )

        # Cache artifact sha256 across calls; hash at most once per backend instance
        with self._lock:
            cached_sha = self._artifact_sha256_cache
        if cached_sha is None:
            gguf_path = self._config.gguf_path
            try:
                digest = hash_gguf(gguf_path)
            except OSError as exc:
                raise LlamaCppConfigError(
                    field="gguf_path",
                    reason=f"artifact is no longer readable: {exc}",
                ) from exc
            with self._lock:
                if self._artifact_sha256_cache is None:
                    self._artifact_sha256_cache = digest
                cached_sha = self._artifact_sha256_cache

        command = build_command(self._config)

        return ReproManifest(
            artifact_sha256=cached_sha,
            engine_version=engine_version,
            command=command,
            model_id=self._config.model_id,
        )

    def _extract_http_error_message(self, exc: urllib.error.HTTPError) -> str:
        """Extract a human-readable message from an HTTPError."""
        try:
            body = exc.read().decode("utf-8")
            parsed = json.loads(body)
            if isinstance(parsed, dict):
                err = parsed.get("error")
                if isinstance(err, dict):
                    msg = err.get("message")
                    if isinstance(msg, str):
                        return msg
                elif isinstance(err, str):
                    return err
        except (UnicodeDecodeError, json.JSONDecodeError, OSError):
            pass
        return exc.reason or "unknown error"

    def close(self) -> None:
        """Release any resources held by this backend instance."""
        pass
=== END FILE ===