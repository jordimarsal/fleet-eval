FILES
vendor/marked.min.js
vendor/highlight.min.js
vendor/fonts/fonts-local.css
vendor/fonts/<woff2 files from /tmp/opencode/fonts>
build.py
tests/build.test.js or new python sanity tests (or extend existing test setup)

TASKS
T1: Vendorize third-party assets into the repo
    depends_on: (none)
    refs: R1
    Copy marked.min.js and highlight.min.js from the previous source into vendor/; copy fonts-local.css and all .woff2 files under vendor/fonts/; verify each required path is non-empty.

T2: Point build.py at in-repo vendors with a hard missing-file check
    depends_on: T1
    refs: R1, R2
    Replace VENDORS='/tmp/opencode/vendors' and FONTS_SRC='/tmp/opencode/fonts' constants with ROOT-relative vendor paths; add an up-front existence+non-empty validation over every required vendor file before any output work; on failure print a clean error naming the missing path and exit non-zero (no traceback).

T3: Enforce group assignment for notes
    depends_on: T2
    refs: R3
    After parsing md/, compute slug → group membership against GROUPS (including '*' wildcards and per-group note lists); collect notes not assigned to any group; if any exist, print the unassigned slugs and exit non-zero with no partial writes.

T4: Harden question schema validation
    depends_on: T2
    refs: R4
    Extend question loading/validation so each extra question (and base questions as applicable) that fails schema checks is reported by id/ref and the build exits non-zero listing every rejected question; keep it in the same validation phase.

T5: Remove date stamp from generated site
    depends_on: T2
    refs: R5
    Find every use of datetime/build-date in templates, index.json generation, footer, meta tags or embed code; remove them or derive everything deterministically from inputs; ensure committed index.html contains no build date.

T6: Add --check mode running all validations read-only
    depends_on: T3, T4
    refs: R6
    Implement `--check` flag: run vendor check + group assignment + question validation + existing link check without writing p/*.html, index.html, index.json or assets; exit non-zero on first/all validation failure with clean messages. Normal build path must reuse the same validation routine and then write outputs only after validations pass.

T7: End-to-end sandbox tests for failures and reproducibility
    depends_on: T6
    refs: R2, R3, R4, R5, R6
    In a temp copy of the repo (with fixtures) assert: missing vendor → exit !=0 naming path; unassigned note fixture → exit !=0 listing slug(s); invalid extra question fixture → exit !=0 listing rejected questions; two builds produce sha256-identical outputs and no date anywhere; `build.py --check` writes nothing and fails on corrupted fixtures. No mutation of the real repo.

GATES
python3 build.py --check (must pass on the committed tree — full validation gate)
npm test (existing suite green plus any new tests from T7)
Sandbox end-to-end runs per verification notes: corrupt-vendor / corrupt-note / corrupt-question fixtures in a temp copy (exit !=0 + expected message), double build in sandbox with identical sha256 hashes and footer without date
grep generated output/index.html for dates, confirm none