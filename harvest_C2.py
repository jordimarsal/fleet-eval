"""Collidor de candidats C2: commits fix de l'estol com a defectes sembrats.

  python3 harvest_C2.py [--max-lines 80] [--max-files 3]

Criteris de candidat:
  - missatge fix/bugfix/corregido/arregla
  - dif petit i revisable (1..3 fitxers, <= max-lines canviades)
  - context suficient per ressenyar (fitxer pre-state <= 400 linies o extret de funcions)

Sortida: corpus/C2/candidates.json (per curacio humana). MAI puja res sol.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
PROJECTS = Path.home() / "Documents/CV/projects"
WORKS = Path.home() / "works/typescript"
# (nom, ruta, es_public): privat -> prompts/answers gitignorats (id C2-Pxx)
REPOS = [
    ("dev-lab", PROJECTS / "dev-lab", True),
    ("ggufbench", PROJECTS / "ggufbench", True),
    ("jordimp", PROJECTS / "jordimp", True),
    ("mussol", PROJECTS / "mussol", True),
    ("quantdelta", PROJECTS / "quantdelta", True),
    ("seekandemploy", PROJECTS / "seekandemploy", True),
    ("buildwright", PROJECTS / "buildwright", True),
    ("codebaserag", PROJECTS / "codebaserag", True),
    ("debrief-mcp", PROJECTS / "debrief-mcp", True),
    ("harness", PROJECTS / "harness", True),
    ("interview-simulator", PROJECTS / "interview-simulator", True),
    ("kafka-adapter-telemetry", PROJECTS / "kafka-adapter-telemetry", True),
    ("redis-toolkit", PROJECTS / "redis-toolkit", True),
    ("riu", PROJECTS / "riu", True),
    ("shortener", PROJECTS / "shortener", True),
    ("model-ci", PROJECTS / "model-ci", True),
    ("estol", PROJECTS / "estol", True),
    ("estol-app", PROJECTS / "estol-app", True),
    ("reddit-bridge", PROJECTS / "reddit-bridge", True),
    ("viatgecio", WORKS / "viatgecio", False),
    ("spring-boot-casino", Path.home() / "works/java/spring-boot-casino", True),
    ("katas-java", Path.home() / "works/java/katas-java", True),
    ("md_mermaid_pdf", Path.home() / "works/python/md_mermaid_pdf", True),
    ("rustcut", Path.home() / "works/rust/rustcut", True),
    ("product-offers", Path.home() / "works/assestments/product-offers", True),
    ("jordimp-sb", Path.home() / "works/jordimp/jordimp-sb", False),
]

FIX_PAT = re.compile(r"\b(fix|bugfix|bug fix|corregido|arregla|correct|wrong|crash)\b", re.I)
NOISE_PAT = re.compile(r"\b(merge|bump|release|version|chore|docs|typo|rename|rebase)\b", re.I)


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def commit_stats(repo: Path, h: str) -> dict | None:
    """numstat + names del commit; None si toca binaris/rename."""
    files = []
    for line in git(repo, "show", "--numstat", "--format=", h).splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            return None  # binari o rename -> fora
        ins, dele, path = parts
        if not (ins.isdigit() and dele.isdigit()):
            return None
        files.append((path, int(ins), int(dele)))
    return files


def main() -> int:
    max_lines = 80
    max_files = 3
    if "--max-lines" in sys.argv:
        i = sys.argv.index("--max-lines")
        max_lines = int(sys.argv[i + 1])
    if "--max-files" in sys.argv:
        i = sys.argv.index("--max-files")
        max_files = int(sys.argv[i + 1])

    out = []
    for repo_name, repo, is_public in REPOS:
        if not repo.exists():
            continue
        log = git(repo, "log", "--format=%H%x1f%s", "--max-count=600",
                  "--grep=fix", "-i")
        for line in log.splitlines():
            if "\x1f" not in line:
                continue
            h, msg = line.split("\x1f", 1)
            if not FIX_PAT.search(msg) or NOISE_PAT.search(msg.split(":")[0]):
                continue
            if "fixup" in msg:
                continue
            files = commit_stats(repo, h)
            if not files or not (1 <= len(files) <= max_files):
                continue
            total = sum(i + d for _, i, d in files)
            if total == 0 or total > max_lines:
                continue
            # nomes codi, tests com a context sempre que el defecte no nomes hi sigui
            if any(f.endswith((".lock", ".json", ".md", ".svg", ".html")) and
                   not any(p.endswith((".py", ".ts", ".js", ".java", ".rs", ".kt")) for p, _, _ in files)
                   for f, _, _ in files):
                continue
            parents = git(repo, "log", "--format=%P", "-1", h).strip().split()
            if len(parents) != 1:
                continue  # merge
            out.append({
                "repo": repo_name, "hash": h[:12], "message": msg,
                "files": [{"path": p, "ins": i, "del": d} for p, i, d in files],
                "total_lines": total, "public": is_public,
            })
    out_dir = HERE / "corpus" / "C2"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "candidates.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(out)} candidats -> {out_dir / 'candidates.json'}")
    by_repo: dict[str, int] = {}
    for c in out:
        by_repo[c["repo"]] = by_repo.get(c["repo"], 0) + 1
    for k, v in sorted(by_repo.items(), key=lambda x: -x[1]):
        print(f"  {k:16s} {v:3d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
