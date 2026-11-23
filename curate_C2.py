"""Curacio semiautomatica C2: esborrany de spec + prompts per a N defectes nous.

  python3 curate_C2.py [--total 41]

Per cada candidat triat:
  - extraccio del excerpt (mateixa mecanica que build_C2.py)
  - patrons = tokens NOUS del remei (afegits pel fix, absents del pre-state),
    filtrats (len>3, alfabetics, no stopwords) -> regex d'alternatives
  - id C2-xx (public) o C2-Pxx (privat); prompts privats a prompts/C2/private/

Sortida: corpus/C2/draft_spec.json + prompts/C2/*.md i taula compacta per
a la revisio humana. NO sobreescriu defects.json ni res de C2-01..09.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
PROJECTS = Path.home() / "Documents/CV/projects"
WORKS = Path.home() / "works/typescript"
REPO_PATHS = {
    "viatgecio": WORKS / "viatgecio",
    "spring-boot-casino": Path.home() / "works/java/spring-boot-casino",
    "katas-java": Path.home() / "works/java/katas-java",
    "md_mermaid_pdf": Path.home() / "works/python/md_mermaid_pdf",
    "rustcut": Path.home() / "works/rust/rustcut",
    "product-offers": Path.home() / "works/assestments/product-offers",
    "jordimp-sb": Path.home() / "works/jordimp/jordimp-sb",
}
CODE_EXT = (".py", ".ts", ".js", ".java", ".rs", ".kt")
STOP = set("""that this with from have into when then them they your their will
shall would could should about which there these those what when where were been
being have has had does done also just only must might make made same such more
most other over under again very some such each once upon upon after before
between during above below further then once here when why how all any both
each few than too very can will just don should now value values error errors
test tests code file files line lines self none true false return returns""".split())

LANG = {".py": "python", ".ts": "typescript", ".js": "javascript",
        ".java": "java", ".rs": "rust", ".kt": "kotlin"}


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def repo_path(name: str) -> Path:
    if name in REPO_PATHS:
        return REPO_PATHS[name]
    return PROJECTS / name


def tokenize(lines: list[str]) -> set[str]:
    toks = set()
    for ln in lines:
        for t in re.findall(r"[A-Za-z_][A-Za-z_0-9]{2,}", ln):
            toks.add(t)
    return toks


def pick_candidates(cands: list[dict], per_repo_cap: int = 8) -> list[dict]:
    """Reparteix entre repos, privilegia difs amb deletions reals en fitxers de codi."""
    by_repo: dict[str, list[dict]] = {}
    for c in cands:
        code = [f for f in c["files"] if f["path"].endswith(CODE_EXT)]
        non_test = [f for f in code if not re.search(r"(test|spec|fixture)", f["path"], re.I)]
        if not non_test:
            continue
        c = {**c, "main_path": non_test[0]["path"]}
        by_repo.setdefault(c["repo"], []).append(c)
    out = []
    # repartiment: viatgecio mes gras, la resta equilibrat
    caps = {"viatgecio": 14, "ggufbench": 6, "jordimp": 4, "spring-boot-casino": 5,
            "kafka-adapter-telemetry": 4, "harness": 3, "md_mermaid_pdf": 3,
            "codebaserag": 2, "buildwright": 2}
    for repo, lst in by_repo.items():
        cap = caps.get(repo, 1)
        out.extend(lst[:cap])
    return out


def draft_entry(cid: str, c: dict) -> dict | None:
    repo = repo_path(c["repo"])
    path = c["main_path"]
    h = c["hash"]
    pre = git(repo, "show", f"{h}^:{path}")
    if not pre:
        return None
    diff = git(repo, "show", f"{h}^..{h}", "--", path, "--unified=0", "--format=")
    added = [ln[1:].strip() for ln in diff.splitlines()
             if ln.startswith("+") and not ln.startswith("+++")]
    deleted = [ln[1:].strip() for ln in diff.splitlines()
               if ln.startswith("-") and not ln.startswith("---")]
    # ancora: primera deleted que existeix al pre-state (distintiva)
    anchor = next((d for d in deleted
                   if len(d.strip()) > 12 and d.strip() in pre), None)
    if anchor is None:
        return None
    # patrons: tokens nous del remei
    new_toks = tokenize(added) - tokenize(deleted) - tokenize(pre.splitlines()) - STOP
    toks = sorted((t for t in new_toks if len(t) > 3 and not t.isdigit()),
                  key=len, reverse=True)[:5]
    if not toks:
        return None
    lines = pre.splitlines()
    try:
        ai = lines.index(next(l for l in lines if anchor.strip() in l))
    except StopIteration:
        return None
    ctx = 14
    lo, hi = max(0, ai - ctx), min(len(lines), ai + ctx + 1)
    ext = "\n".join(lines[lo:hi])
    ext_lang = LANG.get("." + path.rsplit(".", 1)[-1].lower(), "text")
    # fuites: cap linia afegida distintiva dins l'excerpt
    leak = [a for a in added if len(a) > 25 and a in ext
            and a.lstrip().startswith(("#", "//", '"', "*"))]
    return {
        "id": cid, "repo": c["repo"], "hash": h, "message": c["message"],
        "paths": [path], "public": c["public"], "leak": bool(leak),
        "anchor": anchor.strip()[:80], "excerpt": ext, "lang": ext_lang,
        "patterns": [re.escape(t) for t in toks], "tokens": toks,
    }


def main() -> int:
    cands = json.loads((HERE / "corpus/C2/candidates.json").read_text(encoding="utf-8"))
    existing = json.loads((HERE / "corpus/C2/defects.json").read_text(encoding="utf-8"))
    used = {(d["repo"], d["hash"]) for d in existing["defects"]}
    cands = [c for c in cands if (c["repo"], c["hash"]) not in used and c["public"] is not None]
    picked = pick_candidates(cands)
    print(f"candidats utilis: {len(cands)} -> triats: {len(picked)}")
    pub, priv, drafts = 0, 0, []
    for c in picked:
        if c["public"]:
            pub += 1
            cid = f"C2-{pub + 9:02d}"      # C2-10.. (els 9 son fixes)
        else:
            priv += 1
            cid = f"C2-P{priv:02d}"
        d = draft_entry(cid, c)
        if d:
            drafts.append(d)
    for d in drafts:
        # escriu el prompt (privat al seu dir)
        tpl = (HERE / "build_C2.py").read_text(encoding="utf-8")
        m = re.search(r'TEMPLATE = """(.*?)"""', tpl, re.S)
        body = m.group(1).format(repo=d["repo"], path=d["paths"][0],
                                 lang=d["lang"], excerpt=d["excerpt"])
        sub = "" if d["public"] else "private/"
        out = HERE / "prompts/C2" / f"{sub}{d['id']}.md"
        out.parent.mkdir(exist_ok=True)
        out.write_text(body, encoding="utf-8")
    (HERE / "corpus/C2/draft_spec.json").write_text(
        json.dumps({"defects": drafts}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{'id':8s} {'repo':22s} {'pub':4s} tok readeu")
    for d in drafts:
        flag = "AVIS" if d["leak"] else "ok"
        print(f"{d['id']:8s} {d['repo']:22s} {flag:4s} "
              f"{','.join(d['tokens'][:4]):40s} | {d['message'][:60]}")
    print(f"\nesborrany -> corpus/C2/draft_spec.json ({len(drafts)} entrades)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
