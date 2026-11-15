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
