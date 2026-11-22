FILES
assets/marked.min.js
assets/highlight.min.js
assets/fonts-local.css
src/assets/fonts-local.css
build.py

TASKS
T1: Move vendor files to assets and update build.py paths
    depends_on: (none)
    refs: R1, R2
T2: Implement missing file validation with error reporting
    depends_on: T1
    refs: R2, R3
T3: Add schema validation for extra questions
    depends_on: T2
    refs: R4
T4: Ensure no build date is embedded in output
    depends_on: T3
    refs: R5
T5: Implement full content validation via --check flag
    depends_on: T4
    refs: R6

GATES
- Verify that `vendor/marked.min.js`, `vendor/highlight.min.js`, `vendor/fonts/fonts-local.css`, and all `.woff2` files exist in `assets/`
- Run `python3 build.py --check` on a corrupted fixture (missing group or invalid question) → assert exit code ≠ 0 and correct error message appears
- Perform two consecutive builds in sandbox; verify SHA-256 hash of generated site is identical and index.html footer contains no build date
- Confirm `npm test` passes without errors