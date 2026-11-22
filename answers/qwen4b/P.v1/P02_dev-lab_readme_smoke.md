FILES  
README.md  
tests/readme.test.js  
tests/build_smoke.test.js  

TASKS  
T1: Create README in Catalan with required sections and content map  
    depends_on: (none)  
    refs: R1  
T2: Implement smoke test to execute `python3 build.py --check` and validate exit code 0  
    depends_on: T1  
    refs: R2  

GATES  
- Verify existence and content of `README.md` using `tests/readme.test.js` (checks title, intro, "com arrencar", content map, and references to `AGENTS.md`)  
- Verify that `npm test` runs `python3 build.py --check` successfully (exit code 0) via `tests/build_smoke.test.js`  
- Confirm no build or link errors occur during execution of `build.py --check` in a sandboxed environment (simulated via process spawn)