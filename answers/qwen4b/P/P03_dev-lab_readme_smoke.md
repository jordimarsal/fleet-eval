FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Create Catalan README with required sections and links
    depends_on: (none)
    refs: R1
T2: Implement build smoke test in npm test suite
    depends_on: T1
    refs: R2

GATES
- Verify README.md exists and contains correct Catalan content with title, intro, "com arrencar" section, content map, and references to `AGENTS.md` and relevant paths  
- Confirm `npm test` runs `python3 build.py --check` successfully and exits with code 0  
- Validate that `tests/readme.test.js` passes by checking for presence of all required sections and literal commands  
- Ensure `tests/build_smoke.test.js` fails when a mock build error occurs (exit code non-zero) or passes when build succeeds (exit code 0)