FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Create README.md in Catalan with title, intro, "com arrencar" section, content map, and AGENTS.md pointer
    depends_on: (none)
    refs: R1
T2: Write tests/readme.test.js to verify README exists, has required sections, and contains command literals
    depends_on: T1
    refs: R1
T3: Write tests/build_smoke.test.js to spawn `python3 build.py --check` and assert exit 0
    depends_on: (none)
    refs: R2
T4: Add npm script hook so `npm test` runs `python3 build.py --check` as a smoke test
    depends_on: T3
    refs: R2

GATES
- `cat README.md | grep -q "Com arrencar"` — section present
- `cat README.md | grep -q "harness/init.sh"` — command literal present
- `cat README.md | grep -q "python3 build.py"` — command literal present
- `cat README.md | grep -q "index.html"` — command literal present
- `cat README.md | grep -q "md/"` — content directory referenced
- `cat README.md | grep -q "proves.html"` — quiz page referenced
- `cat README.md | grep -q "AGENTS.md"` — AI agent pointer present
- `node tests/readme.test.js` — passes
- `python3 build.py --check` — exits 0
- `node tests/build_smoke.test.js` — passes
- `npm test` — all tests pass, including the new smoke test