FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Update DeptPanel markup to position CTA before body content
    depends_on: (none)
    refs: R1, R2
T2: Implement scoped CSS for filled CTA and reduced card sizing
    depends_on: T1
    refs: R2, R3, R4
T3: Regenerate parity fixture and verify test suite
    depends_on: T2
    refs: R5

GATES
- `npm run build` completes successfully.
- Scan `dist/{en,es,ca}/index.html`: Inside every `.dept-panel`, the first `.btn` element appears in DOM order before any `.cards`, `.ledger`, `.prose`, `.pills`, or `.q-plaque-copy`.
- Built CSS inspection: Contains `.dept-panel__cta .btn { background: var(--y1); }` with `::before` overlay disabled; contains rules disabling `.dept-panel .card::before`; contains hover/focus transform/shadow reductions for `.dept-panel .card`.
- Built CSS inspection: Contains scoped sizing rules for `.dept-panel .card` (padding 12px, gap 8px, font-size 0.88rem).
- Visual pass on deployed home page confirms yellow filled CTAs and smaller cards within panels.
- Keyboard focus pass confirms visible indicators on project cards inside panels.
- `npx vitest run` passes all tests.
- `npm run distill:parity` generates a new `tests/fixtures/parity.json`.
- `git diff --name-only` shows changes limited to `src/components/site/DeptPanel.astro`, `src/styles/site.css`, and `tests/fixtures/parity.json`.