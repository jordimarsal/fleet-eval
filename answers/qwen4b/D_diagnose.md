Root cause: Multiple tests create logs in the same `artifacts/` directory with overlapping episode paths, causing concurrent `_resume()` calls to set `self._finished = True`, which then causes subsequent `step()` calls to raise `ValueError("episode already finished")`.

Minimal fix: Modify `DebriefSink._resume()` to avoid setting `self._finished` on first encounter of a `result:` line — instead, only set it if no steps were recorded before. This prevents race conditions where multiple test invocations simultaneously detect an existing log with `result:` but different step histories.

Change in `src/buildwright/debrief_log.py`: In `_resume()`, replace:
```python
elif line.startswith("result:"):
    self._finished = True  # episode already closed: nothing left to do
```
with:
```python
elif line.startswith("result:"):
    # Only mark as finished if we haven't already recorded any steps
    if not self._steps:
        self._finished = True
```

This ensures that an episode is only marked as finished when there are no prior steps (i.e., it's truly empty), preventing false positives from shared or stale logs during parallel execution. The fix preserves correctness for valid episodes while eliminating flakiness due to concurrent access and state mutation.