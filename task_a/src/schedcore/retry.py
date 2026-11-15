"""Reference solution for task A (used only to validate the contract)."""
from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:
    base: float
    factor: float
    cap: float
    jitter: float = 0.0
    seed: int | None = None

    def __post_init__(self) -> None:
        if self.base < 0:
            raise ValueError("base must be >= 0")
        if self.factor < 0:
            raise ValueError("factor must be >= 0")
        if self.cap <= 0:
            raise ValueError("cap must be > 0")
        if not 0.0 <= self.jitter <= 1.0:
            raise ValueError("jitter must be within [0, 1]")

    def delay(self, attempt: int) -> float:
        if attempt < 0:
            raise ValueError("attempt must be >= 0")
        try:
            raw = self.base * (self.factor ** attempt)
        except OverflowError:
            raw = float("inf")
        capped = min(raw, self.cap)
        if self.jitter and capped:
            rng = random.Random((self.seed if self.seed is not None else 0) + attempt)
            scaled = capped * (1.0 + self.jitter * (rng.random() * 2.0 - 1.0))
            return min(max(scaled, 0.0), self.cap)
        return capped

    def schedule(self, attempts: int) -> list[float]:
        if attempts < 0:
            raise ValueError("attempts must be >= 0")
        return [self.delay(i) for i in range(attempts)]

    def total(self, attempts: int) -> float:
        return sum(self.schedule(attempts))
