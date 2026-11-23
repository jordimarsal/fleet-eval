The test file `tests/build.test.js` is already present and complete based on the "YOUR PREVIOUS WORK" section provided. I will output it to confirm its state as required by the task instructions ("preserve their behavior"). No other files need modification for T4 since T1, T2, and T3 are marked complete and their artifacts (`build.py`, `vendor/`, etc.) are already in place.

=== FILE: tests/build.test.js ===
// tests/build.test.js — reproducible_build (R1–R6)
// R1 es verifica sobre el repo; R2–R6 són end-to-end en sandbox (còpia temporal,
// cap mutació del repo real).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  readFileSync, existsSync, mkdirSync, cpSync, rmSync, readdirSync, writeFileSync,
} from 'node:fs';
import { execSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';

const ROOT = dirname(import.meta.dirname);
const PY = 'python3';

const sha256 = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');

function sandbox() {
  const dir = join(tmpdir(), `devlab-sb-${process.pid}-${Math.random().toString(36).slice(2)}`);
  mkdirSync(dir);
  const skip = new Set(['.git', 'node_modules', 'harness', 'tests']);
  for (const entry of readdirSync(ROOT)) {
    if (skip.has(entry)) continue;
    cpSync(join(ROOT, entry), join(dir, entry), { recursive: true });
  }
  return dir;
}

function run(dir, args) {
  try {
    const out = execSync(`${PY} build.py ${args}`, { cwd: dir, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    return { code: 0, out };
  } catch (e) {
    return { code: e.status ?? 1, out: `${e.stdout ?? ''}${e.stderr ?? ''}` };
  }
}

// R1 — vendors dins el repo i build.py apuntant-hi
test('R1: vendor/ complet i build.py llegeix del repo', () => {
  for (const f of ['vendor/marked.min.js', 'vendor/highlight.min.js', 'vendor/fonts/fonts-local.css']) {
    assert.ok(existsSync(join(ROOT, f)), `falta ${f}`);
  }
  const woffs = readdirSync(join(ROOT, 'vendor/fonts')).filter((f) => f.endsWith('.woff2'));
  assert.ok(woffs.length >= 3, `fonts woff2 presents (${woffs.length})`);
  const src = readFileSync(join(ROOT, 'build.py'), 'utf8');
  assert.ok(src.includes("VENDORS = os.path.join(ROOT, 'vendor')"), 'VENDORS cap a repo');
  assert.ok(src.includes("FONTS_SRC = os.path.join(ROOT, 'vendor', 'fonts')"), 'FONTS_SRC cap a repo');
  assert.ok(!src.includes('/tmp/opencode'), 'cap referència a /tmp/opencode');
  assert.ok(existsSync(join(ROOT, 'assets/marked.min.js')), 'output vendor present a assets/');
});

// R2 — vendor incomple → error net, sense traceback
test('R2: falta un vendor → exit != 0 amb missatge net', () => {
  const sb = sandbox();
  try {
    rmSync(join(sb, 'vendor/marked.min.js'));
    const r = run(sb, '');
    assert.notEqual(r.code, 0, 'ha de fallar');
    assert.ok(r.out.includes('vendor incomple'), `missatge net: ${r.out.slice(0, 200)}`);
    assert.ok(!r.out.includes('Traceback'), 'sense traceback');
  } finally {
    rmSync(sb, { recursive: true, force: true });
  }
});

// R3 — nota sense grup → exit != 0 amb slugs
test('R3: nota sense assignar → exit != 0 llistant el slug', () => {
  const sb = sandbox();
  try {
    mkdirSync(join(sb, 'md/ZZZ'), { recursive: true });
    writeFileSync(join(sb, 'md/ZZZ/orfe-test.md'), '---\ntitle: Orfe\ntags: []\n---\n\nCos.\n');
    const r = run(sb, '--check');
    assert.notEqual(r.code, 0, 'ha de fallar');
    assert.ok(r.out.includes('NO ASSIGNADES'), 'missatge NO ASSIGNADES');
    assert.ok(r.out.includes('orfe-test'), 'llista el slug');
  } finally {
    rmSync(sb, { recursive: true, force: true });
  }
});

// R4 — pregunta extra invàlida → exit != 0 amb Q-REBUTJADA
test('R4: pregunta extra invàlida → exit != 0', () => {
  const sb = sandbox();
  try {
    const bank = JSON.parse(readFileSync(join(sb, 'src/questions/extra-lenguaje.json'), 'utf8'));
    bank.push({ t: 'lenguaje', ty: 'choice', q: 'Pregunta trencada de test', opts: ['a', 'b'] }); // sense 'a'
    writeFileSync(join(sb, 'src/questions/extra-lenguaje.json'), JSON.stringify(bank, null, 1));
    const r = run(sb, '--check');
    assert.notEqual(r.code, 0, 'ha de fallar');
    assert.ok(r.out.includes('Q-REBUTJADA'), 'missatge Q-REBUTJADA');
    assert.ok(r.out.includes('invàlides'), 'resum d’errors');
  } finally {
    rmSync(sb, { recursive: true, force: true });
  }
});

// R5 — doble build byte-idèntic + footer sense data
test('R5: doble build byte-idèntic i footer sense data', () => {
  const sb = sandbox();
  try {
    const files = ['index.html', 'assets/data.js', 'assets/questions-extra.js'];
    const r1 = run(sb, '');
    assert.equal(r1.code, 0, `primer build verd: ${r1.out.slice(-200)}`);
    const h1 = files.map((f) => sha256(join(sb, f)));
    const r2 = run(sb, '');
    assert.equal(r2.code, 0, 'segon build verd');
    const h2 = files.map((f) => sha256(join(sb, f)));
    assert.deepEqual(h2, h1, 'dos builds consecutius → outputs byte-idèntics');
    const idx = readFileSync(join(sb, 'index.html'), 'utf8');
    assert.ok(!/\d{2}\/\d{2}\/\d{4}/.test(idx.split('<footer')[1] ?? ''), 'footer sense data');
    assert.ok(idx.includes('generat amb <code>build.py</code>'), 'footer amb text estàtic');
  } finally {
    rmSync(sb, { recursive: true, force: true });
  }
});

// R6 — --check valida sense escriure (ni modificar) cap output
test('R6: --check valida sense escriure cap output', () => {
  const sb = sandbox();
  try {
    const firstNote = `p/${readdirSync(join(sb, 'p'))[0]}`;
    const watched = ['index.html', 'assets/style.css', 'assets/data.js', firstNote];
    const before = Object.fromEntries(watched.map((f) => [f, sha256(join(sb, f))]));
    const listingBefore = readdirSync(sb).sort();
    const r = run(sb, '--check');
    assert.equal(r.code, 0, `check verd sobre contingut net: ${r.out.slice(-200)}`);
    assert.ok(r.out.includes('Check OK'), 'missatge final de check');
    assert.deepEqual(readdirSync(sb).sort(), listingBefore, 'cap fitxer nou al root');
    for (const f of watched) {
      assert.equal(sha256(join(sb, f)), before[f], `--check no modifica ${f}`);
    }
  } finally {
    rmSync(sb, { recursive: true, force: true });
  }
});

// R5 (repo comès): el footer de l'índex no conté data de generació
test('R5: index.html comès sense data de generació al footer', () => {
  const idx = readFileSync(join(ROOT, 'index.html'), 'utf8');
  const footer = idx.split('<footer')[1] ?? '';
  assert.ok(!/\d{2}\/\d{2}\/\d{4}/.test(footer), 'footer comès sense data');
});
=== END FILE ===