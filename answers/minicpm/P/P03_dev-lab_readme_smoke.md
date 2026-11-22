FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Create README.md in Catalan with required sections
    depends_on: (none)
    refs: R1
T2: Create tests/readme.test.js to verify README structure and content
    depends_on: T1
    refs: R1
T3: Create tests/build_smoke.test.js to run `python3 build.py --check` as smoke test
    depends_on: (none)
    refs: R2

GATES
- `npm test` passes including new tests in tests/readme.test.js and tests/build_smoke.test.js
- README.md exists at root, is in Catalan, and contains all required sections (title, intro, "com arrencar", content map, pointer to AGENTS.md)
- `python3 build.py --check` exits 0 on valid build
- harness/init.sh continues to work (it already runs `npm test` and `build.py --check`)