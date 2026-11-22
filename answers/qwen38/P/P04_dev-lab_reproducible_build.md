FILES
vendor/marked.min.js
vendor/highlight.min.js
vendor/fonts/fonts-local.css
vendor/fonts/Inter-Regular.woff2
vendor/fonts/Inter-Medium.woff2
vendor/fonts/Fraunces-Regular.woff2
build.py
tests/build_reproducible.test.sh

TASKS
T1: Vendor assets ingestion and path migration
    depends_on: (none)
    refs: R1
T2: Implement hard validation for vendor inputs
    depends_on: T1
    refs: R2
T3: Implement group assignment validation
    depends_on: T1
    refs: R3
T4: Implement question schema validation
    depends_on: T1
    refs: R4
T5: Remove build date from output generation
    depends_on: T1
    refs: R5
T6: Implement --check mode
    depends_on: T2, T3, T4
    refs: R6
T7: Create end-to-end verification tests
    depends_on: T2, T3, T4, T5, T6
    refs: R1, R2, R3, R4, R5, R6

GATES
- `python3 build.py --check` exits 0 on clean repo.
- `python3 build.py --check` exits non-zero with specific error messages when simulating missing vendors, unassigned notes, or invalid questions (via sandbox copy).
- Two consecutive builds (`python3 build.py`) produce byte-identical outputs in the `p/` directory and `index.html`.
- `grep -r "datetime" p/index.html` returns no results (no embedded dates).
- `bash tests/build_reproducible.test.sh` passes all assertions for exit codes and file integrity.