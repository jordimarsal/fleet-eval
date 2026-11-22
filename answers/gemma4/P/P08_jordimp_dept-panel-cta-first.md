FILES
src/components/site/DeptPanel.astro
src/components/site/ProjectCard.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Update DeptPanel markup to include CTA buttons between header and body
    depends_on: (none)
    refs: R1
T2: Implement scoped CSS for department panel CTAs (filled yellow, no sweep)
    depends_on: T1
    refs: R2
T3: Implement scoped CSS for project cards inside department panels (reduced size, no sweep, subtle hover)
    depends_on: T1
    refs: R3, R4
T4: Verify non-regression of external styles and regenerate parity fixture
    depends_on: T3
    refs: R5

GATES
- `npm run build` followed by a scan of `dist/{en,es,ca}/index.html` to verify `.btn` position within `.dept-panel`.
- Visual regression check: ensure `.dept-panel .card::before` is disabled and hover transform is $\le$ 2px.
- Accessibility check: confirm keyboard focus on panel cards maintains visible outline and meets F16 tap-target height ($\ge$ 44px).
- `npx vitest run` passes with no regressions.
- `npm run distill:parity` produces a diff containing only the expected markup order changes in `tests/fixtures/parity.json`.