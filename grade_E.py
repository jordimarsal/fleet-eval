"""Task E: deliver a COMPLETE 400-line file with two modifications.

The measured axis is delivery fidelity: does the whole file come back,
parseable, with every original symbol intact and no placeholder shortcuts?
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

FE = Path(__file__).parent
SRC = Path.home() / "Documents/CV/projects/buildwright/src/buildwright/runtime.py"

# top-level symbols that must survive the rewrite
ORIGINAL_SYMBOLS = [
    "class Sandbox", "def resolve_in_sandbox", "def command_allowed",
    "def tool_read_file", "def tool_write_file", "def tool_edit_file",
    "def tool_list_dir", "def tool_run_command", "def build_implementer",
    "class Task", "def parse_tasks", "def next_batch", "def sync_worktree",
    "def create_worktree", "class BatchReport", "def verify_on_disk",
]


def blocks(text: str) -> list[str]:
    return [b for b in re.findall(r"```(?:python|py)?\n(.*?)```", text, re.S) if b.strip()]


def grade(answer: str) -> dict:
    src = SRC.read_text()
    src_lines = len(src.splitlines())
    res: dict = {"src_lines": src_lines, "blocks": 0, "chars": 0,
                 "syntax_ok": False, "symbols_kept": 0, "symbols_missing": [],
                 "placeholder": False, "lines": 0, "line_ratio": 0.0,
                 "added_symbol": False, "modified_applied": False}

    if answer.startswith("<<<NOMÉS REASONING"):
        res["why"] = "content empty: only reasoning delivered"
        return res

    bs = blocks(answer)
    res["blocks"] = len(bs)
    if not bs:
        res["why"] = "no fenced python block"
        return res
    body = max(bs, key=len).strip()
    res["chars"] = len(body)

    # placeholder / truncation shortcuts
    if (re.search(r"^@@ ", body, re.M) or "# rest of the file" in body
            or "# ... unchanged" in body or "pass  # (unchanged" in body
            or body.rstrip().endswith(("...", "…"))):
        res["placeholder"] = True

    try:
        compile(body, "runtime.py", "exec")
        res["syntax_ok"] = True
    except SyntaxError as exc:
        res["why"] = f"syntax: {exc.msg} line {exc.lineno}"
        return res

    res["lines"] = len(body.splitlines())
    res["line_ratio"] = round(res["lines"] / src_lines, 3)

    kept = [s for s in ORIGINAL_SYMBOLS if s in body]
    res["symbols_kept"] = len(kept)
    res["symbols_missing"] = [s for s in ORIGINAL_SYMBOLS if s not in body]

    # the two required edits
    res["added_symbol"] = bool(
        re.search(r"def tool_run_command_dry|def tool_stat_file", body))
    res["modified_applied"] = ("allow" in body and "command_allowed" in body
                               and bool(re.search(r"def command_allowed", body)))
    return res


def main() -> None:
    slug, ansdir = sys.argv[1], Path(sys.argv[2])
    p = ansdir / "E_largefile.md"
    out = grade(p.read_text() if p.exists() else "")
    out["model"] = slug
    (ansdir / "grade_E.json").write_text(json.dumps(out, indent=2))
    verdict = ("COMPLET" if out.get("syntax_ok") and out.get("line_ratio", 0) >= 0.90
               and out["symbols_kept"] == len(ORIGINAL_SYMBOLS) and not out["placeholder"]
               else "INCOMPLET")
    print(f"{slug:24s} {verdict:11s} linies={out.get('lines',0)}/{out['src_lines']} "
          f"({out.get('line_ratio',0):.2f}) simbols={out['symbols_kept']}/16 "
          f"blocs={out['blocks']} placehold={out['placeholder']} "
          f"nou={out.get('added_symbol')} " + (out.get("why", "")))


if __name__ == "__main__":
    main()
