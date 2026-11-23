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


def main() -> int:
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
        gguf = O.MODELS / O.FLEET[slug]
        args = O.build_args(gguf)
        log = HERE / "logs" / f"C2.{slug}.server.log"
        log.parent.mkdir(exist_ok=True)
        import subprocess as sp
        fh = open(log, "w")
        sp.Popen(args, stdout=fh, stderr=sp.STDOUT, start_new_session=True)
        if not O.wait_healthy():
            raise RuntimeError(f"{slug} never healthy (see {log})")
        try:
            found = 0
            for tid in pending:
                pf = PROMPTS / f"{tid}.md"
                answer = _dispatch(pf.read_text(encoding="utf-8"),
                                   out_dir / f"{tid}.answer.md", slug, O.PORT)
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
