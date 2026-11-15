Let me analyze each failing test against the code to identify all bugs.

**Bug 1 — `test_exhaustion_does_not_consume_a_slot`:** When a call is refused, the code does `events.append(now)` before raising. This records the refused call as an event, consuming a slot. The test requires that refused calls must NOT be recorded. Fix: remove the `events.append(now)` on the exhausted path.

**Bug 2 — `test_window_slides_forward` / `test_events_expire_individually_not_all_at_once`:** The expiry check uses strict `<`. At `now = 10.0`, `window = 10.0`, an event at `t=0` gives `0 < 0` → False, so it's not expired. But the test expects events exactly one window old to have expired. Fix: use `<=` instead of `<`.

**Bug 3 — `test_reset_of_an_unused_key_is_a_no_op`:** `reset("never-seen")` calls `self._events[key].clear()`, but `"never-seen"` isn't in `_events`, causing a `KeyError`. Fix: use `.get(key)` with a guard, or pop safely.

Let me verify each fix against all tests:
- Bug 1 fix: refused calls no longer append → `test_exhaustion_does_not_consume_a_slot` passes; other tests unaffected since they don't rely on refused calls being recorded.
- Bug 2 fix (`<=`): `test_window_slides_forward` (event at t=0 expires at now=10) ✓; `test_events_expire_individually` (t=0 expires at now=10, t=5 and t=9 remain) ✓; `test_remaining_reports_the_live_budget` (event at t=0 expires at now=10) ✓.
- Bug 3 fix: `reset` on unseen key is a no-op ✓; `test_reset_clears_one_key` still works because the key exists there.