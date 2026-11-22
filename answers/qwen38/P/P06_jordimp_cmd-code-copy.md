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
T3: Integrate CmdCode into project detail page rendering
    depends_on: T2
    refs: R1, R2, R3
T4: Integrate CmdCode into tooling department page rendering
    depends_on: T2
    refs: R1, R2, R3
T5: Add CSS styles for command code element
    depends_on: T2
    refs: R1
T6: Update parity fixture to reflect new markup
    depends_on: T3, T4
    refs: R3

GATES
npx vitest run src/lib/cmd-code.spec.ts
npx vitest run
git diff --name-only | grep -E "^(src/data/content\.ts|src/lib/__snapshots__/llms-endpoint\.spec\.ts\.snap)$" && exit 1 || true
npm run build
grep -q "<code class=\"cmd-copy\"" dist/en/projects/*/index.html
grep -q "\.cmd-copy" dist/_astro/*.css
grep -q "data-copy" dist/en/projects/*/index.html