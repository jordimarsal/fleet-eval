FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts
src/components/site/HighlightCode.astro
src/pages/[lang]/projects/[slug].astro
src/pages/[lang]/departments/[dept].astro
src/styles/site.css

TASKS
T1: Implement the `cmd-code` segmentation helper
    depends_on: (none)
    refs: R4
T2: Write unit tests for the `cmd-code` helper
    depends_on: T1
    refs: R4
T3: Create the `HighlightCode.astro` component to wrap commands in `<code>` with `.cmd-copy` styling
    depends_on: T1
    refs: R1
T4: Integrate the `HighlightCode` component into the project detail and department page templates
    depends_on: T3
    refs: R1
T5: Add CSS rules for `.cmd-copy` (monospace, background, border) and hover/focus states for the copy affordance
    depends_on: T3
    refs: R1, R2
T6: Implement the copy affordance logic (icon reveal on hover/focus, clipboard write, "copied" feedback) using existing `[data-copy]` machinery
    depends_on: T5
    refs: R2
T7: Verify F17 content assertions remain green and llms.txt outputs are byte-identical
    depends_on: T6
    refs: R3

GATES
- Run `npx vitest run` to ensure all tests pass, specifically `src/lib/cmd-code.spec.ts` and existing F17 tests.
- Verify `git diff` shows changes only in the new util/spec/component, the two rendering surfaces, site.css, and parity fixture (if applicable).
- Confirm `llms.txt` and `llms-full.txt` snapshots are untouched.
- Manual verification: Navigate to a project detail page and a tooling department page (en/es/ca); hover over install commands to see the copy icon; click to verify clipboard write and "copied" feedback.
- Dist scan verification: Check that `<code>` elements wrap install commands and built CSS contains `.cmd-copy` rules.