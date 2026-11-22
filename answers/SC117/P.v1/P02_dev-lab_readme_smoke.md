FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Create README.md in Catalan
    depends_on: (none)
    refs: R1
T2: Implement readme verification test
    depends_on: T1
    refs: R1
T3: Implement build smoke test
    depends_on: (none)
    refs: R2

GATES
- `npm test` passes successfully, including both `readme.test.js` and `build_smoke.test.js`.
- Manual inspection of `README.md` confirms presence of title, intro, "com arrencar" section, content map, and AI pointer in Catalan.
- Verification that `python3 build.py --check` exits with code 0 during the smoke test execution.