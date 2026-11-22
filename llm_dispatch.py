#!/usr/bin/env python3
"""llm_dispatch — one prompt against an OpenAI-compatible endpoint, with timings.

usage: llm_dispatch.py <prompt.md> <out.md> <api_model> <port>

COPIA CANÒNICA VERSIONADA (fleet-eval). Els consumers l'esperen a dues rutes
fora de repo (convenció històrica) — mantén-les sincronitzades amb aquest
fitxer, que és el que mana:

    ~/Documents/CV/projects/llm_dispatch.py   (el que crida run_one.sh, ../)
    /tmp/opencode/llm_dispatch.py             (el que crida run_E.sh)

run_one.sh i run_E.sh prefereixen aquesta còpia de repo i només cauen a les
rutes velles si aquí no hi és. Es va perdre una vegada (2026-11-22, mai no va
estar versionat) i es va haver de recrear: per això ara viu al repo.

Dispatch-driver settings (fleet-eval contract): tool_choice none,
enable_thinking false, initial budget max_tokens 8000.

REGLA D'ESCALAT (2026-11-22, a petició de l'avaluació): si la resposta torna
amb content BUIT i raonament no buit, no és un resultat de capacitat sinó un
artefacte del pressupost (el model es menja el sostre pensant) — el driver
reintenta amb el pressupost següent fins que lliura content o s'acaben els
escalons. El pressupost efectiu i el nombre d'intents viatgen a la línia de
timing (`budget=` i `attempts=`) perquè el receipt digui en quina condició s'ha
mesurat. Si esgota l'últim escaló sense content, el 0 és genuí.

Writes the assistant content to <out.md> and prints one timing line:

    model=<m> wall=<s>s gen=<t>tok/s predicted_n=<n> prompt_n=<n> content_chars=<n> budget=<N> attempts=<k>

Recreado el 2026-11-22 (el fitxer original s'havia perdut del directori de
projectes i de /tmp): el format de la línia de timing i el contracte
(escriptures de la bateria fleet-eval) són els que tenen els receipts a
answers/<slug>/*.timing.
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

BUDGETS = (8000, 16000, 24000)


def main(argv: list[str]) -> int:
    if len(argv) < 5:
        print(__doc__, file=sys.stderr)
        return 2
    prompt_path, out_path, api_model, port = argv[1], argv[2], argv[3], argv[4]
    prompt = Path(prompt_path).read_text(encoding="utf-8")
    body = {
        "model": api_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": BUDGETS[0],
        "tool_choice": "none",
        "stream": False,
        "chat_template_kwargs": {"enable_thinking": False},
    }

    content, reasoning, t, wall, attempts = "", "", {}, 0.0, 0
    for budget in BUDGETS:
        body["max_tokens"] = budget
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/v1/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=1800) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        wall += time.time() - t0
        attempts += 1
        msg = (data.get("choices") or [{}])[0].get("message") or {}
        content = msg.get("content") or ""
        reasoning = msg.get("reasoning_content") or ""
        t = data.get("timings") or {}
        if content.strip():
            break
        # content buit amb raonament = el pressupost s'ha cremat pensant: escala.
        print(f"  [dispatch] content buit amb budget {budget}: escalo a "
              f"{BUDGETS[attempts] if attempts < len(BUDGETS) else 'res'}",
              file=sys.stderr, flush=True)

    Path(out_path).write_text(content, encoding="utf-8")

    predicted_n = t.get("predicted_n") or 0
    prompt_n = t.get("prompt_n") or 0
    ms = t.get("predicted_ms") or 0
    gen = (predicted_n / (ms / 1000.0)) if ms else 0.0
    print(f"model={api_model} wall={wall:.1f}s gen={gen:.0f}tok/s "
          f"predicted_n={predicted_n} prompt_n={prompt_n} "
          f"content_chars={len(content)} reasoning_chars={len(reasoning)} "
          f"budget={body['max_tokens']} attempts={attempts}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
