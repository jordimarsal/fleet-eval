=== FILE: README.md ===
# Repòsitori de Notes i Kates

Aquest és un repòsitori de contingut tècnic curat, estructurat com un lloc web estàtic que inclou notes detallades sobre tecnologia i un camp de proves interactiu amb "kates" (exercicis pràctics).

## Com arrencar

Per visualitzar el contingut o fer servir les eines del repòsitori, utilitza les següents vies:

1. **Preparació inicial**: Executa `harness/init.sh` per configurar l'entorn local si és la primera vegada.
2. **Generar el site**: Utilitza `python3 build.py` per convertir els fitxers Markdown (`md/`) en pàgines HTML (`p/`).
3. **Visualització**:
   - Obre `index.html` al teu navegador per veure el mapa de contingut.
   - Obre `proves.html` per accedir al camp de proves interactiu.
4. **Verificació**: Pots utilitzar `python3 build.py --check` per assegurar-te que no hi ha enllaços trencats ni errors de construcció.

## Mapa de contingut

El contingut està organitzat segons la taxonomi definida a `taxonomy.json`:

- **Notes tècniques**: Situades a la carpeta `md/`. Cada nota té un slug que es reflecteix en el seu fitxer HTML generat a `p/`.
- **Camp de Proves**: Localitzat a `proves.html`, permet practicar amb preguntes de tipus *choice*, *output*, *blank*, *bug* i *order*.
- **Kates**: Exercicis pràctics que poden ser avalats localment mitjançant `grader/grader.py`.

## Per a Agents

Si ets un agent d'IA treballant en aquest repòsitori, consulta el fitxer [AGENTS.md](AGENTS.md) per entendre les convencions, l'estructura de dades i com interactuar amb el sistema de verificació sense degradar la qualitat del contingut.

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