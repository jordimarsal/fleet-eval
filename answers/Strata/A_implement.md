```python
"""Exponential backoff with optional jitter for retry scheduling.

The policy is pure: given the same seed it produces the same sequence of delays,
which makes tests reproducible and production behaviour auditable.
"""
from __future__ import annotations

import random


class RetryPolicy:
    """Geometric backoff capped at ``cap``, optionally jittered."""

    def __init__(
        self,
        base: float,
        factor: float,
        cap: float,
        jitter: float = 0.0,
        seed: int | None = None,
    ) -> None:
        if base < 0:
            raise ValueError("base must be non-negative")
        if factor < 0:
            raise ValueError("factor must be non-negative")
        if cap <= 0:
            raise ValueError("cap must be positive")
        if not (0.0 <= jitter <= 1.0):
            raise ValueError("jitter must be in [0, 1]")

        self._base = float(base)
        self._factor = float(factor)
        self._cap = float(cap)
        self._jitter = float(jitter)
        self._rng = random.Random(seed)

    def delay(self, attempt: int) -> float:
        """Return the delay for a given zero-based attempt index."""
        if attempt < 0:
            raise ValueError("attempt must be non-negative")

        # Compute base * factor**attempt without ever overflowing: cap first.
        if self._factor == 0.0:
            value = self._base if attempt == 0 else 0.0
        elif self._factor == 1.0:
            value = self._base
        else:
            # If base is already at/above cap, no need to exponentiate.
            if self._base >= self._cap:
                value = self._cap
            else:
                # Smallest n such that base * factor**n >= cap.
                import math

                n_to_cap = math.ceil(
                    (math.log(self._cap) - math.log(self._base)) / math.log(self._factor)
                )
                if attempt >= n_to_cap:
                    value = self._cap
                else:
                    value = self._base * (self._factor ** attempt)

        # Apply jitter as a multiplicative perturbation in [1-jitter, 1+jitter].
        if self._jitter > 0.0:
            value *= 1.0 + self._rng.uniform(-self._jitter, self._jitter)

        return float(value)

    def schedule(self, attempts: int) -> list[float]:
        """Return the full delay sequence for ``attempts`` retries."""
        if attempts < 0:
            raise ValueError("attempts must be non-negative")
        return [self.delay(i) for i in range(attempts)]

    def total(self, attempts: int) -> float:
        """Sum of all delays produced by :meth:`schedule`."""
        return sum(self.schedule(attempts))
```