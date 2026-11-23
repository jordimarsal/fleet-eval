"""Grade de C2: quin ressenyador detecta mes defectes reals (i amb menys soroll).

  python3 grade_C2.py

Patrons per defecte a corpus/C2/defects.json (regex sobre la resposta en minuscules,
mateixa mecanica que grade_review de la bateria C v1). Sortida:
  - matriu model x defecte (ok / meitad / —)
  - resum per model: recall, FP estimats
  - grade_C2_summary.json
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
ANSWERS = HERE / "answers"
CORPUS = HERE / "corpus" / "C2"


def load_spec() -> dict[str, list[str]]:
    d = json.loads((CORPUS / "defects.json").read_text(encoding="utf-8"))
    return {x["id"]: x["patterns"] for x in d["defects"]}


def grade_answer(answer: str, patterns: list[str]) -> tuple[bool, str]:
    """True si la resposta connecta el sintoma amb el lloc (patro del remei)."""
    low = answer.lower()
    hit = next((p for p in patterns if re.search(p, low)), None)
    return (hit is not None, hit or "")


def main() -> int:
    pats = load_spec()
    ids = sorted(pats)
    rows: dict[str, dict[str, dict]] = {}
    for f in sorted(ANSWERS.glob("*/C2/*.json")):
        slug = f.parts[-3]
        rec = json.loads(f.read_text(encoding="utf-8"))
        rows.setdefault(slug, {})[rec["task_id"]] = rec

    slugs = sorted(rows, key=lambda s: -sum(rows[s].get(i, {}).get("found", False) for i in ids))
    print(f"{'model':>12s} " + " ".join(f"{i.replace('C2-', ''):>6s}" for i in ids)
          + "   recall    FP")
    summary = {}
    for slug in slugs:
        cells, found_n = [], 0
        fps = 0
        for i in ids:
            r = rows[slug].get(i)
            if r is None:
                cells.append("     —")
                continue
            ok = r.get("found", False)
            found_n += ok
            fps += r.get("false_positives_est", 0)
            cells.append(("   ok" if ok else "  ·") + f"{r.get('items', 0):3d}")
        recall = found_n / len(ids)
        summary[slug] = {"found": found_n, "recall": round(recall, 2), "fp_est": fps}
        print(f"{slug[:12]:>12s} " + " ".join(f"{c:>6s}" for c in cells)
              + f"   {recall:4.2f}  {fps:4d}")

    (HERE / "grade_C2_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(slugs)} models x {len(ids)} defectes -> grade_C2_summary.json")
    print("celda: 'ok' = detectat · numero = ítems reportats (FP si sobren)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
