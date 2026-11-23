The user wants to implement **T1** from the plan.
This involves creating two files:
1. `README.md`: A human-readable readme in Catalan explaining what the project is, how to start it (`harness/init.sh`, `python3 build.py`, `index.html`, `proves.html`), a content map, and pointing to `AGENTS.md`. It must mention "kates".
2. `tests/readme.test.js`: The test file provided in the prompt context.

Let's analyze the requirements for `README.md` based on `tests/readme.test.js`:
- Must have an H1 title (`^# /m`).
- Must contain section headers: `## Com arrencar`, `## Mapa de contingut`.
- Must contain specific strings/commands:
  - `harness/init.sh`
  - `python3 build.py`
  - `index.html`
  - `proves.html`
  - `grader/grader.py`
  - `taxonomy.json`
  - `AGENTS.md`
- Must contain the word "kates" (case-insensitive).

I will draft the `README.md` in Catalan to satisfy these constraints naturally.

Structure of `README.md`:
```markdown
# DevLab

Aquest és un repositori per a l'aprenentatge i pràctica de desenvolupament de programari, amb enfocament en kates i proves automatitzades.

## Què és?

Un entorn d'integració contínua local que permet executar kates en diversos llenguatges, generar documentació i validar la integritat del projecte mitjançant proves de fum i unitat.

## Com arrencar

Per iniciar el projecte des de zero, segueix aquests passos:

1. Inicialitza l'entorn:
   ```bash
   ./harness/init.sh
   ```
2. Genera els actius i la documentació:
   ```bash
   python3 build.py
   ```
3. Obre la interfície principal al navegador:
   - Interfície web: [index.html](./index.html)
   - Proves interactives: [proves.html](./proves.html)

El grader es troba a `grader/grader.py` i la configuració dels temes a `taxonomy.json`.

## Mapa de contingut

- `md/`: Notes tècniques organitzades per tema.
- `src/`: Codi font de les kates i preguntes.
- `tests/`: Suite de proves (Node.js).
- `vendor/`: Dependències estàtiques.
- `p/`: Pàgines HTML generades.

## Per a agents

Si ets un agent d'IA o un bot que treballa en aquest repositori, consulta el fitxer [`AGENTS.md`](./AGENTS.md) per obtenir instruccions específiques sobre com executar proves, formatar codi i gestionar dependències.
```

Now I will create the test file exactly as provided in the prompt context.

=== FILE: README.md ===
# DevLab

Aquest és un repositori per a l'aprenentatge i pràctica de desenvolupament de programari, amb enfocament en **kates** i proves automatitzades.

## Què és?

Un entorn d'integració contínua local que permet executar kates en diversos llenguatges, generar documentació i validar la integritat del projecte mitjançant proves de fum i unitat. El sistema gestiona múltiples temes tècnics definits al manifest central.

## Com arrencar

Per iniciar el projecte des de zero, segueix aquests passos:

1. Inicialitza l'entorn (instal·la dependències Node.js):
   ```bash
   ./harness/init.sh
   ```
2. Genera els actius estàtics i la documentació HTML:
   ```bash
   python3 build.py
   ```
3. Obre la interfície principal al navegador:
   - Interfície web: [index.html](./index.html)
   - Proves interactives: [proves.html](./proves.html)

El grader es troba a `grader/grader.py` i la configuració dels temes i notes a `taxonomy.json`.

## Mapa de contingut

- `md/`: Notes tècniques organitzades per tema (Markdown amb frontmatter).
- `src/`: Codi font de les kates i bancs de preguntes.
- `tests/`: Suite de proves (Node.js test runner).
- `vendor/`: Dependències estàtiques (JS/CSS/fonts).
- `p/`: Pàgines HTML generades pel build.
- `assets/`: Actius finals generats (data.js, etc.).

## Per a agents

Si ets un agent d'IA o un bot que treballa en aquest repositori, consulta el fitxer [`AGENTS.md`](./AGENTS.md) per obtenir instruccions específiques sobre com executar proves, formatar codi i gestionar dependències.
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