"""Mechanically grade one model's 4 answers.

Usage: grade.py <model-slug> <dir-with-answers>
Writes <dir>/grade.json and prints a one-line summary.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def code_blocks(text: str) -> list[str]:
    return re.findall(r"```(?:python|py)?\n(.*?)```", text, re.S)


def run_pytest(cwd: Path) -> tuple[int, int]:
    """Return (passed, failed) for the task's own test file."""
    # NOTE: exactly one -q. A second -q (-qq) suppresses the summary line and
    # both regexes below then find nothing, scoring every model as 0.
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--no-header"],
        cwd=cwd, capture_output=True, text=True, timeout=180,
    )
    out = r.stdout + r.stderr
    m = re.search(r"(\d+) passed", out)
    passed = int(m.group(1)) if m else 0
    m2 = re.search(r"(\d+) failed", out)
    failed = int(m2.group(1)) if m2 else 0
    if "error" in out.lower() and not m:
        failed = failed or 1
    return passed, failed


def grade_code_task(task: str, answer: str) -> dict:
    """A and B: does the delivered file make the real tests pass?"""
    work = ROOT / f"_work_{task}"
    if work.exists():
        shutil.rmtree(work)
    # copy the pristine task tree
    src = ROOT / ("task_a" if task == "A" else "task_b")
    shutil.copytree(src, work, ignore=shutil.ignore_patterns("reference", "__pycache__"))

    blocks = [b for b in code_blocks(answer) if b.strip()]
    res: dict = {"blocks": len(blocks), "chars": 0, "passed": 0, "failed": 0,
                 "syntax_ok": False, "applied": False}

    if not blocks:
        res["why"] = "no fenced python block"
        (work / "_grade.json").write_text(json.dumps(res))
        return res

    # take the largest block: it is the complete file
    body = max(blocks, key=len)
    res["chars"] = len(body)
    # a diff is not an acceptable delivery for A/B
    if re.search(r"^--- a/", body, re.M) or re.search(r"^@@ ", body, re.M):
        res["why"] = "delivered a diff instead of a complete file"
        (work / "_grade.json").write_text(json.dumps(res))
        return res

    target = (
        work / "src/schedcore/retry.py" if task == "A" else work / "src/notify/throttle.py"
    )
    # tolerate a model that wrapped the file in a markdown fence with language
    body = body.strip()
    try:
        compile(body, str(target), "exec")
        res["syntax_ok"] = True
    except SyntaxError as exc:
        res["why"] = f"syntax error: {exc.msg} line {exc.lineno}"
        (work / "_grade.json").write_text(json.dumps(res))
        return res

    target.write_text(body + "\n", encoding="utf-8")
    res["applied"] = True
    passed, failed = run_pytest(work)
    res["passed"], res["failed"] = passed, failed
    # truncation heuristics
    if body.rstrip().endswith(("...", "…")) or "rest unchanged" in body or "TODO" in body:
        res["truncated"] = True
    (work / "_grade.json").write_text(json.dumps(res))
    return res


# --- task C: defect recall -------------------------------------------------
C_DEFECTS = {
    "D1_mutable_default": [r"mutable default", r"tags=\[\]", r"default argument",
                           r"default=\[\]", r"shared.*default"],
    "D2_bare_except": [r"except Exception", r"bare except", r"swallow",
                       r"pass\b.*error", r"silently"],
    "D3_injection": [r"injection", r"f-string", r"f\"SELECT", r"concat",
                     r"parameteriz", r"escap"],
    "D4_leak": [r"leak", r"not clos", r"never clos", r"cursor.*clos", r"close\(\)"],
    "D5_off_by_one": [r"off-by-one", r"off by one", r"len\(users\) - 1",
                      r"last user", r"skips? the last", r"- 1\)"],
    "D6_falsy_id": [r"falsy", r"truthy", r"id of 0", r"\b0\b.*skip",
                    r"not user\.id", r"is None", r"zero"],
    "D7_transaction": [r"rollback", r"transaction", r"partial", r"atomic",
                       r"commit per"],
}
C_FUNCTION_HINT = re.compile(r"save_user|get_user|batch_update|delete_user")


