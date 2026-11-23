Looking at T2, I need to add optional timestamp parsing support for OpenMetrics format to the `/metrics` parser. Let me first examine the existing backend code to understand the current metrics parsing implementation.

Let me check what's currently in the repository state and look at the relevant source files.

Since the repository state shows no previous work yet, I need to understand what exists. Based on the test files provided, I can see there are tests in `test_metrics.py` that reference the metrics parsing behavior. The task is specifically about adding **optional timestamp parsing** for OpenMetrics format.

In OpenMetrics format, metric samples can have an optional timestamp after the value:
```
metric_name{label="value"} 42 1609459200000
# EOF
```

The key insight from the task description is "Add **optional** timestamp parsing support" — meaning the parser should handle lines with timestamps but must still work without them (backward compatible).

Looking at the test file `test_metrics.py`, I don't see explicit tests for timestamped metrics in the excerpts shown, but the task says this depends on T1 (which enhanced numeric parsing) and references R2. Since I'm implementing only T2, I need to modify the metrics parser in `backend.py` to optionally accept a trailing timestamp token after the numeric value.

However, since the repository state is empty (no previous steps implemented), and I'm told to implement ONLY T2 which depends on T1, I need to be careful. Let me re-read the instructions: "Implement ONLY the current step." But T2 depends on T1 being done first. Given that no files exist yet, I'll need to create the backend with both T1's enhancements AND T2's timestamp support, since T2 builds directly on T1's parser.

Wait - let me reconsider. The instruction says "YOUR PREVIOUS WORK IN THIS TASK (complete files you already wrote; preserve their behavior): (none yet)". This means I haven't written anything yet for THIS task (T2). But T1 was supposed to be completed before T2. Since the repo state is empty, perhaps T1 hasn't been committed either, or perhaps I should assume T1's changes are part of what needs to be here.

Given the constraint "implement ONLY this" (T2), but T2 depends on T1, and no code exists, I believe the intent is that I produce the complete file(s) needed for T2 to work, incorporating T1's baseline plus T2's addition. The tests in `test_metrics.py` will validate the combined behavior.

Let me look more carefully at what the metrics parser needs to do based on the tests:
- Parse Prometheus/OpenMetrics text format
- Recognize memory gauges ending in `_bytes` (case-sensitive per R5/T4)
- Extract numeric values (decimal, scientific notation, leading +, NaN, ±Inf per T1)
- Handle labels with braces inside quotes and escaped quotes (T3)
- **NEW for T2**: Optionally parse a trailing timestamp after the value

The OpenMetrics format allows: `metric{labels} value [timestamp]`

