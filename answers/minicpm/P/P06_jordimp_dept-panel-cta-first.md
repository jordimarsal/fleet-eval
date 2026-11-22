FILES
src/components/site/DeptPanel.astro
src/components/site/ProjectCard.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Update DeptPanel.astro to insert CTA buttons between header and body
    depends_on: (none)
    refs: R1
T2: Add scoped CSS for department CTA buttons (filled yellow, no sweep)
    depends_on: T1
    refs: R2
T3: Add scoped CSS to disable project card fill-sweep on hover/focus inside panels
    depends_on: T2
    refs: R3
T4: Add scoped CSS for reduced sizing of project cards inside department panels
    depends_on: T3
    refs: R4
T5: Verify global styles unchanged and regenerate parity fixture
    depends_on: T4
    refs: R5

GATES
- `npm run build` succeeds and dist scan confirms `.btn` placement before panel body in `dept-panel` containers.
- Built CSS contains scoped rules for `.dept-panel__cta .btn` (yellow background, disabled `::before`).
- Built CSS contains scoped rules disabling `.dept-panel .card::before` and adjusting hover transforms/shadows.
- Built CSS contains scoped sizing rules for cards inside panels (padding 12px, gap 8px, font-size 0.88rem).
- `npx vitest run` passes all tests green.
- `npm run distill:parity` produces a fixture diff limited only to panel markup order changes.
- Visual pass on deployed home page confirms CTA positioning, button styling, and card sizing/behavior.