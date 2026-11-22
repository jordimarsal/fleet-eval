FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts
src/components/site/CmdCode.astro
src/pages/[lang]/projects/[slug].astro
src/pages/[lang]/departments/[dept].astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Add pure segmentation helper with colocated spec (red first)
    depends_on: (none)
    refs: R4
T2: Build CmdCode component wrapping the command in <code> with data-copy affordance
    depends_on: T1
    refs: R1, R2
T3: Apply CmdCode to highlight rendering on project detail and tooling department surfaces
    depends_on: T2
    refs: R1, R2, R3
T4: Style .cmd-copy rules in site.css
    depends_on: T2
    refs: R1
T5: Verify full suite green, parity fixture / llms outputs untouched
    depends_on: T3, T4
    refs: R1, R2, R3

GATES
- `npx vitest run` — all green, no F17 tests modified; cmd-code.spec.ts red before implementation of the helper and green after
- `git diff --stat` limited to src/lib/cmd-code.ts, src/lib/cmd-code.spec.ts, src/components/site/CmdCode.astro, src/pages/[lang]/projects/[slug].astro, src/pages/[lang]/departments/[dept].astro, src/styles/site.css, tests/fixtures/parity.json (no content.ts changes)
- Production build (`npm run build` or equivalent astro check/build) succeeds
- Dist scan of project detail pages and tooling department page (en/es/ca) finds `<code>` wrapping the install command and markup containing the `data-copy` control bound to that command; built CSS contains `.cmd-copy` rules (mono font, background, border)
- Manual pass on hover and keyboard focus over the code element: copy icon revealed; activating it writes exact command text to clipboard with visible "copied" feedback (existing [data-copy] machinery)
- Built llms.txt / llms-full.txt output byte-identical to pre-feature state and parity fixture reconciled via scripts/distill-parity.mjs only if rendering diff requires it