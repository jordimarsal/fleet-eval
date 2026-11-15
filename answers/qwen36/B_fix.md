```python
"""Sliding-window rate limiter, keyed per caller.

This module is COMPLETE but contains bugs. The contract in
tests/test_throttle.py is authoritative: when the tests disagree with the
docstrings here, the tests win.
"""
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
        # drop everything that has left the window
        while events and events[0] < now - self._window:
            events.popleft()
        if len(events) >= self._max:
            raise ThrottleExhausted(key)
        events.append(now)
        return True

    def reset(self, key: str) -> None:
        """Forget every recorded event for *key*."""
        if key in self._events:
            self._events[key].clear()

    def remaining(self, key: str) -> int:
        """How many events *key* may still spend right now."""
        now = self._clock()
        events = self._events.get(key, deque())
        while events and events[0] < now - self._window:
            events.popleft()
        return self._max - len(events)
```