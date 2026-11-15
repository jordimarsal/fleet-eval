The root cause is that `find_open_episode` scans a shared directory (`BW_DEBRIEF_ROOT`) for logs matching the test's hardcoded project name ("demo") without checking if the log belongs to the current execution context, causing tests running in parallel or sequentially within the same minute to collide on the same file path.

**Minimal Fix:**

Modify `_debrief_sink` in `src/buildwright/cli.py` to include a unique identifier (such as the PID or a UUID) in the `exec_id` generation when creating new sinks, **and** update `DebriefSink.__init__` in `src/buildwright/debrief_log.py` to handle the race condition where two processes create the same path simultaneously. However, the *smallest* correct change addressing the specific "flaky full run" symptom described (where paths are identical across tests due to timestamp collision) is to make the `exec_id` unique per process instance rather than just per second.

Change this line in `_debrief_sink`:
```python
exec_id = f"exec{datetime.now(UTC):%Y%m%dT%H%MZ}"
```
To:
```python
import uuid
exec_id = f"exec{datetime.now(UTC):%Y%m%dT%H%MZ}-{uuid.uuid4().hex[:8]}"
```

Additionally, because `find_open_episode` relies solely on filename globbing and content checks (`result:`), it will still pick up stale logs from previous test runs if they share the exact same minute-stamp prefix. To fully fix the flakiness caused by shared state in `BW_DEBRIEF_ROOT`, the `DebriefSink` constructor must verify ownership or the CLI must pass a unique session ID. But given the constraint of minimal changes to existing logic, the primary failure mode is **timestamp collision** between tests running close together. The `exec_id` lacks sub-minute precision. By adding a UUID suffix, each test gets a distinct directory even if started in the same second, preventing `find_open_episode` from returning a file created by a different test (or a previous run) that hasn't been finalized yet.