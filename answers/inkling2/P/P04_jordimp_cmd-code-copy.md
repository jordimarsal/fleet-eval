FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts
src/scripts/cmd-code.ts
src/pages/[lang]/projects/[slug].astro
src/pages/[lang]/departments/[dept].astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Add pure segmentation helper with red spec first
    depends_on: (none)
    refs: R4
T2: Wire copyable code into project detail and tooling department rendering surfaces + site.css `.cmd-copy` rules
    depends_on: T1
    refs: R1, R2
T3: Extend parity fixture / assertions for the new markup shape while keeping content source unchanged
    depends_on: T2
    refs: R1, R3
T4: Verify full test suite, dist scans, CSS rules, llms snapshot parity; confirm no edits to F17 tests or content.ts
    depends_on: T3
    refs: R3

GATES
- npx vitest run — full suite green, including colocated cmd-code.spec.ts (match case, no-match passthrough, command at line start/end) and existing F17 content assertions without modification
- npm run build (or equivalent) then dist scan of en/es/ca project detail page and language variants of the tooling department page finds `<code>` wrapping the install command with data-copy affordance bound to the command text
- built CSS contains `.cmd-copy` rules (monospace font, background, border)
- git diff touches only: src/lib/cmd-code.ts, src/lib/cmd-code.spec.ts, the copy binding script, the two rendering surfaces, site.css, and tests/fixtures/parity.json — content.ts, llms.txt / llms-full.txt output byte-identical
- manual pass: hover/focus on code element reveals icon; click writes exact command to clipboard and shows visible "copied" feedback via existing [data-copy] machinery