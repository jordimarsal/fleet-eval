```python
"""Exponential-backoff retry policy with optional jitter.

The scheduler uses this to space out retries of failed jobs.  ``retry`` builds on
the same conventions as schedcore.store: full type annotations, stdlib only,
explicit exception types.
"""
from __future__ import annotations

import math
import random


class PolicyError(Exception):
    """Base class for every retry-policy failure."""


class InvalidPolicy(PolicyError):
    """Raised when construction parameters are invalid."""


class RetryPolicy:
    """Computes delay values for an exponential-backoff schedule.

    Parameters
    ----------
    base : float
        The initial delay in seconds.
    factor : float
        Multiplier applied per attempt.
    cap : float
        Maximum delay value.
    jitter : float, default 0.0
        Fractional noise added uniformly within [-jitter * delay, +jitter * delay].
        Must be in [0, 1].
    seed : int | None, default None
        Random seed for deterministic jitter output.
    """

    def __init__(
        self,
        *,
        base: float,
        factor: float,
        cap: float,
        jitter: float = 0.0,
        seed: int | None = None,
    ) -> None:
        if base <= 0:
            raise InvalidPolicy(f"base must be positive, got {base}")
        if factor < 0:
            raise InvalidPolicy(f"factor must be non-negative, got {factor}")
        if cap <= 0:
            raise InvalidPolicy(f"cap must be positive, got {cap}")
        if not (0.0 <= jitter <= 1.0):
            raise InvalidPolicy(
                f"jitter must be in [0, 1], got {jitter}"
            )

        self._base = base
        self._factor = factor
        self._cap = cap
        self._jitter = jitter
        self._rng = random.Random(seed) if seed is not None else random.Random()

    def delay(self, attempt: int) -> float:
        """Return the delay before *attempt* retries."""
        if attempt < 0:
            raise ValueError("attempt must be non-negative")

        # Compute raw value without risking OverflowError on large powers.
        if self._factor == 0.0:
            raw = 0.0 if attempt > 0 else self._base
        elif attempt == 0:
            raw = self._base
        else:
            # Use log to avoid overflow when factor**attempt would explode.
            raw = self._base * math.exp(attempt * math.log(self._factor))

        capped = min(raw, self._cap)

        if self._jitter > 0.0 and capped > 0.0:
            noise = (self._rng.random() - 0.5) * 2.0 * self._jitter * capped
            return max(0.0, capped + noise)

        return capped

    def schedule(self, attempts: int) -> list[float]:
        """Return a list of delays for the first *attempts* retries."""
        if attempts < 0:
            raise ValueError("attempts must be non-negative")
        return [self.delay(i) for i in range(attempts)]

    def total(self, attempts: int) -> float:
        """Return the sum of all delays up to *attempts* retries."""
        return sum(self.schedule(attempts))
```