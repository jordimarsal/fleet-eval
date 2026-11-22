FILES
README.md
tests/readme.test.js
tests/build_smoke.test.js
package.json

TASKS
T1: Crear README.md en català al root
    depends_on: (none)
    refs: R1
T2: Afegir el smoke-test de build dins la suite npm test
    depends_on: T1
    refs: R2
T3: Verificar que la suite queda verda i tancar
    depends_on: T2
    refs: R1, R2

GATES
- `npm test` termina exit 0 amb els dos nous tests inclosos
- `python3 build.py --check` exit 0 directament
- `node --test tests/readme.test.js` verifica existència/seccions/literals de comandos del README (com arrencar, md/, proves.html, AGENTS.md)
- `node --test tests/build_smoke.test.js` spawneja `python3 build.py --check` i passa només si exit 0
- Revisar git diff per assegurar cap altre fitxer tocat no previst