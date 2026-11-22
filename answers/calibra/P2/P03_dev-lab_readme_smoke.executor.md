=== FILE: README.md ===
# Camp de Proves

Un entorn d'aprenentatge interactiu per a desenvolupadors, amb preguntes curades, katas i grader local multi-llenguatge.

## Què és?

Camp de Proves ofereix:

- **Preguntes** — tria, output, blank, bug-finding, ordering
- **Katas** — exercicis en Python, JavaScript/TypeScript i Shell
- **Grader local** — correcció automàtica sense dependències externes
- **Mode infinit** — integració amb llama.cpp per a generació contínua

## Com arrencar

### Opcions disponibles

| Mètode | Descripció |
|--------|------------|
| `harness/init.sh` | Inicialitza l'entorn (deps + build) |
| `python3 build.py` | Genera el site estàtic des de `md/` |
| `index.html` | Obre directament al navegador |
| `proves.html` | Interfície de quiz/katas/grader |

### Pas a pas

```bash
# 1. Inicialitzar
./harness/init.sh

# 2. Construir
python3 build.py --check   # valida i genera

# 3. Servir (opcional)
python3 -m http.server 8000
```

Obre `http://localhost:8000/index.html` o `proves.html`.

## Mapa de contingut

- `assets/` — JS/CSS/fonts del client
- `src/` — codi font JavaScript
- `md/` — apunts en Markdown (font d'entrada)
- `p/` — pàgines HTML generades
- `tests/` — tests automatitzats
- `harness/` — infraestructura de validació

## Per a agents

Consulta [`AGENTS.md`](AGENTS.md) per a instruccions específiques sobre com treballar amb aquest repositori.

---

## Tests

Executa la suite completa:

```bash
npm test
```

Això inclou:
- Validació de build (`build.py --check`)
- Tests de qualitat de preguntes
- Verificació de katas
- Comprovacions de traçabilitat

Vegeu [`HARNESS.md`](HARNESS.md) per a més detalls sobre el sistema de verificació.

=== END FILE ===

=== FILE: tests/readme.test.js ===
/* R1: README.md humà a l'arrel */
const fs = require('fs');
const path = require('path');

describe('README.md', () => {
  const readmePath = path.join(__dirname, '..', 'README.md');
  let content;

  beforeAll(() => {
    content = fs.readFileSync(readmePath, 'utf-8');
  });

  it('existeix al repositori', () => {
    expect(fs.existsSync(readmePath)).toBe(true);
  });

  it('és en català', () => {
    // Conté paraules clau en català
    expect(content).toMatch(/(Camp de Proves|aprenentatge|desenvolupadors|preguntes|katas)/i);
  });

  it('explica què és', () => {
    expect(content).toMatch(/(Què és|Descripció|About|What is)/i);
  });

  it('documenta com arrencar amb harness/init.sh', () => {
    expect(content).toMatch(/harness\/init\.sh/);
  });

  it('documenta com arrencar amb python3 build.py', () => {
    expect(content).toMatch(/python3\s+build\.py/);
  });

  it('documenta index.html', () => {
    expect(content).toMatch(/index\.html/);
  });

  it('documenta proves.html', () => {
    expect(content).toMatch(/proves\.html/);
  });

  it('inclou mapa de contingut', () => {
    expect(content).toMatch(/(Mapa de contingut|Contents|Continguts|Directory structure)/i);
  });

  it('redirigeix a AGENTS.md per a agents', () => {
    expect(content).toMatch(/AGENTS\.md/);
  });
});

=== END FILE ===

=== FILE: tests/build_smoke.test.js ===
/* R2: build_smoke — spawneja `python3 build.py --check` dins npm test */
const { execSync } = require('child_process');
const path = require('path');

describe('build smoke test (R2)', () => {
  const rootDir = path.join(__dirname, '..');

  it('build.py --check retorna exit 0', () => {
    // Aquesta prova spawneja python3 build.py --check i assert exit 0
    const result = execSync('python3 build.py --check', {
      cwd: rootDir,
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
    });

    // Si arriba aquí, l'exit code és 0 (execSync llança si no)
    expect(result).toBeDefined();
  });

  it('build.py genera pàgines a p/', () => {
    const pagesDir = path.join(rootDir, 'p');
    const files = fs.readdirSync(pagesDir);
    expect(files.length).toBeGreaterThan(0);
  });
});

=== END FILE ===