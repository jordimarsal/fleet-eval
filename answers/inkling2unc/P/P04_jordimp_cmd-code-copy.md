FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts
src/components/site/CmdCode.astro
src/pages/[lang]/projects/[slug].astro
src/pages/[lang]/departments/[dept].astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Build pure segmentation helper with colocated spec
    depends_on: (none)
    refs: R4, R3
T2: Add .cmd-copy styles and copyable code component
    depends_on: T1
    refs: R1, R2, R3
T3: Wire highlight lines through the new component on both rendering surfaces
    depends_on: T2
    refs: R1, R2, R3
GATES
- npx vitest run green (includes cmd-code.spec.ts match/no-match/line-start/line-end cases and untouched F17 content assertions)
- built site dist scan of en/es/ca project detail pages and tooling department page finds <code> wrapping install command; dist CSS contains .cmd-copy rules (mono font, background, border)
- markup check: data-copy affordance bound to command text + control; manual hover/focus shows icon, click copies exact command and shows copied feedback via existing [data-copy] machinery
- git diff limited to src/lib/cmd-code.ts(+spec), CmdCode.astro, the two rendering surfaces, src/styles/site.css and tests/fixtures/parity.json; llms.txt / llms-full.txt output byte-identical