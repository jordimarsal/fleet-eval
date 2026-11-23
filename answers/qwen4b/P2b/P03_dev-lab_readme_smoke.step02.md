The test file `tests/build_smoke.test.js` is already provided as part of "TESTS THE FINAL RESULT MUST PASS". Let me verify if it exists in the repository state and check what's needed.

Looking at the current repository state, I see the file tree is empty (no files listed after "CURRENT REPOSITORY STATE"). However, the task says T1 depends on creating README.md which was already done in previous work. 

For T2, I need to ensure `tests/build_smoke.test.js` exists with the correct content. The test file is already specified in the "TESTS THE FINAL RESULT MUST PASS" section, so I just need to create it.

Let me also check if there are any other requirements - the gate says "Confirm `npm test` runs `python3 build.py --check` successfully and exits with code 0". This means the test should pass when the build succeeds.

Since the test file content is already defined in the plan, I'll create it exactly as specified:

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