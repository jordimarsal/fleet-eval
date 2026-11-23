The user wants to implement **T2: Implement build smoke test integration into npm test**.

Looking at the plan and the provided context:
1.  **Files needed**: `tests/build_smoke.test.js` is listed in the FILES section of the plan.
2.  **Current State**: The repository state shows no previous work for T2. However, the "TESTS THE FINAL RESULT MUST PASS" section provides the exact content for `tests/build_smoke.test.js`.
3.  **Task Description**: "Implement build smoke test integration into npm test". This usually implies ensuring the test file exists and potentially updating `package.json` if it's not running tests automatically (though standard `node:test` runners often pick up files in `tests/`). Let's check if there are other requirements.
4.  **Gates**:
    *   `npm test` passes successfully.
    *   `python3 build.py --check` exits with code 0.
    *   `tests/readme.test.js` verifies... (This is T1, but T2 depends on T1).
    *   `tests/build_smoke.test.js` spawns `python3 build.py --check` and asserts exit code 0.

The prompt asks to implement ONLY this step (T2). The primary artifact for T2 is the test file itself, which integrates the build check into the test suite. The provided "TESTS THE FINAL RESULT MUST PASS" block contains the full implementation of `tests/build_smoke.test.js`.

I need to output `tests/build_smoke.test.js`.

Are there any other files?
The plan lists:
- `README.md` (T1)
- `tests/readme.test.js` (T1)
- `tests/build_smoke.test.js` (T2)

Since I am only doing T2, I should only output `tests/build_smoke.test.js`.

Let's verify the content of `tests/build_smoke.test.js` from the context provided in "TESTS THE FINAL RESULT MUST PASS". It uses `node:test`, `assert`, `spawn`. It checks that `python3 build.py --check` returns exit code 0. This matches the gate requirements.

One detail: Does `npm test` automatically run this? Usually, if `package.json` has `"test": "node --test tests/"` or similar, it will pick it up. If not, I might need to modify `package.json`. However, the prompt says "Implement ONLY this step... Output ONLY the files this step needs". Modifying `package.json` is often part of "integration into npm test". But looking at the existing repo state (which is empty in the prompt's view but implied to exist based on dependencies), and the fact that other tests like `grader.test.js` exist, there is likely already a test runner configured. The specific instruction for T2 is "Implement build smoke test integration into npm test". Creating the file *is* the implementation of the test logic. If the runner isn't set up, that would be a separate infrastructure task usually done earlier or as part of setup. Given the constraints and typical patterns in these tasks, providing the test file is the core requirement.

Let's double check if I should output `package.json`.
The plan doesn't list `package.json` in FILES. It lists `README.md`, `tests/readme.test.js`, `tests/build_smoke.test.js`. This strongly suggests I only need to provide the files listed under FILES that correspond to my current task. My current task is T2, which corresponds to `tests/build_smoke.test.js`.

Therefore, I will output `tests/build_smoke.test.js` with the content provided in the context.

=== FILE: tests/build_smoke.test.js ===
// tests/build_smoke.test.js — readme_smoke (R2)
// Smoke-test dins npm test: si el build falla o hi ha un enllaç trencat,
// la suite és vermella (abans només es veia a les portes manuals).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { join } from 'node:path';

const ROOT = process.cwd();

test('R2: python3 build.py --check passa dins la suite (smoke)', async () => {
  const out = await new Promise((resolve, reject) => {
    const p = spawn('python3', ['build.py', '--check'], { cwd: ROOT });
    let stdout = '';
    const timer = setTimeout(() => {
      p.kill('SIGKILL');
      reject(new Error('build.py --check no acaba en 60 s'));
    }, 60000);
    p.stdout.on('data', (d) => { stdout += d; });
    p.stderr.on('data', (d) => { stdout += d; });
    p.on('error', (e) => { clearTimeout(timer); reject(e); });
    p.on('exit', (code) => { clearTimeout(timer); resolve({ code, stdout }); });
  });
  assert.equal(out.code, 0, `build.py --check exit ${out.code}:\n${out.stdout.slice(-400)}`);
});
=== END FILE ===