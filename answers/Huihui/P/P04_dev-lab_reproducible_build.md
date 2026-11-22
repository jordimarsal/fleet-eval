FILES
vendor/marked.min.js
vendor/highlight.min.js
vendor/fonts/fonts-local.css
build.py
tests/build_reproducible.test.js
tests/validation_errors.test.js

TASKS
T1: Vendor assets migration and path update
    depends_on: (none)
    refs: R1
T2: Implement hard validation logic for vendors, groups, and questions
    depends_on: T1
    refs: R2, R3, R4
T3: Implement reproducible build output and --check mode
    depends_on: T2
    refs: R5, R6
T4: Add automated verification tests
    depends_on: T3
    refs: R1, R2, R3, R4, R5, R6

GATES
- `python3 build.py --check` exits 0 with no file writes on a clean repo.
- Sandbox test: Remove `vendor/marked.min.js`, run `build.py`, assert exit != 0 and stderr contains "marked.min.js".
- Sandbox test: Create orphan note in `md/Java/orphan.md` not listed in GROUPS, run `build.py`, assert exit != 0 and stderr contains "orphan".
- Sandbox test: Inject invalid question schema into `src/questions/extra-dades.json`, run `build.py`, assert exit != 0 and stderr lists the rejected question ID.
- Reproducibility check: Run `build.py` twice, compare SHA-256 of all files in `p/` and `index.html`; verify `index.html` does not contain current date string.
- `npm test` passes (including new tests for validation logic).