ROLE: implementation planner. A feature has been approved. You get the
approved requirements and the repository file tree BEFORE implementation.
Write the implementation plan with EXACTLY these three sections:

FILES
<repo-relative path of every file you would create or modify, one per line>

TASKS
T1: <short title>
    depends_on: (none)
    refs: R1, R2
T2: <short title>
    depends_on: T1
    refs: R3
(... ordered so dependencies come first; every requirement must be covered
 by the refs of at least one task)

GATES
<the verification gates you would run before closing the feature>

--- APPROVED REQUIREMENTS ---
R1: The repository shall contain every vendor input the build requires (`vendor/marked.min.js`, `vendor/highlight.min.js`, `vendor/fonts/fonts-local.css`, and the `vendor/fonts/*.woff2` files), and `build.py` shall source vendors and fonts from these in-repo paths instead of `/tmp/opencode/*`.

R2: When a required vendor input is missing or empty, the build shall exit with a non-zero status and a clean error message naming the missing path (no Python traceback).

R3: When a note cannot be assigned to any group, the build shall exit with a non-zero status reporting the unassigned slugs.

R4: When an extra question fails schema validation, the build shall exit with a non-zero status reporting each rejected question.

R5: The generated site shall not embed the build date; two consecutive builds on different days shall produce byte-identical outputs.

R6: `build.py --check` shall run every content validation (group assignment, question validation, link check) without writing any output file, and shall exit non-zero on any validation error.  ## Verification notes - R1: fitxers vendor presents + `build.py` referencia els nous paths (test mecànic). - R2/R3/R4/R6: tests end-to-end en sandbox (còpia temporal del repo amb fixture   corrupta → assert exit != 0 i missatge esperat); cap mutació del repo real. - R5: doble build a la sandbox amb hash sha256 idèntic + footer de l'`index.html`   comès sense data. - Porta de la feature: `python3 build.py --check` (ara validació completa) +   `npm test`.

--- FEATURE TITLE ---
feat(build): build reproduïble amb vendors al repo i validacions dures

