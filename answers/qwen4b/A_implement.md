```python
"""Retry policy with exponential backoff and optional jitter."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional
from random import Random


@dataclass
class RetryPolicy:
    """A retry policy that computes delays using exponential backoff with optional jitter.

    Args:
        base: The initial delay in seconds.
        factor: The multiplicative factor applied on each attempt.
        cap: Maximum delay in seconds (applies before overflow).
        jitter: Optional jitter range [0, 1], defaults to 0.0.
        seed: Optional seed for reproducible jitter (if provided).

    Raises:
        ValueError: If any of the parameters are invalid.
    """

    base: float
    factor: float
    cap: float
    jitter: float = 0.0
    seed: Optional[int] = None

    def __post_init__(self) -> None:
        if self.base <= 0:
            raise ValueError("base must be positive")
        if self.factor <= 0:
            raise ValueError("factor must be positive")
        if self.cap <= 0:
            raise ValueError("cap must be positive")
        if self.jitter < 0 or self.jitter > 1:
            raise ValueError("jitter must be in [0, 1]")
        if self.seed is not None and not isinstance(self.seed, int):
            raise ValueError("seed must be an integer")

    def _delay(self, attempt: int) -> float:
        """Compute the delay for a given attempt."""
        if attempt < 0:
            raise ValueError("attempt cannot be negative")

        # Apply exponential backoff with cap
        delay = self.base * (self.factor ** attempt)
        if delay >= self.cap:
            return self.cap

        # Apply jitter only if enabled
        if self.jitter > 0:
            # Use a deterministic random generator based on seed
            rng = Random(self.seed) if self.seed is not None else Random()
            jitter_amount = rng.random() * self.jitter
            delay += jitter_amount
            # Ensure jitter doesn't exceed the cap
            if delay > self.cap:
                delay = self.cap
        return delay

    def delay(self, attempt: int) -> float:
        """Return the delay for a single attempt."""
        return self._delay(attempt)

    def schedule(self, attempts: int) -> List[float]:
        """Return list of delays for each attempt from 0 to attempts-1."""
        if attempts <= 0:
            return []
        if attempts < 0:
            raise ValueError("attempts must be non-negative")
        return [self.delay(i) for i in range(attempts)]

    def total(self, attempts: int) -> float:
        """Return sum of all delays in the schedule."""
        if attempts <= 0:
            return 0.0
        if attempts < 0:
            raise ValueError("attempts must be non-negative")
        return sum(self.delay(i) for i in range(attempts))
```