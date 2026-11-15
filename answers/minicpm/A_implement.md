```python
"""Exponential backoff retry policy with optional jitter.

This module provides a ``RetryPolicy`` class that computes delay times for
retry attempts using exponential backoff. It supports capping the maximum delay,
adding deterministic jitter, and validating input parameters.

All implementations use only the Python standard library and are fully typed.
"""
from __future__ import annotations

import math
import random
from typing import List


class RetryPolicy:
    """Configurable exponential backoff retry policy.

    The delay for attempt ``n`` (0-indexed) is computed as:
        base * factor ** n
    subject to the ``cap`` constraint. If ``jitter`` is provided, a random
    offset is added within the range [-jitter * delay, +jitter * delay].

    Parameters
    ----------
    base : float
        Initial delay in seconds. Must be > 0.
    factor : float
        Multiplicative factor for each subsequent attempt.
    cap : float
        Maximum allowed delay in seconds. Must be > 0.
    jitter : float, optional
        Relative jitter amplitude in [0, 1]. Default is 0.0.
    seed : int | None, optional
        Random seed for deterministic jitter. Default is None.

    Raises
    ------
    ValueError
        If ``base`` <= 0, ``cap`` <= 0, or ``jitter`` is not in [0, 1].
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
        if cap <= 0:
            raise ValueError("cap must be positive")
        if not (0.0 <= jitter <= 1.0):
            raise ValueError("jitter must be between 0 and 1 inclusive")

        self.base = base
        self.factor = factor
        self.cap = cap
        self.jitter = jitter
        self.seed = seed

        # Initialize random generator if jitter is enabled
        if jitter > 0.0:
            self._rng = random.Random(seed)
        else:
            self._rng = None

    def delay(self, attempt: int) -> float:
        """Compute the delay for a given attempt number.

        Parameters
        ----------
        attempt : int
            The attempt index (0-based). Must be >= 0.

        Returns
        -------
        float
            The computed delay in seconds.

        Raises
        ------
        ValueError
            If ``attempt`` is negative.
        """
        if attempt < 0:
            raise ValueError("attempt must be non-negative")

        # Compute exponential backoff value
        # Use min to avoid overflow for large attempts when factor > 1
        if self.factor == 0.0:
            exp_value = 0.0 if attempt > 0 else self.base
        else:
            # For very large exponents, math.pow can overflow.
            # We cap the exponent effectively by checking against log(cap/base)
            if self.factor > 1.0:
                max_exp = math.log(self.cap / self.base) / math.log(self.factor)
                if attempt > max_exp:
                    exp_value = self.cap
                else:
                    exp_value = self.base * (self.factor ** attempt)
            elif self.factor == 1.0:
                exp_value = self.base
            else:  # 0 < factor < 1
                exp_value = self.base * (self.factor ** attempt)

        # Apply cap
        delayed = min(exp_value, self.cap)

        # Apply jitter if enabled
        if self.jitter > 0.0 and self._rng is not None:
            # Jitter range: [-jitter * delay, +jitter * delay]
            offset = self._rng.uniform(-self.jitter, self.jitter) * delayed
            delayed += offset

        return delayed

    def schedule(self, attempts: int) -> List[float]:
        """Generate a list of delays for the first ``attempts`` retries.

        Parameters
        ----------
        attempts : int
            Number of retry delays to generate. Must be >= 0.

        Returns
        -------
        List[float]
            List of delay times in seconds.

        Raises
        ------
        ValueError
            If ``attempts`` is negative.
        """
        if attempts < 0:
            raise ValueError("attempts must be non-negative")
        return [self.delay(i) for i in range(attempts)]

    def total(self, attempts: int) -> float:
        """Compute the total time spent waiting across ``attempts`` retries.

        Parameters
        ----------
        attempts : int
            Number of retry delays to sum. Must be >= 0.

        Returns
        -------
        float
            Sum of all delay times.
        """
        return sum(self.schedule(attempts))
```