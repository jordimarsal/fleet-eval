FILES
src/lib/cmd-code.spec.ts
src/lib/cmd-code.ts
src/components/site/ProjectCard.astro
src/components/site/DeptPanel.astro
src/styles/site.css

TASKS
T1: Implement pure segmentation helper for install commands in highlight lines
    depends_on: (none)
    refs: R4
T2: Write unit tests for cmd-code helper (match, no-match, start/end positions)
    depends_on: T1
    refs: R4
T3: Add `.cmd-copy` CSS rules to site.css (monospace font, background, border)
    depends_on: (none)
    refs: R1
T4: Wire copy affordance into ProjectCard.astro render of highlight lines
    depends_on: [T1, T3]
    refs: R1, R2
T5: Wire copy affordance into DeptPanel.astro render of highlight lines
    depends_on: [T1, T3]
    refs: R1, R2
T6: Verify content source unchanged and F17 assertions still green
    depends_on: [T4, T5]
    refs: R3

GATES
- `npx vitest run src/lib/cmd-code.spec.ts` passes (R4)
- `npx vitest run` passes with zero regressions on existing test suite (R3)
- Manual inspection of dist output on project detail page and tooling department page confirms `<code>` wrapping install commands in en/es/ca variants (R1)
- Built CSS contains `.cmd-copy` selector with monospace font, background color, and border declaration (R1)
- Hover/focus interaction on rendered code elements reveals copy icon; click writes command text to clipboard and shows "copied" label via `[data-copy]` machinery (R2)
- `git diff` shows changes only in the five planned files plus site.css; no modifications to `src/data/content.ts`, `llms.txt`, or `llms-full.txt` (R3)