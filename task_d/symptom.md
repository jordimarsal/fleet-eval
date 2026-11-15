# Symptom: `ValueError: episode already finished` (flaky, only in full runs)

`uv run pytest tests/test_loop.py -q` on a developer machine:

```
3 failed, 28 passed in 2.86s
```

Same command one second later: `2 failed, 29 passed`. Running any single
failing test **alone** always passes (20/20). The failures only appear when
several tests run in the same pytest process.

On CI (ubuntu-latest, no developer env vars) the same suite is green.

The failing tests are:

- `test_parallel_starts_both_features`
- `test_cli_queue_picks_pending_after_finalize`
- `test_cli_run_parks_and_gate_approve_finalizes`

They all fail the same way:

```
src/buildwright/loop.py:1172: in node
>       ctx.debrief.step(...)
src/buildwright/debrief_log.py:121: in step
>       raise ValueError("episode already finished")
E   ValueError: episode already finished
E   During task with name 'verify'
```

Notes gathered while debugging (all verified true):

- The tests never read `artifacts/` themselves; they only drive `cmd_harness_run`.
- Each test creates its own temp project under `tmp_path`, so the project
  paths differ between tests.
- A debug plugin printed the sink path when the exception fired; the path was
  `/home/jordi/.../debrief-mcp/artifacts/demo/exec20261115T1623Z/f2_hub.log`
  with `finished=True` at construction time — the same path was reached by
  more than one test.
- `demo` is the project name the test fixture uses; `BW_DEBRIEF_ROOT` was set
  in the developer's shell to `/home/jordi/.../debrief-mcp/artifacts`.
- `find_open_episode()` scans `exec*/<feature>.log` and skips files that
  already contain `result:`; it returns `None` when there is no open one.
- `_resume()` sets `self._finished = True` when it reads a `result:` line.
- `step()` raises when `self._finished` is true.

Task: identify the root cause (or causes) and describe the minimal fix.
Do not rewrite the module; explain precisely which lines interact badly and
what the smallest correct change is.
