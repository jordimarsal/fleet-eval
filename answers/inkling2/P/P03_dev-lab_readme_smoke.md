FILES
README.md
package.json
tests/readme.test.js
tests/build_smoke.test.js

TASKS
T1: Redactar README.md en català amb estructura i comandes del projecte
    depends_on: (none)
    refs: R1
T2: Afegir test que verifica la presència i el contingut de README.md (seccions, comandes literals, mapa de continguts, remitent a AGENTS.md)
    depends_on: T1
    refs: R1
T3: Afegir smoke-test que executa `python3 build.py --check` dins la suite de proves (exit 0)
    depends_on: (none)
    refs: R2
T4: Confirmar/actualitzar el wire-up d'npm test perquè inclou automàticament els nous tests
    depends_on: T2, T3
    refs: R1, R2
GATES
- `npm test` passa completament (inclous `tests/readme.test.js` i `tests/build_smoke.test.js`)
- `python3 build.py --check` exit 0 independentment (validació del gate directament observable)
- Revisió manual: README.md en català amb títol, intro de la feina del laboratori, secció "com arrencar" amb els tres comandos exactes (`harness/init.sh`, `python3 build.py`, obrir `index.html`), mapa de continguts apuntant a `md/` i al quiz a `proves.html`, i remitent a `AGENTS.md`
- Assegurar que cap canvi funcional s'introduïa fora dels files previstos