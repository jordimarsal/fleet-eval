"""P2: el pla es mesura pel seu efecte — executor fix + tests reals de la feature.

  PLANNER (model sota test) → pla → EXECUTOR FIX (qwen36) → codi → TESTS REALS → % verds

Calibració (run_P2.py calibra): dona a l'executor els plans HUMANS (tasks.md) —
si el pla humà passa els tests amb l'executor, l'executor és instrument vàlid.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

import llm_dispatch as D
import orchestrate as O
import P2_sandbox as S

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus" / "plans"
ANSWERS = HERE / "answers"
PROMPTS = HERE / "prompts" / "P2"

EXECUTOR = "qwen36"          # executor fix per a tota la bateria (configurable: --executor X)
CTX = 32768                  # prompt dels tests + digest; més que prou

EXEC_PROMPT = """You are an implementer working from a plan. Implement it so the provided tests pass.

--- PLAN (defines which files to create and where) ---
{plan}

--- EXISTING SOURCE FILES (before implementation, excerpts — for style/imports only) ---
{digest}

--- TESTS THE RESULT MUST PASS (read carefully: they define the exact API) ---
{tests}

Output ONLY the files the plan asks for, at EXACTLY the paths the plan lists, in this format:

=== FILE: relative/path.ext ===
<file contents>
=== END FILE ===

Write the implementation files (not the tests — they already exist). No prose
outside the file blocks. Do not invent extra files beyond what the plan asks."""


def load_task(task_id: str) -> dict:
    for f in sorted(CORPUS.glob("P*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if d["task_id"] == task_id:
            return d
    raise FileNotFoundError(task_id)


def _pre_tests(repo: Path, ref: str) -> set[str]:
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", ref],
                       cwd=str(repo), capture_output=True, text=True)
    return {p for p in r.stdout.splitlines()
            if S.TEST_PAT.search(p) or S.FIXTURE_PAT.search(p)}


def human_plan(d: dict) -> str:
    """Pla humà: el tasks.md de la spec (checklist T1..Tn amb refs)."""
    spec = Path.home() / "Documents/CV/projects" / d["repo"] / "harness" / "specs" / d["feature"] / "tasks.md"
    if spec.exists():
        return spec.read_text(encoding="utf-8")
    # fallback: reconstrueix del corpus
    return "\n".join(f"- {t}" for t in d.get("tasks", []))


def tree_at(repo: Path, ref: str) -> str:
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", ref],
                       cwd=str(repo), capture_output=True, text=True)
    paths = [p for p in r.stdout.splitlines() if p and not re.search(r"node_modules|\.git/", p)]
    return "\n".join(paths[:400])


def digest_at(repo: Path, ref: str) -> str:
    r = subprocess.run(["git", "ls-tree", "-r", "-l", ref],
                       cwd=str(repo), capture_output=True, text=True)
    sizes = {}
    for line in r.stdout.splitlines():
        m = re.match(r"^\d+\s+blob\s+[0-9a-f]+\s+(\d+)\t(.+)$", line)
        if m:
            sizes[m.group(2)] = int(m.group(1))
    src = sorted((p for p in sizes if p.endswith((".py", ".ts", ".astro", ".js", ".mjs"))
                  and sizes[p] > 0 and not re.search(r"\.min\.|\.bundle\.", p)),
                 key=lambda p: -sizes[p])
    parts = []
    for p in src[:8]:
        r2 = subprocess.run(["git", "show", f"{ref}:{p}"], cwd=str(repo),
                            capture_output=True, text=True)
        if r2.returncode != 0:
            continue
        lines = []
        total = 0
        for line in r2.stdout.splitlines()[:60]:
            b = len(line.encode("utf-8", "replace")) + 1
            if total + b > 4000:
                break
            lines.append(line)
            total += b
        parts.append(f"--- {p} ---\n" + "\n".join(lines))
    return "\n".join(parts) if parts else "(no source files)"


def ensure_executor_server(executor: str | None = None) -> None:
    """Para qualsevol servidor i engega l'executor una vegada."""
    import subprocess as sp
    executor = executor or EXECUTOR
    O.stop_server()
    gguf = O.MODELS / O.FLEET[executor]
    args = O.build_args(gguf)
    if CTX:
        args += ["-c", str(CTX)]
    log = HERE / "logs" / f"P2.{executor}.server.log"
    log.parent.mkdir(exist_ok=True)
    fh = open(log, "w")
    sp.Popen(args, stdout=fh, stderr=sp.STDOUT, start_new_session=True)
    if not O.wait_healthy():
        raise RuntimeError(f"executor {executor} never healthy (see {log})")
    print(f"executor {executor} healthy", flush=True)


