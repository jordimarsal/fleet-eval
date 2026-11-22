FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Create README.md in Catalan
    depends_on: (none)
    refs: R1
T2: Create readme.test.js for README verification
    depends_on: T1
    refs: R1
T3: Create build_smoke.test.js for npm test integration
    depends_on: (none)
    refs: R2

GATES
- Run `npm test` to ensure all tests pass, including the new `readme.test.js` and `build_smoke.test.js`.
- Manually verify `README.md` content matches requirements (title, intro, "com arrencar", content map, commands, paths, AGENTS.md pointer).
- Verify `python3 build.py --check` exits with 0 on the current repository state.