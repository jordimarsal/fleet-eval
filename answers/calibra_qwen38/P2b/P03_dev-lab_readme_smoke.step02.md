The task is to create `tests/build_smoke.test.js`. Looking at the "TESTS THE FINAL RESULT MUST PASS" section, the exact content and behavior are defined. I will generate this file exactly as specified.

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