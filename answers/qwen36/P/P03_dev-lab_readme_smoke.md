FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Create README.md at root in Catalan with title, intro, "com arrencar" section and content map
    depends_on: (none)
    refs: R1
T2: Write tests/readme.test.js to verify README exists, has required sections and command literals
    depends_on: T1
    refs: R1
T3: Write tests/build_smoke.test.js that spawns `python3 build.py --check` and asserts exit 0
    depends_on: (none)
    refs: R2
T4: Verify npm test runs both new tests alongside existing suite
    depends_on: T2, T3
    refs: R1, R2

GATES
- `npm test` passes end-to-end (all existing + new tests green)
- `cat README.md | grep -c "com arrencar"` ≥ 1 (section present)
- `cat README.md | grep -c "harness/init.sh"` ≥ 1 (command literal present)
- `cat README.md | grep -c "AGENTS.md"` ≥ 1 (AI agent pointer present)
- `cat README.md | grep -c "proves.html"` ≥ 1 (quiz link present)
- `cat README.md | grep -c "md/"` ≥ 1 (content directory reference present)
- `node tests/readme.test.js` exits 0
- `node tests/build_smoke.test.js` exits 0