Root cause: because the developer’s `BW_DEBRIEF_ROOT` is shared by all tests, `_debrief_sink`’s minute-precision fresh-exec id can point at another test’s already-finalized `<exec>/<feature>.log`, and `DebriefSink.__init__` resumes it as finished.

The bad interaction is:

- `base = settings.debrief_root or ...` makes every temp `demo` project write to the same central `/.../artifacts/demo` tree.
- After an earlier test finalizes, `find_open_episode()` skips that log because it contains `result:` and returns `None`.
- The fresh branch then computes `exec_id = f"exec{datetime.now(UTC):%Y%m%dT%H%MZ}"`; in the same UTC minute it builds the identical path.
- `DebriefSink.__init__` sees `path.exists()`, calls `_resume()`, reads `result:`, sets `_finished=True`; later `step()` raises.

Minimal fix: in `cli._debrief_sink`, when no open episode exists, do not assume the minute-stamped candidate path is new; make the fresh exec directory collision-free before constructing `DebriefSink` — e.g., use sub-second precision (`%Y%m%dT%H%M%S%fZ`) or loop until `(base / project_name / exec_id / f"{feature_name}.log").exists()` is false. Also make the suite hermetic by monkeypatching `BW_DEBRIEF_ROOT`/`settings.debrief_root` to a per-test temp dir.