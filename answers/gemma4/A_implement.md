```python
"""Implements exponential backoff with jitter."""
from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:
    """Calculates delays for retrying operations using exponential backoff."""

    base: float
    factor: float
    cap: float
    jitter: float = 0.0
    seed: int | None = None

    def __post_init__(self) -> None:
        if self.base < 0:
            raise ValueError("base must be non-negative")
        if self.cap <= 0:
            raise ValueError("cap must be positive")
        if not (0.0 <= self.jitter <= 1.0):
            raise ValueError("jitter must be between 0 and 1")

    def delay(self, attempt: int) -> float:
        """Returns the delay in seconds for a given attempt number."""
        if attempt < 0:
            raise ValueError("attempt cannot be negative")

        # Calculate base delay: base * (factor ** attempt)
        # To prevent OverflowError, we check if factor is > 1 and attempt is large
        try:
            if self.factor > 1.0 and attempt > 1000:
                # If factor > 1, it will definitely exceed any reasonable cap quickly
                raw_delay = self.cap + 1.0
            else:
                raw_delay = self.base * (self.factor ** attempt)
        except OverflowError:
            raw_delay = self.cap + 1.0

        actual_delay = min(raw_delay, self.cap)

        if self.jitter > 0:
            # Use a local Random instance to ensure determinism via seed
            rng = random.Random(self.seed)
            # jitter=0.5 means range [base*(1-0.5), base*(1+0.5)]
            # which is equivalent to actual_delay * (1 + random_in_range(-jitter, jitter))
            multiplier = 1.0 + rng.uniform(-self.jitter, self.jitter)
            return actual_delay * multiplier

        return actual_delay

    def schedule(self, attempts: int) -> list[float]:
        """Returns a list of delays for the first N attempts."""
        if attempts < 0:
            raise ValueError("attempts cannot be negative")
        return [self.delay(i) for i in range(attempts)]

    def total(self, attempts: int) -> float:
        """Returns the sum of all delays for the first N attempts."""
        return sum(self.schedule(attempts))
```