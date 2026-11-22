FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Move department CTAs between panel header and body in DeptPanel.astro
    depends_on: (none)
    refs: R1
T2: Add scoped filled-CTA rules for .dept-panel__cta buttons in site.css
    depends_on: T1
    refs: R2
T3: Scope down card fill-sweep overlay and hover affordance inside panels
    depends_on: T1
    refs: R3, R4
T4: Apply reduced sizing to project cards inside panels (tap targets ≥44px preserved)
    depends_on: T1
    refs: R4
T5: Regenerate parity fixture and confirm no outside-panel changes
    depends_on: T2, T3, T4
    refs: R5

GATES
- npm run build succeeds; scan over dist/{en,es,ca}/index.html asserts inside every dept-panel the first .btn occurs before the panel body (.cards / .ledger / .prose / .pills / .q-plaque-copy) — covers R1
- grep built CSS for `.dept-panel__cta .btn { background: var(--y1) }` with disabled ::before fill-sweep; visual pass on deployed home covering CTA placement — covers R2
- grep built CSS for scoped `.dept-panel .card::before` disabled plus reduced hover transform (≤2px lift) and hard shadow (≤5px) inside panels; keyboard focus pass shows visible indicator — covers R3
- grep built CSS for scoped padding 12px / gap 8px / summary font-size 0.88rem in panels; confirm whole-card link height ≥44px (multi-line links) via dist scan + visual pass — covers R4
- npx vitest run fully green (existing tests unchanged stay green) — covers R5
- npm run distill:parity regenerates tests/fixtures/parity.json with a diff limited to panel markup order — covers R5
- git diff confined to src/components/site/DeptPanel.astro, src/styles/site.css and tests/fixtures/parity.json — covers R5
- Verify /projects index cards unchanged visually and that llms.txt / llms-full.txt content is untouched — covers R5