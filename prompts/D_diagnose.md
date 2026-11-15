ROLE: reviewer. Diagnose a flaky test failure from the evidence below.

=== symptom.md ===
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


=== src/buildwright/debrief_log.py (complete, pre-fix) ===
```python
"""Native debrief evidence: one BuildwrightLog-format file per feature episode.

debrief's ``run.inspect`` reads a ``key: value`` + ``step:`` log (its ADR-0002
adapter is the other place that knows this format); the loop is the only witness
of role outcomes, so it emits the contract lines itself — write at the source,
pin the shape with tests (the regexes below are mirrored from
``debrief/src/debrief/adapters/buildwright_log.py``; a divergence fails our
tests before it fails debrief's reader).

Human feedback keeps flowing through ``runlog.emit``: debrief ignores those
timestamped free-text lines, while every ``step:`` line here records one role
outcome the moment the loop knows it. ``result:`` is written only on a clean
finalize — a parked or aborted episode stays without it (the header is optional
in debrief's reader, and inventing an outcome for an unfinished episode would
fabricate evidence).

Not emitted (yet): gauntlet-module rejections (optional module, not installed
in any consuming project — add a ``step`` at the reject branch when one does).
"""

from __future__ import annotations

import re
import sys
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

OUTCOMES = frozenset({"pass", "fail"})
_STEP_RE = re.compile(
    r"^step:\s*(?P<ordinal>\d+)\s+"
    r"role=(?P<role>\S+)\s+"
    r"model=(?P<model>\S+)\s+"
    r"outcome=(?P<outcome>\S+)\s+"
    r'reason="(?P<reason>[^"]*)"\s+'
    r"evidence=(?P<evidence>\S+)$"
)
_RESULT_RE = re.compile(r"^(?P<outcome>\S+)(?:\s+failed_steps=(?P<failed_steps>\S*))?$")

_HEADER = "buildwright run log — evidence of one episode; debrief reads it, never edits it"


def engine_build() -> str:
    """The writer's identity as one token: buildwright-<version>."""
    try:
        return f"buildwright-{version('buildwright')}"
    except PackageNotFoundError:  # direct src/ checkout without an install
        return "buildwright-dev"


def sanitize(text: str) -> str:
    """One line, no double quotes — the adapter's reason regex is ``[^"]*``."""
    return " ".join(text.split()).replace('"', "'").strip()


class DebriefSink:
    """Streams one feature episode into ``<artifacts root>/<project>/exec<id>/<feature>.log``.

    Headers go down at creation (the feature and role routing are known then),
    one ``step:`` line per recorded outcome, and ``result:`` at ``finish()`` —
    computed from the recorded steps so it can never contradict them. The
    caller picks the location: inside the project (self-contained mode,
    finalize commits it) or a central debrief evidence tree (BW_DEBRIEF_ROOT,
    the mode the debrief MCP reads).
    """

    def __init__(
        self,
        path: Path,
        feature: str,
        engine: str,
        roles: dict[str, str],
        run_id: str | None = None,
    ) -> None:
        self.path = path
        self.run_id = run_id or (
            f"{feature}-{datetime.now(UTC):%Y-%m-%dT%H-%MZ}"
        )
        self._feature = feature
        self._steps: list[tuple[str, str, str, str, str]] = []
        self._finished = False
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            self._resume(path)
            return
        roles_header = " ".join(f"BW_ROLE_{r.upper()}={m}" for r, m in roles.items())
        path.write_text(
            "\n".join(
                [
                    _HEADER,
                    f"run: {self.run_id}",
                    f"engine_build: {engine}",
                    f"task: {feature}",
                    f"roles: {roles_header}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

    def _resume(self, path: Path) -> None:
        """Continue an unfinished episode: re-read its steps so ordinals and the
        result computation cover the whole history, not just this invocation."""
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("step:"):
                m = _STEP_RE.match(line)
                if m is None:  # pragma: no cover — our own writer wrote it
                    raise ValueError(f"existing step line is malformed: {line!r}")
                self._steps.append(
                    (m["role"], m["model"], m["outcome"], m["reason"], m["evidence"])
                )
            elif line.startswith("result:"):
                self._finished = True  # episode already closed: nothing left to do

    def step(self, role: str, model: str, outcome: str, reason: str, evidence: str) -> None:
        """Record one role outcome. Only pass/fail exist — anything else is a
        writer bug that must fail here, not corrupt debrief's reader."""
        if outcome not in OUTCOMES:
            raise ValueError(f"outcome must be one of {sorted(OUTCOMES)}: {outcome!r}")
        if self._finished:
            raise ValueError("episode already finished")
        clean = sanitize(reason)
        if not clean:
            raise ValueError("an empty reason would forge an evidence line")
        self._steps.append((role, model, outcome, clean, evidence))
        with self.path.open("a", encoding="utf-8") as f:
            f.write(
                f"step: {len(self._steps):02d} role={role} model={model} "
                f'outcome={outcome} reason="{clean}" evidence={evidence}\n'
            )

    def finish(self) -> str | None:
        """Write the ``result:`` header; None when the episode logged no steps
        (a headers-only log would read as a lie by omission in debrief)."""
        if self._finished:
            return None
        self._finished = True
        if not self._steps:
            return None
        failed = [str(i) for i, s in enumerate(self._steps, 1) if s[2] == "fail"]
        result = "pass" if not failed else f"fail failed_steps={','.join(failed)}"
        if _RESULT_RE.fullmatch(result) is None:  # pragma: no cover — writer bug guard
            print(f"debrief: malformed result line {result!r}", file=sys.stderr)
            return None
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"result: {result}\n")
        return result


def find_open_episode(base: Path, project_name: str, feature: str) -> Path | None:
    """The most recent episode log for this feature that has no ``result:`` yet —
    the file a resumed run must keep writing to, so one episode stays one file
    across human gates. Exec dirs are UTC-stamped, so name order is time order.
    None → start a fresh exec dir."""
    episodes = sorted((base / project_name).glob(f"exec*/{feature}.log"))
    for path in reversed(episodes):
        if "result:" not in path.read_text(encoding="utf-8"):
            return path
    return None

```

