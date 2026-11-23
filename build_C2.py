"""Constructor de prompts C2: estat PRE del commit fix = codi amb el defecte.

  python3 build_C2.py

Per a cada defecte de corpus/C2/defects.json:
  - extreu el fitxer a hash^ (pre-state, amb el defecte)
  - retalla l'excerpt al voltant de l'ancora (context lines; tots els matches
    si all_anchors)
  - COMPROVA QUE CAP linia afegida pel fix fuiti a l'excerpt
  - escriu prompts/C2/<id>.md i corpus/C2/<id>.json (metadades de l'excerpt)
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
PROJECTS = Path.home() / "Documents/CV/projects"
CORPUS = HERE / "corpus" / "C2"
PROMPTS = HERE / "prompts" / "C2"

TEMPLATE = """ROLE: reviewer. Review the proposed change below as if it were a pull request
against an internal project ({repo}). This is an excerpt of `{path}`
({lang}) as proposed.

```{lang}
{excerpt}
```

Report every real defect you can find: correctness bugs, security issues,
resource leaks, broken assumptions, contract violations. Do not report style
preferences or naming opinions. For each defect give the function or location
name and one sentence on why it is wrong.

OUTPUT FORMAT: a numbered list, one defect per line, starting at 1. No preamble.
"""


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {args} failed: {r.stderr[-300:]}")
    return r.stdout


def excerpt(pre: str, anchors: list[str], ctx: int) -> tuple[str, str]:
    """Retalla el pre-state al voltant de les ancores. Retorna (text, rang)."""
    lines = pre.splitlines()
    hits: list[int] = []
    for a in anchors:
        for i, ln in enumerate(lines):
            if a in ln:
                hits.append(i)
                if a not in [x for x in anchors if x != a]:
                    break  # una sola aparicio per ancora distincte
    if not hits:
        raise RuntimeError("cap ancora trobada al pre-state")
    regions: list[list[int]] = []
    for h in sorted(hits):
        lo, hi = max(0, h - ctx), min(len(lines), h + ctx + 1)
        if regions and lo <= regions[-1][1]:
            regions[-1][1] = hi
        else:
            regions.append([lo, hi])
    parts = []
    for lo, hi in regions:
        parts.append(f"// lines {lo + 1}-{hi} of {len(lines)}\n" + "\n".join(lines[lo:hi]))
    rng = "+".join(f"{lo}-{hi}" for lo, hi in regions)
    return "\n\n".join(parts), rng


def added_lines(repo: Path, h: str, path: str) -> list[str]:
    """Linies afegides pel fix (per al check de fuites)."""
    diff = git(repo, "show", f"{h}^..{h}", "--", path, "--unified=0", "--format=")
    return [ln[1:] for ln in diff.splitlines() if ln.startswith("+") and len(ln) > 25]


def main() -> int:
    spec = json.loads((CORPUS / "defects.json").read_text(encoding="utf-8"))
    PROMPTS.mkdir(parents=True, exist_ok=True)
    leaks = 0
    for d in spec["defects"]:
        repo = PROJECTS / d["repo"]
        path = d["paths"][0]
        pre = git(repo, "show", f"{d['hash']}^:{path}")
        anchors = [a.replace('\\"', '"') for a in d["anchors"]]
        text, rng = excerpt(pre, anchors, d["context"])
        # check de fuites: NOMES linies de comentari/docstring afegides pel fix
        # que tambe surtin a l'excerpt (structurally impossible per codi nou:
        # l'excerpt ve del pre-state; el risc es text explicatiu compartit).
        bad = [ln for ln in added_lines(repo, d["hash"], path)
               if ln in text and ln.lstrip().startswith(("#", "//", '"', "*"))]
        if bad:
            leaks += 1
            print(f"  AVIS {d['id']}: {len(bad)} linies de comentari del fix a l'excerpt")
            for b in bad[:3]:
                print(f"    + {b[:90]}")
        prompt = TEMPLATE.format(repo=d["repo"], path=path, lang=d["lang"], excerpt=text)
        (PROMPTS / f"{d['id']}.md").write_text(prompt, encoding="utf-8")
        rec = {k: d[k] for k in ("id", "repo", "hash", "message", "paths", "patterns")}
        rec.update({"excerpt_ranges": rng, "pre_bytes": len(pre), "prompt_bytes": len(prompt)})
        (CORPUS / f"{d['id']}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  {d['id']} [{d['repo']}] {rng} · prompt {len(prompt)} B")
    print(f"\n{len(spec['defects'])} prompts -> {PROMPTS} · avis informatius={leaks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