def _dispatch(prompt: str, out_path: Path, api_model: str, port: int = 8999,
              max_tokens: int | None = None, budget_suffix: str = "") -> str:
    """Crida llm_dispatch.py (script CLI) i retorna el content.

    max_tokens: sostre dur (sense escalat) per a l'execucio incremental.
    budget_suffix: etiqueta per als fitxers .prompt/.timing (p.ex. step03).
    """
    sfx = f".{budget_suffix}" if budget_suffix else ""
    pf = out_path.with_name(out_path.stem + sfx + ".prompt.md")
    pf.write_text(prompt, encoding="utf-8")
    cmd = [sys.executable, str(HERE / "llm_dispatch.py"),
           str(pf), str(out_path), api_model, str(port)]
    if max_tokens:
        cmd.append(str(max_tokens))
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        raise RuntimeError(f"dispatch failed: {r.stderr[-500:]}")
    # la línia de timing és a stdout; el content, al fitxer
    out_path.with_name(out_path.stem + sfx + ".timing.txt").write_text(
        r.stdout.strip(), encoding="utf-8")
    return out_path.read_text(encoding="utf-8") if out_path.exists() else ""


def baseline_tests(task_id: str, d: dict, repo: Path) -> tuple[int, int]:
    """Codi REAL (post_ref) + tests → denominador fix i validació del sandbox.

    Sense això, un codi d'executor que trenca imports fa caure el denominador
    (vitest/pytest no compten els tests que no es poden col·leccionar) i el %
    deixa de ser comparable. El baseline hauria de passar 100%.
    """
    cache = ANSWERS / "baseline" / f"{task_id}.json"
    if cache.exists():
        j = json.loads(cache.read_text(encoding="utf-8"))
        return j["verds"], j["total"]
    wt = S.ensure_worktree(d["repo"], d["post_ref"])
    S.install_deps(wt)
    # al post_ref els tests ja hi són; executem els de la feature
    r = sh_git(repo, ["diff", "--name-only", d["pre_ref"], d["post_ref"]])
    changed = set(r.stdout.splitlines())
    pre_t = _pre_tests(repo, d["pre_ref"])
    all_tests = S.test_files_at(repo, d["post_ref"])
    feat = [p for p in all_tests if p not in pre_t or p in changed]
    verds, total, out = S.run_tests(wt, feat, d["repo"])
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps({"task_id": task_id, "verds": verds, "total": total,
                                 "tail": out[-500:]}, indent=2), encoding="utf-8")
    return verds, total


def sh_git(repo: Path, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=str(repo), capture_output=True, text=True)


def run_one(task_id: str, plan_text: str, slug: str = "calibra") -> dict:
    d = load_task(task_id)
    repo = Path.home() / "Documents/CV/projects" / d["repo"]
    t0 = time.time()

    # 1. sandbox al pre_ref
    wt = S.ensure_worktree(d["repo"], d["pre_ref"])
    S.install_deps(wt)

    # 2. tests de la feature: els copiem JA (l'executor els veurà) i els executarem
    all_tests = S.copy_tests(wt, repo, d["post_ref"])
    r = subprocess.run(["git", "diff", "--name-only", d["pre_ref"], d["post_ref"]],
                       cwd=str(repo), capture_output=True, text=True)
    changed = set(r.stdout.splitlines())
    pre_t = _pre_tests(repo, d["pre_ref"])
    feature_tests = [p for p in all_tests
                     if p not in pre_t or p in changed]
    if not feature_tests:
        feature_tests = [p for p in all_tests if p in changed]
    # contingut dels tests (contracte exacte de l'API) — cap de 8k chars per fitxer
    tests_txt_parts = []
    for p in feature_tests:
        if p.endswith((".snap", ".json")):
            continue
        f = wt / p
        if f.exists():
            txt = f.read_text(encoding="utf-8", errors="replace")
            tests_txt_parts.append(f"--- {p} ---\n{txt[:8000]}")
    tests_txt = "\n\n".join(tests_txt_parts) or "(no tests)"

    # 3. executor (amb els tests al davant; el PLA és l'única guia d'ubicació)
    prompt = EXEC_PROMPT.format(plan=plan_text,
                                digest=digest_at(repo, d["pre_ref"]), tests=tests_txt)
    out_md = ANSWERS / slug / "P2" / f"{task_id}.executor.md"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    content = _dispatch(prompt, out_md, EXECUTOR)
    files = S.parse_executor_files(content)
    retry_note = ""
    if not files:
        # el model es va encallar en prosa/raonament sense lliurar cap fitxer:
        # reintenta amb ordre directe (mateix cost que un buit, evita un 0 fals)
        content = _dispatch(
            prompt + "\n\nIMPORTANT: Do NOT analyze or explain. Your FIRST line must be "
                     "'=== FILE: <path> ==='. Emit the file contents now.",
            out_md.with_name(out_md.stem + ".retry.md"), EXECUTOR)
        files = S.parse_executor_files(content)
        retry_note = "retry_no_files"
    n_written = S.apply_files(wt, files)
    # els tests són sagrats: si l'executor n'ha lliurat de propis, els re-copiem
    S.copy_tests(wt, repo, d["post_ref"])

    # 4. córrer tests de la feature
    verds, total_run, out = S.run_tests(wt, feature_tests, d["repo"])
    # denominador FIX: el total que dóna el codi real (post_ref), no el que
    # deixa el codi de l'executor (un import trencat baixaria el total)
    base_v, total = baseline_tests(task_id, d, repo)
    total = total or total_run
    score = min(verds / total, 1.0) if total else 0.0

    rec = {
        "task_id": task_id, "repo": d["repo"], "pre_ref": d["pre_ref"],
        "post_ref": d["post_ref"], "executor": EXECUTOR,
        "files_delivered": sorted(files), "n_written": n_written,
        "test_files": feature_tests, "verds": verds, "total": total,
        "total_run": total_run, "baseline_verds": base_v,
        "score": round(score, 4), "wall_s": round(time.time() - t0, 1),
        "retry": retry_note, "test_output_tail": out[-1500:],
    }
    out_dir = ANSWERS / slug / "P2"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{task_id}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2),
                                             encoding="utf-8")
    return rec


