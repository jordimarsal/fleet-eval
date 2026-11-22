=== FILE: README.md ===
# Camp de Proves

Documentació i eines del projecte **Camp de Proves**: un site estàtic autocontingut amb notes curates sobre JavaScript/TypeScript/Python (pàgines generades des de Markdown) més una pàgina interactive de proves — quiz, mode infinit i kates graduades localment.

Tot el contingut és generat a partir dels fitxers font (`md/`, `src/`) mitjançant `build.py`. No editeu els artefactes precompilats directament; feu canvis als fonts i reconstruïu.

## Com arrencar

```bash
harness/init.sh        # preparació inicial del repo (deps + validacions)
python3 build.py       # genèra l'site estàtic (index.html, proofs.html → index i pàgines)
open index.html        # obre la portada / catàleg de notes
open proofs.html       # obre el Camp de Proves interactiu
python3 build.py --check   # portes CI: verifica coherència sense escriure sortida
```

- **Portada / índex de notes**: `index.html`
- **Proves**: `proves.html` (quiz + kates amb grader local via `grader/grader.py`)
- **Taxonomia**: `taxonomy.json` defineix temes, carpetes i ordrem del contingut
- Tests d'unitat: `npm test`

## Mapa de contingut

| Recursos | On |
| --- | --- |
| Notes (font) | `md/<tema>/*.md` — frontmatter `title`/`desc` i cos en Markdown |
| Catàleg general | `index.html` generat des de `md/` + `taxonomy.json` |
| Pàgina de proves | `proves.html` — quiz, mode infinit (llama.cpp) i kates |
| Grader local | `grader/grader.py` — avalua les kates multi-llenguatge en local |
| Preguntes | `src/questions.js` (banc curatejat, publicats com `assets/questions.js`) |
| Build | `build.py` (generat → `p/`, `index.html`, `assets/…`) |
| Fonts / estils | `vendor/` i `src/` / arxius CSS |

Les **kates** són exercicis locals graduats amb grader; són entre els recursos on pots provar programació per llenguatges sense servei extern.

## Per a agents

Si treballeu sobre aquest repo, llegiu **AGENTS.md** abans de tocar res: conté regles del projecte, línies d'autoria i contractes dels tests. Els tests que han de passar estan a `tests/` (inclòs el smoke R2 dins `npm test`). Executeu sempre `python3 build.py --check` i `npm test` abans de tancar un batch.

=== END FILE ===