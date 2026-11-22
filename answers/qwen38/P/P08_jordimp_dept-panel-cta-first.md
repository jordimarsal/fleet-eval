FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Move CTA buttons above panel body in DeptPanel markup
    depends_on: (none)
    refs: R1
T2: Add scoped CSS for filled yellow CTA and disabled sweep overlay
    depends_on: T1
    refs: R2
T3: Disable card hover/focus sweep and reduce sizing inside panels
    depends_on: T1
    refs: R3, R4
T4: Regenerate parity fixture to match new markup order
    depends_on: T1, T2, T3
    refs: R5

GATES
npm run build && node scripts/check-dist.mjs --assert-dept-panel-order
npx vitest run
npm run distill:parity && git diff --exit-code tests/fixtures/parity.json || echo "Fixture updated as expected"
git status --porcelain | grep -E "(DeptPanel\.astro|site\.css|parity\.json)" && ! git status --porcelain | grep -vE "(DeptPanel\.astro|site\.css|parity\.json)"