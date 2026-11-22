FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Update DeptPanel markup to insert CTA between header and body
    depends_on: (none)
    refs: R1
T2: Add scoped CSS for filled yellow CTA buttons in panels
    depends_on: T1
    refs: R2
T3: Add scoped CSS to disable fill-sweep overlay on panel cards
    depends_on: T1
    refs: R3
T4: Add scoped CSS for reduced sizing of panel cards
    depends_on: T1
    refs: R4
T5: Regenerate parity fixture and verify global styles unchanged
    depends_on: T4
    refs: R5

GATES
- `npm run build` succeeds without errors.
- Scan `dist/{en,es,ca}/index.html` confirms `.btn` appears before panel body elements inside every `dept-panel`.
- Built CSS contains scoped rules for `.dept-panel__cta .btn` background and disabled `::before`, and scoped rules disabling `.dept-panel .card::before` with adjusted hover transforms/shadows.
- Visual inspection confirms panel cards have 12px padding, 8px gap, 0.88rem summary font-size, and maintain ≥44px link height.
- Full `npx vitest run` passes all existing tests.
- `npm run distill:parity` produces a fixture diff limited only to panel markup order changes.
- `git diff` shows modifications restricted to `DeptPanel.astro`, `site.css`, and `tests/fixtures/parity.json`.