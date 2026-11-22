=== FILE: README.md ===
# Camp de Proves

Projecte de pràctica i repàs per a l'aprenentatge de Java i altres llenguatges. Inclou un sistema de quiz, kates (exercicis de codi) i gestió de contingut via Markdown.

## Com arrencar

Per a una instal·lació inicial del medi de proves (harness):
1. Executa `harness/init.sh` per configurar l'entorn.
2. Genera el site estàtic amb `python3 build.py`.
3. Obre `index.html` al teu navegador per començar a jugar.

El sistema utilitza `taxonomy.json` per definir els temes i la estructura de notes. Per als exercicis de codi (kates), es fa servir `grader/grader.py`.

## Mapa de contingut

- **Notes**: El contingut principal es troba en la carpeta `md/`.
- **Proves**: La pàgina de quiz i kates és `proves.html`.
- **Estàtic**: Tot el generat es troba en les rutes d'assets i la carpeta de sortida definida pel script de build.

## Agents

Per a agents de IA que analitzen aquest repositori, consultin `AGENTS.md` per entendre la lògica de validació i la estructura de dades.

## Kates

El projecte inclou un sistema de "kates" per validar la resolució de problemes de programació de manera local.
=== END FILE ===

=== FILE: tests/readme.test.js ===
// tests/readme.test.js — readme_smoke (R1)
// El README és l'entrada humana del repo: ha d'existir i explicar el mínim
// indispensable (què és, com arrencar, on és el contingut, per a agents).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = process.cwd();

test('R1: README.md existeix i explica què és, com arrencar i on és el contingut', () => {
  const md = readFileSync(join(ROOT, 'README.md'), 'utf8');
  assert.match(md, /^# /m, 'sense títol H1');
  for (const seccio of ['## Com arrencar', '## Mapa de contingut']) {
    assert.ok(md.includes(seccio), `falta la secció "${seccio}"`);
  }
  for (const comanda of ['harness/init.sh', 'python3 build.py', 'index.html',
    'proves.html', 'grader/grader.py', 'taxonomy.json']) {
    assert.ok(md.includes(comanda), `falta la comanda/referència "${comanda}"`);
  }
  assert.ok(md.includes('AGENTS.md'), 'falta la referència per a agents (AGENTS.md)');
  assert.ok(md.toLowerCase().includes('kates'), 'falta esmentar les kates');
});
=== END FILE ===

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