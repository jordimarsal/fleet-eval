#!/usr/bin/env python3
"""harvest_plans.py — build the P corpus: real SDD specs → planning tasks.

Font de veritat: specs SDD ja fetes i aprovades de l'estol (156 a 12 projectes).
Cada spec dona TRES veritats mecàniques:
  - els fitxers que REALMENT va tocar la feature (git diff del rang de commits)
  - els requisits aprovats (## Rn de requirements.md)
  - la descomposició real (Tn + depends_on + refs de tasks.md — un DAG parsegable)

I l'INPUT de la tasca és l'estat del repo ANTERIOR (git worktree al commit pare):
les reqs aprovades + l'arbre de fitxers. Avantatge metodològic: repos privats
locals — cap model de la flota pot haver-se memoritzat la solució.

Filtres de qualitat (el que no els passa, es salta amb el motiu):
  - 1..4 commits que matchen la feature pel seu id (subject conventional)
  - rang de diff de FILES_MIN..FILES_MAX fitxers
  - >= REQ_MIN requisits i >= TASK_MIN tasques a la spec
  - <= MAX_PER_REPO specs per repo, <= MAX_TASKS tasques al corpus

usage: python3 harvest_plans.py [--out prompts/P] [--limit N]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ESTOL = Path.home() / "Documents/CV/projects"
HERE = Path(__file__).resolve().parent
OUT_CORPUS = HERE / "corpus" / "plans"
OUT_PROMPTS = HERE / "prompts" / "P"

MAX_PER_REPO = 6
MAX_TASKS = 36
FILES_MIN, FILES_MAX = 3, 18
REQ_MIN = 2
TASK_MIN = 3
TREE_CAP = 400
COMMIT_MAX = 6
DIGEST_FILES = 8      # fitxers font més grans: contingut al digest
DIGEST_LINES = 60     # línies per fitxer al digest
DIGEST_BYTES = 4000   # cap per fitxer (60 línies de minified poden ser enormes)
MINIFIED = re.compile(r"\.min\.(js|css)$|\.bundle\.", re.I)

TREE_NOISE = re.compile(
    r"(^|/)(node_modules|\.venv|venv|__pycache__|dist|build|\.git)/"
    r"|\.(png|jpg|jpeg|gif|ico|svg|woff2?|ttf|lock)$"
    r"|(^|/)(uv\.lock|package-lock\.json|pnpm-lock\.yaml|poetry\.lock)$", re.I)

PROMPT = """ROLE: implementation planner. A feature has been approved. You get the
approved requirements and the repository file tree BEFORE implementation.
Write the implementation plan with EXACTLY these three sections:

FILES
<repo-relative path of every file you would create or modify, one per line>

TASKS
T1: <short title>
    depends_on: (none)
    refs: R1, R2
T2: <short title>
    depends_on: T1
    refs: R3
(... ordered so dependencies come first; every requirement must be covered
 by the refs of at least one task)

GATES
<the verification gates you would run before closing the feature>

--- APPROVED REQUIREMENTS ---
{requirements}

--- FEATURE TITLE ---
{title}

--- REPOSITORY FILE TREE (before implementation{tree_note}) ---
{tree}

--- KEY SOURCE FILES (before implementation, excerpts) ---
{digest}

Write ONLY the plan (the three sections). No prose outside them."""


def run(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True)


def parse_requirements(text: str) -> list[tuple[str, str]]:
    """## R<n> blocks -> [(rid, statement)] — skips the '# Requirements' H1."""
    reqs: list[tuple[str, str]] = []
    cur: str | None = None
    buf: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(R\d+)\b", line)
        if m:
            if cur:
                reqs.append((cur, " ".join(buf).strip()))
            cur, buf = m.group(1), []
        elif cur is not None:
            if re.match(r"^#\s+\w", line):        # another H1: stop the block
                reqs.append((cur, " ".join(buf).strip()))
                cur, buf = None, []
                continue
            buf.append(line)
    if cur:
        reqs.append((cur, " ".join(buf).strip()))
    return [(rid, s) for rid, s in reqs if s]


