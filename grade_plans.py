#!/usr/bin/env python3
"""grade_plans.py — mechanical grader for the P (planner) battery.

Nota el pla lliurat contra la font de veritat del corpus (el que REALMENT va
passar): fitxers canviats pel commit real, requisits aprovats, descomposició
amb depends_on/refs. Tot mecànic — cap LLM judge (regla de fleet-eval).

Components (P score = 0.55*file_f1 + 0.30*coverage + 0.15*breakdown):
  file_f1   recall+precision del llistat FILES del pla contra els fitxers
            canviats realment. Matching tolerant: igualtat, tail de path o
            basename (els fitxers NOUS de la feature no es poden saber amb nom
            exacte). La precision penalitza abocar l'arbre sencer i els paths
            inventats (ni a l'arbre pre ni a la veritat).
  coverage  fracció de requisits aprovats (Rn) mapats a tasques del pla
            (refs de la secció TASKS; si no, menció dins de TASKS).
  breakdown la secció TASKS es parseja (>=1 tasca), cap depends_on penjant
            (tot dep referencedefinit) i GATES no buit amb test/gate.

usage: grade_plans.py <slug> [answers_dir]
writes: <answers_dir>/grade_P.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus" / "plans"
W_FILE, W_COV, W_BREAK = 0.85, 0.10, 0.05   # v2: file_f1 és l'únic discriminatiu
                                            # (v1 0.55/0.30/0.15: coverage i breakdown
                                            # eren constants per a tothom)

SEC = re.compile(r"^(FILES|TASKS|GATES)\s*$", re.MULTILINE)


def sections(text: str) -> dict[str, str]:
    """Splits the plan into FILES/TASKS/GATES sections (case-insensitive headers)."""
    found: dict[str, str] = {}
    marks = [(m.group(1).upper(), m.start(), m.end()) for m in SEC.finditer(text)]
    for i, (name, _s, e) in enumerate(marks):
        stop = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        found[name] = text[e:stop].strip()
    return found


def paths_of(block: str) -> list[str]:
    """Repo-relative path-looking tokens from a FILES block."""
    out = []
    for line in block.splitlines():
        p = line.strip().strip("-*` ")
        p = re.sub(r"^\d+[.)]\s*", "", p)
        if re.match(r"^[\w./\\-]+(/[\w./\\-]+)*\.\w{1,6}$", p):
            out.append(p.lstrip("./"))
    return out


def path_hit(p: str, t: str) -> bool:
    """Exact, tail-of-path or basename match (new files can't be guessed exactly)."""
    if p == t:
        return True
    if p.endswith("/" + t) or t.endswith("/" + p):
        return True
    return Path(p).name == Path(t).name


def file_score(proposed: list[str], truth: list[str], tree: list[str]) -> tuple[float, dict]:
    hits, seen_t = set(), set()
    hallucinated = []
    tree_set = set(tree)
    for p in proposed:
        matched = None
        for t in truth:
            if t in seen_t:
                continue
            if path_hit(p, t):
                matched = t
                break
        if matched:
            seen_t.add(matched)
        elif p not in tree_set and not any(path_hit(p, t) for t in tree):
            hallucinated.append(p)
    recall = len(seen_t) / len(truth) if truth else 0.0
    precise = len(seen_t) / len(proposed) if proposed else 0.0
    f1 = (2 * recall * precise / (recall + precise)) if (recall + precise) else 0.0
    return f1, {"recall": round(recall, 3), "precision": round(precise, 3),
                "hits": sorted(seen_t), "missed": sorted(set(truth) - seen_t),
                "hallucinated": sorted(set(hallucinated))}


def coverage_of(tasks_block: str, reqs: list[str]) -> tuple[float, list[str]]:
    """Fraction of approved requirements mapped by task refs (fallback: mention)."""
    refs = set(re.findall(r"R\d+", tasks_block))
    covered = [r for r in reqs if r in refs]
    missed = [r for r in reqs if r not in covered]
    return (len(covered) / len(reqs) if reqs else 0.0), missed


def breakdown_of(tasks_block: str, gates_block: str, truth_tasks: dict) -> tuple[float, dict]:
    ids = set(re.findall(r"\bT\d+\b", tasks_block))
    if not ids:
        return 0.0, {"reason": "no hi ha descomposició Tn"}
    deps = re.findall(r"depends_on:\s*(.+)", tasks_block)
    dangling = []
    for d in deps:
        for ref in re.findall(r"T\d+", d):
            if ref not in ids:
                dangling.append(ref)
    gates_ok = bool(gates_block) and bool(re.search(r"test|gate|pytest|check|verif|lint", gates_block, re.I))
    score = (0.0 if dangling else 0.5) + (0.5 if gates_ok else 0.0)
    return score, {"tasks_planned": len(ids),
                   "tasks_real": len(truth_tasks),
                   "dangling_deps": sorted(set(dangling)),
                   "gates_ok": gates_ok}


def grade_one(task_json: dict, answer_path: Path, tree: list[str]) -> dict:
    truth = task_json["truth"]
    if not answer_path.exists() or not answer_path.read_text(encoding="utf-8", errors="replace").strip():
        return {"task_id": task_json["task_id"], "score": 0.0,
                "passed": False, "detail": "delivery buida (fins i tot escalant)"}
    text = answer_path.read_text(encoding="utf-8", errors="replace")
    secs = sections(text)
    files_block = secs.get("FILES", "")
    tasks_block = secs.get("TASKS", "")
    gates_block = secs.get("GATES", "")
    if not (files_block or tasks_block):
        return {"task_id": task_json["task_id"], "score": 0.0, "passed": False,
                "detail": "sense seccions FILES/TASKS (prosa?)"}
    proposed = paths_of(files_block)
    f1, fdet = file_score(proposed, truth["files"], tree)
    cov, missed_req = coverage_of(tasks_block, truth["requirements"])
    brk, bdet = breakdown_of(tasks_block, gates_block, truth["tasks"])
    score = W_FILE * f1 + W_COV * cov + W_BREAK * brk
    return {"task_id": task_json["task_id"], "repo": task_json["repo"],
            "score": round(score, 3), "passed": score >= 0.5,
            "file_f1": round(f1, 3), "coverage": round(cov, 3), "breakdown": round(brk, 3),
            "files_proposed": len(proposed), "files_real": len(truth["files"]),
            "req_missed": missed_req, **fdet, **bdet}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    slug = sys.argv[1]
    answers = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "answers" / slug / "P"
    tasks = sorted(CORPUS.glob("P*.json"))
    if not tasks:
        print("corpus buit: corre harvest_plans.py primer", file=sys.stderr)
        return 1
    per_task = []
    for tj in tasks:
        d = json.loads(tj.read_text(encoding="utf-8"))
        # l'arbre pre el reconstruim del propi prompt (secció FILE TREE, abans del digest)
        prompt = (HERE / "prompts" / "P" / f"{d['task_id']}.md").read_text(encoding="utf-8")
        m = re.search(r"REPOSITORY FILE TREE[^\n]*\n(.*?)\n--- KEY SOURCE FILES",
                      prompt, re.S)
        tree = [l.strip() for l in (m.group(1).splitlines() if m else []) if l.strip()]
        r = grade_one(d, answers / f"{d['task_id']}.md", tree)
        per_task.append(r)
        print(f"  {r['task_id']:46s} {r['score']:.2f}  "
              f"f1={r.get('file_f1','-')} cov={r.get('coverage','-')} brk={r.get('breakdown','-')}"
              + ("" if r.get("passed") else f"  [{r.get('detail','FAIL')}]"))
    total = round(sum(r["score"] for r in per_task) / len(per_task), 3)
    out = {"P": {"score": total, "passed": total >= 0.5, "tasks": len(per_task),
                 "passed_n": sum(1 for r in per_task if r["passed"]),
                 "per_task": per_task}}
    dest = answers.parent / "grade_P.json"
    dest.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"P: {total} ({out['P']['passed_n']}/{len(per_task)} tasques >=0.5) -> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
