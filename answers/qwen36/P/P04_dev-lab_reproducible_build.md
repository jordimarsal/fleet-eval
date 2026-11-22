FILES
vendor/marked.min.js
vendor/highlight.min.js
vendor/fonts/fonts-local.css
vendor/fonts/Inter-Regular.woff2
vendor/fonts/Inter-Bold.woff2
vendor/fonts/Fraunces-SemiBold.woff2
vendor/fonts/Fraunces-Bold.woff2
build.py

TASKS
T1: Create vendor directory structure and copy assets into it
    depends_on: (none)
    refs: R1
T2: Update build.py to source vendors and fonts from in-repo paths instead of /tmp/opencode/*
    depends_on: T1
    refs: R1
T3: Add missing-vendor validation at build start with clean error messages naming each missing path
    depends_on: T2
    refs: R2
T4: Add unassigned-notes validation that exits non-zero reporting slugs not matched to any group
    depends_on: T2
    refs: R3
T5: Add extra-question schema validation that exits non-zero reporting rejected questions
    depends_on: T2
    refs: R4
T6: Remove build date from generated output so two builds produce byte-identical results
    depends_on: T2
    refs: R5
T7: Implement --check mode that runs all validations without writing output files
    depends_on: T2
    refs: R6

GATES
- `python3 build.py --check` passes on the current repo (exit 0, no output written).
- `npm test` passes.
- Sandbox test: remove one vendor file → `build.py` exits non-zero with message naming the missing path; no traceback.
- Sandbox test: corrupt a note slug so it matches no group → exit non-zero listing the unassigned slug(s).
- Sandbox test: inject an invalid question into `questions-extra.js` → exit non-zero listing the rejected question.
- Sandbox test: run `build.py` twice on different days → sha256 of `index.html` and all `.html` in `p/` are identical across both runs.
- Verify `index.html` footer contains no build timestamp.