FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js
package.json

TASKS
T1: Redactar README en català amb intro del lab, secció "com arrencar" i mapa de contingut
    depends_on: (none)
    refs: R1
T2: Afegir tests/readme.test.js que verifica existència, seccions i literals de comandes del README
    depends_on: T1
    refs: R1
T3: Afegir tests/build_smoke.test.js que executa `python3 build.py --check` com a smoke-test dins la suite npm test
    depends_on: (none)
    refs: R2
T4: Verificar/ajustar el script `npm test` de package.json perquè inclogui automàticament els nous fitxers de test i validar la integració amb harness/init.sh
    depends_on: T2, T3
    refs: R1, R2

GATES
- `npm test` exit 0 (inclou tests/readme.test.js i tests/build_smoke.test.js)
- `tests/readme.test.js` passa: README existent a l'arrel, amb títol, intro, secció "com arrencar" i mapa de contingut; conté literals `harness/init.sh`, `python3 build.py`, `index.html`, referències a `md/` i `proves.html` i enllaç a AGENTS.md
- `tests/build_smoke.test.js` surt amb exit 0 comprovant `python3 build.py --check` (build + link check)
- Revisar que harness/init.sh continua passant (executa npm test i build.py --check; duplicitat assumida ~1-2 s)