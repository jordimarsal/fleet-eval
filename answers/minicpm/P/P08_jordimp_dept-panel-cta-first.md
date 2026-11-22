FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Update DeptPanel.astro to insert CTA button between header and body
    depends_on: (none)
    refs: R1
T2: Add CSS for filled yellow CTA buttons inside department panels
    depends_on: T1
    refs: R2
T3: Disable yellow fill-sweep overlay on project cards within department panels
    depends_on: T2
    refs: R3
T4: Apply reduced sizing (padding, gap, font-size) to project cards inside department panels
    depends_on: T3
    refs: R4
T5: Regenerate parity fixture and verify all tests pass
    depends_on: T4
    refs: R5

GATES
- `npm run build` succeeds without errors
- Scan `dist/{en,es,ca}/index.html` confirms CTA button placement in every `dept-panel` (R1)
- Built CSS contains scoped rules for `.dept-panel__cta .btn` with `var(--y1)` background and disabled `::before` (R2)
- Built CSS contains scoped rules disabling `.dept-panel .card::before` and reducing hover transform/shadow (R3)
- Built CSS contains scoped sizing rules for cards inside panels (padding 12px, gap 8px, summary font-size 0.88rem) (R4)
- `npx vitest run` passes all tests green
- `npm run distill:parity` regenerates `tests/fixtures/parity.json` with diff limited to panel markup order
- `git diff` shows changes only in `DeptPanel.astro`, `site.css`, and `tests/fixtures/parity.json`