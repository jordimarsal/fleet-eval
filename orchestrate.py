#!/usr/bin/env python3
"""Run the 4-task battery against every fleet model, ONE engine at a time.

For each model: build the server command from its .txt profile, start it,
wait for /health, run the 4 prompts, grade, stop the server.

usage: orchestrate.py [slug ...]     (default: all llama.cpp chat models)
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HOME = Path.home()
FE = Path(__file__).parent
MODELS = HOME / "ia/llama/models"
LOGS = FE / "logs"
LOGS.mkdir(exist_ok=True)

# slug -> gguf filename (chat models only; embeddings/mmproj excluded)
FLEET = {
    "qwen36": "qwen36-35b-distill-mxfp4_moe.gguf",
    "minicpm": "MiniCPM-V-4_7-35B-A3B-Q4_K_M.gguf",
    "qwen38": "Qwen3.8-27B-UD-Q3_K_XL.gguf",
    "gemma4": "gemma-4-26B-A4B-it-UD-Q5_K_XL.gguf",
    "SC117": "Qwen3.6-35B-A3B-uncensored-heretic-Native-MTP-Preserved-APEX-I-Compact.gguf",
    "Huihui": "Huihui-Qwen3.8-27B-abliterated-UD-Q3_K_XL.gguf",
    "qwen4b": "Qwen3-4B-Instruct-2507-Q4_K_M.gguf",   # floor control
}
PORT = 8999


def build_args(gguf: Path) -> list[str]:
    sys.path.insert(0, str(HOME / "ia/llama"))
    from ggufbench import server  # type: ignore

    return server.build_args(str(gguf), "fixed", PORT)


def health(timeout: float = 0.0) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=3) as r:
            return b"ok" in r.read()
    except Exception:
        return False


def wait_healthy(limit: float = 300.0) -> bool:
    t0 = time.time()
    while time.time() - t0 < limit:
        if health():
            return True
        time.sleep(2)
    return False


def stop_server() -> None:
    subprocess.run(["pkill", "-f", "llama-server"], capture_output=True)
    for _ in range(30):
        time.sleep(1)
        out = subprocess.run(["pgrep", "-f", "llama-server"], capture_output=True, text=True)
        if not out.stdout.strip():
            return
    subprocess.run(["pkill", "-9", "-f", "llama-server"], capture_output=True)
    time.sleep(3)


def dispatch(slug: str) -> None:
    r = subprocess.run(
        ["bash", str(FE / "run_one.sh"), slug, str(PORT), slug],
        capture_output=True, text=True,
    )
    (LOGS / f"{slug}.dispatch.log").write_text(r.stdout + r.stderr)
    print(r.stdout.strip())


def grade(slug: str) -> dict:
    r = subprocess.run(
        [sys.executable, str(FE / "grade.py"), slug, str(FE / "answers" / slug)],
        capture_output=True, text=True,
    )
    print(r.stdout.strip() or r.stderr.strip())
    p = FE / "answers" / slug / "grade.json"
    return json.loads(p.read_text()) if p.exists() else {}


def main() -> None:
    wanted = sys.argv[1:] or list(FLEET)
    results: dict = {}
    summary_path = FE / "results.json"
    if summary_path.exists():
        results = json.loads(summary_path.read_text())

    for slug in wanted:
        if slug not in FLEET:
            print(f"?? {slug}: no such model")
            continue
        gguf = MODELS / FLEET[slug]
        if not gguf.exists():
            print(f"!! {slug}: missing {gguf}")
            continue
        if (FE / "answers" / slug / "grade.json").exists():
            print(f"== {slug}: already graded, skipping")
            results[slug] = json.loads((FE / "answers" / slug / "grade.json").read_text())
            continue

        print(f"\n=== {slug} ===", flush=True)
        stop_server()
        args = build_args(gguf)
        (LOGS / f"{slug}.cmd").write_text(" ".join(args) + "\n")
        log = open(LOGS / f"{slug}.server.log", "w")
        proc = subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT,
                                cwd=str(HOME / "ia/llama"))
        if not wait_healthy():
            print(f"!! {slug}: never became healthy — skipping")
            proc.terminate()
            continue
        print(f"   healthy; battery running", flush=True)
        try:
            dispatch(slug)
        except Exception as exc:  # keep going with the rest of the fleet
            print(f"!! {slug}: dispatch error {exc}")
        results[slug] = grade(slug)
        summary_path.write_text(json.dumps(results, indent=2))
        stop_server()
        print(f"   done ({len(results)}/{len(wanted)})", flush=True)

    stop_server()
    print("\n=== RESUM ===")
    for slug, g in results.items():
        if g:
            a, b = g.get("A", {}), g.get("B", {})
            print(f"{slug:10s} A:{a.get('passed', 0):>2}/10 B:{b.get('passed', 0):>2}/10 "
                  f"C:{g.get('C', {}).get('recall', 0):.2f} D:{g.get('D', {}).get('total', 0)}/7")


if __name__ == "__main__":
    main()
