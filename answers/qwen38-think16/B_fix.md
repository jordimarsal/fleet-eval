```python
"""Sliding-window rate limiter, keyed per caller."""
from __future__ import annotations

from collections import deque
from collections.abc import Callable


class ThrottleExhausted(Exception):
    """Raised when a key has spent its whole budget inside the window."""


class Throttle:
    """Allow at most ``max_events`` per ``window`` seconds, per key."""

    def __init__(self, max_events: int, window: float, clock: Callable[[], float]) -> None:
        if max_events <= 0:
            raise ValueError("max_events must be > 0")
        if window <= 0:
            raise ValueError("window must be > 0")
        self._max = max_events
        self._window = window
        self._clock = clock
        self._events: dict[str, deque[float]] = {}

    def allow(self, key: str) -> bool:
        """Record one event for *key*, or raise ThrottleExhausted."""
        now = self._clock()
        events = self._events.setdefault(key, deque())
        # Drop everything that has left the window; an event exactly one
        # window old is expired by contract.
        while events and events[0] <= now - self._window:
            events.popleft()
        if len(events) >= self._max:
            raise ThrottleExhausted(key)
        events.append(now)
        return True

    def reset(self, key: str) -> None:
        """Forget every recorded event for *key*."""
        self._events.pop(key, None)

    def remaining(self, key: str) -> int:
        """How many events *key* may still spend right now."""
        now = self._clock()
        events = self._events.get(key)
        if events is None:
            return self._max
        while events and events[0] <= now - self._window:
            events.popleft()
        return self._max - len(events)
```