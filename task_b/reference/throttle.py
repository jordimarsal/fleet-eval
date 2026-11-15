"""Reference solution for task B (used only to validate the contract)."""
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

    def _drop_expired(self, key: str, now: float) -> deque[float]:
        events = self._events.setdefault(key, deque())
        while events and events[0] <= now - self._window:
            events.popleft()
        return events

    def allow(self, key: str) -> bool:
        now = self._clock()
        events = self._drop_expired(key, now)
        if len(events) >= self._max:
            raise ThrottleExhausted(key)  # a refusal records nothing
        events.append(now)
        return True

    def reset(self, key: str) -> None:
        if key in self._events:
            self._events[key].clear()

    def remaining(self, key: str) -> int:
        events = self._drop_expired(key, self._clock())
        return self._max - len(events)
