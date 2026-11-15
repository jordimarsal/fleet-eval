"""Build prompt E: reproduce runtime.py COMPLETELY with two modifications."""
from pathlib import Path

SRC = Path.home() / "Documents/CV/projects/buildwright/src/buildwright/runtime.py"
src = SRC.read_text()
out = Path(__file__).parent / "prompts" / "E_largefile.md"

E = f"""ROLE: implementer. You must return a COMPLETE rewritten file.

=== FILE: src/buildwright/runtime.py (COMPLETE, {len(src.splitlines())} lines) ===
```python
{src}
```

Apply EXACTLY these two changes and keep everything else byte-for-byte the same:

1. ADD a new module-level function after `tool_run_command`:

```python
def tool_stat_file(sandbox: Sandbox, path: str) -> str:
    \"\"\"Size in bytes of one file inside the sandbox, or an error string.\"\"\"
```
   It must use `resolve_in_sandbox` for the path, raise/return the same style of
   error message the neighbouring `tool_*` functions use, and be fully annotated.

2. CHANGE `command_allowed` so it also rejects any command containing a
   shell redirection (`>`, `>>`, `<`) — the check must happen BEFORE the
   existing logic, and the existing behaviour must be preserved for commands
   with no redirections.

CONSTRAINTS (all graded):
- Return the WHOLE file: all 401 original lines, modified as instructed.
- Every original top-level `def`/`class` must still be present with its body.
- No placeholders: never write `...`, `# rest unchanged`, `@@` diff headers,
  or any elision. If you think a part is unchanged, write it out in full.
- The result must parse as valid Python.
- Do not add imports that are not already there, unless change 1 needs one.

OUTPUT FORMAT (strict): exactly ONE fenced python block containing the COMPLETE
file, nothing else. This is a long file; budget your output for all of it.
"""
out.write_text(E)
print(f"E: {len(E)} chars ~{len(E)//4} tokens (prompt) · file is {len(src.splitlines())} lines ~3474 tokens to emit")
