Root cause: `find_open_episode` performs a non-atomic check-and-resume on shared file paths. It scans for logs without a `result:` line to determine if an episode is open. However, between the scan (in `_debrief_sink`) and the actual resume (in `DebriefSink.__init__`), another test process can finalize that same log file by writing the `result:` line. When the second test then resumes from that path, it reads the now-present `result:` line in `_resume`, sets `self._finished = True`, but proceeds to use the sink as if it were active. Subsequent calls to `step()` raise `ValueError("episode already finished")`. This race condition manifests only when multiple tests run concurrently or sequentially in the same process with shared artifact roots (`BW_DEBRIEF_ROOT`).

Minimal fix: Modify `find_open_episode` to be atomic by verifying the file's state immediately before returning it, or better yet, handle the race inside `DebriefSink.__init__`. The smallest correct change is in `DebriefSink.__init__`: after calling `self._resume(path)`, check if `self._finished` is True. If so, treat this as a fresh start rather than a resume, effectively ignoring the stale file because another process has already closed it. Specifically, replace the early return in `__init__` after `_resume` with a conditional reset of internal state or simply allow the caller to detect the finished state. However, since `find_open_episode` is used to *locate* an open episode, the most precise fix is to make `find_open_episode` re-validate the file content right before returning, ensuring no `result:` was written between the glob and the read. Alternatively, simpler: In `_debrief_sink`, after getting `existing`, re-read its last line to confirm it doesn't end with `result:`. But the cleanest minimal fix is in `DebriefSink.__init__`: if `_resume` sets `_finished = True`, do not return; instead, generate a new path (fresh exec dir) for this test instance, effectively treating the resumed-but-finished log as "used up".

Change `DebriefSink.__init__`:
```python
if path.exists():
    self._resume(path)
    if self._finished:
        # Another process finalized this; start fresh
        exec_id = f"exec{datetime.now(UTC):%Y%m%dT%H%MZ}"
        path = base / project_name / exec_id / f"{feature}.log"
        # Re-initialize attributes for new path...
```