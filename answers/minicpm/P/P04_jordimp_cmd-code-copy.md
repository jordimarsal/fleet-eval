FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts
src/components/highlight.astro
src/styles/site.css
src/scripts/copy.ts

TASKS
T1: Implement the `cmd-code` segmentation helper
    depends_on: (none)
    refs: R4
T2: Write unit tests for the `cmd-code` helper
    depends_on: T1
    refs: R4
T3: Create the copy affordance script and integrate it with existing `[data-copy]` machinery
    depends_on: (none)
    refs: R2
T4: Update the highlight rendering component to wrap install commands in `<code>` with the copy affordance
    depends_on: T1, T3
    refs: R1, R2
T5: Add CSS rules for `.cmd-copy` styling (monospace, background, border)
    depends_on: T4
    refs: R1
T6: Verify content source unchanged and F17 tests pass
    depends_on: T4
    refs: R3

GATES
- Run `npx vitest run` to ensure all tests pass, specifically `cmd-code.spec.ts` and existing F17 assertions.
- Verify `git diff` shows changes only in expected files (util, spec, component, css, script) and that `llms.txt`/`llms-full.txt` are untouched.
- Manual verification: Navigate to project detail and tooling department pages (en/es/ca), hover over install command highlights to confirm copy icon appears, click to verify clipboard write and "copied" feedback.
- Confirm built CSS contains `.cmd-copy` rules with monospace font, background, and border.