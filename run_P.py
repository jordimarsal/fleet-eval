#!/usr/bin/env python3
"""run_P.py — run the P (planner) battery for slugs, one engine at a time.

Mateix patró que orchestrate.py: stop → build_args (perfil del model) → start
→ wait_healthy → dispatch de cada prompt del corpus amb llm_dispatch.py (amb
escalat de pressupost) → grade_plans.py → stop.

usage: python3 run_P.py [slug ...]    (default: tota la flota amb el gguf al disc)
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import orchestrate as O  # noqa: E402  (FLEET, MODELS, build_args, stop_server, ...)

LOGS = HERE / "logs"
CORPUS = HERE / "corpus" / "plans"


def dispatch_task(slug: str, prompt: Path, out_md: Path, port: int) -> None:
    driver = HERE / "llm_dispatch.py"
    r = subprocess.run(
        [sys.executable, str(driver), str(prompt), str(out_md), slug, str(port)],
        capture_output=True, text=True)
    out_md.with_suffix(".timing").write_text(r.stdout + r.stderr, encoding="utf-8")
    line = (r.stdout or r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr).strip() else "?"
    print(f"    {out_md.stem}: {line}")


def grade(slug: str) -> dict:
    r = subprocess.run(
        [sys.executable, str(HERE / "grade_plans.py"), slug,
         str(HERE / "answers" / slug / "P")],
        capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    p = HERE / "answers" / slug / "grade_P.json"
    return json.loads(p.read_text()) if p.exists() else {}


def main() -> int:
    corpus = sorted(CORPUS.glob("P*.json"))
    if not corpus:
        print("corpus buit: corre harvest_plans.py primer", file=sys.stderr)
        return 1
    # --ctx N: override del context del perfil (darrer -c guanya a llama.cpp). Útil
    # quan el pin del .txt només carrega amb la màquina callada i la bateria P (que
    # no mesura context) ha de córrer amb el despatx actiu. Queda al log del server.
    ctx_override = None
    if "--ctx" in sys.argv:
        ctx_override = int(sys.argv[sys.argv.index("--ctx") + 1])
        sys.argv.remove("--ctx")
        sys.argv.remove(str(ctx_override))
    wanted = sys.argv[1:] or [s for s, f in O.FLEET.items()
                              if (O.MODELS / f).exists()]
    results: dict[str, dict] = {}
    summary = HERE / "grade_P_summary.json"
    if summary.exists():
        results = json.loads(summary.read_text())
    print(f"corpus: {len(corpus)} tasques · flota: {wanted}")
    for slug in wanted:
        gguf = O.MODELS / O.FLEET.get(slug, "")
        if not gguf.exists():
            print(f"!! {slug}: falta {gguf} — skip")
            continue
        if (HERE / "answers" / slug / "grade_P.json").exists():
            print(f"== {slug}: grade_P ja hi és, skip (esborra'l per re-córrer)")
            results[slug] = json.loads((HERE / "answers" / slug / "grade_P.json").read_text())["P"]
            continue
        print(f"\n=== {slug} ===", flush=True)
        O.stop_server()
        args = O.build_args(gguf)
        if ctx_override:
            args += ["-c", str(ctx_override)]
        (LOGS / f"{slug}.P.server.log").write_text(" ".join(args) + "\n")
        log = open(LOGS / f"{slug}.P.server.log", "a")
        proc = subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT,
                                cwd=str(O.HOME / "ia/llama"))
        if not O.wait_healthy():
            print(f"!! {slug}: never healthy — skip")
            proc.terminate()
            continue
        outdir = HERE / "answers" / slug / "P"
        outdir.mkdir(parents=True, exist_ok=True)
        t0 = time.monotonic()
        for tj in corpus:
            d = json.loads(tj.read_text(encoding="utf-8"))
            dispatch_task(slug, HERE / "prompts" / "P" / f"{d['task_id']}.md",
                          outdir / f"{d['task_id']}.md", O.PORT)
        print(f"   bateria feta en {time.monotonic() - t0:.0f}s; grading…", flush=True)
        results[slug] = grade(slug)["P"]
        summary.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        O.stop_server()
    O.stop_server()
    print("\n=== RESUM P ===")
    for slug, g in sorted(results.items(), key=lambda kv: -(kv[1] or {}).get("score", 0)):
        if g:
            print(f"{slug:14s} P:{g.get('score')}  ({g.get('passed_n')}/{g.get('tasks')} >=0.5)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
