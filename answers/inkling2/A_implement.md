```python
"""Deterministic exponential retry delays with a final ceiling and optional bounded jitter.

``RetryPolicy`` computes the delay that should be waited before a given job
attempt. The policy is built from an initial base, a growth factor, a hard
cap, and optionally a deterministic jitter controlled by an integer seed.
The implementation avoids raising ``OverflowError`` for very large attempt
counts: once the computed geometric estimate reaches the cap it stops being
computed and returns the capped value instead of evaluating the raw power.
"""
from __future__ import annotations

import random


class RetryPolicy:
    """Compute configurable retries with a stable computation order."""

    def __init__(
        self,
        base: float,
        factor: float,
        cap: float,
        jitter: float = 0.0,
        seed: int | None = None,
    ) -> None:
        if not _is_real(base) or isinstance(base, bool):
            raise ValueError("base must be a real number")
        if not _is_real(factor) or isinstance(factor, bool):
            raise ValueError("factor must be a real number")
        if not _is_real(cap) or isinstance(cap, bool):
            raise ValueError("cap must be a real number")
        if not _is_real(jitter) or isinstance(jitter, bool):
            raise ValueError("jitter must be a real number")
        if not math_isfinite(base) or not math_isfinite(factor) or not math_isfinite(cap):
            raise ValueError("base, factor and cap must be finite")
        if base <= 0.0:
            raise ValueError("base must be positive")
        if factor < 0.0:
            raise ValueError("factor must be non-negative")
        if cap <= 0.0:
            raise ValueError("cap must be positive")
        if jitter < 0.0 or jitter > 1.0:
            raise ValueError("jitter must lie in [0, 1]")
        if seed is not None:
            if isinstance(seed, bool) or not isinstance(seed, int):
                raise ValueError("seed must be an integer")

        self._base = float(base)
        self._factor = float(factor)
        self._cap = float(cap)
        self._jitter = float(jitter)
        self._seed = seed
        self._rng: random.Random | None = None

    def delay(self, attempt: int) -> float:
        """Return the bounded delay for ``attempt`` (zero indexed)."""
        _validate_attempt(attempt)
        raw = self._raw_growth(attempt)
        center = min(raw, self._cap)
        if self._jitter == 0.0:
            return center
        low = center * (1.0 - self._jitter)
        high = center * (1.0 + self._jitter)
        sample = self._sample(attempt)
        # Keep explicit ordering so finite floating-point bounds stay valid.
        delta = max(high - low, 0.0)
        return min(max(low + delta * sample, low), high)

    def schedule(self, attempts: int) -> list[float]:
        """Return delays for a run of consecutive attempts starting at zero."""
        _validate_nonnegative_count(attempts)
        if attempts <= 0:
            return []
        return [self.delay(i) for i in range(attempts)]

    def total(self, attempts: int) -> float:
        """Return the sum of the first ``attempts`` scheduled delays."""
        _validate_nonnegative_count(attempts)
        if attempts <= 0:
            return 0.0
        return sum(self.schedule(attempts))

    def _raw_growth(self, attempt: int) -> float:
        factor = self._factor
        base = self._base
        cap = self._cap

        if attempt == 0:
            return base
        if factor == 0.0:
            return 0.0
        if factor <= 1.0 or math_isfinite(cap / base) is False:
            # Non-growing factors cannot overflow by repeated growth; reducing
            # to this branch keeps very large exponents bounded too.
            value = base * (factor**attempt)
            return min(value, cap)
        current = base
        remaining = attempt
        while remaining > 0:
            if current >= cap:
                return cap
            next_current = current * factor
            if not math_isfinite(next_current):
                return cap
            current = next_current
            remaining -= 1
        return min(current, cap)

    def _sample(self, attempt: int) -> float:
        seed = self._seed if self._seed is not None else 0
        keyed = random.Random(f"{seed}:{attempt}")
        return keyed.random()


def _is_real(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def math_isfinite(value: float) -> bool:
    from math import isfinite

    try:
        number = float(value)
    except (OverflowError, TypeError, ValueError):
        return False
    return isfinite(number)


def _validate_attempt(attempt: int) -> int:
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 0:
        raise ValueError("attempt must be a non-negative integer")
    return attempt


def _validate_nonnegative_count(attempts: int) -> int:
    if isinstance(attempts, bool) or not isinstance(attempts, int) or attempts < 0:
        raise ValueError("attempts must be a non-negative integer")
    return attempts
```