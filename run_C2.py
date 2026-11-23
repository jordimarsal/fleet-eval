"""Runner de C2: cada model de la flota ressenya els 9 defectes reals.

  python3 run_C2.py [slug...]          (default: tota la FLEET)

El model ES el ressenyador (sense executor extern). Serial per model:
parar servidor -> engegar el model -> dispatchar els 9 prompts -> guardar.
Sortida: answers/<slug>/C2/<task_id>.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import orchestrate as O
from run_P2 import ANSWERS, _dispatch
import grade_C2 as G

HERE = Path(__file__).parent
PROMPTS = HERE / "prompts" / "C2"


def grade_rec(task_id: str, answer: str) -> dict:
    ok, hit = G.grade_answer(answer, G.load_spec()[task_id])
    items = _numbered(answer)
    return {
        "task_id": task_id, "found": ok, "pattern": hit,
        "items": items,
        "false_positives_est": max(0, items - (1 if ok else 0)),
        "answer_chars": len(answer),
    }


def _numbered(answer: str) -> int:
    import re
    return len(re.findall(r"^\s*\d+[.)]\s", answer, re.M))


def wait_servers_gone(timeout: float = 45.0) -> None:
    """Bloqueja fins que cap llama-server del rig viu (els /app/ son contenidors)."""
    import time
    import subprocess as sp
    t0 = time.time()
    while time.time() - t0 < timeout:
        r = sp.run(["pgrep", "-af", "llama-server"], capture_output=True, text=True)
        alive = [ln for ln in r.stdout.splitlines() if "/app/" not in ln]
        if not alive:
            time.sleep(2)  # gracia: deixa que la VRAM es liquidí del tot
            return
        time.sleep(1)


def main() -> int:
    # regla d'or: Strata i llama.cpp es disputen la VRAM. Fail fast.
    import subprocess as sp
    r = sp.run(["pgrep", "-f", "Strata/engine/strata"], capture_output=True, text=True)
    if r.stdout.strip():
        print("AVORTAT: Strata esta en marxa (pgrep engine/strata). Atura'l primer.")
        return 2
    slugs = sys.argv[1:] or list(O.FLEET)
    ids = sorted(G.load_spec())
    print(f"C2: {len(ids)} defectes reals x {len(slugs)} models", flush=True)
    for slug in slugs:
        out_dir = ANSWERS / slug / "C2"
        out_dir.mkdir(parents=True, exist_ok=True)
        pending = [i for i in ids if not (out_dir / f"{i}.json").exists()]
        if not pending:
            print(f"[{slug}] complet, salt", flush=True)
            continue
        O.stop_server()
        wait_servers_gone()
        gguf = O.MODELS / O.FLEET[slug]
        args = O.build_args(gguf)
        # context de ressenya: 200k demanat explicitament (els prompts fan ~2.5k,
        # pero es vol marge; per sota del sostre auditat de qwen38, 262k)
        # EXCEPCIO: els Inklings (MoE looped) no capen 200k de buffer de calcul
        # en 2x16GB -> 64k (C2.inkling2.server.log: 5.18GB de pp buffer a CUDA1)
        ctx = 65536 if slug.startswith("inkling") else 200000
        args += ["-c", str(ctx)]
        log = HERE / "logs" / f"C2.{slug}.server.log"
        log.parent.mkdir(exist_ok=True)
        import subprocess as sp
        fh = open(log, "w")
        sp.Popen(args, stdout=fh, stderr=sp.STDOUT, start_new_session=True)
        if not O.wait_healthy():
            raise RuntimeError(f"{slug} never healthy (see {log})")
        try:
            found = 0
            crashes = 0
            for tid in pending:
                sub = "" if not tid.startswith("C2-P") else "private/"
                pf = PROMPTS / sub / f"{tid}.md"
                if not pf.exists():
                    print(f"  [{slug}] {tid} SENSE PROMPT, salt", flush=True)
                    continue
                answer = ""
                try:
                    answer = _dispatch(pf.read_text(encoding="utf-8"),
                                       out_dir / f"{tid}.answer.md", slug, O.PORT)
                except Exception as e:
                    crashes += 1
                    rec = {"task_id": tid, "found": False, "pattern": "",
                           "items": 0, "false_positives_est": 0, "answer_chars": 0,
                           "crash": True, "note": f"{type(e).__name__}: {str(e)[:120]}"}
                    (out_dir / f"{tid}.json").write_text(
                        json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
                    print(f"  [{slug}] {tid} CRASH #{crashes} ({rec['note'][:60]})",
                          flush=True)
                    # el servidor ha pogut morir: torna'l en peu
                    if not O.wait_healthy(limit=15):
                        O.stop_server()
                        wait_servers_gone()
                        sp.Popen(args, stdout=fh, stderr=sp.STDOUT, start_new_session=True)
                        if not O.wait_healthy():
                            raise RuntimeError(f"{slug} unusable after crash")
                    if crashes > max(3, len(pending) // 3):
                        print(f"  [{slug}] massa crashes ({crashes}), avortant slug",
                              flush=True)
                        break
                    continue
                rec = grade_rec(tid, answer)
                (out_dir / f"{tid}.json").write_text(
                    json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
                found += rec["found"]
                print(f"  [{slug}] {tid} {'ok ' if rec['found'] else '·  '}"
                      f"items={rec['items']:2d} {rec['pattern'][:40]}", flush=True)
            print(f"== {slug}: {found}/{len(ids)}", flush=True)
        finally:
            O.stop_server()
    print("\n=== resum ===")
    raise SystemExit(summarize())


def summarize() -> int:
    import subprocess
    r = subprocess.run([sys.executable, str(HERE / "grade_C2.py")],
                       capture_output=True, text=True)
    print(r.stdout)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
