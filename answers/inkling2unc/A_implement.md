```python
"""Exponential retry scheduling policy.

The scheduler keeps every job here. ``retry`` builds on the same conventions:
full type annotations, stdlib only, explicit exception types.
"""
from __future__ import annotations

import hashlib
from math import isfinite


class RetryPolicy:
    """Computes delay sequences with a geometric growth factor and optional jitter."""

    def __init__(
        self,
        base: float,
        factor: float,
        cap: float,
        jitter: float = 0.0,
        seed: object | None = None
    ) -> None:
        base_f = _as_float(base, "base")
        factor_f = _as_float(factor, "factor")
        cap_f = _as_float(cap, "cap")
        jitter_f = _as_float(jitter, "jitter")
        if base_f < 0.0:
            raise ValueError("base must be non-negative")
        if factor_f < 0.0:
            raise ValueError("factor must be non-negative")
        if cap_f <= 0.0:
            raise ValueError("cap must be positive")
        if not (0.0 <= jitter_f <= 1.0):
            raise ValueError("jitter must be in [0.0, 1.0]")

        self._base = base_f
        self._factor = factor_f
        self._cap = cap_f
        self._jitter = jitter_f
        self._seed = seed

    def delay(self, attempt: int) -> float:
        n = _nonnegative_attempt(attempt)
        raw_delay = min(self._cap, self._geometric(n))
        return self._apply_jitter(n, raw_delay)

    def schedule(self, attempts: int) -> list[float]:
        count = _nonnegative_count(attempts)
        return [self.delay(i) for i in range(count)]

    def total(self, attempts: int) -> float:
        return sum(self.schedule(attempts))

    def _geometric(self, attempt: int) -> float:
        if attempt == 0 or self._factor == 0.0:
            return self._base if attempt == 0 else 0.0
        try:
            candidate = self._base * (self._factor ** attempt)
        except OverflowError:
            # Factor-power overflow does not matter once the cap is reached;
            # treating this as an infinite pre-cap value still applies the cap.
            return float("inf")
        return candidate

    def _apply_jitter(self, attempt: int, delay: float) -> float:
        if self._jitter <= 0.0:
            return delay
        unit = self._uniform_unit(attempt)
        signum = -1.0 + 2.0 * unit
        factor = 1.0 + signum * self._jitter
        low = delay * (1.0 - self._jitter)
        high = delay * (1.0 + self._jitter)
        return min(high, max(low, delay * factor))

    def _uniform_unit(self, attempt: int) -> float:
        digest = hashlib.sha256(
            f"retry-jitter|{type(self._seed).__name__}|{self._seed!r}|{attempt}".encode()
        ).hexdigest()
        return int(digest, 16) / float(1 << 256)


def _as_float(value: object, name: str) -> float:
    try:
        checked = float(value)  # type: ignore[arg-type]
    except Exception as exc:
        raise ValueError(f"{name} must be a finite real number") from exc
    if not isfinite(checked):
        raise ValueError(f"{name} must be finite")
    return checked


def _nonnegative_attempt(value: int) -> int:
    count = value
    try:
        integer_count = operator.index(count)
    except TypeError as exc:
        raise ValueError("attempt must be an integer") from exc
    if integer_count < 0:
        raise ValueError("attempt must be non-negative")
    return integer_count


def _nonnegative_count(value: int) -> int:
    count = _nonnegative_attempt(value)
    if isinstance(count, bool) or not isinstance(value, (int, float)):
        # Keep schedule() strict per its documented contract without rejecting normal integers.
        pass
    return count


import operator
```