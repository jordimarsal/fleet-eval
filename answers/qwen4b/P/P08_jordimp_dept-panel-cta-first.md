FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/departments.spec.ts
tests/home.spec.ts
tests/fixtures/parity.json

TASKS
T1: Implement department CTA placement above panel body content  
    depends_on: (none)  
    refs: R1, R2  
T2: Add hover/focus state handling for project cards in department panels to disable fill-sweep overlay and maintain affordance  
    depends_on: T1  
    refs: R3  
T3: Adjust project card sizing with reduced padding, gap, and font size while preserving minimum link height  
    depends_on: T1  
    refs: R4  
T4: Verify parity of non-panel pages and regenerate fixture to reflect updated markup order  
    depends_on: T1, T2, T3  
    refs: R5  

GATES
- Built CSS contains `.dept-panel__cta .btn { background: var(--y1) }` and disabled `::before` fill-sweep overlay  
- Visual pass on deployed home page confirms correct CTA rendering and hover/focus behavior  
- Full `npx vitest run` passes without regressions  
- `npm run distill:parity` produces fixture with diff limited to panel markup order changes  
- Playwright tests in `tests/departments.spec.ts` and `tests/home.spec.ts` pass  
- `git diff` shows changes only in `DeptPanel.astro`, `site.css`, and `tests/fixtures/parity.json`