I'll create the backend module with the full implementation including T1+T2 features since they're tightly coupled in the same parsing function.

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
    """
    result: dict[str, str] = {}
    if not label_str or label_str == "{}":
        return result

    inner = label_str
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

        # Parse key
        key_start = i
        while i < n and inner[i] != "=":
            i += 1
        if i >= n:
            break
        key = inner[key_start:i].strip()
        i += 1  # skip '='

        # Parse value (must be quoted)
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


def _parse_metrics_text(text: str) -> dict[str, float]:
    """Parse Prometheus/OpenMetrics text format into a flat name->value map.

    Each sample line has the form:
        metric_name [ {labels} ] value [ timestamp ]

    The timestamp is optional (OpenMetrics extension). Only the first occurrence
    of each metric name is kept (Prometheus convention for gauges/counters in
    this context; we take max later for memory peaks).

    Returns a mapping from full metric name (without labels) to its numeric value.
    If multiple samples share the same name with different label sets, all are
    collected under the same key and the caller can decide aggregation.
    Here we store as a list of values per name so the caller can compute max.
    """
    # We'll collect all values per metric name
    values_by_name: dict[str, list[float]] = {}

    lines = text.splitlines()
    for line in lines:
        stripped = line.strip()
        # Skip comments and empty lines
        if not stripped or stripped.startswith("#"):
            continue

        tokens = stripped.split(None, 3)  # split into at most 4 parts
        if len(tokens) < 2:
            continue

        name_part = tokens[0]
        rest = tokens[1:] if len(tokens) > 1 else []

        # Separate name and labels
        metric_name = name_part
        if "{" in name_part:
            brace_idx = name_part.index("{")
            metric_name = name_part[:brace_idx].strip()

        # The remaining tokens after the name/labels part contain value [timestamp]
        # Re-parse more carefully: find where the value starts
        # Format: name{labels} value [timestamp]
        # After splitting on whitespace with maxsplit=3, we may have issues.
        # Let's re-approach: use regex to match the sample pattern.

    # Better approach: regex-based parsing
    # Pattern: ^(\S+?)(\{[^}]*\})?\s+(\S+)\s*(\d+)?$
    # But labels can contain braces inside quotes, so simple \{[^}]*\} won't work.
    # We need a smarter parser.

    values_by_name.clear()
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Try to parse using a state-machine approach
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

        # Skip optional labels
        if i < n and stripped[i] == "{":
            # Find matching closing brace, accounting for quoted strings
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

    return {name: vals for name, vals in values_by_name.items()}


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

        # Capture fingerprint
        fingerprint = parsed.get("system_fingerprint")
        if isinstance(fingerprint, str) and fingerprint.strip():
            with self._lock:
                self._last_fingerprint = fingerprint.strip()

        # Record success
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
        """Fetch /metrics and compute peak memory; combine with run stats for tps."""
        url = f"{self._config.base_url}{METRICS_PATH}"
        req = urllib.request.Request(url, method="GET")

        peak_memory_gib: float | None = None
        try:
            with urllib.request.urlopen(req, timeout=self._config.timeout_s) as resp:
                body_bytes = resp.read()
            text = body_bytes.decode("utf-8", errors="replace")
            samples = _parse_metrics_text(text)

            # Find all metric names ending in "_bytes" (case-sensitive per R5/T4)
            max_bytes: float | None = None
            for name, values in samples.items():
                if name.endswith("_bytes"):
                    for val in values:
                        if math.isfinite(val):
                            if max_bytes is None or val > max_bytes:
                                max_bytes = val
            if max_bytes is not None and max_bytes >= 0:
                peak_memory_gib = max_bytes / (2**30)
        except (urllib.error.HTTPError, urllib.error.URLError, OSError):
            pass  # metrics endpoint unavailable -> no peak

        tokens_per_second: float | None = None
        with self._lock:
            success_count = self._success_count
            tokens_out_total = self._tokens_out_total
            duration_total = self._duration_total_s

        if success_count > 0 and duration_total > 0:
            tokens_per_second = tokens_out_total / duration_total

        return ResourceMetrics(
            tokens_per_second=tokens_per_second,
            peak_memory_gib=peak_memory_gib,
        )

    def manifest(self) -> ReproManifest:
        """Build a reproducible manifest with cached artifact hash."""
        config = self._config

        # Resolve engine_version: pinned value takes precedence over observed fingerprint
        engine_version: str | None = None
        if config.engine_version is not None:
            engine_version = config.engine_version
        else:
            with self._lock:
                fp = self._last_fingerprint
            if fp is not None:
                engine_version = fp
            else:
                from quantdelta.backends.llamacpp.errors import LlamaCppConfigError

                raise LlamaCppConfigError(
                    field="engine_version",
                    reason="no pinned engine version and no observed system_fingerprint yet",
                )

        # Cache artifact sha256 across calls (thread-safe via lock)
        with self._lock:
            if self._artifact_sha256_cache is None:
                try:
                    self._artifact_sha256_cache = hash_gguf(config.gguf_path)
                except OSError as exc:
                    from quantdelta.backends.llamacpp.errors import LlamaCppConfigError

                    raise LlamaCppConfigError(
                        field="gguf_path",
                        reason=f"artifact is no longer readable: {exc}",
                    ) from exc
            artifact_sha256 = self._artifact_sha256_cache

        command = build_command(config)

        return ReproManifest(
            artifact_sha256=artifact_sha256,
            engine_version=engine_version,
            command=command,
            model_id=config.model_id,
        )

    def close(self) -> None:
        """Release any resources held by