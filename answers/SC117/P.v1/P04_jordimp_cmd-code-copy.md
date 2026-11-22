FILES
src/lib/cmd-code.spec.ts
src/lib/cmd-code.ts
src/components/site/CaseMotif.astro
src/components/site/DeptPanel.astro
src/styles/site.css
src/scripts/copy.ts

TASKS
T1: Implement pure segmentation helper for install commands
    depends_on: (none)
    refs: R4
T2: Write unit tests for segmentation helper
    depends_on: T1
    refs: R4
T3: Add CSS styles for code element and copy affordance
    depends_on: (none)
    refs: R1, R2
T4: Integrate copy logic into existing script
    depends_on: T3
    refs: R2
T5: Update CaseMotion component to wrap commands in <code> with data attributes
    depends_on: T1, T4
    refs: R1, R2
T6: Update DeptPanel component to wrap commands in <code> with data attributes
    depends_on: T1, T4
    refs: R1, R2
T7: Verify content source unchanged and tests pass
    depends_on: T5, T6
    refs: R3

GATES
- `npx vitest run` passes all existing tests including new `cmd-code.spec.ts`.
- `git diff` confirms only expected files are modified.
- Manual verification on local dev server: hover over install command in a project detail page shows copy icon; click copies text and shows "copied" feedback.
- Visual inspection of rendered HTML confirms `<code>` tags surround the command text with appropriate classes.