=== src/buildwright/cli.py::_debrief_sink (complete, pre-fix) ===
```python
def _debrief_sink(
    settings: Settings, project: HarnessProject, feature_name: str
) -> debrief_log.DebriefSink:
    """The episode sink for one feature: resume its open log when a previous
    invocation left one unfinished (parked at a human gate), else open a fresh
    exec dir. Base is BW_DEBRIEF_ROOT (the central debrief evidence tree the MCP
    reads) or, unset, the project's own artifacts/ (self-contained mode)."""
    base = settings.debrief_root or (project.root / "artifacts")
    project_name = project.feature_list.project.name
    roles = {
        "planner": settings.role_model("planner"),
        "worker": settings.role_model("worker"),
        "reviewer": settings.role_model("reviewer"),
    }
    existing = debrief_log.find_open_episode(base, project_name, feature_name)
    if existing is not None:
        return debrief_log.DebriefSink(
            existing, feature=feature_name, engine=debrief_log.engine_build(), roles=roles
        )
    exec_id = f"exec{datetime.now(UTC):%Y%m%dT%H%MZ}"
    return debrief_log.DebriefSink(
        base / project_name / exec_id / f"{feature_name}.log",
        feature=feature_name,
        engine=debrief_log.engine_build(),
        roles=roles,
        run_id=f"{feature_name}-{datetime.now(UTC):%Y-%m-%dT%H-%MZ}",
    )


```

OUTPUT FORMAT: at most 300 words. First line: the root cause in one sentence.
Then the minimal fix, naming the exact function and what must change.
