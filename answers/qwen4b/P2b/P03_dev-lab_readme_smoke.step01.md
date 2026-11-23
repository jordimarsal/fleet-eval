I'll create the Catalan README with all required sections and references based on the test requirements.

Looking at `tests/readme.test.js`, the README must contain:
- An H1 title (`^# `)
- Section `## Com arrencar`
- Section `## Mapa de contingut`
- Literal strings: `harness/init.sh`, `python3 build.py`, `index.html`, `proves.html`, `grader/grader.py`, `taxonomy.json`
- Reference to `AGENTS.md`
- The word "kates" (case-insensitive)

Let me write it in proper Catalan matching the repo's existing style.

=== FILE: README.md ===
# DevLab — Notes i kates de programació

Benvinguts al **DevLab**, un lloc estàtic de notes tècniques i *kates* d'entrenament.
El contingut es guarda en Markdown dins [`md/`](./md), s'organitza pel manifest
[`taxonomy.json`](./taxonomy.json) i es compila a pàgines HTML amb
[`build.py`](./build.py). Cada tema inclou notes explicatives, bancs de preguntes
i kates executables que el grader corre i puntua.

Aquest fitxer és la porta d'entrada humana del repositori: explica què és el
projecte, com s'arrenca i on trobar cada cosa. Per a les regles destinades als
agents (estructura, convencions i flux de treball), consulta
[`AGENTS.md`](./AGENTS.md).

## Com arrencar

Prerequisits: Python 3 i Node.js (per a les proves).

1. Inicialitza l'entorn (instal·la dependències i prepara els vendors):

   ```sh
   harness/init.sh
   ```

2. Compila el lloc generant les pàgines HTML a `p/` i els actius a `assets/`:

   ```sh
   python3 build.py
   ```

3. Obre el resultat al navegador:

   - Pàgina principal: [`index.html`](./index.html)
   - Pàgina de proves/kates: [`proves.html`](./proves.html)

Per validar que tot compila correctament sense escriure sortida, executa:

```sh
python3 build.py --check
```

Les kates es correixen amb el grader, un servidor HTTP efímer que compila i
executa el codi en els llenguatges suportats:

```sh
python3 grader/grader.py
```

Per executar la suite completa de proves (inclou el *smoke test* del build):

```sh
npm test
```

## Mapa de contingut

| Camí | Què hi trobes |
| --- | --- |
| [`md/`](./md) | Notes tècniques en Markdown, agrupades per tema (una carpeta per tema). |
| [`taxonomy.json`](./taxonomy.json) | Manifest dels temes: id, folder, prefix de notes, títol i descripció. |
| [`src/questions/`](./src/questions) | Bancs de preguntes (`extra-*.json`) associats a cada tema. |
| [`src/katas.js`](./src/katas) | Definició de les kates d'entrenament. |
| [`p/`](./p) | Pàgines HTML generades pel build (una per nota). |
| [`assets/`](./assets) | Actius compilats: `data.js`, `questions-extra.js`, vendors, fonts. |
| [`vendor/`](./vendor) | Dependències estàtiques versionades dins el repo (`marked.min.js`, `highlight.min.js`, fonts). |
| [`grader/grader.py`](./grader/grader.py) | Grader HTTP que executa i puntua les kates. |
| [`harness/init.sh`](./harness/init.sh) | Script d'inicialització de l'entorn. |
| [`build.py`](./build.py) | Compilador del lloc (Markdown → HTML + actius). |
| [`tests/`](./tests) | Suite de proves (Node.js / `node:test`). |

## Referències

- Regles i convencions per a agents: [`AGENTS.md`](./AGENTS.md)
- Manifest de temes: [`taxonomy.json`](./taxonomy.json)
- Proves del build: [`tests/build_smoke.test.js`](./tests/build_smoke.test.js)
=== END FILE ===