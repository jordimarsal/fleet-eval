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