--- REPOSITORY FILE TREE (before implementation) ---
.opencode/agent/implementer.md
.opencode/agent/leader.md
.opencode/agent/reviewer.md
.opencode/agent/spec-author.md
AGENTS.md
HARNESS.md
assets/data.js
assets/export-css.js
assets/fonts.css
assets/highlight.min.js
assets/index.js
assets/katas.js
assets/llama.js
assets/marked.min.js
assets/note.js
assets/proves.js
assets/questions-extra.js
assets/questions.js
assets/style.css
build.py
docs/architecture.md
docs/conventions.md
docs/specs.md
docs/verification.md
grader/grader.py
harness/CHECKPOINTS.md
harness/feature_list.json
harness/init.sh
harness/progress/current.md
harness/progress/history.md
harness/progress/impl_brand_logo_favicon.md
harness/specs/brand_logo_favicon/APPROVAL
harness/specs/brand_logo_favicon/design.md
harness/specs/brand_logo_favicon/requirements.md
harness/specs/brand_logo_favicon/review.md
harness/specs/brand_logo_favicon/tasks.md
harness/tools/check-traceability.py
harness/tools/validate-feature-list.py
index.html
index.json
md/Java/advice-4fc9a4.md
md/Java/anonim-class-1258db.md
md/Java/cache-3f2030.md
md/Java/commons-build-plugin-readme-805b2e.md
md/Java/controller-38f83a.md
md/Java/enums-d37b1b.md
md/Java/exception-8729fc.md
md/Java/feing-0c9772.md
md/Java/functional-interfaces-57b8b7.md
md/Java/int-6af365.md
md/Java/intstreams-f8b7c1.md
md/Java/jedis-d89384.md
md/Java/jpa-3fb91f.md
md/Java/json-47213a.md
md/Java/lists-b928d6.md
md/Java/logs-c5fde1.md
md/Java/lombok-3a0d79.md
md/Java/mongo-query-70171c.md
md/Java/optional-8304e6.md
md/Java/overriding-5856ae.md
md/Java/play-adba21.md
md/Java/ram-56964f.md
md/Java/reactor-reactive-759852.md
md/Java/redis-0cddf0.md
md/Java/regex-da9a77.md
md/Java/restcontroller-ce2242.md
md/Java/snippets-34a9ba.md
md/Java/streams-71e2f7.md
md/Java/string-2f64ba.md
md/Java/swagger-025f5b.md
md/Java/swagger-editor-81748c.md
md/Java/tuples-f0d7b6.md
md/Java/utils-e163d3.md
md/Java/validation-4ffd20.md
md/Java/zip-633316.md
md/Junit/goldenmaster-93b1f5.md
md/Maven/altres-27a006.md
md/Maven/archetype-creacio-windows-e8eb55.md
md/Maven/crear-projecte-web-8c250a.md
md/Maven/empaquetar-fc3138.md
md/Maven/import-jar-local-a90e52.md
md/Maven/run-4a142c.md
md/Maven/run-without-tests-d4d200.md
md/Maven/zsh-65c15d.md
md/Patrons/arquitectura-5473d6.md
md/Patrons/builder-dba2e7.md
md/Patrons/helper-3fcc58.md
md/Patrons/patterns-3b80ba.md
md/Tests/articles-test-010155.md
md/Tests/before-after-2bc738.md
md/Tests/get-test-a5b2a9.md
md/Tests/imports-57a925.md
md/Tests/jacoco-2-402dc9.md
md/Tests/jacoco-9174a7.md
md/Tests/junit-5-021c20.md
md/Tests/parametrized-test-055bd9.md
md/Tests/tdd-7902f6.md
opencode.json
p/advice-4fc9a4.html
p/altres-27a006.html
p/anonim-class-1258db.html
p/archetype-creacio-windows-e8eb55.html
p/arquitectura-5473d6.html
p/articles-test-010155.html
p/before-after-2bc738.html
p/builder-dba2e7.html
p/cache-3f2030.html
p/commons-build-plugin-readme-805b2e.html
p/controller-38f83a.html
p/crear-projecte-web-8c250a.html
p/empaquetar-fc3138.html
p/enums-d37b1b.html
p/exception-8729fc.html
p/feing-0c9772.html
p/functional-interfaces-57b8b7.html
p/get-test-a5b2a9.html
p/goldenmaster-93b1f5.html
p/helper-3fcc58.html
p/import-jar-local-a90e52.html
p/imports-57a925.html
p/int-6af365.html
p/intstreams-f8b7c1.html
p/jacoco-2-402dc9.html
p/jacoco-9174a7.html
p/jedis-d89384.html
p/jpa-3fb91f.html
p/json-47213a.html
p/junit-5-021c20.html
p/lists-b928d6.html
p/logs-c5fde1.html
p/lombok-3a0d79.html
p/mongo-query-70171c.html
p/optional-8304e6.html
p/overriding-5856ae.html
p/parametrized-test-055bd9.html
p/patterns-3b80ba.html
p/play-adba21.html
p/ram-56964f.html
p/reactor-reactive-759852.html
p/redis-0cddf0.html
p/regex-da9a77.html
p/restcontroller-ce2242.html
p/run-4a142c.html
p/run-without-tests-d4d200.html
p/snippets-34a9ba.html
p/streams-71e2f7.html
p/string-2f64ba.html
p/swagger-025f5b.html
p/swagger-editor-81748c.html
p/tdd-7902f6.html
p/tuples-f0d7b6.html
p/utils-e163d3.html
p/validation-4ffd20.html
p/zip-633316.html
p/zsh-65c15d.html
package.json
proves.html
src/index.js
src/katas.js
src/llama.js
src/note.js
src/proves.js
src/questions.js
src/questions/extra-dades.json
src/questions/extra-eines.json
src/questions/extra-lenguaje.json
src/questions/extra-maven.json
src/questions/extra-patrons.json
src/questions/extra-spring.json
src/questions/extra-streams.json
src/questions/extra-tests.json
src/style.css
tests/brand.test.js
tests/questions.test.js

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- assets/data.js (first 0 lines of 92911 bytes) ---

--- assets/questions-extra.js (first 0 lines of 86563 bytes) ---

--- assets/questions.js (first 56 lines of 31643 bytes) ---
/* Banc de preguntes del Camp de Proves — curat des dels apunts.
   Tipus: choice (tria), output (què imprimeix), blank (omple), bug (troba la línia), order (ordena) */
