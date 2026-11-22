FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts
src/components/site/ProjectCard.astro
src/components/site/DeptPanel.astro
src/styles/site.css

TASKS
T1: Implement `cmdCode` segmentation helper
    depends_on: (none)
    refs: R4
T2: Write unit tests for `cmdCode` helper
    depends_on: T1
    refs: R4
T3: Add `.cmd-copy` CSS rules to site stylesheet
    depends_on: (none)
    refs: R1
T4: Integrate copy affordance into ProjectCard component
    depends_on: [T1, T3]
    refs: R1, R2
T5: Integrate copy affordance into DeptPanel component
    depends_on: [T1, T3]
    refs: R1, R2
T6: Verify content immutability and test suite status
    depends_on: [T4, T5]
    refs: R3

GATES
- `npx vitest run src/lib/cmd-code.spec.ts` passes (unit tests green)
- `npx vitest run` passes globally without modifying F17 tests (content assertions green)
- `git diff` confirms only new util/spec/component files, two rendering surfaces, site.css, and parity fixture are modified; `src/data/content.ts` is untouched.
- `llms.txt` and `llms-full.txt` snapshots remain byte-identical.
- Manual verification on `/en/projects/[slug]/`, `/es/projects/[slug]/`, `/ca/projects/[slug]/`, `/en/departments/[dept]/`, `/es/departments/[dept]/`, `/ca/departments/[dept]/`: `<code>` wraps install commands with monospace styling/background/border; hover/focus reveals copy icon; click copies text to clipboard and shows "copied" feedback.