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
R1: The repository shall contain a `README.md` at the root, in Catalan, that explains — with a title, an intro of what the lab is, a "com arrencar" section and a content map — how to run it (`harness/init.sh`, `python3 build.py`, obrir `index.html`) and where the study content lives (`md/`, quiz a `proves.html`), with a pointer to `AGENTS.md` for AI agents.

R2: The test suite (`npm test`) shall execute `python3 build.py --check` as a smoke test that fails the suite when the build or a link check fails.  ## Verification notes - R1: testable mecànicament (`tests/readme.test.js` — existència, seccions i literals de comandes). - R2: testable mecànicament (`tests/build_smoke.test.js` — spawneja `python3 build.py --check`, exit 0) i negativament (simulant un fitxer trencat en un sandbox temporal? no: suficient comprovar exit 0 i que el test és part de la suite). - Impacte del smoke-test a les portes: `harness/init.sh` (que ja corre `npm test` i `build.py --check` per separat) passa a validar-lo dues vegades — cost ~1-2 s, assumit.

--- FEATURE TITLE ---
feat(content): readme_smoke — README humà i smoke-test de build dins npm test

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
harness/progress/impl_django_ab.md
harness/progress/impl_ecommerce_integrations.md
harness/progress/impl_infra_cicd.md
harness/progress/impl_js_ts_frontend.md
harness/progress/impl_llm_rag_prod.md
harness/progress/impl_multi_lang_grader.md
harness/progress/impl_postgres_celery.md
harness/progress/impl_python_core.md
harness/progress/impl_reproducible_build.md
harness/progress/impl_shell_scripting.md
harness/progress/impl_tech_taxonomy.md
harness/specs/brand_logo_favicon/APPROVAL
harness/specs/brand_logo_favicon/design.md
harness/specs/brand_logo_favicon/requirements.md
harness/specs/brand_logo_favicon/review.md
harness/specs/brand_logo_favicon/tasks.md
harness/specs/django_ab/APPROVAL
harness/specs/django_ab/design.md
harness/specs/django_ab/requirements.md
harness/specs/django_ab/review.md
harness/specs/django_ab/tasks.md
harness/specs/ecommerce_integrations/APPROVAL
harness/specs/ecommerce_integrations/design.md
harness/specs/ecommerce_integrations/requirements.md
harness/specs/ecommerce_integrations/review.md
harness/specs/ecommerce_integrations/tasks.md
harness/specs/infra_cicd/APPROVAL
harness/specs/infra_cicd/design.md
harness/specs/infra_cicd/requirements.md
harness/specs/infra_cicd/review.md
harness/specs/infra_cicd/tasks.md
harness/specs/js_ts_frontend/APPROVAL
harness/specs/js_ts_frontend/design.md
harness/specs/js_ts_frontend/requirements.md
harness/specs/js_ts_frontend/review.md
harness/specs/js_ts_frontend/tasks.md
harness/specs/llm_rag_prod/APPROVAL
harness/specs/llm_rag_prod/design.md
harness/specs/llm_rag_prod/requirements.md
harness/specs/llm_rag_prod/review.md
harness/specs/llm_rag_prod/tasks.md
harness/specs/multi_lang_grader/APPROVAL
harness/specs/multi_lang_grader/design.md
harness/specs/multi_lang_grader/requirements.md
harness/specs/multi_lang_grader/review.md
harness/specs/multi_lang_grader/tasks.md
harness/specs/postgres_celery/APPROVAL
harness/specs/postgres_celery/design.md
harness/specs/postgres_celery/requirements.md
harness/specs/postgres_celery/review.md
harness/specs/postgres_celery/tasks.md
harness/specs/python_core/APPROVAL
harness/specs/python_core/design.md
harness/specs/python_core/requirements.md
harness/specs/python_core/review.md
harness/specs/python_core/tasks.md
harness/specs/reproducible_build/APPROVAL
harness/specs/reproducible_build/design.md
harness/specs/reproducible_build/requirements.md
harness/specs/reproducible_build/review.md
harness/specs/reproducible_build/tasks.md
harness/specs/shell_scripting/APPROVAL
harness/specs/shell_scripting/design.md
harness/specs/shell_scripting/requirements.md
harness/specs/shell_scripting/review.md
harness/specs/shell_scripting/tasks.md
harness/specs/tech_taxonomy/APPROVAL
harness/specs/tech_taxonomy/design.md
harness/specs/tech_taxonomy/requirements.md
harness/specs/tech_taxonomy/review.md
harness/specs/tech_taxonomy/tasks.md
harness/tools/check-traceability.py
harness/tools/validate-feature-list.py
index.html
index.json
md/ABTesting/ab-test-fonaments.md
md/ABTesting/ab-test-mida-mostral.md
md/Celery/celery-semantica.md
md/Celery/celery-vs-rabbitmq.md
md/Django/django-orm-querysets.md
md/Django/django-vs-fastapi.md
md/ECommerce/ecom-edi-x12.md
md/ECommerce/ecom-integracio-robustesa.md
md/ECommerce/ecom-netsuite-suitetalk.md
md/ECommerce/ecom-sp-api-shopify.md
md/Frontend/front-react-next.md
md/Frontend/front-react-vs-vue.md
md/Frontend/front-ts-tipus.md
md/Frontend/front-vue-basics.md
md/Infra/infra-cicd-gitlab-github.md
md/Infra/infra-docker-imatges.md
md/Infra/infra-k8s-concepts.md
md/Infra/infra-openshift-des-de-k8s.md
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
md/LLM/llm-eval-gate.md
md/LLM/llm-quality-prod.md
md/LLM/llm-rag-vs-finetuning.md
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
md/Postgres/postgres-jsonb-cte.md
md/Postgres/postgres-upsert-indexs.md
md/Postgres/postgres-vs-oracle.md
md/Python/fastapi-dependencies.md
md/Python/fastapi-pydantic.md
md/Python/fastapi-sqlalchemy.md
md/Python/pytest-async.md
md/Python/pytest-fixtures.md
md/Python/pytest-mocks.md
md/Python/python-asyncio.md
md/Python/python-idiomes.md
md/Python/python-typing.md
md/Shell/shell-pipelines.md
md/Shell/shell-scripting.md
md/Shell/shell-text.md
md/Tests/articles-test-010155.md
md/Tests/before-after-2bc738.md
md/Tests/get-test-a5b2a9.md
md/Tests/goldenmaster-93b1f5.md
md/Tests/imports-57a925.md
md/Tests/jacoco-2-402dc9.md
md/Tests/jacoco-9174a7.md
md/Tests/junit-5-021c20.md
md/Tests/parametrized-test-055bd9.md
md/Tests/tdd-7902f6.md
opencode.json
p/ab-test-fonaments.html
p/ab-test-mida-mostral.html
p/advice-4fc9a4.html
p/altres-27a006.html
p/anonim-class-1258db.html
p/archetype-creacio-windows-e8eb55.html
p/arquitectura-5473d6.html
p/articles-test-010155.html
p/before-after-2bc738.html
p/builder-dba2e7.html
p/cache-3f2030.html
p/celery-semantica.html
p/celery-vs-rabbitmq.html
p/commons-build-plugin-readme-805b2e.html
p/controller-38f83a.html
p/crear-projecte-web-8c250a.html
p/django-orm-querysets.html
p/django-vs-fastapi.html
p/ecom-edi-x12.html
p/ecom-integracio-robustesa.html
p/ecom-netsuite-suitetalk.html
p/ecom-sp-api-shopify.html
p/empaquetar-fc3138.html
p/enums-d37b1b.html
p/exception-8729fc.html
p/fastapi-dependencies.html
p/fastapi-pydantic.html
p/fastapi-sqlalchemy.html
p/feing-0c9772.html
p/front-react-next.html
p/front-react-vs-vue.html
p/front-ts-tipus.html
p/front-vue-basics.html
p/functional-interfaces-57b8b7.html
p/get-test-a5b2a9.html
p/goldenmaster-93b1f5.html
p/helper-3fcc58.html
p/import-jar-local-a90e52.html
p/imports-57a925.html
p/infra-cicd-gitlab-github.html
p/infra-docker-imatges.html
p/infra-k8s-concepts.html
p/infra-openshift-des-de-k8s.html
p/int-6af365.html
p/intstreams-f8b7c1.html
p/jacoco-2-402dc9.html
p/jacoco-9174a7.html
p/jedis-d89384.html
p/jpa-3fb91f.html
p/json-47213a.html
p/junit-5-021c20.html
p/lists-b928d6.html
p/llm-eval-gate.html
p/llm-quality-prod.html
p/llm-rag-vs-finetuning.html
p/logs-c5fde1.html
p/lombok-3a0d79.html
p/mongo-query-70171c.html
p/optional-8304e6.html
p/overriding-5856ae.html
p/parametrized-test-055bd9.html
p/patterns-3b80ba.html
p/play-adba21.html
p/postgres-jsonb-cte.html
p/postgres-upsert-indexs.html
p/postgres-vs-oracle.html
p/pytest-async.html
p/pytest-fixtures.html
p/pytest-mocks.html
p/python-asyncio.html
p/python-idiomes.html
p/python-typing.html
p/ram-56964f.html
p/reactor-reactive-759852.html
p/redis-0cddf0.html
p/regex-da9a77.html
p/restcontroller-ce2242.html
p/run-4a142c.html
p/run-without-tests-d4d200.html
p/shell-pipelines.html
p/shell-scripting.html
p/shell-text.html
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
src/questions/extra-ab.json
src/questions/extra-celery.json
src/questions/extra-dades.json
src/questions/extra-django.json
src/questions/extra-ecommerce.json
src/questions/extra-eines.json
src/questions/extra-fastapi.json
src/questions/extra-frontend.json
src/questions/extra-infra.json
src/questions/extra-lenguaje.json
src/questions/extra-llm.json
src/questions/extra-maven.json
src/questions/extra-patrons.json
src/questions/extra-postgres.json
src/questions/extra-pytest.json
src/questions/extra-python.json
src/questions/extra-shell.json
src/questions/extra-spring.json
src/questions/extra-streams.json
src/questions/extra-tests.json
src/style.css
taxonomy.json
tests/brand.test.js
tests/build.test.js
tests/django_ab.test.js
tests/ecommerce.test.js
tests/frontend.test.js
tests/grader-helpers.mjs
tests/grader.test.js
tests/infra_cicd.test.js
tests/katas_python_js.test.js
tests/katas_shell.test.js
tests/katas_ts.test.js
tests/llm_rag_prod.test.js
tests/postgres_celery.test.js
tests/python_core.test.js
tests/questions.test.js
tests/shell_scripting.test.js
tests/taxonomy.test.js
vendor/fonts/fonts-local.css
vendor/highlight.min.js
vendor/marked.min.js

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- assets/data.js (first 0 lines of 180312 bytes) ---