def parse_tasks(text: str) -> dict[str, dict]:
    """- [x] T1: title / depends_on: ... / refs: ... -> {T1: {...}}"""
    tasks: dict[str, dict] = {}
    cur: str | None = None
    for line in text.splitlines():
        m = re.match(r"^-?\s*\[.\]\s*(T\d+):\s*(.+?)\s*$", line.strip())
        if m:
            cur = m.group(1)
            tasks[cur] = {"title": m.group(2).strip(), "depends_on": [], "refs": []}
            continue
        if cur is None:
            continue
        m2 = re.search(r"depends_on:\s*(\S.*)$", line)
        if m2:
            deps = [d.strip().rstrip(",") for d in m2.group(1).split(",")]
            tasks[cur]["depends_on"] = [d for d in deps if d and d != "(none)"]
            continue
        m3 = re.search(r"refs:\s*(\S.*)$", line)
        if m3:
            tasks[cur]["refs"] = re.findall(r"R\d+", m3.group(1))
    return tasks


def feature_commits(repo: Path, feature_id: str) -> list[tuple[str, int, str]]:
    r = run(repo, "log", "--format=%H%x00%ct%x00%s", "-i", f"--grep={feature_id}")
    out = []
    for line in r.stdout.splitlines():
        parts = line.split("\0", 2)
        if len(parts) == 3:
            out.append((parts[0], int(parts[1]), parts[2]))
    out.sort(key=lambda c: c[1])
    return out


def tree_at(repo: Path, ref: str) -> list[str]:
    r = run(repo, "ls-tree", "-r", "--name-only", ref)
    paths = [p for p in r.stdout.splitlines() if p and not TREE_NOISE.search(p)]
    return paths[:TREE_CAP]


SOURCE_EXT = (".py", ".ts", ".mjs", ".js", ".astro", ".sh", ".java",
              ".css", ".scss", ".html", ".svelte", ".vue")


def digest_at(repo: Path, ref: str, tree: list[str]) -> str:
    """Digest determinista i CEC (requirement-blind): contingut (cap DIGEST_LINES)
    dels DIGEST_FILES fitxers font més grans de l'arbre. Mai depèn dels requisits:
    si el digest filtrés per paraules dels requisits, filtraria cap als fitxers de
    la veritat i el file recall deixaria de mesurar res."""
    r = run(repo, "ls-tree", "-r", "-l", ref)
    sizes: dict[str, int] = {}
    for line in r.stdout.splitlines():
        m = re.match(r"^\d+\s+blob\s+[0-9a-f]+\s+(\d+)\t(.+)$", line)
        if m:
            sizes[m.group(2)] = int(m.group(1))
    src = sorted((p for p in tree
                  if p.lower().endswith(SOURCE_EXT) and p in sizes and sizes[p] > 0
                  and not MINIFIED.search(p)),
                 key=lambda p: -sizes[p])
    parts = []
    for p in src[:DIGEST_FILES]:
        r = run(repo, "show", f"{ref}:{p}")
        if r.returncode != 0:
            continue
        lines: list[str] = []
        total = 0
        for line in r.stdout.splitlines()[:DIGEST_LINES]:
            b = len(line.encode("utf-8", "replace")) + 1
            if total + b > DIGEST_BYTES:
                break
            lines.append(line)
            total += b
        parts.append(f"--- {p} (first {len(lines)} lines of {sizes[p]} bytes) ---\n"
                     + "\n".join(lines))
    return "\n".join(parts) if parts else "(no source files could be read)"


