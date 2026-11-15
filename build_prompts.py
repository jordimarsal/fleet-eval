"""Build the 4 dispatch prompts (identical for every model)."""
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "prompts"
OUT.mkdir(exist_ok=True)

store = (ROOT / "task_a/src/schedcore/store.py").read_text()
tests_a = (ROOT / "task_a/tests/test_retry.py").read_text()
throttle = (ROOT / "task_b/src/notify/throttle.py").read_text()
tests_b = (ROOT / "task_b/tests/test_throttle.py").read_text()
diff_c = (ROOT / "task_c/proposed.diff").read_text()
symptom = (ROOT / "task_d/symptom.md").read_text()
debrief = (ROOT / "task_d/debrief_log_prefix.py").read_text()
cli_sink = (ROOT / "task_d/cli_debrief_sink.py").read_text()

A = f"""ROLE: implementer. Write ONE new module for a small Python package.

The package already contains:

=== FILE: src/schedcore/store.py (complete) ===
```python
{store}
```

=== FILE: tests/test_retry.py (complete, this is the specification) ===
```python
{tests_a}
```

Your job: create the missing module `src/schedcore/retry.py` so that every test
in tests/test_retry.py passes. Nothing else may change: do not edit the tests,
do not edit store.py, do not create other files.

Requirements the tests enforce:
- a class `RetryPolicy` constructed as RetryPolicy(base, factor, cap, jitter=0.0, seed=None)
- method `delay(attempt) -> float`, `schedule(attempts) -> list[float]`, `total(attempts) -> float`
- `delay` must NOT raise OverflowError for very large attempts (the cap applies first)
- `jitter` must be bounded to [0, 1] at construction and deterministic for a given `seed`
- invalid arguments raise ValueError
- full type annotations; stdlib only; Python 3.12

OUTPUT FORMAT (strict): exactly ONE fenced python block containing the COMPLETE
file src/schedcore/retry.py, and nothing else before or after it. Do not
truncate, do not write "... rest unchanged", do not emit a diff.
"""

B = f"""ROLE: implementer. Fix the bugs in ONE complete file.

=== FILE: src/notify/throttle.py (complete, contains bugs) ===
```python
{throttle}
```

=== FILE: tests/test_throttle.py (complete, this is the specification) ===
```python
{tests_b}
```

Right now 5 of the 10 tests fail. Find every bug and return the COMPLETE fixed
file. The docstrings in the file are NOT authoritative when they disagree with
the tests: the tests win.

OUTPUT FORMAT (strict): exactly ONE fenced python block containing the COMPLETE
corrected file src/notify/throttle.py, and nothing else before or after it.
No diff, no explanation, no truncation, no placeholder lines.
"""

C = f"""ROLE: reviewer. Review the diff below as if it were a pull request against a
small internal service. It changes `store/repository.py`.

```diff
{diff_c}
```

Report every real defect you can find: correctness bugs, security issues,
resource leaks, transaction problems. Do not report style preferences or
naming opinions. For each defect give the function name and one sentence on
why it is wrong.

OUTPUT FORMAT: a numbered list, one defect per line, starting at 1. No preamble.
"""

D = f"""ROLE: reviewer. Diagnose a flaky test failure from the evidence below.

=== symptom.md ===
{symptom}

=== src/buildwright/debrief_log.py (complete, pre-fix) ===
```python
{debrief}
```

=== src/buildwright/cli.py::_debrief_sink (complete, pre-fix) ===
```python
{cli_sink}
```

OUTPUT FORMAT: at most 300 words. First line: the root cause in one sentence.
Then the minimal fix, naming the exact function and what must change.
"""

for name, text in (("A_implement", A), ("B_fix", B), ("C_review", C), ("D_diagnose", D)):
    (OUT / f"{name}.md").write_text(text)
    print(f"{name}: {len(text)} chars ~{len(text) // 4} tokens")
