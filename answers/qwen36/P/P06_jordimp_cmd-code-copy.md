FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts
src/styles/site.css
src/components/site/ProjectCard.astro
src/pages/[lang]/projects/[slug].astro
src/pages/[lang]/departments/[dept].astro

TASKS
T1: Implement `cmd-code` segmentation helper
    depends_on: (none)
    refs: R3, R4
T2: Write unit tests for `cmd-code` helper
    depends_on: T1
    refs: R4
T3: Add `.cmd-copy` CSS rules to site stylesheet
    depends_on: (none)
    refs: R1
T4: Wire copy affordance into ProjectCard component
    depends_on: [T1, T3]
    refs: R1, R2
T5: Wire copy affordance into project detail page
    depends_on: [T1, T3]
    refs: R1, R2
T6: Wire copy affordance into department pages
    depends_on: [T1, T3]
    refs: R1, R2
T7: Run full test suite and verify parity fixture unchanged
    depends_on: [T2, T4, T5, T6]
    refs: R3

GATES
- `npx vitest run` passes with zero failures (unit + spec coverage intact).
- `git diff --stat` shows only the six files listed above plus no changes to `src/data/content.ts`, `llms.txt`, or `llms-full.txt`.
- Playwright smoke against `/en/projects/`, `/es/projects/`, `/ca/projects/`, `/en/departments/tooling/`, `/es/departments/tooling/`, `/ca/departments/tooling/`: each renders `<code>` wrapping the install command; hover/focus reveals `[data-copy]` icon; click writes command to clipboard and shows "copied" label.
- CSS audit confirms `.cmd-copy` rules exist in built stylesheet with monospace font, background, and border properties.