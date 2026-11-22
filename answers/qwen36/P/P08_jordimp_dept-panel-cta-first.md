FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Move CTA buttons above panel body in DeptPanel.astro
    depends_on: (none)
    refs: R1
T2: Add scoped CSS for filled-yellow CTA and disabled card overlay inside panels
    depends_on: T1
    refs: R2, R3
T3: Reduce project-card sizing inside department panels via scoped CSS
    depends_on: T2
    refs: R4
T4: Regenerate parity fixture to match new markup order
    depends_on: T3
    refs: R5

GATES
- `npm run build` succeeds; scan `dist/{en,es,ca}/index.html` confirms first `.btn` before panel body (` .cards`, `.ledger`, `.prose`, `.pills`, `.q-plaque-copy`) inside every `dept-panel`.
- Built CSS contains `.dept-panel__cta .btn { background: var(--y1) }` with `::before` disabled; visual pass on deployed home shows yellow-filled CTAs distinct from project cards.
- Built CSS disables `.dept-panel .card::before`; hover/focus transform ≤ 2px, shadow ≤ 5px; keyboard focus retains visible outline indicator.
- Built CSS enforces reduced card sizing (padding 12px, gap 8px, summary font-size 0.88rem); whole-card link heights ≥ 44px; F16 tap-target rule respected.
- `/projects` index cards retain original styling; `llms.txt` / `llms-full.txt` content unchanged; all existing tests green via `npx vitest run`.
- `npm run distill:parity` produces a fixture whose diff covers only panel markup order changes.
- `git diff` limited to `DeptPanel.astro`, `site.css`, and `tests/fixtures/parity.json`.