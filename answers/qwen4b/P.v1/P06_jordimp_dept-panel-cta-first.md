FILES  
src/components/site/DeptPanel.astro  
src/styles/site.css  
tests/fixtures/parity.json  

TASKS  
T1: Implement department CTA rendering above panel body  
    depends_on: (none)  
    refs: R1, R2  
T2: Apply hover/focus state rules to project cards in department panels  
    depends_on: T1  
    refs: R3  
T3: Adjust card sizing and spacing for department panels  
    depends_on: T1  
    refs: R4  
T4: Regenerate parity fixture and verify no unintended changes  
    depends_on: T1, T2, T3  
    refs: R5  

GATES  
- Built CSS contains `.dept-panel__cta .btn { background: var(--y1) }` and disabled `::before` overlay  
- Visual pass on deployed home page confirms correct CTA placement and styling  
- `npx vitest run` passes all tests; no regressions in existing test suites  
- `npm run distill:parity` produces fixture with diff limited to panel markup order  
- `dist/{en,es,ca}/index.html` scan confirms first `.btn` appears before any `.cards`, `.ledger`, `.prose`, `.pills`, or `.q-plaque-copy`  
- F16 tap-target rule verified: all whole-card links have height ≥ 44px  
- Keyboard focus pass shows visible affordance on card hover/focus without fill-sweep overlay