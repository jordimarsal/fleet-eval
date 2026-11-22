FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Create Catalan README.md
    depends_on: (none)
    refs: R1
T2: Implement README content verification tests
    depends_on: T1
    refs: R1
T3: Implement build smoke test in npm suite
    depends_on: (none)
    refs: R2
T4: Implement build smoke test verification
    depends_on: T3
    refs: R2

GATES
- `npm test` passes successfully.
- `README.md` exists and contains required Catalan sections (Title, Intro, "com arrencar", Content Map) and specific command literals (`harness/init.sh`, `python3 build.py`, `index.html`).
- `README.md` contains pointers to `md/`, `proves.html`, and `AGENTS.md`.
- `npm test` executes `python3 build.py --check` via the new smoke test.