FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts
src/components/site/CmdCode.astro
src/pages/[lang]/projects/[slug].astro
src/pages/[lang]/departments/[dept].astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Implement pure segmentation helper and unit tests
    depends_on: (none)
    refs: R4
T2: Create CmdCode component with copy affordance
    depends_on: T1
    refs: R1, R2
T3: Update rendering surfaces to use CmdCode
    depends_on: T2
    refs: R1, R2, R3
T4: Add CSS styles for command code element
    depends_on: T2
    refs: R1
T5: Verify content source integrity and snapshots
    depends_on: T3
    refs: R3
T6: Update parity fixture if necessary
    depends_on: T3
    refs: R3

GATES
- npx vitest run src/lib/cmd-code.spec.ts --run
- npx vitest run src/data/content.spec.ts --run
- git diff --name-only | grep -E "^(src/data/content\.ts|src/lib/__snapshots__/llms-endpoint\.spec\.ts\.snap)$" && echo "FAIL: content or llms snapshot modified" || echo "PASS: content and llms untouched"
- npx astro build
- grep -r "<code class=\"cmd-copy\"" dist/ | wc -l > /dev/null && echo "PASS: code elements found in dist" || echo "FAIL: no cmd-copy code elements"
- grep -q "\.cmd-copy" dist/_astro/*.css && echo "PASS: CSS rules present" || echo "FAIL: CSS rules missing"
- npx playwright test tests/smoke.spec.ts tests/projects.spec.ts tests/departments.spec.ts