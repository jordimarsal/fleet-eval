"""Analisi de la bateria P2b reduida: porta de decissio del senyal de planner.

  python3 analyze_P2b.py [--human calibra_qwen38]

Compara, per tasca i planner (mateix executor qwen38):
  - taula score/verds/pasos/monotonia
  - delta huma − model per tasca (el senyal)
  - correlacio pasos ↔ score (sobre/infra-descomposicio)
  - veredicte mecanic de la porta: huma guanya >=5/8 tasques I delta mitja >= 0.05
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

HERE = Path(__file__).parent
ANSWERS = HERE / "answers"
MODEL_PLANNERS = ["Huihui", "qwen4b"]


def load_rows(executor: str) -> list[dict]:
    rows = []
    for f in sorted(ANSWERS.glob("*/P2b/*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        if r.get("executor") != executor:
            continue
        rows.append(r)
    return rows


def by_task(rows: list[dict]) -> dict[str, dict[str, dict]]:
    out: dict[str, dict[str, dict]] = {}
    for r in rows:
        out.setdefault(r["task_id"], {})[r["planner_slug"]] = r
    return out


def spearman(xs: list[float], ys: list[float]) -> float | None:
    n = len(xs)
    if n < 3:
        return None

    def rank(v: list[float]) -> list[float]:
        order = sorted(range(n), key=lambda i: v[i])
        rk = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                rk[order[k]] = avg
            i = j + 1
        return rk

    rx, ry = rank(xs), rank(ys)
    mr_x = sum(rx) / n
    mr_y = sum(ry) / n
    num = sum((a - mr_x) * (b - mr_y) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mr_x) ** 2 for a in rx) * sum((b - mr_y) ** 2 for b in ry))
    return num / den if den else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--human", default="calibra_qwen38")
    ap.add_argument("--executor", default="qwen38")
    args = ap.parse_args()

    rows = load_rows(args.executor)
    if not rows:
        print(f"sense registres amb executor={args.executor}")
        return 1
    tab = by_task(rows)
    planners = [args.human] + [p for p in MODEL_PLANNERS
                               if p != args.human and any(p in t for t in tab.values())]

    print(f"executor={args.executor} · huma={args.human} · planners={planners}")
    print(f"{'tasca':46s} " + " ".join(f"{p:>18s}" for p in planners))
    hdr = f"{'':46s} " + " ".join(f"{'score':>7s} {'pas':>4s} {'mn':>3s} {'Δhum':>6s}" for _ in planners)
    print(hdr)

    deltas: dict[str, list[float]] = {p: [] for p in planners}
    wins = {p: 0 for p in planners}
    losses = {p: 0 for p in planners}
    ties = {p: 0 for p in planners}
    for tid in sorted(tab):
        cells = []
        hum = tab[tid].get(args.human)
        hs = hum["score"] if hum else None
        for p in planners:
            r = tab[tid].get(p)
            if not r:
                cells.append(f"{'—':>22s}")
                continue
            d = (hs - r["score"]) if (hs is not None and p != args.human) else None
            if p != args.human:
                deltas[p].append(d)
                if d > 1e-9:
                    wins[p] += 1
                elif d < -1e-9:
                    losses[p] += 1
                else:
                    ties[p] += 1
            dtxt = f"{d:+.2f}" if d is not None else "  —"
            cells.append(f"{r['score']:7.2f} {r['n_steps']:4d} "
                         f"{'Y' if r['monotone'] else 'n':>3s} {dtxt:>6s}")
        print(f"{tid:46s} " + " ".join(f"{c:>18s}" for c in cells))

    print("\n=== agregat per planner ===")
    for p in planners:
        rs = [tab[t][p] for t in tab if p in tab[t]]
        if not rs:
            continue
        ms = sum(r["score"] for r in rs) / len(rs)
        mono = sum(r["monotone"] for r in rs)
        cor = spearman([float(r["n_steps"]) for r in rs], [r["score"] for r in rs])
        line = (f"{p:>16s}: n={len(rs):2d} score_mig={ms:.3f} mono={mono}/{len(rs)}"
                f" ρ(pasos,score)={'—' if cor is None else f'{cor:+.2f}'}")
        if p != args.human:
            dm = deltas[p]
            dmean = sum(dm) / len(dm) if dm else 0.0
            line += f" | vs huma: +{wins[p]} ={ties[p]} -{losses[p]} delta_mig={dmean:+.3f}"
        print(line)

    print("\n=== porta de decissio ===")
    hum_rows = [tab[t][args.human] for t in tab if args.human in tab[t]]
    ok = True
    for p in planners[1:]:
        dm = deltas[p]
        if not dm:
            print(f"  {p}: SENSE mostres")
            ok = False
            continue
        dmean = sum(dm) / len(dm)
        beats = wins[p] > losses[p]
        strong = dmean >= 0.05
        consistent = wins[p] >= math.ceil(0.6 * len(dm))
        verdict = "SENVALID ✓" if (beats and strong and consistent) else "SENVAL NO"
        ok &= beats and strong and consistent
        print(f"  {p}: huma>{p} en {wins[p]}/{len(dm)} tasques · delta_mig={dmean:+.3f} "
              f"(llindar +0.05) → {verdict}")
    if not hum_rows:
        print("  (sense plans humans mesurats)")
    else:
        ms = sum(r["score"] for r in hum_rows) / len(hum_rows)
        print(f"  huma: score_mig={ms:.3f} en {len(hum_rows)} tasques")
    print("\nCriteri: huma guanya >=60% tasques I delta_mig >= +0.05 en tots els planners."
          if ok else
          "\nSi no es compleix per a tots: senyal de planner PLÀ, s'enterra el routing de planner.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
