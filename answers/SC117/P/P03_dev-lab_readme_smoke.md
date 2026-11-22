FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Create README.md at root
    depends_on: (none)
    refs: R1
T2: Implement tests/readme.test.js
    depends_on: T1
    refs: R1
T3: Implement tests/build_smoke.test.js
    depends_on: (none)
    refs: R2
T4: Verify npm test suite passes with new smoke test
    depends_on: T3
    refs: R2

GATES
- `npm test` exits with code 0 and includes output from `tests/readme.test.js` and `tests/build_smoke.test.js`.
- `python3 build.py --check` executes successfully within the test environment.
- Manual inspection of `README.md` confirms Catalan language, required sections (title, intro, com arrencar, content map), and pointer to `AGENTS.md`.