FILES
README.md
package.json
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Create Catalan README with required structure and commands
    depends_on: (none)
    refs: R1
T2: Implement build smoke test in npm test suite
    depends_on: T1
    refs: R2

GATES
- Run `npm test` to verify both new tests pass (`readme.test.js` checks existence, sections, literals; `build_smoke.test.js` spawns `python3 build.py --check` and asserts exit 0).
- Verify `harness/init.sh` executes successfully without timeout issues due to the added smoke test overhead (~1-2s).
- Confirm `README.md` is valid Markdown and contains all specified Catalan sections ("com arrencar", content map, pointer to AGENTS.md).