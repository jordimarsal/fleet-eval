FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Create Catalan README with required structure and commands
    depends_on: (none)
    refs: R1
T2: Implement build smoke test integration into npm test
    depends_on: T1
    refs: R2

GATES
- `npm test` passes successfully.
- `python3 build.py --check` exits with code 0.
- `tests/readme.test.js` verifies existence of `README.md`, presence of "com arrencar" section, specific command literals (`harness/init.sh`, `python3 build.py`, `index.html`), content map references (`md/`, `proves.html`), and pointer to `AGENTS.md`.
- `tests/build_smoke.test.js` spawns `python3 build.py --check` and asserts exit code 0.