def model_plan(task_id: str, planner_slug: str) -> str | None:
    """Pla del model: el FILES/TASKS/GATES que el planner va produir a P1 (.md)."""
    for ext in (".md", ".json"):
        f = ANSWERS / planner_slug / "P" / f"{task_id}{ext}"
        if not f.exists():
            continue
        if ext == ".md":
            return f.read_text(encoding="utf-8") or None
        d = json.loads(f.read_text(encoding="utf-8"))
        plan = d.get("plan") or d.get("content") or d.get("text") or ""
        if not plan:
            plan = d.get("plan_md") or d.get("answer") or ""
        if plan:
            return plan
    return None


def main() -> int:
    global EXECUTOR
    args = sys.argv[1:]
    # --executor <slug>: model que fa d'executor (default qwen36)
    if "--executor" in args:
        i = args.index("--executor")
        EXECUTOR = args[i + 1]
        del args[i:i + 2]
    mode = args[0] if args else "calibra"
    # slugs: a calibra n'hi ha cap (plans humans); a run, els planners
    slugs = args[1:] if mode == "run" else []
    if mode == "run" and not slugs:
        slugs = [s for s, f in O.FLEET.items() if (HERE / "answers" / s / "P").exists()]

    # tasques amb tests reals (nous/tocats vs pre_ref)
    with_tests = []
    for f in sorted(CORPUS.glob("P*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        repo = Path.home() / "Documents/CV/projects" / d["repo"]
        r = subprocess.run(["git", "diff", "--name-only", d["pre_ref"], d["post_ref"]],
                           cwd=str(repo), capture_output=True, text=True)
        changed = r.stdout.splitlines()
        pre_t = _pre_tests(repo, d["pre_ref"])
        has_test = any((S.TEST_PAT.search(p) or S.FIXTURE_PAT.search(p)) and p not in pre_t
                       for p in changed)
        if has_test:
            with_tests.append(d["task_id"])

    print(f"P2[{mode}]: {len(with_tests)} tasques amb tests reals", flush=True)
    ensure_executor_server()
    try:
        targets = ([(f"calibra_{EXECUTOR}", None)] if mode == "calibra"
               else [(s, s) for s in slugs])
        for slug, planner in targets:
            n_done = n_skip = n_corrupt = 0
            for tid in with_tests:
                # una tasca només és mesurable si el codi REAL passa els seus tests
                d0 = load_task(tid)
                repo0 = Path.home() / "Documents/CV/projects" / d0["repo"]
                bv, bt = baseline_tests(tid, d0, repo0)
                if not bt or bv != bt:
                    n_corrupt += 1
                    print(f"  [{slug}] {tid:44s} SKIP corpus corrupte "
                          f"(baseline {bv}/{bt})", flush=True)
                    continue
                out = ANSWERS / slug / "P2" / f"{tid}.json"
                if out.exists():
                    n_skip += 1
                    continue
                d = load_task(tid)
                if mode == "calibra":
                    plan = human_plan(d)
                else:
                    plan = model_plan(tid, planner)
                    if plan is None:
                        continue
                rec = run_one(tid, plan, slug)
                n_done += 1
                print(f"  [{slug}] {tid:44s} verds={rec['verds']}/{rec['total']} "
                      f"score={rec['score']} files={rec['n_written']} wall={rec['wall_s']}s",
                      flush=True)
            # resum per slug
            rows = [json.loads(f.read_text(encoding="utf-8"))
                    for f in sorted((ANSWERS / slug / "P2").glob("*.json"))]
            if rows:
                tv = sum(r["verds"] for r in rows)
                tt = sum(r["total"] for r in rows)
                print(f"\n=== P2[{mode}] {slug} ===", flush=True)
                print(f"executor={EXECUTOR} · tests verds: {tv}/{tt} "
                      f"({(tv/tt if tt else 0):.1%}) · {len(rows)} tasques "
                      f"(nous={n_done} skip={n_skip} corrupte={n_corrupt})", flush=True)
                for r in sorted(rows, key=lambda x: -x["score"]):
                    print(f"  {r['task_id']:46s} {r['verds']:2d}/{r['total']:2d}  {r['score']:.2f}",
                          flush=True)
    finally:
        O.stop_server()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
