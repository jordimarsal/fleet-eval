=== FILE: README.md ===
# Camp de Proves

Aquest repositori conté el sistema del "Camp de Proves", un entorn interactiu per practicar conceptes de programació (principalment Java) mitjançant quizes i kates.

## Com arrencar

Per configurar l'entorn i generar el site estàtic, segueix aquests passos:

1. **Inicialització**: Executa el script d'harness per preparar l'entorn:
   `bash harness/init.sh`
2. **Generació del site**: Utilitza el script de Python per compilar els fitxers Markdown en pàgines HTML:
   `python3 build.py`
3. **Visualització**: Obre directament el fitxer `index.html` al teu navegador per veure la pàgina principal o `proves.html` per accedir al camp de proves.

El sistema utilitza `taxonomy.json` per definir l'estructura dels temes i `grader/grader.py` per a les tasques de correcció automàtica (kates).

## Mapa de contingut

- **Contingut Teòric**: Notes generades des de fitxers `.md` situats a la carpeta `md/`.
- **Camp de Proves**: Quizes interactius i kates (exercicis pràctics amb grader local).
- **Assets**: Recursos compartits com CSS, JS i imatges.
- **Harness**: Scripts d'automatització i configuració.

Per a agents de IA que analitzen aquest repositori, consultin `AGENTS.md` per una guia detallada de l'estructura i les convencions.

Les kates permeten un feedback immediat sobre la qualitat del codi escrit.
=== END FILE ===

=== FILE: AGENTS.md ===
# Agent Guide

This repository contains the "Camp de Proves" project, a web-based interactive learning environment for programming concepts.

## Project Structure

- `/md`: Source Markdown files for study notes.
- `/p`: Generated HTML pages from Markdown.
- `/assets`: Static assets (JS, CSS, images).
- `/vendor`: Third-party libraries and fonts.
- `/harness`: Automation scripts and logs.
- `build.py`: The main build engine that converts MD to HTML.
- `taxonomy.json`: Defines the hierarchy and metadata of all themes.
- `index.html`: Entry point for the documentation site.
- `proves.html`: Entry point for the interactive quiz/kata system.

## Key Workflows

### 1. Content Generation
The build process is driven by `python3 build.py`. It reads `taxonomy.json` and parses files in `/md`. Use `--check` to validate the integrity of the taxonomy and links without generating files.

### 2. Testing & Validation
- **Smoke Tests**: Run `npm test` to execute automated checks including the build validation.
- **Kates**: Local grading is handled via Python scripts in the grader directory.

### 3. Theme Management
The site supports `light` and `dark` modes, persisted via `localStorage` and propagated through URL parameters (`?theme=...`).

## Development Conventions
- All new content should be added as `.md` files in the appropriate subdirectory within `/md`.
- Ensure `taxonomy.json` is updated whenever a new theme or folder is created.
- Always run `python3 build.py --check` before committing changes to ensure no broken references exist.
=== END FILE ===

=== FILE: harness/progress/impl_readme_smoke.md ===
| Requirement | Test Case | File Created | Status |
| :--- | :--- | :--- | :--- |
| R1: README existence & info | `tests/readme.test.js` | `README.md`, `AGENTS.md` | ✅ PASS |
| R2: Build smoke test | `tests/build_smoke.test.js` | N/A (Existing) | ✅ PASS |
| R3: Traceability | Manual/Automated | `harness/progress/impl_readme_smoke.md` | ✅ PASS |
=== END FILE ===