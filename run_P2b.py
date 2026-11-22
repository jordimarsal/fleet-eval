"""Runner de P2b (execucio incremental dirigida pel pla).

  python3 run_P2b.py calibra [--executor gemma4]
  python3 run_P2b.py run <slug...> [--executor gemma4]

Nota = tests verds al final / baseline real. Corba de progres per pas.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import orchestrate as O
import P2_sandbox as S
import P2_incremental as I
from run_P2 import (_pre_tests, ANSWERS, CORPUS, EXEC_PROMPT, baseline_tests,
                    ensure_executor_server, load_task, model_plan, human_plan)


def feature_tests_and_text(task_id: str, d: dict, repo: Path, wt: Path) -> tuple[list[str], str]:
    S.copy_tests(wt, repo, d["post_ref"])
    r = subprocess.run(["git", "diff", "--name-only", d["pre_ref"], d["post_ref"]],
                       cwd=str(repo), capture_output=True, text=True)
    changed = set(r.stdout.splitlines())
    pre_t = _pre_tests(repo, d["pre_ref"])
    feat = [p for p in S.test_files_at(repo, d["post_ref"]) if p not in pre_t or p in changed]
    parts = []
    for p in feat:
        if p.endswith((".snap", ".json")):
            continue
        f = wt / p
        if f.exists():
            parts.append(f"--- {p} ---\n{f.read_text(encoding='utf-8', errors='replace')[:8000]}")
    return feat, ("\n\n".join(parts) or "(no tests)")


def main() -> int:
    args = sys.argv[1:]
    executor = "gemma4"
    if "--executor" in args:
        i = args.index("--executor")
        executor = args[i + 1]
        del args[i:i + 2]
    only = None
    if "--task" in args:
        i = args.index("--task")
        only = args[i + 1]
        del args[i:i + 2]
    mode = args[0] if args else "calibra"
    slugs = args[1:] if mode == "run" else []

    with_tests = []
    for f in sorted(CORPUS.glob("P*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if only and d["task_id"] != only:
            continue
        repo = Path.home() / "Documents/CV/projects" / d["repo"]
        r = subprocess.run(["git", "diff", "--name-only", d["pre_ref"], d["post_ref"]],
                           cwd=str(repo), capture_output=True, text=True)
        changed = r.stdout.splitlines()
        pre_t = _pre_tests(repo, d["pre_ref"])
        if any((S.TEST_PAT.search(p) or S.FIXTURE_PAT.search(p)) and p not in pre_t
               for p in changed):
            with_tests.append(d["task_id"])

    print(f"P2b[{mode}]: {len(with_tests)} tasques amb tests · executor={executor}", flush=True)
    ensure_executor_server(executor)
    try:
        targets = ([(f"calibra_{executor}", None)] if mode == "calibra"
                   else [(s, s) for s in slugs])
        for slug, planner in targets:
            out_dir = ANSWERS / slug / "P2b"
            for tid in with_tests:
                d = load_task(tid)
                repo = Path.home() / "Documents/CV/projects" / d["repo"]
                bv, bt = baseline_tests(tid, d, repo)
                if not bt or bv != bt:
                    print(f"  [{slug}] {tid:44s} SKIP baseline {bv}/{bt}", flush=True)
                    continue
                if (out_dir / f"{tid}.json").exists():
                    continue
                plan = human_plan(d) if mode == "calibra" else model_plan(tid, planner)
                if plan is None:
                    continue
                wt = S.ensure_worktree(d["repo"], d["pre_ref"])
                S.install_deps(wt)
                _, tests_txt = feature_tests_and_text(tid, d, repo, wt)
                rec = I.run_incremental(tid, plan, slug, d, repo, executor,
                                        tests_txt, base_total=bt)
                print(f"  [{slug}] {tid:44s} pasos={rec['n_steps']} "
                      f"budget/pas={rec['per_step_budget']} verds={rec['verds_final']}/{bt} "
                      f"score={rec['score']:.3f} corba={rec['progress']}", flush=True)
            rows = [json.loads(f.read_text(encoding="utf-8"))
                    for f in sorted(out_dir.glob("*.json"))]
            if rows:
                tv = sum(r["verds_final"] for r in rows)
                tt = sum(r["baseline_total"] for r in rows)
                print(f"\n=== P2b {slug} ===", flush=True)
                print(f"executor={executor} · verds {tv}/{tt} "
                      f"({(tv/tt if tt else 0):.1%}) · {len(rows)} tasques", flush=True)
                for r in sorted(rows, key=lambda x: -x["score"]):
                    print(f"  {r['task_id']:46s} pasos={r['n_steps']:2d} "
                          f"{r['verds_final']:3d}/{r['baseline_total']:<3d} {r['score']:.2f} "
                          f"mono={r['monotone']}", flush=True)
    finally:
        O.stop_server()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
