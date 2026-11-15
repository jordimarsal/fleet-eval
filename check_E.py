"""Functional check for task E deliveries: does the delivered runtime.py WORK?

Run: python3 check_E.py <slug>
Extracts the block, writes it, then exercises the two required behaviours.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FE = Path(__file__).parent
# runtime.py imports pydantic_ai; borrow buildwright's venv so the probe can exec
BWPY = str(Path.home() / "Documents/CV/projects/buildwright/.venv/bin/python")


def blocks(text: str) -> list[str]:
    return [b for b in re.findall(r"```(?:python|py)?\n(.*?)```", text, re.S) if b.strip()]


PROBE = '''
import sys, tempfile, pathlib
mod = sys.modules["runtime"]
ok, fail = [], []
sb_root = pathlib.Path(tempfile.mkdtemp())
(sb_root / "f.txt").write_text("hello world")

# --- change 1: tool_stat_file exists and works
try:
    out = mod.tool_stat_file(mod.Sandbox(root=sb_root), "f.txt")
    ok.append("tool_stat_file runs") if str(11) in str(out) else fail.append(f"tool_stat_file -> {out!r}")
except Exception as e:
    fail.append(f"tool_stat_file raised {type(e).__name__}: {e}")

# --- change 1b: refuses to escape the sandbox (returns an ERROR string or raises)
try:
    out = mod.tool_stat_file(mod.Sandbox(root=sb_root), "../../etc/passwd")
    low = str(out).lower()
    if "error" in low or "escape" in low or "not found" in low or "denied" in low:
        ok.append("tool_stat_file blocks escape")
    else:
        fail.append(f"tool_stat_file returned a size for an escaped path -> {out!r}")
except Exception:
    ok.append("tool_stat_file blocks escape")

# --- change 2: command_allowed rejects redirections
try:
    r = mod.command_allowed("echo hi > /tmp/x", ("echo",))
    if r is False or r == 0:
        ok.append("command_allowed rejects > redirect")
    else:
        fail.append(f"command_allowed allowed > -> {r!r}")
except Exception as e:
    fail.append(f"command_allowed raised {type(e).__name__}: {e}")

# --- change 2b: existing behaviour preserved (allowed command, no redirect)
try:
    r = mod.command_allowed("echo hi", ("echo",))
    if r:
        ok.append("command_allowed still allows echo")
    else:
        fail.append("command_allowed broke the ALLOW path")
except Exception as e:
    fail.append(f"command_allowed(allow) raised {type(e).__name__}: {e}")

# --- change 2c: genuinely dangerous command still rejected
try:
    r = mod.command_allowed("rm -rf /", ("echo",))
    if not r:
        ok.append("command_allowed still rejects rm -rf")
    else:
        fail.append("command_allowed allowed rm -rf")
except Exception as e:
    fail.append(f"command_allowed(deny) raised {type(e).__name__}: {e}")

print("OK:" + "|".join(ok))
print("FAIL:" + "|".join(fail))
'''


def main() -> None:
    slug, ansdir = sys.argv[1], Path(sys.argv[2])
    p = ansdir / "E_largefile.md"
    if not p.exists():
        print(f"{slug:24s} (sense resposta)")
        return
    bs = blocks(p.read_text())
    if not bs:
        print(f"{slug:24s} (cap bloc)")
        return
    body = max(bs, key=len)
    if body.startswith("<<<NOMÉS"):
        print(f"{slug:24s} CONTENT BUIT (només reasoning)")
        return

    d = Path(tempfile.mkdtemp(prefix=f"e_{slug}_"))
    try:
        (d / "runtime.py").write_text(body)
        (d / "probe.py").write_text(PROBE)
        # third-party imports used by runtime.py must be importable
        r = subprocess.run([BWPY, "-c",
                            "import runtime; exec(open('probe.py').read())"],
                           cwd=d, capture_output=True, text=True, timeout=60)
        out = r.stdout + r.stderr
        ok = re.search(r"^OK:(.*)$", out, re.M)
        fail = re.search(r"^FAIL:(.*)$", out, re.M)
        oks = [x for x in (ok.group(1).split("|") if ok else []) if x]
        fails = [x for x in (fail.group(1).split("|") if fail else []) if x]
        if "Traceback" in out and not ok:
            tail = out.strip().splitlines()[-1][:80]
            print(f"{slug:24s} IMPORT/EXEC ERROR: {tail}")
        else:
            print(f"{slug:24s} {len(oks)}/5 correctes" +
                  (f"  FALLA: {fails}" if fails else "  TOTES OK"))
        (ansdir / "grade_E_func.json").write_text(json.dumps({"ok": oks, "fail": fails}, indent=1))
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    main()
