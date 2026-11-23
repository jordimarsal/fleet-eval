# Notes per a article — "Avaluació de LLM locals per rols agènics: pla, execució, ressenya"

> Dossier de treball (2026-11-23). Tot el que hi ha aquí és reproduïble des
> d'aquest repo: corpus, scripts, respostes i grading mecànic. Públic el que
> marca `public`; el material de repos privats (viatgecio, jordimp-sb) viu
> gitignorat i les seves dades NO surten aquí.

## El pitch en un paràgraf

Vam voler saber si una flota de 10 LLM locals (2×RTX 5080, llama.cpp + Strata)
pot rebre **rols diferents per mèrit mesurat** — planner, implementer,
reviewer — en lloc d'un "model diari" per a tot. Vam construir tres instruments
de mesura amb grading mecànic (sense jutges LLM): una bateria de planner
mesurat per l'**efecte** del pla (P2b), i una bateria de reviewer amb **defectes
reals** collits del propi historial git (C2). Resultat: dos dels tres senyals
van morir amb honors — i el procés de matar-los és el material de l'article.

## Cronologia de la campanya

| Data | Què |
|---|---|
| 2026-11-15 | Bateria de dispatch (A-E): 5 tasques × 8 models, grading mecànic. gemma4 millor implementador (10/10+10/10); Strata referència revisant (C 0.86) |
| 2026-11-22 | Bateria P (planner vs specs reals, ratio 1.95) → P2 one-shot (no discrimina: l'executor compensava qualsevol pla) → **P2b incremental** dirigit pel pla |
| 2026-11-23 | P2b reduïda (n=8): humà vs Huihui vs qwen4b → senyal de planner PLA → porta NO. C2: collita de commits `fix` reals → n=9 → ampliació a n=33 → verdict |

## Instruments (tots al repo)

- **P2b** (`run_P2b.py`): el pla es mesura pel seu efecte. L'executor queda
  constret: implementa només el pas T_k amb pressupost repartit (48000/n_steps,
  cap 12000). Nota = tests verds finals / baseline real. Corba de progrés per pas.
- **C2** (`harvest_C2.py` → `curate_C2.py` → `build_C2.py` → `run_C2.py` →
  `grade_C2.py`): defectes reals = estat PRE de commits `fix` de l'estol.
  Collita: 170 fix-commits de 23 repos → 381 candidats → 33 defectes curats
  (25 públics + 8 privats gitignorats). Patrons de grading derivats del
  **vocabulari del remei** (tokens afegits pel fix absents del pre-state):
  el model no pot veure'ls.
- **Grading**: regex sobre la resposta (mateixa mecànica que la bateria C v1),
  recall per defecte + FP estimats (ítems reportats − encerts). Sense jutges.

## Resultats clau

### 1. Planner (P2b, n=8 tasques, executor qwen38 fix)

| Planner | Score mig | Monotonia | Δ vs humà |
|---|---|---|---|
| humà | 0.198 | 6/8 | — |
| Huihui | 0.204 | 8/8 | 0 victòries d'humà, Δ −0.006 |
| qwen4b | 0.098 | 7/8 | 1 victòria (P01, +0.80) |

**Veredicte**: la porta de decissió (humà guanya ≥60% tasques i Δmig ≥ +0.05)
falla per als dos → **routing de planner enterrat**. P1 v2 (ratio 1.95) queda
com a diagnòstic, no com a senyal de routing.

Matisos que l'article ha de contar:
- L'instrument SÍ discrimina quan l'executor arriba: P01 → humà 0.80, Huihui
  0.85, qwen4b 0.00 amb el mateix executor. El problema és el rang del corpus:
  5 de 8 tasques són inassolibles amb qualsevol pla (zeros idèntics en one-shot).
- El mode incremental allibera l'executor: P01 one-shot 0.00 → incremental 0.80
  amb el mateix pla humà.
- Artefacte detectat: budget/pas = 48000/n_steps penalitza mecànicament els
  plans fins (part del ρ(pasos, score) negatiu és això, no qualitat del pla).
- L'humà és l'únic planner no monòton: els seus corbes baixen i es recuperen
  (iteració real); els models fan camins estrets que no trenquen res... i no
  arriben enlloc nou.

### 2. Reviewer (C2, n=33 defectes reals, 10 models)

| Model | n=9 | **n=33** | FP total |
|---|---|---|---|
| inkling2 | 0.33 | **0.33** (11/33) | 170 |
| Strata (ref.) | 0.33 | 0.27 (9/33) | 164 |
| minicpm | **0.56** | 0.27 (9/33) | 144 |
| Huihui / SC117 / inkling2unc | — | 0.24 (8/33) | 104-156 |
| qwen38 | 0.22 | 0.21 (7/33) | 91 |
| gemma4 | 0.11 | 0.18 (6/33) | 136 |
| qwen36 | 0.00 | 0.18 (6/33) | 239 |
| qwen4b | 0.00 | 0.12 (4/33) | 206 |

**Veredicte**: McNemar aparellat sobre el mateix corpus — **cap parell
significatiu** (p mínima 0.18, inkling2 vs gemma4). La banda 0.12-0.33 comprèn
tota la flota. Routing de reviewer per model indefensable amb aquestes dades.

### 3. El winner's curse, demostrat en viu

minicpm va guanyar la primera onada (n=9) amb 0.56. Amb corpus nou (n=33) va
caure al 0.27 — regressió a la mitjana per selecció del màxim amb mostra petita.
És el perill estàndard dels leaderboards per defectes: **el guanyador d'una
bateria petita sol ser el de la mostra més afortidora, no el millor model**.

### 4. Sintètic vs real (el gap de benchmark)

El mateix Strata que fa 0.86 al dif sintètic de la bateria C v1 fa 0.27 amb
defectes reals collits del git. Els benchmarks sintètics de revisió sobreestimen
massa — el tamís és el tipus de defecte: els reals requereixen llegir codi de
producció amb context incomplet, no reconèixer 7 anti-patrons clàssics.

### 5. Els rols no es transfereixen

gemma4: 1r d'implementació (10/10+10/10 al dispatch) → 9è de 10 ressenyant
(0.18). La idea de best-of-breed **per rol** continua sent teòricament bona i
empíricament morta amb aquesta flota: no hi ha cap rol (planner, reviewer) on
un model local domini de manera estadísticament defensable.

## Limitacions a declarar (honestes)

- Grading per regex: el recall és un **límit inferior** (paràfrasis vàlides que
  no toquen el patró compten com a miss). Els patrons els va derivar el remei,
  no un humà lector.
- 33 defectes: Wilson CI ±17pp a p=0.5. Per significar un gap de 3-5 defectes
  aparellats caldrien ~200-300 defectes — fora de l'abast del corpus propi
  (~150 candidats revisables a l'estol sencer).
- 1 sola corrida per (model, defecte); sense repeats k>1.
- Els patrons/geniva de la curació van passar per filtre humà (16 descarts:
  renoms mypy, cosètica sonar, copies, 1 duplicat).
- inkling2unc: inestable en servei (2 crashes de servidor documentats, un
  reproduïble amb el prompt C2-15; el registre queda als answers).
- Corpus esbiaixat al codi propi (portfolio + works): els estils de defecte
  són els meus, no els del mercat.

## Material per escriure (on viu cada cosa)

- Taula final + FP: `grade_C2_summary.json` (regenerable amb `python3 grade_C2.py`)
- Matriu completa per defecte: sortida de `grade_C2.py` (cel·la ok/n + ítems)
- McNemar: aparellat sobre `answers/<slug>/C2/*.json` (script al log de sessió;
  p valors al resum de resultats)
- Corbes de progrés P2b: camps `progress` dins `answers/calibra_qwen38/P2b/*.json`
- Defectes públics + patrons: `corpus/C2/defects.json`; candidats: `candidates.json`
- Els 9 prompts v1 i els 33 finals: `prompts/C2/`
- Crash log inkling2unc: `logs/C2.inkling2unc.server.log` (stack a server_queue)
- Commits de referència: `1afca01..9b7dc74` (P2b), `c75da30` (infra C2),
  `412ac43` (corpus n=33), `5a1551b` (resultats n=9), `775120f` (resultats n=33)

## Angles possibles (per decidir)

- **A — El null honest**: "Vam voler enrutar LLM locals per rol i el mesurament
  va matar la idea dues vegades". Estructura: hipòtesi → instruments → verdict
  → lliçons de mesurament. El més fàcil de defensar; el més valuós per a
  enginyers que fan routing amb bateries petites.
- **B — El winner's curse en evals de LLM**: minicpm com a cas d'estudi en viu
  (0.56 → 0.27). Curt, didàctic, aplicable a qualsevol leaderboard de defectes.
- **C — Sintètic vs real en revisió de codi**: el gap 0.86 → 0.27 del mateix
  model. Requereix explicar bé la construcció del corpus (la part més rica:
  collita de commits fix, remei com a clau de grading).

## ANGLE ESCOLLIT: B — winner's curse (decisio 2026-11-23)

### Les xifres nuclears (verificades)

| Fet | Valor |
|---|---|
| minicpm, primera onada (n=9) | **5/9 = 0.556** — "el millor ressenyador de la flota" |
| minicpm, corpus nou (24 defectes, mateix grading) | **4/24 = 0.167** |
| minicpm total (n=33) | 9/33 = 0.27 — mig taulell |
| Simulació: 10 models idèntics (p=0.27), n=9 | **E[max] = 0.51** — l'observat (0.56) ÉS el màxim esperat d'una flota igualada |
| Idem | **P(que algun model "lideri" amb ≥5/9) = 50%** |
| Idem | **P(que algun model faci 0/9) = 45%** — els dos zeros observats (qwen36, qwen4b) també |
| McNemar aparellat, n=33 | cap parell significatiu (p mín 0.18) |

Script reproduïble: `docs/winner_curse_sim.py` (sortida verificada).

### Esquelet de l'article (≈1500-1800 paraules)

1. **Hook**: "La setmana passada la nostra bateria va coronar un guanyador.
   Aquesta setmana, el mateix grading amb més defectes l'ha executat."
   minicpm 0.56 → 0.167 en material nou.
2. **Context en 5 línies**: flota local de 10 LLM (2×RTX 5080); volíem routing
   per rol; calia saber qui era el millor ressenyador.
3. **La bateria** (breu): 9 defectes reals collits del propi git (estat PRE de
   commits fix), grading mecànic pel remei. Taules de la primera onada.
4. **La temptació**: declara minicpm guanyador, enruta-hi les ressenyes. És el
   que fan els leaderboards cada dia.
5. **Per què vam dubtar**: Wilson CI ±32pp a n=9; escollir el màxim de 10 models
   = escollir la sort.
6. **La simulació** (la peça central): taula E[max]/P(max≥5/9)/P(min=0). La
   forma del rànquing observat és la d'una flota igualada.
7. **La comprovació empírica**: ampliació a n=33 (mateix grading, corpus nou,
   23 repos). Col·lapse a la banda 0.12-0.33; McNemar pla. El tall fi:
   0.556 → 0.167 en material fresc.
8. **Lliçons** (la part portable):
   - El guanyador d'una bateria petita mesura la seva sort, no la seva qualitat.
   - Amplia ABANS de coronar; si no pots ampliar, no coronis: assigna esglaons.
   - Test aparellat sobre corpus idèntic, mai comparació de punts solts.
   - Publica el null: ens va costar una jornada, estalvia'n milers.
9. **Què fem ara**: sense guanyador → esglaons (Strata com a referència,
   banda alta intercanviable) i routing només on hi ha senyal (implementer).
10. **Reproducció**: repo, scripts, corpus (públic), sim.

### Decisions pendents de l'article
- Idioma: EN (abast) — les notes estan en català per treballar.
- On: blog personal / dev.to? (definir)
- Nom de la flota i hardware al text (2×RTX 5080, llama.cpp b####, Strata).

## Obert (si l'article es fa, aquests forats es poden mencionar o tapar)

- n=50 era l'objectiu declarat; vam tancar a n=33 per poda de curació honesta
  (41 esborranys → 25 publics + 8 privats vàlids). L'ampliació a ~100 no canvia
  el veredicte de cap parell observable amb aquest tamís de gap.
- Bateria C2 amb models no locals (frontiera via API) com a sostre de referència
  — no corregut; seria el comparador natural per situar la flota.
- Repetits k=3 només per al capdamunt, mai fets.
- El rol implementer (bateria A del dispatch) sí que té senyal (gemma4 net) —
  és l'única peça de routing viva; el best-of-breed per **idioma** (`by_lang` de
  ggufbench) queda com a única via de routing defensada.
