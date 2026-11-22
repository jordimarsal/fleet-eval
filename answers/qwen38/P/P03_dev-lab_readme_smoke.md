FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Create Catalan README with required structure and commands
    depends_on: (none)
    refs: R1
T2: Implement mechanical test suite for README content validation
    depends_on: T1
    refs: R1
T3: Implement build smoke test within npm test suite
    depends_on: (none)
    refs: R2

GATES
- `npm test` passes successfully (including new readme and build smoke tests)
- `python3 build.py --check` exits with code 0
- `cat README.md` confirms presence of title, intro, "com arrencar" section, content map, and pointer to AGENTS.md in Catalan