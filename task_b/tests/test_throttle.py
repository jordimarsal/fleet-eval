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
