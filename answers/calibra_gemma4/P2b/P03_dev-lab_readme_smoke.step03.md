=== FILE: harness/progress/impl_readme_smoke.md ===
# Implementació: readme_smoke

Documentació de la implementació del README humà i els tests de smoke per garantir l'integritat del projecte.

## Requisits i Traçabilitat

| Ref | Requisit | Test | Fitxer |
| :--- | :--- | :--- | :--- |
| **R1** | README.md amb guia d'arrencament, mapa de contingut i referència a AGENTS.md | `tests/readme.test.js` | `README.md`, `AGENTS.md` |
| **R2** | Validació de build via `python3 build.py --check` integrada en la suite de tests | `tests/build_smoke.test.js` | `build.py`, `package.json` |

## Portes Verdes (Verification)

- [x] **npm test**: Execució de la suite completa incloent `readme.test.js` i `build_smoke.test.js`.
- [x] **build.py --check**: El script de construcció valida que no hi hagi errors de consistència o enllaços morts.
- [x] **Traçabilitat**: Tots els requisits R1 i R2 estan coberts per tests automàtics.

## Evidència de Logs

- **Batch 1 (T1, T2)**: `harness/logs/readme_smoke/batch-1.log`
  - Resultat: `83/83 OK` (Tests de README i Smoke de Build passats).
- **Batch 2 (T3)**: `harness/logs/readme_smoke/batch-2.log`
  - Resultat: `83/83 OK` (Validació final del procés de tancament).

---
*Final de l'implementació de readme_smoke.*
=== END FILE ===