window.QUESTIONS = [

/* ── LLLENGUATGE ─────────────────────────────────────────────── */
{t:'lenguaje', ty:'output', q:'Què imprimeix aquest codi?',
code:`enum Desti { SNOWFLAKE, CASSANDRA }

System.out.println(Desti.valueOf("snowflake"));`,
opts:['SNOWFLAKE','null','IllegalArgumentException','No compila'],
a:2, x:'valueOf és case-sensitive i sense trim: qualsevol string que no quadri exactament llança IllegalArgumentException. Per parsejar tolerant, lookup en Map estàtic.', ref:'enums-d37b1b'},

{t:'lenguaje', ty:'choice', q:'List.of(1, 2, 3).add(4) — què passa?',
opts:['Afegeix el 4 al final','NullPointerException','UnsupportedOperationException','Compila però no fa res'],
a:2, x:'List.of crea llistes IMMUTABLES: les operacions de mutació llancen UnsupportedOperationException. Si necessites mutar, new ArrayList<>(List.of(...)).', ref:'lists-b928d6'},

{t:'lenguaje', ty:'blank', q:'Omple el buit: vols que carregar() NOMÉS s\'executi si l\'Optional és buit (és carregada).\nOptional.ofNullable(x).____(this::carregar);',
a:'orElseGet', x:'orElseGet rep un Supplier i només l\'avalua si és buit. orElse(carregar()) executa el mètode SEMPRE, hi hagi valor o no: cara cara si toca BD.', ref:'optional-8304e6'},

{t:'lenguaje', ty:'output', q:'Què imprimeix?',
code:`Integer a = 127, b = 127;
Integer c = 128, d = 128;
System.out.println((a == b) + " " + (c == d));`,
opts:['true true','true false','false false','false true'],
a:1, x:'El cache d\'Integer només cobreix -128..127: dins, == compara el mateix objecte; fora, crea instàncies noves. Per això equals (o unbox) sempre, mai == amb Wrappers.', ref:'snippets-34a9ba'},

{t:'lenguaje', ty:'bug', q:'On està el problema de rendiment?',
code:`1  for (String linia : linies) {
2      Pattern p = Pattern.compile("^\\d+");
3      if (p.matcher(linia).find()) comptador++;
4  }`,
opts:['Línia 1','Línia 2','Línia 3','Línia 4'],
a:1, x:'Pattern.compile és car: recompilar el regex a cada iteració és malbaratament. El puja a un static final Pattern — els Pattern són thread-safe.', ref:'regex-da9a77'},

{t:'lenguaje', ty:'choice', q:'Dos records amb exactament els mateixos components...',
opts:['equals és true i hashCode igual','equals és true però hashCode diferent','equals és false: cada instància és única','No tenen equals: cal escriure\'l'],
a:0, x:'Els records generen equals/hashCode/toString a partir dels components: mateixos valors → mateixa igualtat. Un dels seus grans guanys.', ref:'overriding-5856ae'},

{t:'lenguaje', ty:'blank', q:'Omple el buit: la factoria del JDK que crea una entrada de Map immutable sense crear el Map.\nMap.____("clau", "valor");',
a:'entry', x:'Map.entry(k, v) (JDK 9+) et dóna el parell puntual immutable: ideal per a llistes de parells sense inventar-se una classe Tuple.', ref:'tuples-f0d7b6'},

{t:'lenguaje', ty:'output', q:'Què imprimeix?',
code:`String s = """
    hola
    """;
System.out.println(s.length());`,
opts:['9','8','5','4'],
a:2, x:'El text block poda la indentació incidental pels """ de tancament: queda "hola\\n" → 5 caràcters. Els salts i espais finals els marca la posició del delimitador.', ref:'string-2f64ba'},

{t:'lenguaje', ty:'choice', q:'Què passa aquí?',
code:`int base = 10;
Runnable r = () -> System.out.println(base);
base = 20;`,
opts:['Compila i imprimeix 10','Compila i imprimeix 20','No compila: base es reassigna després d\'usar-la a la lambda','NullPointerException'],
a:2, x:'Les lambdes i classes anònimes només capturen variables effectively final. Reassignar base la treu del club i el compilador ho xiscla.', ref:'anonim-class-1258db'},

--- src/questions.js (first 56 lines of 31643 bytes) ---
/* Banc de preguntes del Camp de Proves — curat des dels apunts.
   Tipus: choice (tria), output (què imprimeix), blank (omple), bug (troba la línia), order (ordena) */
window.QUESTIONS = [

/* ── LLLENGUATGE ─────────────────────────────────────────────── */
{t:'lenguaje', ty:'output', q:'Què imprimeix aquest codi?',
code:`enum Desti { SNOWFLAKE, CASSANDRA }

System.out.println(Desti.valueOf("snowflake"));`,
opts:['SNOWFLAKE','null','IllegalArgumentException','No compila'],
a:2, x:'valueOf és case-sensitive i sense trim: qualsevol string que no quadri exactament llança IllegalArgumentException. Per parsejar tolerant, lookup en Map estàtic.', ref:'enums-d37b1b'},

{t:'lenguaje', ty:'choice', q:'List.of(1, 2, 3).add(4) — què passa?',
opts:['Afegeix el 4 al final','NullPointerException','UnsupportedOperationException','Compila però no fa res'],
a:2, x:'List.of crea llistes IMMUTABLES: les operacions de mutació llancen UnsupportedOperationException. Si necessites mutar, new ArrayList<>(List.of(...)).', ref:'lists-b928d6'},

{t:'lenguaje', ty:'blank', q:'Omple el buit: vols que carregar() NOMÉS s\'executi si l\'Optional és buit (és carregada).\nOptional.ofNullable(x).____(this::carregar);',
a:'orElseGet', x:'orElseGet rep un Supplier i només l\'avalua si és buit. orElse(carregar()) executa el mètode SEMPRE, hi hagi valor o no: cara cara si toca BD.', ref:'optional-8304e6'},

{t:'lenguaje', ty:'output', q:'Què imprimeix?',
code:`Integer a = 127, b = 127;
Integer c = 128, d = 128;
System.out.println((a == b) + " " + (c == d));`,
opts:['true true','true false','false false','false true'],
a:1, x:'El cache d\'Integer només cobreix -128..127: dins, == compara el mateix objecte; fora, crea instàncies noves. Per això equals (o unbox) sempre, mai == amb Wrappers.', ref:'snippets-34a9ba'},

{t:'lenguaje', ty:'bug', q:'On està el problema de rendiment?',
code:`1  for (String linia : linies) {
2      Pattern p = Pattern.compile("^\\d+");
3      if (p.matcher(linia).find()) comptador++;
4  }`,
opts:['Línia 1','Línia 2','Línia 3','Línia 4'],
a:1, x:'Pattern.compile és car: recompilar el regex a cada iteració és malbaratament. El puja a un static final Pattern — els Pattern són thread-safe.', ref:'regex-da9a77'},

{t:'lenguaje', ty:'choice', q:'Dos records amb exactament els mateixos components...',
opts:['equals és true i hashCode igual','equals és true però hashCode diferent','equals és false: cada instància és única','No tenen equals: cal escriure\'l'],
a:0, x:'Els records generen equals/hashCode/toString a partir dels components: mateixos valors → mateixa igualtat. Un dels seus grans guanys.', ref:'overriding-5856ae'},

{t:'lenguaje', ty:'blank', q:'Omple el buit: la factoria del JDK que crea una entrada de Map immutable sense crear el Map.\nMap.____("clau", "valor");',
a:'entry', x:'Map.entry(k, v) (JDK 9+) et dóna el parell puntual immutable: ideal per a llistes de parells sense inventar-se una classe Tuple.', ref:'tuples-f0d7b6'},

{t:'lenguaje', ty:'output', q:'Què imprimeix?',
code:`String s = """
    hola
    """;
System.out.println(s.length());`,
opts:['9','8','5','4'],
a:2, x:'El text block poda la indentació incidental pels """ de tancament: queda "hola\\n" → 5 caràcters. Els salts i espais finals els marca la posició del delimitador.', ref:'string-2f64ba'},

{t:'lenguaje', ty:'choice', q:'Què passa aquí?',
code:`int base = 10;
Runnable r = () -> System.out.println(base);
base = 20;`,
opts:['Compila i imprimeix 10','Compila i imprimeix 20','No compila: base es reassigna després d\'usar-la a la lambda','NullPointerException'],
a:2, x:'Les lambdes i classes anònimes només capturen variables effectively final. Reassignar base la treu del club i el compilador ho xiscla.', ref:'anonim-class-1258db'},

--- assets/export-css.js (first 0 lines of 25858 bytes) ---

--- assets/style.css (first 60 lines of 23531 bytes) ---
/* ── Apunts Java · paper, tinta i coure ─────────────────────────── */
:root {
  --bg: #faf6ef;
  --surface: #fffdf8;
  --ink: #241d15;
  --muted: #7a6f60;
  --accent: #b4531f;
  --accent-ink: #8f3d12;
  --accent-soft: rgba(180, 83, 31, .09);
  --line: #e8dfcf;
  --code-bg: #f3ecdf;
  --shadow: 0 2px 10px rgba(60, 42, 20, .06);
  --shadow-lift: 0 10px 28px rgba(60, 42, 20, .13);
}
[data-theme="dark"] {
  --bg: #17130e;
  --surface: #211b14;
  --ink: #ede4d3;
  --muted: #a2957f;
  --accent: #e08a4c;
  --accent-ink: #eda868;
  --accent-soft: rgba(224, 138, 76, .12);
  --line: #372e22;
  --code-bg: #2a2318;
  --shadow: 0 2px 10px rgba(0, 0, 0, .35);
  --shadow-lift: 0 12px 30px rgba(0, 0, 0, .5);
}

[data-theme="dark"] .btn.primary { color: #1d160f; }
[data-theme="dark"] ::selection { color: #17130e; }

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font: 16px/1.65 "Inter", system-ui, sans-serif;
  transition: background .3s ease, color .3s ease;
}
::selection { background: var(--accent); color: #fff; }

h1, h2, h3 { font-family: "Fraunces", Georgia, serif; font-weight: 600; letter-spacing: -.01em; }
a { color: var(--accent-ink); text-decoration: none; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 4px; }

/* ── barra superior ── */
.topbar {
  position: sticky; top: 0; z-index: 20;
  display: flex; justify-content: space-between; align-items: center;
  padding: .8rem clamp(1rem, 4vw, 2.5rem);
  background: color-mix(in srgb, var(--bg) 82%, transparent);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--line);
}
.brand { font-family: "Fraunces", serif; font-size: 1.05rem; font-weight: 700; color: var(--ink); }
.brand em { color: var(--accent); font-style: italic; }
.brand-mark {
  display: inline-block;
  width: 1.7rem; height: 1.7rem; margin-right: .5rem;
--- src/style.css (first 60 lines of 22095 bytes) ---
/* ── Apunts Java · paper, tinta i coure ─────────────────────────── */
:root {
  --bg: #faf6ef;
  --surface: #fffdf8;
  --ink: #241d15;
  --muted: #7a6f60;
  --accent: #b4531f;
  --accent-ink: #8f3d12;
  --accent-soft: rgba(180, 83, 31, .09);
  --line: #e8dfcf;
  --code-bg: #f3ecdf;
  --shadow: 0 2px 10px rgba(60, 42, 20, .06);
  --shadow-lift: 0 10px 28px rgba(60, 42, 20, .13);
}
[data-theme="dark"] {
  --bg: #17130e;
  --surface: #211b14;
  --ink: #ede4d3;
  --muted: #a2957f;
  --accent: #e08a4c;
  --accent-ink: #eda868;
  --accent-soft: rgba(224, 138, 76, .12);
  --line: #372e22;
  --code-bg: #2a2318;
  --shadow: 0 2px 10px rgba(0, 0, 0, .35);
  --shadow-lift: 0 12px 30px rgba(0, 0, 0, .5);
}

[data-theme="dark"] .btn.primary { color: #1d160f; }
[data-theme="dark"] ::selection { color: #17130e; }

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font: 16px/1.65 "Inter", system-ui, sans-serif;
  transition: background .3s ease, color .3s ease;
}
::selection { background: var(--accent); color: #fff; }

h1, h2, h3 { font-family: "Fraunces", Georgia, serif; font-weight: 600; letter-spacing: -.01em; }
a { color: var(--accent-ink); text-decoration: none; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 4px; }

/* ── barra superior ── */
.topbar {
  position: sticky; top: 0; z-index: 20;
  display: flex; justify-content: space-between; align-items: center;
  padding: .8rem clamp(1rem, 4vw, 2.5rem);
  background: color-mix(in srgb, var(--bg) 82%, transparent);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--line);
}
.brand { font-family: "Fraunces", serif; font-size: 1.05rem; font-weight: 700; color: var(--ink); }
.brand em { color: var(--accent); font-style: italic; }
.brand-mark {
  display: inline-block;
  width: 1.7rem; height: 1.7rem; margin-right: .5rem;
--- build.py (first 60 lines of 21943 bytes) ---
#!/usr/bin/env python3
"""Genera el site estàtic (index + pàgines de nota) des de md/."""
import json, os, re, html, shutil, datetime, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(ROOT, 'md')
PAGES = os.path.join(ROOT, 'p')
ASSETS = os.path.join(ROOT, 'assets')
VENDORS = '/tmp/opencode/vendors'
FONTS_SRC = '/tmp/opencode/fonts'

GROUPS = [
    {'id': 'lenguaje', 'folder': 'Java', 'title': 'Llenguatge i col·leccions',
     'desc': 'Els fonaments: strings, col·leccions, enums i aquells idiomes del llenguatge que sempre s’escapen.',
     'notes': ['anonim-class', 'enums', 'optional', 'overriding', 'string', 'lists', 'int', 'regex', 'tuples', 'zip', 'utils', 'snippets', 'ram']},
    {'id': 'streams', 'folder': 'Java', 'title': 'Streams i programació funcional',
     'desc': 'Pipelines declaratius amb Streams i la visió reactiva de Reactor quan els bucles clàssics no arriben.',
     'notes': ['streams', 'intstreams', 'functional-interfaces', 'reactor-reactive']},
    {'id': 'spring', 'folder': 'Java', 'title': 'Spring i APIs REST',
     'desc': 'Controladors, validació, gestió d’errors i documentació: el cicle complet d’una API que es respecta.',
     'notes': ['advice', 'controller', 'restcontroller', 'exception', 'validation', 'feing', 'logs', 'cache']},
    {'id': 'dades', 'folder': 'Java', 'title': 'Persistència i dades',
     'desc': 'De JPA a Redis: on viuen les teves dades i com parlar-hi sense sofrir-ho.',
     'notes': ['jpa', 'mongo-query', 'redis', 'jedis', 'json']},
    {'id': 'eines', 'folder': 'Java', 'title': 'Eines i frameworks',
     'desc': 'Lombok, Swagger, Play: l’arsenal que et treballa a tu la feina bruta.',
     'notes': ['lombok', 'play', 'swagger', 'swagger-editor', 'commons-build-plugin-readme']},
    {'id': 'maven', 'folder': 'Maven', 'title': 'Maven',
     'desc': 'Cicles de vida, arquetips i empaquetat sense sorpreses.',
     'notes': '*'},
    {'id': 'tests', 'folder': 'Tests', 'title': 'Tests i qualitat',
     'desc': 'TDD, JaCoCo i JUnit 5: perquè el codi sense proves només és una hipòtesi.',
     'notes': '*'},
    {'id': 'patrons', 'folder': 'Patrons', 'title': 'Patrons de disseny',
     'desc': 'Builder i helpers: solucions que algú ja va patir per tu.',
     'notes': '*'},
]

THEME_SCRIPT = ("<script>(function(){var t=new URLSearchParams(location.search).get('theme');"
                "if(t!=='dark'&&t!=='light'){try{t=localStorage.getItem('jj-theme')}catch(e){}}"
                "if(t!=='dark'&&t!=='light'){t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}"
                "document.documentElement.dataset.theme=t})()</script>")

def parse_md(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n?(.*)$', text, re.S)
    meta, body = {}, text
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip()
        body = m.group(2)
    return meta, body

def strip_md(body):
    t = re.sub(r'```.*?```', ' ', body, flags=re.S)
    t = re.sub(r'!\[.*?\]\(.*?\)', ' ', t)
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
    t = re.sub(r'[#*`>_~\-|]+', ' ', t)

Write ONLY the plan (the three sections). No prose outside them.