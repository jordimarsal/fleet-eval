FILES
build.py
vendor/marked.min.js
vendor/highlight.min.js
vendor/fonts/fonts-local.css
vendor/fonts/*.woff2

TASKS
T1: Move vendor assets to `vendor/` directory
    depends_on: (none)
    refs: R1
T2: Update `build.py` paths and remove date embedding
    depends_on: T1
    refs: R1, R5
T3: Implement strict validation logic for vendors, groups, and questions
    depends_on: T2
    refs: R2, R3, R4
T4: Wire up `--check` flag to run validations without output
    depends_on: T3
    refs: R6

GATES
- `python3 build.py --check`: Exits 0 on clean repo; exits non-zero with specific error messages on corrupted fixtures (missing vendor, unassigned slug, invalid question schema).
- `npm test`: All existing tests pass.
- Reproducibility check: Two consecutive builds (`python3 build.py`) produce byte-identical `index.html` and `p/*.html` files (verified via sha256sum), confirming no build date is embedded.