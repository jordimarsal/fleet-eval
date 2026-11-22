FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Create README.md in Catalan
    depends_on: (none)
    refs: R1
T2: Implement README content verification tests
    depends_on: T1
    refs: R1
T3: Implement build smoke test in npm suite
    depends_on: (none)
    refs: R2
T4: Integrate smoke test into existing test runner
    depends_on: T3
    refs: R2

GATES
- `npm test` executes successfully and includes both `readme.test.js` and `build_smoke.test.js`.
- `python3 build.py --check` returns exit code 0 when run manually.
- `README.md` contains all required sections: title, intro, "com arrencar", content map, and pointer to `AGENTS.md`.
- `README.md` contains exact command literals: `harness/init.sh`, `python3 build.py`, and `index.html`.
- `README.md` correctly references the existence of `md/` and `proves.html`.