def grade_review(answer: str) -> dict:
    low = answer.lower()
    found, missing = [], []
    for did, pats in C_DEFECTS.items():
        if any(re.search(p, low) for p in pats):
            found.append(did)
        else:
            missing.append(did)
    # false positives: defect-looking claims about functions/behaviour not seeded
    claims = len(re.findall(r"^\s*\d+[.)]\s", answer, re.M))
    res = {
        "found": found, "missing": missing, "recall": round(len(found) / len(C_DEFECTS), 2),
        "numbered_items": claims,
        "false_positives_est": max(0, claims - len(found)),
        "functions_named": sorted(set(C_FUNCTION_HINT.findall(answer))),
    }
    return res


# --- task D: diagnosis -----------------------------------------------------
D_ROOT_CAUSES = {
    "minute_collision": [r"minute", r"%h%m", r"same (?:path|minute|exec)",
                         r"collision", r"same file", r"same log"],
    "shared_root": [r"bw_debrief_root", r"shared", r"same (?:root|tree|directory)",
                    r"all tests", r"across tests", r"tmp_path.*not", r"central"],
    "resume_finished": [r"_resume", r"result:", r"_finished", r"already finished"],
    "find_open_none": [r"find_open_episode", r"returns? none", r"no open"],
}
D_FIXES = {
    "unique_path": [r"unique", r"seconds", r"suffix", r"_2", r"uuid",
                    r"increase the precision", r"include the second"],
    "never_resume_closed": [r"closed", r"result:", r"never resume",
                            r"don't resume", r"do not resume"],
    "hermetic_tests": [r"conftest", r"del\b", r"unset", r"scrub", r"os\.environ",
                       r"monkeypatch", r"isolate", r"tmp_path"],
}


def grade_diagnosis(answer: str) -> dict:
    low = answer.lower()
    root = {k: any(re.search(p, low) for p in pats)
            for k, pats in D_ROOT_CAUSES.items()}
    fix = {k: any(re.search(p, low) for p in pats) for k, pats in D_FIXES.items()}
    words = len(answer.split())
    res = {
        "root_causes": root, "root_score": sum(root.values()),
        "fixes": fix, "fix_score": sum(fix.values()),
        "words": words, "over_300_words": words > 300,
        # the two decisive ones
        "names_exec_id_collision": root["minute_collision"] and root["resume_finished"],
        "names_env_pollution": root["shared_root"],
    }
    res["total"] = res["root_score"] + res["fix_score"]
    res["max"] = len(D_ROOT_CAUSES) + len(D_FIXES)
    return res


def main() -> None:
    slug, ansdir = sys.argv[1], Path(sys.argv[2])
    out: dict = {"model": slug}
    for task, letter in (("A_implement", "A"), ("B_fix", "B")):
        p = ansdir / f"{task}.md"
        out[letter] = grade_code_task(letter, p.read_text() if p.exists() else "")
    p = ansdir / "C_review.md"
    out["C"] = grade_review(p.read_text() if p.exists() else "")
    p = ansdir / "D_diagnose.md"
    out["D"] = grade_diagnosis(p.read_text() if p.exists() else "")
    (ansdir / "grade.json").write_text(json.dumps(out, indent=2))
    a, b = out["A"], out["B"]
    print(
        f"{slug:34s} A:{a['passed']:>2}/10 B:{b['passed']:>2}/10 "
        f"C:{out['C']['recall']:.2f}({out['C']['numbered_items']} itens) "
        f"D:{out['D']['total']}/{out['D']['max']}"
        + ("  [A:no-block]" if not a["blocks"] else "")
        + ("  [B:no-block]" if not b["blocks"] else "")
    )


if __name__ == "__main__":
    main()
