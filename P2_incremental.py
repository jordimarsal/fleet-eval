"""P2b: execucio INCREMENTAL dirigida pel pla (mesura el planner, no l'executor).

Invariant: l'executor es fix i queda constret pel pla.
  - el pla decideix QUANTS passos hi ha, QUIN abast te cada un i en quin ORDRE
  - l'executor rep el pla complet + l'estat actual del repo + els tests, i se li
    demana implementar NOMES el pas T_k
  - el pressupost de sortida es TOTAL i es reparteix entre els passos:
        per_step = clamp(TOTAL / n_steps, MIN_STEP, MAX_STEP)
    -> un pla massa gruixut no hi cap en un pas; un pla inflat de passos trivials
       no te prou pressupost per fer res. La granularitat del pla importa.
  - nota = tests verds al final / baseline real (denominador fix)
  - corba de progres: verds despres de cada pas (un bon pla es monotona)
"""
from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path

import orchestrate as O
import P2_sandbox as S

HERE = Path(__file__).resolve().parent
ANSWERS = HERE / "answers"

TOTAL_BUDGET = 48000     # tokens de sortida per tasca, repartits entre passos
MIN_STEP = 3000          # un pas trivial no pot fer res amb menys
MAX_STEP = 12000         # cap d'un sol pas: un pla massa gruixut falla

STEP_PROMPT = """You are an implementer working through a plan STEP BY STEP.

--- FULL PLAN (for context) ---
{plan}

--- CURRENT STEP TO IMPLEMENT NOW (implement ONLY this) ---
{step}

--- CURRENT REPOSITORY STATE (file tree, after previous steps) ---
{tree}

--- YOUR PREVIOUS WORK IN THIS TASK (complete files you already wrote; preserve their behavior) ---
{working}

--- OTHER SOURCE FILES (excerpts, for style/imports) ---
{digest}

--- TESTS THE FINAL RESULT MUST PASS (they define the exact API) ---
{tests}

Implement ONLY the current step. Output ONLY the files this step needs, at the
paths the plan gives, in this format:

=== FILE: relative/path.ext ===
<file contents>
=== END FILE ===

When you output a file again, output its COMPLETE contents (never a fragment)
and preserve the behaviour that already works. Do not implement later steps.
No prose outside the file blocks."""


def parse_steps(plan: str) -> list[dict]:
    """Extreu T1..Tn del pla (tasks.md huma o FILES/TASKS/GATES dels models)."""
    lines = plan.splitlines()
    starts = []
    for i, ln in enumerate(lines):
        m = re.match(r"^\s*(?:-\s*\[[ xX]\]\s*)?(T\d+)\s*:\s*(.+?)\s*$", ln)
        if m:
            starts.append((i, m.group(1), m.group(2)))
    steps = []
    for idx, (i, tid, title) in enumerate(starts):
        end = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
        body_lines = lines[i + 1:end]
        # talla si apareix una seccio GATES abans del seguent T
        cut = [j for j, l in enumerate(body_lines) if re.match(r"^\s*GATES\s*$", l)]
        if cut:
            body_lines = body_lines[:cut[0]]
        body = "\n".join(l for l in body_lines if l.strip())
        dep = re.search(r"depends_on\s*:\s*(.+)", body)
        refs = re.search(r"refs\s*:\s*(.+)", body)
        steps.append({"id": tid, "title": title, "depends_on": dep.group(1).strip() if dep else "",
                      "refs": refs.group(1).strip() if refs else "", "body": body})
    return steps


def topo_order(steps: list[dict]) -> list[dict]:
    """Ordre estable respectant depends_on (que poden ser ids o '(none)')."""
    by_id = {s["id"]: s for s in steps}
    done: set[str] = set()
    out: list[dict] = []
    pending = list(steps)
    while pending:
        progressed = False
        for s in list(pending):
            deps = {d.strip() for d in re.findall(r"T\d+", s["depends_on"] or "")}
            if deps <= done:
                out.append(s)
                done.add(s["id"])
                pending.remove(s)
                progressed = True
        if not progressed:  # cicle o deps desconegudes: respecta l'ordre del text
            out.extend(pending)
            break
    return out


def working_set(wt: Path, touched: list[str], per_file: int = 12000,
                total_cap: int = 40000) -> str:
    """Contingut COMPLET dels fitxers que ja hem tocat (per no reescriure a cegues)."""
    parts, used = [], 0
    for rel in reversed(touched):  # els mes recents primer
        p = wt / rel
        if not p.is_file():
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        chunk = txt[:per_file]
        if used + len(chunk) > total_cap:
            break
        parts.append(f"--- {rel} ---\n{chunk}")
        used += len(chunk)
    return "\n\n".join(parts) if parts else "(none yet)"


