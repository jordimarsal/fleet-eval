ROLE: implementer. Fix the bugs in ONE complete file.

=== FILE: src/notify/throttle.py (complete, contains bugs) ===
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
            # A refused call still proves the caller is active: remember it so
            # a spammer cannot keep probing for free.
            events.append(now)
            raise ThrottleExhausted(key)
        events.append(now)
        return True

    def reset(self, key: str) -> None:
        """Forget every recorded event for *key*."""
        self._events[key].clear()

    def remaining(self, key: str) -> int:
        """How many events *key* may still spend right now."""
        now = self._clock()
        events = self._events.get(key, deque())
        while events and events[0] < now - self._window:
            events.popleft()
        return self._max - len(events)

```

=== FILE: tests/test_throttle.py (complete, this is the specification) ===
```python
"""Contract for notify.throttle — this file is the specification."""
import pytest

from notify.throttle import Throttle, ThrottleExhausted


def test_first_calls_are_allowed():
    t = Throttle(max_events=3, window=10.0, clock=lambda: 0.0)
    assert [t.allow("a") for _ in range(3)] == [True, True, True]


def test_fourth_call_in_window_is_blocked():
    t = Throttle(max_events=3, window=10.0, clock=lambda: 0.0)
    for _ in range(3):
        t.allow("a")
    with pytest.raises(ThrottleExhausted):
        t.allow("a")


def test_keys_are_counted_independently():
    t = Throttle(max_events=2, window=10.0, clock=lambda: 0.0)
    assert t.allow("a") is True
    assert t.allow("a") is True
    assert t.allow("b") is True  # a different key has its own budget


def test_window_slides_forward():
    now = [0.0]
    t = Throttle(max_events=2, window=10.0, clock=lambda: now[0])
    assert t.allow("a") is True
    assert t.allow("a") is True
    with pytest.raises(ThrottleExhausted):
        t.allow("a")
    now[0] = 10.0  # exactly one window later: the first events have expired
    assert t.allow("a") is True


def test_events_expire_individually_not_all_at_once():
    now = [0.0]
    t = Throttle(max_events=3, window=10.0, clock=lambda: now[0])
    t.allow("a")  # t=0
    now[0] = 5.0
    t.allow("a")  # t=5
    now[0] = 9.0
    t.allow("a")  # t=9 -> budget full
    with pytest.raises(ThrottleExhausted):
        t.allow("a")
    now[0] = 10.0  # only the t=0 event expired -> one slot free
    assert t.allow("a") is True
    with pytest.raises(ThrottleExhausted):
        t.allow("a")  # t=5 and t=9 still count


def test_exhaustion_does_not_consume_a_slot():
    now = [0.0]
    t = Throttle(max_events=2, window=10.0, clock=lambda: now[0])
    assert t.allow("a") is True
    assert t.allow("a") is True
    for _ in range(5):
        with pytest.raises(ThrottleExhausted):
            t.allow("a")  # a refused call must NOT be recorded
        now[0] += 1.0  # t=1..5, still inside the window of the t=0 events
    now[0] = 10.0  # both recorded events expired -> the FULL budget is back
    assert t.allow("a") is True
    assert t.allow("a") is True
    with pytest.raises(ThrottleExhausted):
        t.allow("a")


def test_reset_of_an_unused_key_is_a_no_op():
    t = Throttle(max_events=1, window=10.0, clock=lambda: 0.0)
    t.reset("never-seen")  # must not raise
    assert t.allow("never-seen") is True


def test_reset_clears_one_key():
    t = Throttle(max_events=1, window=10.0, clock=lambda: 0.0)
    t.allow("a")
    t.allow("b")
    with pytest.raises(ThrottleExhausted):
        t.allow("a")
    t.reset("a")
    assert t.allow("a") is True
    with pytest.raises(ThrottleExhausted):
        t.allow("b")  # resetting "a" must not touch "b"


def test_remaining_reports_the_live_budget():
    now = [0.0]
    t = Throttle(max_events=3, window=10.0, clock=lambda: now[0])
    assert t.remaining("a") == 3
    t.allow("a")
    assert t.remaining("a") == 2
    now[0] = 10.0  # the event expired
    assert t.remaining("a") == 3


def test_negative_settings_are_rejected():
    with pytest.raises(ValueError):
        Throttle(max_events=0, window=10.0, clock=lambda: 0.0)
    with pytest.raises(ValueError):
        Throttle(max_events=1, window=-1.0, clock=lambda: 0.0)

```

Right now 5 of the 10 tests fail. Find every bug and return the COMPLETE fixed
file. The docstrings in the file are NOT authoritative when they disagree with
the tests: the tests win.

OUTPUT FORMAT (strict): exactly ONE fenced python block containing the COMPLETE
corrected file src/notify/throttle.py, and nothing else before or after it.
No diff, no explanation, no truncation, no placeholder lines.
