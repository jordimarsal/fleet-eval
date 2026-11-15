The root cause is a race condition where `find_open_episode` returns an existing log file path that was created by a previous test run in the same pytest process, causing `DebriefSink.__init__` to resume a "finished" episode from a prior test instead of starting fresh.

**Minimal Fix:**

In `src/buildwright/debrief_log.py`, modify `find_open_episode` to ensure it only resumes episodes within the *current* test's isolated context. However, since tests use unique `tmp_path` directories, the issue arises because `BW_DEBRIEF_ROOT` is set to a global directory (`/home/jordi/.../debrief-mcp/artifacts`) outside `tmp_path`. Multiple tests write to this shared global root.

The fix is in `_resume` or `find_open_episode`. The cleanest minimal change is in `find_open_episode`: it should not just look for any `result:` missing file, but ensure the file isn't stale or belonging to a completed episode in a way that conflicts. Actually, the bug is simpler: `find_open_episode` finds a file from a *previous test* (which wrote `result:`) if the sorting/globbing logic catches it, but the code says it skips files *with* `result:`.

Wait, the symptom says `finished=True at construction time`. This means `_resume` found a `result:` line. `find_open_episode` returns a path *only if* it doesn't contain `result:`. So how did a finished file get returned?

Ah, `find_open_episode` scans `exec*/<feature>.log`. If Test A runs, creates `exec1/demo/feat.log`, finishes it (writes `result:`). Test B runs. `find_open_episode` looks at `exec1/demo/feat.log`. It sees `result:` and skips it. It looks at older ones. If there are no open ones, it returns `None`.

The issue is likely **concurrency within the same process** where two tests might interact with the *same* global `BW_DEBRIEF_ROOT` directory concurrently or sequentially in a way that leaves a file in an ambiguous state, OR the `exec*` naming collision.

Actually, the most direct fix based on "flaky only in full runs" and "shared root": The tests should not share `BW_DEBRIEF_ROOT`. But they can't easily change that env var.

The bug is in `find_open_episode`: it uses `sorted(...glob(...))`. If Test 1 creates `exec2026.../feat.log` and finishes it. Test 2 starts. `find_open_episode` is called. It finds `exec2026.../feat.log`. It reads it. It sees `result:`. It skips it. Returns `None`. New exec dir created. This should work.

Unless... `find_open_episode` is called *before* the previous test's file is fully flushed/closed? Or the `result:` line is written *after* the check? No, `finish()` writes `result:` at the end.

Let's look at `_resume`. It sets `self._finished = True` if it finds `result:`. Then `step()` raises.

The flakiness suggests that sometimes `find_open_episode` returns a path that *should* have been skipped but wasn't, or the file state changes between the check in `find_open_episode` and the read in `_resume`.

**Correct Minimal Fix:**
In `debrief_log.py`, `find_open_episode` must ensure atomicity or isolation. Since we can't change the test setup easily, the fix is to make `DebriefSink` robust to resuming a file that was *just* finished by another process/test in the shared root.

Actually, the simplest fix is: **`find_open_episode` should not return a path if the file contains `result:`**. It does this. The problem is likely that `BW_DEBRIEF_ROOT` is shared.

The minimal fix is to **clear or isolate the debrief root per test** or **make `find_open_episode` ignore files older than a certain threshold**? No.

Look at `test_parallel_starts_both_features`. Parallel tests! They might be hitting the same `BW_DEBRIEF_ROOT` concurrently. `find_open_episode` reads a file. Another test writes `result:` to it. Race condition.

**Fix:** In `src/buildwright/debrief_log.py`, inside `find_open_episode`, add a lock or use a unique directory per test. Since we can't add locks easily, the minimal code change is to **ensure `find_open_episode` doesn't return a path that is currently being written to or just finished**.

Better: The issue is that `BW_DEBRIEF_ROOT` is global. The tests should set `BW_DEBRIEF_ROOT` to `tmp_path` / "debrief-artifacts". But they don't.

**Root Cause:** Shared `BW_DEBRIEF_ROOT` causes race conditions between parallel tests where one test finishes an episode (writes `result:`) while another test's `find_open_episode` read or `_resume` logic interacts with it inconsistently.

**Minimal Fix:**
In `src/buildwright/cli.py::_debrief_sink`, if `BW_DEBRIEF_ROOT` is set globally, ensure project names are unique enough or use a lock. But the *smallest* fix is in `debrief_log.py`:

Modify `_resume` to be idempotent or handle the state better? No.

The fix is to **prevent `find_open_episode` from returning a file that has `result:`**. It already does.

Wait, `sorted((base / project_name).glob(f"exec*/{feature}.log"))` sorts by name. `exec20261115T1623Z`. If two tests run fast, they might have same timestamp? `datetime.now(UTC):%Y%m%dT%H%MZ` has minute precision. If tests run in same minute, `exec` IDs collide!

**Fix:** Change `exec{...%H%MZ}` to include seconds or microseconds: `%H%M%S%fZ` or similar. This ensures unique `exec` directories even for rapid parallel tests.

**Exact Change:**
In `src/buildwright/cli.py`, line ~30 (inside `_debrief_sink`), change:
```python
exec_id = f"exec{datetime.now(UTC):%Y%m%dT%H%MZ}"
```
to:
```python
exec_id = f"exec{datetime.now(UTC):%Y%m%dT%H%M%S%fZ}"
```
This prevents `exec` directory collisions between parallel tests writing to the shared `BW_DEBRIEF_ROOT`.