def tree_now(wt: Path) -> str:
    r = subprocess.run(["git", "ls-files"], cwd=str(wt), capture_output=True, text=True)
    files = [p for p in r.stdout.splitlines() if p and ".venv/" not in p
             and "node_modules/" not in p]
    return "\n".join(files[:400])


def digest_now(wt: Path) -> str:
    """Digest dels fitxers font mes grans de l'estat ACTUAL del worktree."""
    cand = []
    for p in (wt).rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(wt))
        if any(x in rel for x in (".venv/", "node_modules/", ".git/")):
            continue
        if p.suffix.lower() not in (".py", ".ts", ".astro", ".js", ".mjs"):
            continue
        if re.search(r"\.min\.|\.bundle\.", rel):
            continue
        try:
            cand.append((p.stat().st_size, rel, p))
        except OSError:
            pass
    cand.sort(reverse=True)
    parts = []
    for size, rel, p in cand[:8]:
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines, total = [], 0
        for line in txt.splitlines()[:60]:
            b = len(line.encode("utf-8", "replace")) + 1
            if total + b > 4000:
                break
            lines.append(line)
            total += b
        parts.append(f"--- {rel} ---\n" + "\n".join(lines))
    return "\n".join(parts) if parts else "(no source files)"


def run_incremental(task_id: str, plan_text: str, slug: str, d: dict, repo: Path,
                    executor: str, tests_txt: str, base_total: int) -> dict:
    from run_P2 import _dispatch  # reutilitza el cridador de llm_dispatch

    wt = S.ensure_worktree(d["repo"], d["pre_ref"])
    S.install_deps(wt)
    # tests de la feature al worktree (els executarem despres de cada pas)
    S.copy_tests(wt, repo, d["post_ref"])
    r = subprocess.run(["git", "diff", "--name-only", d["pre_ref"], d["post_ref"]],
                       cwd=str(repo), capture_output=True, text=True)
    changed = set(r.stdout.splitlines())
    pre_t = {p for p in subprocess.run(["git", "ls-tree", "-r", "--name-only", d["pre_ref"]],
                                       cwd=str(repo), capture_output=True, text=True).stdout.splitlines()
             if S.TEST_PAT.search(p) or S.FIXTURE_PAT.search(p)}
    feature_tests = [p for p in S.test_files_at(repo, d["post_ref"])
                     if p not in pre_t or p in changed]

    steps = topo_order(parse_steps(plan_text))
    if not steps:  # pla sense Tn: un unic pas amb tot el pla
        steps = [{"id": "T1", "title": "implement the plan", "depends_on": "",
                  "refs": "", "body": plan_text}]
    n = len(steps)
    per_step = max(MIN_STEP, min(MAX_STEP, TOTAL_BUDGET // n))

    progress, applied_total = [], 0
    touched: list[str] = []
    out_dir = ANSWERS / slug / "P2b"
    out_dir.mkdir(parents=True, exist_ok=True)

    for k, s in enumerate(steps, 1):
        prompt = STEP_PROMPT.format(
            plan=plan_text, step=f"{s['id']}: {s['title']}\n{s['body']}",
            tree=tree_now(wt), working=working_set(wt, touched),
            digest=digest_now(wt), tests=tests_txt)
        out_md = out_dir / f"{task_id}.step{k:02d}.md"
        content = _dispatch(prompt, out_md, executor, max_tokens=per_step,
                            budget_suffix=f"step{k}")
        files = S.parse_executor_files(content)
        applied_total += S.apply_files(wt, files)
        for rel in files:
            if rel not in touched:
                touched.append(rel)
        S.copy_tests(wt, repo, d["post_ref"])  # tests sagrats
        verds, trun, _ = S.run_tests(wt, feature_tests, d["repo"])
        progress.append(verds)

    final = progress[-1] if progress else 0
    score = min(final / base_total, 1.0) if base_total else 0.0
    rec = {
        "task_id": task_id, "repo": d["repo"], "executor": executor,
        "planner_slug": slug, "mode": "incremental",
        "n_steps": n, "per_step_budget": per_step,
        "steps": [f"{s['id']}: {s['title']}" for s in steps],
        "verds_final": final, "baseline_total": base_total,
        "score": round(score, 4), "progress": progress,
        "files_applied": applied_total,
        "monotone": all(b >= a for a, b in zip(progress, progress[1:])),
    }
    (out_dir / f"{task_id}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2),
                                             encoding="utf-8")
    return rec
