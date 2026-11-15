```python
"""Exponential backoff retry policy with optional jitter."""
from __future__ import annotations

import random


class RetryPolicy:
    """Computes exponential backoff delays with an upper bound and optional jitter.

    Parameters
    ----------
    base : float
        Delay for attempt 0. Must be non-negative.
    factor : float
        Multiplier applied per attempt. Must be non-negative.
    cap : float
        Maximum delay value. Must be positive.
    jitter : float, optional
        Fractional jitter in [0, 1]. Default is 0.0 (no jitter).
    seed : int | None, optional
        Seed for the internal RNG used when jitter > 0.
    """

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
        if not 0.0 <= jitter <= 1.0:
            raise ValueError("jitter must be between 0 and 1 inclusive")

        self._base = base
        self._factor = factor
        self._cap = cap
        self._jitter = jitter
        self._rng = random.Random(seed)

    def delay(self, attempt: int) -> float:
        """Return the backoff delay for the given zero-based attempt index."""
        if attempt < 0:
            raise ValueError("attempt must be non-negative")

        # Compute base * factor ** attempt without risking OverflowError.
        # If the exponent is large enough that the result would exceed cap,
        # we can short-circuit to cap (since cap > 0).
        if self._factor == 0.0:
            raw = self._base if attempt == 0 else 0.0
        elif self._factor == 1.0:
            raw = self._base
        else:
            # Use logarithmic check to avoid overflow.
            # We want to know if base * factor**attempt > cap.
            # Since all values are non-negative and cap > 0:
            #   base * factor**attempt <= cap
            #   => log(base) + attempt*log(factor) <= log(cap)  (if base>0, factor>0)
            
            if self._base == 0.0:
                raw = 0.0
            else:
                import math
                
                # Check if it will definitely exceed cap
                # If factor > 1:
                if self._factor > 1.0:
                    # Try to compute; if it overflows, return cap.
                    try:
                        raw = self._base * (self._factor ** attempt)
                    except OverflowError:
                        raw = float("inf")
                else:
                    # factor < 1, value decreases or stays same
                    raw = self._base * (self._factor ** attempt)

        # Apply cap
        if raw > self._cap:
            raw = self._cap

        # Apply jitter
        if self._jitter > 0.0:
            # Jitter is multiplicative: delay * (1 +/- jitter)
            # The test says: 8 * (1 +/- 0.5) -> [4, 12]
            # So we multiply by a uniform random number in [1-jitter, 1+jitter]
            multiplier = self._rng.uniform(1.0 - self._jitter, 1.0 + self._jitter)
            raw *= multiplier
            
            # Re-apply cap after jitter? 
            # Test: base=8, factor=1, cap=100, jitter=0.5
            # Max possible without cap: 8 * 1.5 = 12 <= 100.
            # If jitter pushes it over cap, should it be capped again?
            # Usually yes, to respect the hard limit.
            if raw > self._cap:
                raw = self._cap

        return float(raw)

    def schedule(self, attempts: int) -> list[float]:
        """Return a list of delays for the given number of attempts."""
        if attempts < 0:
            raise ValueError("attempts must be non-negative")
        return [self.delay(i) for i in range(attempts)]

    def total(self, attempts: int) -> float:
        """Return the sum of all delays in the schedule for the given attempts."""
        return sum(self.schedule(attempts))
```