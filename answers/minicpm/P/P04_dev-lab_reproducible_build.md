FILES
vendor/marked.min.js
vendor/highlight.min.js
vendor/fonts/fonts-local.css
vendor/fonts/*.woff2
build.py

TASKS
T1: Create vendor directory and populate with required files
    depends_on: (none)
    refs: R1
T2: Update build.py to source vendors and fonts from in-repo paths
    depends_on: T1
    refs: R1
T3: Add missing vendor input validation with clean error messages
    depends_on: T2
    refs: R2
T4: Add unassigned note slug validation
    depends_on: T2
    refs: R3
T5: Add extra question schema validation
    depends_on: T2
    refs: R4
T6: Remove build date embedding for reproducible builds
    depends_on: T2
    refs: R5
T7: Implement --check flag for pre-build validation
    depends_on: T3, T4, T5, T6
    refs: R6

GATES
- `python3 build.py --check` passes with exit code 0 on clean repo
- `npm test` passes
- Verify vendor files exist at correct paths: `vendor/marked.min.js`, `vendor/highlight.min.js`, `vendor/fonts/fonts-local.css`, `vendor/fonts/*.woff2`
- Verify `build.py` references `vendor/` paths instead of `/tmp/opencode/*`
- Test missing vendor file scenario: expect non-zero exit with clean error message naming the missing path
- Test unassigned note scenario: expect non-zero exit with reported slugs
- Test invalid question scenario: expect non-zero exit with rejected questions listed
- Verify byte-identical outputs from two consecutive builds on different days (sha256 hash comparison)
- Verify `index.html` footer does not contain build date