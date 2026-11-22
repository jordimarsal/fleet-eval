FILES
vendor/marked.min.js
vendor/highlight.min.js
vendor/fonts/fonts-local.css
vendor/fonts/*.woff2
build.py
index.html
tests/build.test.js

TASKS
T1: Vendorize vendor assets and fonts in repo
    depends_on: (none)
    refs: R1
T2: Add startup validation of required in-repo inputs with clean errors
    depends_on: T1
    refs: R2
T3: Enforce group assignment; error out on unassigned notes with slugs
    depends_on: T1
    refs: R3
T4: Validate extra question schema at build time; report rejected questions
    depends_on: T1
    refs: R4
T5: Make output deterministic; remove build date from generated site
    depends_on: T1
    refs: R5
T6: Implement `--check` mode running full content validation without writing files
    depends_on: T2, T3, T4, T5
    refs: R6
T7: Add tests: sandbox failure-mode e2e checks + double-build identity check
    depends_on: T6
    refs: R2, R3, R4, R5, R6

GATES
- python3 build.py --check exits 0 on the healthy repo
- npm test passes (including new sandbox fixture tests for missing vendor/unassigned note/invalid question)
- In a temp copy of the repo: deleting or emptying each required vendor input → non-zero exit and clean message naming the path, no traceback
- Sandbox builds twice on different day boundaries produce byte-identical outputs (sha256 match across all generated files) with committed index.html footer containing no date
- A corrupted notes assignment / extra question fixture in a sandbox yields non-zero exit reporting unassigned slugs / rejected questions