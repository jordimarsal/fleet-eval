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
T3: Integrate CmdCode into project detail page
    depends_on: T2
    refs: R1, R2, R3
T4: Integrate CmdCode into department page
    depends_on: T2
    refs: R1, R2, R3
T5: Add CSS styles for command code element
    depends_on: T2
    refs: R1
T6: Update parity fixture to reflect new markup structure
    depends_on: T3, T4
    refs: R3

GATES
- `npx vitest run` passes all tests including new cmd-code.spec.ts and existing F17 content assertions
- `git diff --stat` confirms changes limited to: src/lib/cmd-code.ts, src/lib/cmd-code.spec.ts, src/components/site/CmdCode.astro, src/pages/[lang]/projects/[slug].astro, src/pages/[lang]/departments/[dept].astro, src/styles/site.css, tests/fixtures/parity.json
- `git diff src/data/content.ts` shows no changes (content source unchanged)
- `git diff src/lib/__snapshots__/llms-endpoint.spec.ts.snap` shows no changes (llms snapshot untouched)
- Build succeeds with `npm run build`
- Dist scan of built HTML for project detail page finds `<code class="cmd-copy"` wrapping install commands in en/es/ca locales
- Dist scan of built HTML for department pages finds `<code class="cmd-copy"` wrapping install commands where applicable
- Built CSS contains `.cmd-copy` rules with monospace font-family, background-color, and border properties
- Manual verification: hover over command code element reveals copy icon; clicking copies exact command text to clipboard and displays "copied" feedback label
- Keyboard focus on command code element also reveals copy affordance