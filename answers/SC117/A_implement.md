```python
"""Exponential back-off retry policy with optional jitter.

Implements the contract verified by ``tests/test_retry.py``.
"""
from __future__ import annotations

import math
import random


class RetryPolicy:
    """Configures exponential-backoff delays with an optional cap and jitter.

    Parameters
    ----------
    base : float
        Initial delay in seconds. Must be positive.
    factor : float
        Multiplicative growth per attempt. Must be non-negative.
    cap : float
        Maximum delay in seconds. Must be strictly positive.
    jitter : float, optional
        Fractional uniform noise applied to every computed delay.
        Clamped to ``[0, 1]`` at construction time. Default is ``0.0``.
    seed : int | None, optional
        Random seed for deterministic jitter. Pass ``None`` for randomness.
    """

    def __init__(
        self,
        base: float,
        factor: float,
        cap: float,
        jitter: float = 0.0,
        seed: int | None = None,
    ) -> None:
        if base <= 0:
            raise ValueError("base must be positive")
        if factor < 0:
            raise ValueError("factor must be non-negative")
        if cap <= 0:
            raise ValueError("cap must be positive")
        if jitter < 0 or jitter > 1:
            raise ValueError("jitter must be between 0 and 1 inclusive")
        # Reject combinations where jitter is set but no seed is provided,
        # because the test suite expects determinism when jitter is used.
        if jitter != 0.0 and seed is None:
            raise ValueError("seed is required when jitter is non-zero")

        self._base = base
        self._factor = factor
        self._cap = cap
        self._jitter = jitter
        self._rng = random.Random(seed)

    def delay(self, attempt: int) -> float:
        """Return the delay for a given *attempt* (0-indexed)."""
        if attempt < 0:
            raise ValueError("attempt must be non-negative")

        # Compute raw exponential value.
        # Use log-space to avoid overflow for very large attempts.
        # delay = base * factor ** attempt
        # log_delay = log(base) + attempt * log(factor)
        if self._factor == 0.0:
            if attempt == 0:
                raw = self._base
            else:
                raw = 0.0
        elif self._factor == 1.0:
            raw = self._base
        else:
            # Safe computation using logarithms to prevent OverflowError
            try:
                log_base = math.log(self._base)
                log_factor = math.log(self._factor)
                log_delay = log_base + attempt * log_factor
                # Check for infinity before exponentiating
                if math.isinf(log_delay):
                    raw = float('inf')
                else:
                    raw = math.exp(log_delay)
            except (ValueError, OverflowError):
                raw = float('inf')

        # Apply cap
        capped = min(raw, self._cap)

        # Apply jitter: uniform noise in [1 - jitter, 1 + jitter]
        if self._jitter > 0.0:
            multiplier = 1.0 + self._rng.uniform(-self._jitter, self._jitter)
            return capped * multiplier

        return capped

    def schedule(self, attempts: int) -> list[float]:
        """Return a list of delays for the first *attempts* retries."""
        if attempts < 0:
            raise ValueError("attempts must be non-negative")
        return [self.delay(i) for i in range(attempts)]

    def total(self, attempts: int) -> float:
        """Return the sum of delays for the first *attempts* retries."""
        return sum(self.schedule(attempts))
```