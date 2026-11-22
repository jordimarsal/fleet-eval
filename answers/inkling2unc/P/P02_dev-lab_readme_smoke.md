FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js
package.json

TASKS
T1: Create Catalan README at repo root
    depends_on: (none)
    refs: R1
T2: Add npm smoke-test that runs `python3 build.py --check`
    depends_on: (none)
    refs: R2

GATES
- npm test passes (includes the new build smoke test)
- npx/node tests/readme.test.js exits 0 (existència, seccions i literals de comandes del README)
- node tests/build_smoke.test.js exits 0 with exit code 0 from `python3 build.py --check`
- python3 build.py --check still succeeds standalone (harness/init.sh keeps double validation by design, cost ~1–2 s accepted)
- No regression in existing suite (npm test green overall)