--- assets/questions-extra.js (first 0 lines of 173815 bytes) ---

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

--- index.html (first 58 lines of 29549 bytes) ---
<!doctype html>
<html lang="ca">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>dev-lab · Índex</title>
<link rel="icon" type="image/svg+xml" href="assets/logo.svg">
<link rel="stylesheet" href="assets/fonts.css">
<link rel="stylesheet" href="assets/style.css">
<script>(function(){var t=new URLSearchParams(location.search).get('theme');if(t!=='dark'&&t!=='light'){try{t=localStorage.getItem('jj-theme')}catch(e){}}if(t!=='dark'&&t!=='light'){t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}document.documentElement.dataset.theme=t})()</script>
</head>
<body class="index-page">
<header class="topbar">
  <span class="brand"><img class="brand-mark" src="assets/logo.svg" alt="" width="27" height="27"> dev-<em>lab</em></span>
  <div class="topbar-tools">
    <a class="llama-pill" data-llama-pill href="proves.html" title="Comprovant llama.cpp…"><span class="lp-dot"></span><span class="lp-text">llama.cpp…</span></a>
    <button class="theme-btn" id="theme-btn" aria-label="Canviar tema">◐</button>
  </div>
</header>
<main class="wrap">
  <section class="hero">
    <p class="kicker">Quadern personal · extret de Joplin</p>
    <h1>Notes i drills,<br><span class="accent">multi-tech</span>.</h1>
    <p class="lede">93 apunts destil·lats d'anys de codi: del Java al Python, de Maven a FastAPI. Cerca, llegeix i practica.</p>
    <div class="stats">
      <div><strong>93</strong><span>apunts</span></div>
      <div><strong>20</strong><span>temes</span></div>
      <div><strong>213</strong><span>min de lectura</span></div>
    </div>
    <a class="btn primary hero-cta" href="proves.html">Al camp de proves →</a>
  </section>
  <section class="searchbar">
    <input type="search" id="search" placeholder="Cerca entre els apunts…" autocomplete="off" aria-label="Cerca entre els apunts">
    <kbd>/</kbd>
  </section>
  <p class="search-info" id="search-info" hidden></p>
  <section class="import-zone" id="import-zone">
    <div class="import-head">
      <h2>Importa un markdown</h2>
      <p>Arrossega un <code>.md</code> (o prova'l) i previsualitza'l amb l'estil del site. Si t'agrada, desa'l com a HTML autònom.</p>
    </div>
    <div class="drop" id="drop" tabindex="0" role="button" aria-label="Importar fitxer markdown">
      <input type="file" id="file-input" accept=".md,.markdown,.txt" hidden>
      <p class="drop-main">Deixa anar aquí el teu <strong>.md</strong></p>
      <p class="drop-alt">o fes clic per triar-lo</p>
    </div>
    <div class="imports-list" id="imports-list" hidden>
      <p class="imports-title">Importats en aquest navegador</p>
      <div id="imports-cards"></div>
    </div>
  </section>
  <div id="groups">
<section class="group" id="lenguaje">
  <div class="group-head">
    <h2>Llenguatge i col·leccions</h2>
    <p>Els fonaments: strings, col·leccions, enums i aquells idiomes del llenguatge que sempre s’escapen.</p>
    <span class="group-stats">13 notes · 30 min</span>
  </div>
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
--- build.py (first 60 lines of 23029 bytes) ---
#!/usr/bin/env python3
"""Genera el site estàtic (index + pàgines de nota) des de md/."""
import json, os, re, html, shutil, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(ROOT, 'md')
PAGES = os.path.join(ROOT, 'p')
ASSETS = os.path.join(ROOT, 'assets')
TAXONOMY = os.path.join(ROOT, 'taxonomy.json')
VENDORS = os.path.join(ROOT, 'vendor')
FONTS_SRC = os.path.join(ROOT, 'vendor', 'fonts')

def load_taxonomy():
    """R1-R3: llegeix i valida taxonomy.json; retorna la forma GROUPS."""
    try:
        data = json.load(open(TAXONOMY, encoding='utf-8'))
    except Exception as e:
        sys.exit(f'taxonomy.json invàlid: {e}')
    themes = data.get('themes') if isinstance(data, dict) else None
    if not isinstance(themes, list) or not themes:
        sys.exit('taxonomy.json invàlid: falta la llista "themes"')
    groups, seen = [], set()
    for t in themes:
        if not isinstance(t, dict):
            sys.exit('taxonomy.json invàlid: tema no-objecte')
        missing = [k for k in ('id', 'folder', 'title', 'desc', 'notes') if k not in t]
        if missing:
            sys.exit(f"taxonomy.json invàlid: tema {t.get('id', '?')} sense {', '.join(missing)}")
        if t['id'] in seen:
            sys.exit(f"taxonomy.json invàlid: id duplicat '{t['id']}'")
        if t['notes'] != '*' and (not isinstance(t['notes'], list) or not t['notes']):
            sys.exit(f"taxonomy.json invàlid: '{t['id']}': notes ha de ser \"*\" o una llista no buida")
        seen.add(t['id'])
        groups.append(t)
    return groups


GROUPS = load_taxonomy()

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

Write ONLY the plan (the three sections). No prose outside them.