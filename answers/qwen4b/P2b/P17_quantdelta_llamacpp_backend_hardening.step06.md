Looking at T6, I need to ensure `LlamaCppBackend` is thread-safe with proper locking around `run()`, `metrics()`, and `manifest()`. The existing code has a `_lock` but doesn't use it. Let me analyze what state mutations need protection and how the tests expect concurrency behavior.

Key observations from the tests:
- `test_parallel_runs_keep_counters_exact_and_metrics_stay_live`: 64 threads × 5 runs on one backend; counters must be exact; `metrics()` callable while runs in flight.
- `test_concurrent_manifest_calls_hash_the_artifact_once`: 8 concurrent `manifest()` calls compute hash exactly once (cache).
- R11 storm: 300 runs over 64 threads, zero lost updates.

The lock must protect counter/fingerprint/sha256-cache mutations. Since HTTP I/O happens inside `run()`, holding the lock across the whole request would serialize all runs — but the stub server is threaded so that's fine for correctness, and the tests only require exactness + liveness of `metrics()`. However, serializing 300 runs through one lock could be slow but acceptable. But there's a subtlety: `metrics()` reads counters AND does an HTTP GET to `/metrics`. If `metrics()` holds the lock during its HTTP call, and `run()` also needs the lock, they'd block each other — still correct, just slower. The test asserts `live_snapshots > 0` meaning `metrics()` must return at least once while runs are alive. That works even if serialized.

But wait — if `run()` holds `_lock` for the entire duration including the network call, then with 64 threads all blocked on the lock, only one run proceeds at a time. The barrier releases all 64 simultaneously; they queue on the lock. Each finishes quickly against the local stub. This is fine.

However, a cleaner design per ADR-006 (referenced) is typically: do I/O outside the lock, mutate state under the lock. Let me use that pattern to avoid unnecessary serialization and keep `metrics()` responsive. Actually, re-reading: the simplest robust approach that satisfies "zero lost updates" is to guard the *state mutations* with the lock. For `manifest()`'s hash cache, guard read+compute+store atomically so concurrent calls compute once.

Let me implement:
- `run()`: perform HTTP + parse without holding lock; then acquire lock to update `_success_count`, `_tokens_out_total`, `_duration_total_s`, `_last_fingerprint`.
- `metrics()`: acquire lock to snapshot counters (read-only), release, then do HTTP GET for peak memory (no lock needed for that part since it doesn't touch shared mutable state). But reading counters must be consistent — take them under lock.
- `manifest()`: acquire lock; check `_artifact_sha256_cache`; if None, call `hash_gguf` while... but calling hash inside lock blocks other manifest/run/metrics. The test wants exactly one hash computation across 8 threads. If we hold the lock during hashing, only one thread hashes and others wait then see the cached value → counter["calls"]==1. 

But holding the lock during a slow hash (0.05s sleep in test) means run()/metrics() block too — acceptable for correctness. However, to keep `metrics()` live during runs, better not to hold lock during I/O. Let me structure `manifest()` to: lock → resolve engine_version (needs `_last_fingerprint`) → check cache → if miss, compute hash (release lock? no—must ensure single computation). 

The cleanest way to guarantee "compute once" is double-checked locking with the cache as the guard. Since `hash_gguf` is pure/deterministic on the file, computing it twice would give same result but the test counts calls==1. So I must ensure only one thread ever invokes `hash_gguf`. Holding the lock around the entire cache-check-and-compute achieves that.

Let me write it so the lock is held for the critical sections only where shared state is read/written, and for `manifest()` the whole body under lock (it's short except hashing; acceptable). Actually to be safe and match "metrics stays live while runs in flight", let me NOT hold the lock during the HTTP GET in metrics, and NOT hold it during network in run. For manifest, hold lock across the logic including hash — this briefly blocks others but tests pass.

Wait, there's a risk: in `test_parallel_runs...`, the main thread calls `instance.metrics()` in a loop while worker threads call `run()`. If `run()` holds the lock only for the tiny counter update, `metrics()` can proceed freely. Good. If `manifest()` isn't called in that test, no issue.

In `test_concurrent_manifest_calls_hash_the_artifact_once`, 8 threads call `manifest()`. With lock held across compute, exactly one hashes. 

Now, does holding the lock during `hash_gguf` (0.05s) cause any deadlock? No other lock involved. Fine.

Let me also make sure `close()` exists (tests call `instance.close()`). The current file excerpt was truncated before showing `close()`, `metrics()`, `manifest()`. I must provide complete files preserving existing behavior. Since the provided backend.py is cut off mid-function (`error="malforme`), I need to reconstruct the full file faithfully based on all test expectations.

This is large. Let me carefully build the complete `backend.py` satisfying every referenced test, then add locking.

Let me enumerate required behaviors from tests:

**config.py**: LlamaCppConfig with fields base_url, model_id, gguf_path, timeout_s, max_tokens=1024, temperature=0.0, engine_version=None. Validation per test_config.py. Frozen (reject reassignment → pydantic frozen or dataclass frozen; but it raises ValidationError for attribute reassignment and LlamaCppConfigError for field issues). It's a pydantic model likely (ValidationError import in test_config). base_url normalization: strip trailing slashes, lowercase scheme, reject bad URLs with specific reasons. Coerce string gguf_path to Path. Reject missing/dir gguf. 

Given complexity and that T6 depends on T5 which already produced config/manifest, but my job is ONLY T6 — yet I must output complete files at plan paths. The instruction says implement only current step but output complete files this step needs. The files needed for T6 are backend.py primarily. But backend imports config & manifest which already exist from prior steps. However the repo state shows them as "other source files" excerpts (truncated). Since I can't see full config.py/manifest.py, and they're not part of T6's file list... Actually FILES list includes backend.py, config.py, manifest.py, and two test files. But "implement ONLY this" = T6. The previous work section gave me backend.py content (truncated). 

I think the safest interpretation: produce the complete `backend.py` with thread-safety added, preserving all existing behavior implied by tests. I will NOT rewrite config.py or manifest.py since those were completed in earlier tasks (T1-T5) and aren't changed by T6. But the file tree is empty and I don't have their full contents. Given the harness likely already has them, I should only emit what T6 changes: `backend.py`.

But the truncated backend.py means I'm reconstructing it fully anyway. Let me write a complete, correct backend.py that passes all the shown tests AND adds locking. I'll base config/manifest usage on how tests use them.

Let me now also confirm `metrics()` return type: `ResourceMetrics`? Tests access `.tokens_per_second`, `.peak_memory_gib`. And `TaskOutput` from core.models. `manifest()` returns `ReproManifest`.

For peak memory HTTP GET to /metrics: on 404/501 → None. Parse text via `_parse_metrics_text` + `_extract_peak_memory_gib`.

Let me write the full backend.py now.

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
        fingerprint: str | None = None
        if isinstance(fingerprint_raw, str) and fingerprint_raw.strip() != "":
            fingerprint = fingerprint_raw

        # Record success under the lock so concurrent runs keep exact totals.
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
           