def harvest_repo(repo_dir: Path, out: list[dict], state: dict) -> None:
    repo = repo_dir.resolve()
    name = repo.name
    if not (repo / ".git").exists():
        return
    specs = sorted((repo / "harness" / "specs").glob("*/tasks.md")) \
        if (repo / "harness" / "specs").exists() else []
    taken = 0
    for tasks_md in specs:
        if taken >= MAX_PER_REPO or len(out) >= MAX_TASKS:
            return
        feature = tasks_md.parent.name
        tasks = parse_tasks(tasks_md.read_text(encoding="utf-8", errors="replace"))
        # La feature ha d'estar COMPLETADA: APPROVAL explícit o totes les tasques [x].
        approved = (tasks_md.parent / "APPROVAL").exists()
        completed = bool(tasks) and all(
            re.match(r"^-?\s*\[x\]", l.strip())
            for l in tasks_md.read_text(encoding="utf-8", errors="replace").splitlines()
            if re.match(r"^-?\s*\[.\]", l.strip()))
        if not (approved or completed):
            state[f"{name}/{feature}"] = "ni APPROVAL ni totes les tasques [x]"
            continue
        reqs = parse_requirements((tasks_md.parent / "requirements.md").read_text(encoding="utf-8", errors="replace")) \
            if (tasks_md.parent / "requirements.md").exists() else []
        if len(reqs) < REQ_MIN:
            state[f"{name}/{feature}"] = f"requisits {len(reqs)} < {REQ_MIN}"
            continue
        if len(tasks) < TASK_MIN:
            state[f"{name}/{feature}"] = f"tasques {len(tasks)} < {TASK_MIN}"
            continue
        commits = feature_commits(repo, feature)
        if not (1 <= len(commits) <= COMMIT_MAX):
            state[f"{name}/{feature}"] = f"commits que matchen: {len(commits)}"
            continue
        first, last = commits[0][0], commits[-1][0]
        pre = f"{first}~1"
        diff = run(repo, "diff", "--name-only", f"{first}~1", last)
        files = sorted(set(p for p in diff.stdout.splitlines() if p))
        if not (FILES_MIN <= len(files) <= FILES_MAX):
            state[f"{name}/{feature}"] = f"fitxers canviats {len(files)} fora de [{FILES_MIN},{FILES_MAX}]"
            continue
        tree = tree_at(repo, pre)
        if not tree:
            state[f"{name}/{feature}"] = "arbre buit al pre-ref"
            continue
        taken += 1
        task_id = f"P{len(out) + 1:02d}_{name}_{feature}"
        req_txt = "\n\n".join(f"{rid}: {s}" for rid, s in reqs)
        title = commits[-1][2]
        digest = digest_at(repo, pre, tree)
        prompt = PROMPT.format(requirements=req_txt, title=title,
                               tree="\n".join(tree),
                               tree_note="" if len(tree) < TREE_CAP else ", truncated",
                               digest=digest)
        OUT_PROMPTS.mkdir(parents=True, exist_ok=True)
        OUT_CORPUS.mkdir(parents=True, exist_ok=True)
        (OUT_PROMPTS / f"{task_id}.md").write_text(prompt, encoding="utf-8")
        truth = {
            "task_id": task_id,
            "repo": name,
            "feature": feature,
            "title": title,
            "pre_ref": pre,
            "post_ref": last,
            "commits": [c[0] for c in commits],
            "truth": {
                "files": files,
                "requirements": [rid for rid, _ in reqs],
                "req_statements": {rid: s for rid, s in reqs},
                "tasks": tasks,
            },
        }
        (OUT_CORPUS / f"{task_id}.json").write_text(
            json.dumps(truth, indent=1, ensure_ascii=False), encoding="utf-8")
        out.append(truth)


def main() -> int:
    limit = MAX_TASKS
    argv = sys.argv[1:]
    if "--limit" in argv:
        limit = int(argv[argv.index("--limit") + 1])
    # Neteja sortides anteriors perquè els ids P01.. es tornin a assignar nets
    for d in (OUT_CORPUS, OUT_PROMPTS):
        if d.exists():
            for f in d.glob("*"):
                f.unlink()
    repos = sorted(p for p in ESTOL.iterdir()
                   if p.is_dir() and (p / ".git").exists())
    out: list[dict] = []
    state: dict[str, str] = {}
    for repo in repos:
        if len(out) >= limit:
            break
        harvest_repo(repo, out, state)
    out = out[:limit]
    print(f"corpus: {len(out)} tasques")
    for t in out:
        print(f"  {t['task_id']:48s} fitxers={len(t['truth']['files']):2d} "
              f"reqs={len(t['truth']['requirements'])} tasques={len(t['truth']['tasks'])}")
    skips = {k: v for k, v in state.items()}
    print(f"\nsaltades: {len(skips)} (motius a corpus/plans_skips.json)")
    (OUT_CORPUS.parent / "plans_skips.json").write_text(
        json.dumps(skips, indent=1, ensure_ascii=False), encoding="utf-8")
    return 0 if len(out) >= 6 else 1


if __name__ == "__main__":
    sys.exit(main())
