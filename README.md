# fleet-eval

**Five dispatch-role tasks × eight local fleet models, graded mechanically.**

A standardised battery to answer *"what is each model actually good at?"* with
evidence instead of vibes. It complements [ggufbench](https://github.com/jordimarsal/ggufbench)
(which measures quality/speed of models in isolation) with the axis the bench
does not touch: **delivery fidelity in a dispatch role** — does the model return
the complete file it was asked for, in the format it was asked for, inside the
token budget it was given?

## The five tasks

| # | Task | What it measures |
|---|---|---|
| **A** | Implement `schedcore/retry.py` from a red test file (complete new module) | spec → code, edge cases (overflow, jitter determinism, validation) |
| **B** | Fix 3 seeded bugs in a complete file (`notify/throttle.py`), 10 tests | surgical repair against a failing suite |
| **C** | Review a real `git diff` with 7 seeded defects | review recall + false positives |
| **D** | Diagnose a real flaky-test bug with known ground truth (`episode already finished`) | root-cause reasoning from evidence |
| **E** | Reproduce a complete 401-line file (`runtime.py`) with 2 modifications | delivery fidelity at ~3.5k output tokens |

Every contract was validated **before** any model saw it: reference solutions
score 10/10 (A, B), the buggy file fails 5 tests (B), the diff passes
`git apply --check` (C), and the diagnosis has a documented ground truth (D).

## Rules

- Identical prompts for every model; full untruncated files as context
  (784–3835 prompt tokens — no OOM risk, nothing truncated).
- `tool_choice: none`, `enable_thinking: false`, `max_tokens: 8000`
  (the dispatch driver settings).
- **One engine at a time** — llama.cpp and Strata share VRAM.
- Grading is mechanical: pytest for A/B, keyword-recall over the seeded defect
  list for C/D, symbol + line-ratio + functional probe for E. No LLM judge.
- A delivery failure (empty content, prose instead of a file) scores 0 and is
  flagged; it is never reinterpreted as a capability result.

## Results (2026-11-15)

| model | A impl | B fix | C rev | D diag | E compl | E func | wall | t/s |
|---|---|---|---|---|---|---|---|---|
| **gemma4** | **10/10** | **10/10** | 0.86 | **7/7** | 1.03 | 5/5 | 16.7s | 127 |
| Strata | 9/10 | **10/10** | 0.86 | **7/7** | 1.03 | 5/5 | 35.6s | 74 |
| minicpm | 9/10 | 6/10 | 0.86 | **7/7** | 1.04 | 5/5 | 19.5s | 184 |
| Huihui | 9/10 | 6/10 | 0.86 | 6/7 | 1.03 | 5/5 | 48.6s | 66 |
| SC117 | 9/10 | 6/10 | 0.71 | 5/7 | 1.04 | 5/5 | 13.4s | 174 |
| qwen36 | 7/10 | 6/10 | 0.71 | 4/7 | 1.03 | 5/5 | 10.7s | **201** |
| qwen4b | 7/10 | 6/10 | 0.71 | 3/7 | 1.05 | 5/5 | 9.4s | 188 |
| qwen38 | 9/10 | 0/10 ⚠ | 0.57 | **7/7** | 1.03 | 5/5 | 28.7s | 97 |

- **C** = defect recall over 7 seeded defects (nobody found all 7);
  *fp* = estimated false positives.
- **E compl** = delivered lines / 401 (≥0.90 with all symbols = COMPLET);
  **E func** = the 5 behavioural probes all pass.
- ⚠ qwen38's B is a **format failure**: it delivered a prose explanation of the
  three bugs (all correct) with zero fenced code blocks — scored 0, never
  reinterpreted as "bad at fixing bugs".

### Findings that changed prior beliefs

1. **Delivery fidelity is not a fleet problem.** All 8 models returned the
   complete 401-line file, parseable, 16/16 symbols, 5/5 functional — including
   the 4B floor control. The earlier `loop.py` "failure" was an *infeasible
   request*: 1670 lines ≈ 17053 output tokens vs an 8000 ceiling. Impossible
   for any model; the model was never the problem.
2. **One shared real bug: `<` vs `<=`** on the sliding-window boundary. Only
   gemma4 and Strata changed it; every other model copied the original line.
   In task A the common miss was jitter determinism (`Random(seed)` re-seeded
   per call vs a shared generator).
3. **`enable_thinking: false` is mandatory for qwen38 delivery** — with
   thinking on and an 8000-token ceiling, content came back *empty* (reasoning
   only) on 3 of 4 tasks; those scores are delivery failures, not capability.
   With `max_tokens: 16000` + thinking it scored A 10/10, B 10/10 (3 tasks
   still hit the ceiling).
4. **Review recall saturates below 1.00 for everyone.** The most-missed
   defects were the falsy-id skip (`if not user.id`) and the cursor leak.

### Dispatch map (evidence-based)

| use | model | evidence |
|---|---|---|
| **Implement code** | **gemma4** (1st) → minicpm / Huihui / SC117 | only model acing A **and** B; 9/10 group behind it |
| **Review / diagnose** | **Strata** (reference) → gemma4 | perfect B + 7/7 D; slow (74 t/s) so not an implementer |
| **Speed / tools / short text** | qwen36, qwen4b | 201/188 t/s but 7/10 A, 3-4/7 D — never code with edge cases |
| **Daily model, vision** | qwen38 | only with thinking ON + ≥16k budget for code |

## Layout

```
build_prompts.py / build_prompt_E.py   prompt generation (identical for all)
prompts/                              the 5 prompts as sent
task_{a..d}/                          fixtures + reference/ solutions
orchestrate.py                        start → health → run → grade → stop, per model
run_one.sh / master.sh / run_E*.sh     thin wrappers around the same dispatch
grade.py / grade_E.py / check_E.py     mechanical graders (one -q for pytest!)
answers/<slug>/                       raw answers, .timing, grade*.json
final_table.json                      the table above, machine-readable
```

## Grading bug worth remembering

`pytest -q -q` (`-qq`) suppresses the summary line, so any regex on
`N passed` / `N failed` silently returns nothing and **every model scores 0**.
The graders use exactly one `-q`. Caught mid-run; two models were re-graded.

## Run it

```sh
# engines stopped first — one at a time
python3 orchestrate.py            # all llama.cpp models
bash run_E.sh Strata - 8080 qwen3.8-flash-next-iq3_xxs   # Strata row
python3 grade.py <slug> answers/<slug>
```
