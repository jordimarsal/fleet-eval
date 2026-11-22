FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Move department CTA buttons into DeptPanel markup, placing them between header and body content
    depends_on: (none)
    refs: R1
T2: Style department CTA buttons with filled yellow background (`var(--y1)`), disable fill-sweep overlay
    depends_on: T1
    refs: R2
T3: Disable project card hover/focus fill-sweep overlay inside department panels; reduce lift ≤ 2px, hard shadow ≤ 5px
    depends_on: T1
    refs: R3
T4: Reduce project card sizing inside department panels: padding 12px, gap 8px, summary font-size 0.88rem; ensure whole-card link heights ≥ 44px
    depends_on: T3
    refs: R4
T5: Regenerate parity fixture to reflect new panel markup order; verify no unintended diffs in `/projects`, `llms.txt`, or tests
    depends_on: T4
    refs: R5

GATES
- `npm run build` succeeds without errors
- Scan `dist/{en,es,ca}/index.html`: every `dept-panel` has its first `.btn` before any of `.cards`, `.ledger`, `.prose`, `.pills`, `.q-plaque-copy`
- Built CSS contains scoped rule `.dept-panel__cta .btn { background: var(--y1) }` with disabled `::before`
- Built CSS contains scoped rules disabling `.dept-panel .card::before` and reducing hover transform/shadow inside panels
- Keyboard focus pass on deployed home confirms visible focus indicator preserved
- Built CSS contains scoped sizing rules for cards (padding 12px, gap 8px, summary font-size 0.88rem)
- Whole-card links inside department panels have height > 44px (F16 tap-target rule respected)
- Full `npx vitest run` passes green
- `npm run distill:parity` produces a fixture whose diff covers only panel markup order changes
- `git diff` limited to `DeptPanel.astro`, `site.css`, and `tests/fixtures/parity.json`