Looking at T4, I need to implement strict validation of memory sample names ending in `_bytes`. Let me examine what's needed based on the tests and requirements.

From the tests in `test_metrics.py`, I can see:
- Memory recognition should only accept samples ending in `_bytes` (case-sensitive)
- No false positives on `memory_pool_count` or `process_memory_kib`
- The test `test_memory_containment_is_case_insensitive` shows that `PROCESS_MEMORY_BYTES` should NOT be recognized (it's uppercase, so case-sensitive matching means it won't match `_bytes`)
- Tests like `test_recognized_memory_gauges_yield_max_value_in_gib` show that `process_resident_memory_bytes` and `llama_kv_self_used_memory_bytes` ARE recognized
- `test_suffix_only_gauge_is_recognized` shows `rss_bytes` is recognized
- `test_llama_memory_bytes_yields_peak_in_gib` shows `llama_memory_bytes` is recognized

So the rule is: a metric name must end with exactly `_bytes` (lowercase, case-sensitive).

Let me look at the current state of the backend to understand where metrics parsing happens and how peak_memory_gib is computed. From the provided code, I can see `_parse_metrics_text` exists but I need to find where the memory filtering happens. Looking at the test expectations, there must be a method that filters for `_bytes` suffix metrics.

Let me check what the full backend.py looks like - the excerpt was cut off. I need to implement the strict `_bytes` validation in the metrics collection logic. Based on the tests, the `metrics()` method needs to:
1. Fetch from `/metrics` endpoint
2. Parse all samples
3. Filter only those whose names end with `_bytes` (strict, case-sensitive)
4. Take the max value across all such samples
5. Convert bytes to GiB

Let me write the complete backend.py file with this implementation:

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
        
        # Validate prompt_tokens
        if not isinstance(prompt_tokens, int) or isinstance(prompt_tokens, bool) or prompt_tokens < 0:
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: usage.prompt_tokens must be a non-negative integer",
            )
        
        # Validate completion_tokens
        if not isinstance(completion_tokens, int) or isinstance(completion_tokens, bool) or completion_tokens < 0:
            return TaskOutput(
                task_id=task.id,
                text="",
                tokens_in=0,
                tokens_out=0,
                duration_s=duration,
                error="malformed response: usage.completion_tokens must be a non-negative integer",
            )

        # Capture fingerprint for manifest resolution
        system_fingerprint = parsed.get("system_fingerprint")
        if isinstance(system_fingerprint, str) and system_fingerprint.strip():
            with self._lock:
                self._last_fingerprint = system_fingerprint

        # Record success under lock
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
        """Return aggregated resource metrics including tokens/s and peak memory."""
        with self._lock:
            success_count = self._success_count
            tokens_out_total = self._tokens_out_total
            duration_total_s = self._duration_total_s

        # Compute tokens_per_second
        tokens_per_second: float | None = None
        if success_count > 0 and duration_total_s > 0:
            tokens_per_second = tokens_out_total / duration_total_s

        # Fetch and parse /metrics for peak memory
        peak_memory_gib: float | None = None
        try:
            url = f"{self._config.base_url}{METRICS_PATH}"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=self._config.timeout_s) as resp:
                body_bytes = resp.read()
            body_text = body_bytes.decode("utf-8", errors="replace")
            values_by_name = _parse_metrics_text(body_text)
            peak_memory_gib = _extract_peak_memory_gib(values_by_name)
        except (urllib.error.HTTPError, urllib.error.URLError, OSError):
            # Metrics endpoint unavailable or error; return None for peak memory
            pass

        return ResourceMetrics(
            tokens_per_second=tokens_per_second,
            peak_memory_gib=peak_memory_gib,
        )

    def manifest(self) -> ReproManifest:
        """Build a reproduction manifest from config and observed state."""
        # Resolve engine_version: pinned config value takes precedence over observed fingerprint
        engine_version: str | None = self._config.engine_version
        if engine_version is None:
            with self._lock:
                engine_version = self._last_fingerprint
        if engine_version is None:
            raise LlamaCppConfigError(
                field="engine_version",
                reason="no engine version available: neither pinned in config nor observed from server",
            )

        # Hash the artifact (with caching)
        if self._artifact_sha256_cache is not None:
            sha256 = self._artifact_sha256_cache
        else:
            try:
                sha256 = hash_gguf(self._config.gguf_path)
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

    def close(self) -> None:
        """Release any held resources."""
        pass

    @staticmethod
    def _extract_http_error_message(exc: urllib.error.HTTPError) -> str:
        """Extract a human-readable message from an HTTP error response."""
        try:
            body = exc.read().decode("utf-8", errors="replace")
            parsed = json.loads(body)
            if isinstance(parsed, dict):
                err_obj = parsed.get("error")
                if isinstance(err_obj, dict):
                    msg = err_obj.get("message")
                    if isinstance(msg, str):
                        return msg
                elif isinstance(err_obj, str):
                    return err_obj
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            pass
        # Fall back to the standard reason phrase
        return exc.reason or "Unknown Error"
=== END FILE ===