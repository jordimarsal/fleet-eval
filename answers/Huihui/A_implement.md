```python
"""Exponential backoff retry policy with optional jitter."""
from __future__ import annotations

import random


class RetryPolicy:
    """Computes exponential backoff delays with an upper bound and optional jitter."""

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
            raise ValueError("jitter must be in [0, 1]")
        self._base = base
        self._factor = factor
        self._cap = cap
        self._jitter = jitter
        self._rng = random.Random(seed)

    def delay(self, attempt: int) -> float:
        if attempt < 0:
            raise ValueError("attempt must be non-negative")
        
        # Compute the raw delay without risking overflow
        # If factor is 0 and attempt > 0, result is 0
        # If factor is 1, result is base
        # Otherwise, we check if it exceeds cap before computing power to avoid OverflowError
        
        if self._factor == 0.0:
            raw = self._base if attempt == 0 else 0.0
        elif self._factor == 1.0:
            raw = self._base
        else:
            # Check if log(cap / base) < attempt * log(factor)
            # To avoid math.log issues with 0 or negative numbers (though validated), 
            # we can just try to compute but catch OverflowError, or use logs.
            # Using logs is safer for very large attempts.
            import math
            
            if self._base == 0.0:
                raw = 0.0
            else:
                # We want to know if base * factor**attempt > cap
                # log(base) + attempt * log(factor) > log(cap)
                # Note: if factor < 1, this decreases. But typically factor >= 1 in backoff.
                # The tests imply standard exponential growth.
                
                # Edge case: factor could be between 0 and 1? Tests don't explicitly forbid it except factor=0.
                # Let's assume standard behavior where factor >= 1 usually, but handle generally.
                
                if self._cap <= 0:
                    capped = True
                else:
                    # If base is already > cap, it's capped.
                    if self._base > self._cap:
                        capped = True
                    elif self._factor == 1.0:
                        capped = False
                    else:
                        # Use logarithms to determine if the value exceeds the cap
                        # This avoids computing huge powers.
                        try:
                            # If factor is 0, handled above.
                            # If base is 0, handled above.
                            # log(factor) can be negative if factor < 1.
                            log_cap = math.log(self._cap)
                            log_base = math.log(self._base)
                            log_factor = math.log(self._factor)
                            
                            # We want to check if base * factor**attempt > cap
                            # log(base) + attempt * log(factor) > log(cap)
                            current_log_val = log_base + attempt * log_factor
                            capped = current_log_val > log_cap
                        except ValueError:
                            # Should not happen given validation (positive numbers)
                            capped = False

                if capped:
                    raw = self._cap
                else:
                    # Safe to compute now because we know it won't overflow float64 significantly 
                    # or at least it's within bounds relative to cap which is a finite float.
                    # Actually, even if not "capped" by our logic, factor**attempt could still be large 
                    # but less than cap/base. Since cap is a float, the result will fit in a float.
                    raw = self._base * (self._factor ** attempt)

        # Apply jitter
        if self._jitter > 0.0:
            # Jitter adds/subtracts up to jitter fraction of the delay
            # The test says: 8 * (1 +/- 0.5) -> [4, 12]
            # So multiplier is uniform(1 - jitter, 1 + jitter)
            multiplier = self._rng.uniform(1.0 - self._jitter, 1.0 + self._jitter)
            final_delay = raw * multiplier
        else:
            final_delay = raw
            
        return float(final_delay)

    def schedule(self, attempts: int) -> list[float]:
        if attempts < 0:
            raise ValueError("attempts must be non-negative")
        return [self.delay(i) for i in range(attempts)]

    def total(self, attempts: int) -> float:
        return sum(self.schedule(attempts))
```