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
- `tool_choice: none`, `enable_thinking: false`, budget inicial `max_tokens: 8000`
  (the dispatch driver settings).
- **Escalació de pressupost (2026-11-22):** si la resposta torna amb content BUIT
  i raonament no buit, el model s'ha menjar el sostre pensant — això no mesura
  capacitat sinó el pressupost. El driver (`llm_dispatch.py`) reintentà
  automàticament amb 16000 i després 24000 fins que lliuri content; el
  pressupost efectiu i els intents viatgen a la línia de timing (`budget=`,
  `attempts=`) i la nota queda al receipt. Un 0 amb `attempts=3` SÍ que és un
  resultat genuí. Precendent: el qwen38 amb 8000 va lliurar buit a 3 de 4
  tasques i amb 16000 va puntuar A 10/10 B 10/10 — el 0 era l'artefacte, no el
  model (README finding 3, ara ferit al driver i no a mà).
- **One engine at a time** — llama.cpp and Strata share VRAM.
- Grading is mechanical: pytest for A/B, keyword-recall over the seeded defect
  list for C/D, symbol + line-ratio + functional probe for E. No LLM judge.
- A delivery failure at the LAST budget step (still empty at 24000, or prose
  instead of a file) scores 0 and is flagged; it is never reinterpreted as a
  capability result.

## P battery (2026-11-22) — who is the best PLANNER?

Motivació: el routing de farga escollia worker per A+B i reviewer per tradició
(Strata), però no hi havia CAP mesura de planning. La font de veritat no és un
pla escrit a mà: són **specs SDD reals ja implementades de l'estol** — el pla
del model es nota contra el que REALMENT va passar:

| veritat | d'on |
|---|---|
| fitxers canviats | `git diff --name-only <pre>..<post>` del commit real de la feature |
| requisits aprovats | `requirements.md` (Rn) de la spec |
| descomposició real | `tasks.md` (Tn + depends_on + refs — un DAG parsegable) |

I l'*input* és el repo ANTERIOR (requirements aprovats + arbre de fitxers al
commit pare). **Contaminació zero**: repos privats locals, cap model de la
flota pot haver-se memoritzat la solució.

- Corpus: `python3 harvest_plans.py` (filtres: feature completa amb 1-6 commits,
  3-15 fitxers canviats, ≥2 requisits, ≥3 tasques) → 12 tasques de 6 repos.
- Runner: `python3 run_P.py [slug ...]`; grader: `grade_plans.py`.
- P score = **0.55 × file_f1** (recall+precision del llistat FILES contra els
  fitxers reals, matching tolerant per tail/basename) **+ 0.30 × coverage**
  (requisits mapats a tasques) **+ 0.15 × breakdown** (TASKS parsejable, cap
  dependència penjant, GATES amb tests). Tot mecànic: no LLM judge.
- Limitació declarada: el pla real és UN camí vàlid — la nota mesura resultats
  (fitxers/requisits), no prosa. I el code-by-lang de ggufbench segueix sent la
  font per al worker per idioma (fleet-eval és python-only a A/B/E).

## Results (2026-11-15; +2 models 2026-11-22)

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
| **inkling2** ★ | **10/10**¹ | **10/10** | **1.00** | 6/7 | 0.95 | 5/5 | 673s¹ | 36 |
| **inkling2unc** ★ | **10/10**¹ | **10/10** | 0.86 | 6/7 | 0.95 | 5/5 | 587s¹ | 36 |

¹ **escalat de pressupost**: la A va lliurar buit a 8000 (el model es menja el sostre
raonant, ~26k chars de thinking) i va puntuar 10/10 amb 16000 (`attempts=2`). El wall de
la A inclou els dos intents. És el primer model al qual la regla d'escalat del driver
s'aplica i confirma el precedent del qwen38: el 0 inicial mesurava el pressupost, no el
model. La C d'inkling2 (1.00, els 8 defectes) és la millor revisió mai mesurada aquí, i
la B 10/10 empata el màxim de la flota.

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
| **Implement code** | **gemma4 / inkling2** (1st) → minicpm / Huihui / SC117 | A+B 10/10 (inkling2 amb budget 16000, vegeu la nota ¹); 9/10 group behind it |
| **Review / diagnose** | **Strata** (reference) → gemma4 → **inkling2** | perfect B + 7/7 D (Strata); inkling2: C 1.00, la millor revisió de la flota |
| **Speed / tools / short text** | qwen36, qwen4b | 201/188 t/s but 7/10 A, 3-4/7 D — never code with edge cases |
| **Daily model, vision** | qwen38 | only with thinking ON + ≥16k budget for code |

## Layout

```
build_prompts.py / build_prompt_E.py   prompt generation (identical for all)
prompts/                              the 5 prompts as sent
task_{a..d}/                          fixtures + reference/ solutions
orchestrate.py                        start → health → run → grade → stop, per model
run_one.sh / master.sh / run_E*.sh     thin wrappers around the same dispatch
llm_dispatch.py                        the dispatch driver (VERSIONED since 2026-11-22:
                                       it was lost once — run_one/run_E prefer this
                                       copy and fall back to the historical paths
                                       ../ and /tmp/opencode, keep them in sync)
grade.py / grade_E.py / check_E.py     mechanical graders (one -q for pytest!)
harvest_plans.py                       build the P corpus: real SDD specs of the
                                       estol → planning tasks (file-set from the
                                       real commit, approved requirements, real
                                       task DAG; private repos = zero leakage)
prompts/P/ + corpus/plans/             the P prompts and their ground truth
run_P.py / grade_plans.py              run + mechanical grade of the P battery
                                       (file_f1 0.55 · requirement coverage 0.30 ·
                                       breakdown/gates 0.15 — no LLM judge)
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
