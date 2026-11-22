FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Update DeptPanel markup to insert CTA between header and body
    depends_on: (none)
    refs: R1
T2: Add CSS for filled yellow CTA buttons in panels
    depends_on: T1
    refs: R2
T3: Add CSS to disable card overlay and adjust hover effects inside panels
    depends_on: T1
    refs: R3
T4: Add CSS for reduced sizing of project cards inside panels
    depends_on: T1
    refs: R4
T5: Regenerate parity fixture to match new panel markup order
    depends_on: T1
    refs: R5
T6: Run full test suite to verify no regressions
    depends_on: T2, T3, T4, T5
    refs: R5

GATES
- `npm run build` succeeds without errors
- `npx vitest run` passes all tests
- `npm run distill:parity` produces a fixture diff limited only to panel markup order changes
- Visual verification on deployed home page confirms:
  - Department CTAs appear above cards with filled yellow background
  - Operations panel includes CV button in correct position
  - Project cards inside panels have reduced padding/gap/font-size
  - Card overlays are disabled inside panels; hover/focus states remain visible