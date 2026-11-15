ROLE: implementer. Write ONE new module for a small Python package.

The package already contains:

=== FILE: src/schedcore/store.py (complete) ===
```python
"""In-memory job store with a bounded history.

The scheduler keeps every job here. ``retry`` builds on the same conventions:
full type annotations, stdlib only, explicit exception types.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class StoreError(Exception):
    """Base class for every store failure."""


class UnknownJob(StoreError):
    """Raised when a job id is not present in the store."""


@dataclass
class Job:
    id: str
    kind: str
    payload: dict[str, Any] = field(default_factory=dict)
    attempts: int = 0
    last_error: str | None = None


class Store:
    """Keeps jobs in insertion order, evicting the oldest past ``limit``."""

    def __init__(self, limit: int = 1000) -> None:
        if limit <= 0:
            raise ValueError("limit must be positive")
        self._limit = limit
        self._jobs: dict[str, Job] = {}
        self._order: list[str] = []

    def put(self, job: Job) -> None:
        if job.id in self._jobs:
            raise StoreError(f"duplicate job id: {job.id}")
        if len(self._order) >= self._limit:
            oldest = self._order.pop(0)
            del self._jobs[oldest]
        self._jobs[job.id] = job
        self._order.append(job.id)

    def get(self, job_id: str) -> Job:
        try:
            return self._jobs[job_id]
        except KeyError:
            raise UnknownJob(job_id) from None

    def __len__(self) -> int:
        return len(self._jobs)

    def ids(self) -> list[str]:
        return list(self._order)

```

=== FILE: tests/test_retry.py (complete, this is the specification) ===
```python
"""Contract for schedcore.retry.RetryPolicy — this file is the specification."""
import pytest

from schedcore.retry import RetryPolicy


def test_first_attempt_uses_base():
    p = RetryPolicy(base=1.0, factor=2.0, cap=60.0)
    assert p.delay(0) == pytest.approx(1.0)


def test_grows_geometrically():
    p = RetryPolicy(base=1.0, factor=2.0, cap=60.0)
    assert [p.delay(i) for i in range(5)] == pytest.approx([1.0, 2.0, 4.0, 8.0, 16.0])


def test_caps_the_delay():
    p = RetryPolicy(base=2.0, factor=10.0, cap=30.0)
    assert p.delay(0) == pytest.approx(2.0)
    assert p.delay(1) == pytest.approx(20.0)
    assert p.delay(2) == pytest.approx(30.0)  # 200 -> capped


def test_caps_even_when_the_power_overflows():
    # 2.0 * 10.0 ** 10_000 raises OverflowError if computed naively.
    p = RetryPolicy(base=2.0, factor=10.0, cap=30.0)
    assert p.delay(10_000) == pytest.approx(30.0)


def test_zero_factor():
    p = RetryPolicy(base=5.0, factor=0.0, cap=10.0)
    assert p.delay(0) == pytest.approx(5.0)
    assert p.delay(3) == pytest.approx(0.0)


def test_negative_attempt_is_rejected():
    p = RetryPolicy(base=1.0, factor=2.0, cap=60.0)
    with pytest.raises(ValueError):
        p.delay(-1)


def test_invalid_construction_is_rejected():
    with pytest.raises(ValueError):
        RetryPolicy(base=-1.0, factor=2.0, cap=60.0)
    with pytest.raises(ValueError):
        RetryPolicy(base=1.0, factor=2.0, cap=0.0)
    with pytest.raises(ValueError):
        RetryPolicy(base=1.0, factor=1.5, cap=60.0, jitter=1.5)


def test_schedule():
    p = RetryPolicy(base=1.0, factor=2.0, cap=60.0)
    assert p.schedule(3) == pytest.approx([1.0, 2.0, 4.0])
    assert p.schedule(0) == []
    with pytest.raises(ValueError):
        p.schedule(-1)


def test_total_is_the_sum_of_the_schedule():
    p = RetryPolicy(base=1.0, factor=2.0, cap=60.0)
    assert p.total(3) == pytest.approx(7.0)


def test_jitter_is_bounded_and_deterministic():
    p = RetryPolicy(base=8.0, factor=1.0, cap=100.0, jitter=0.5, seed=7)
    for i in range(20):
        assert 4.0 <= p.delay(i) <= 12.0  # 8 * (1 +/- 0.5)

    q = RetryPolicy(base=8.0, factor=1.0, cap=100.0, jitter=0.5, seed=7)
    assert [q.delay(i) for i in range(20)] == [p.delay(i) for i in range(20)]

    r = RetryPolicy(base=8.0, factor=1.0, cap=100.0, jitter=0.5, seed=8)
    assert [r.delay(i) for i in range(20)] != [p.delay(i) for i in range(20)]

```

Your job: create the missing module `src/schedcore/retry.py` so that every test
in tests/test_retry.py passes. Nothing else may change: do not edit the tests,
do not edit store.py, do not create other files.

Requirements the tests enforce:
- a class `RetryPolicy` constructed as RetryPolicy(base, factor, cap, jitter=0.0, seed=None)
- method `delay(attempt) -> float`, `schedule(attempts) -> list[float]`, `total(attempts) -> float`
- `delay` must NOT raise OverflowError for very large attempts (the cap applies first)
- `jitter` must be bounded to [0, 1] at construction and deterministic for a given `seed`
- invalid arguments raise ValueError
- full type annotations; stdlib only; Python 3.12

OUTPUT FORMAT (strict): exactly ONE fenced python block containing the COMPLETE
file src/schedcore/retry.py, and nothing else before or after it. Do not
truncate, do not write "... rest unchanged", do not emit a diff.
