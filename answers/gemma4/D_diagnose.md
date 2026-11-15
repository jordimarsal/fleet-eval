The root cause is a collision in the shared `BW_DEBRIEF_ROOT` directory caused by tests using a hardcoded project name (`demo`) while relying on a global environment variable that persists across test runs within the same process.

When `BW_DEBRIEF_ROOT` is set, `find_open_episode` scans `/home/jordi/.../artifacts/demo/exec*/...`. Because multiple tests use the project name `demo`, a second test can "resume" an unfinished log file left behind by a previous test if they happen to share the same timestamped directory or if `find_open_episode` picks up a file from a prior run that hasn't been cleaned up. Since the resumed `DebriefSink` sees a `result:` line (or is incorrectly matched), it sets `self._finished = True`, causing subsequent `step()` calls to raise `ValueError`. This explains why it only fails in full runs (where state accumulates) and not when running tests in isolation.

**Minimal Fix:**

In `src/buildwright/cli.py`, modify the `_debrief_sink` function to ensure that the `base` path is unique to the specific test instance even when `BW_DEBRIEF_ROOT` is set. 

The most robust minimal change is to incorporate the `project.root` (which contains the unique `tmp_path`) into the search path to prevent cross-test contamination:

```python
# src/buildwright/cli.py

def _debrief_sink(settings, project, feature_name):
    # Change this:
    # base = settings.debrief_root or (project.root / "artifacts")
    
    # To this:
    if settings.debrief_root:
        # Scope the debrief root by the unique project root to prevent collisions
        base = settings.debrief_root / project.root.name 
    else:
        base = project.root / "artifacts"
    ...
```

*Note: Alternatively, ensuring tests unset `BW_DEBRIEF_ROOT` or use a unique subdirectory per test via a fixture would also resolve the collision.*