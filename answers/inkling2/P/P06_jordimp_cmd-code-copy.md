FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts
src/components/site/CmdCopy.astro
src/pages/[lang]/projects/[slug].astro
src/pages/[lang]/departments/[dept].astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Pure segmentation helper for install-command highlight lines (red first, then green)
    depends_on: (none)
    refs: R4
T2: Copyable `<code class="cmd-copy">` render path — CSS rules and Astro component
    depends_on: T1
    refs: R1, R2
T3: Wire the copyable command into the project detail page rendering surface
    depends_on: T2
    refs: R1, R2
T4: Wire the copyable command into the tooling department page rendering surface
    depends_on: T2
    refs: R1, R2
T5: Keep F17 content / llms snapshots / parity fixture honest
    depends_on: T3, T4
    refs: R3

GATES
- npx vitest run (full suite green; cmd-code.spec.ts passed red→green without touching any existing test or src/data/content.ts)
- git diff limited to the new util/spec/component, the two rendering surfaces, site.css and tests/fixtures/parity.json; content.ts untouched
- dist scan of project detail pages and the tooling department page (en/es/ca) for <code wrapping the install command, plus built CSS containing .cmd-copy rules (mono font, background, border)
- Manual pass on a built page: hover/focus reveals icon, activation writes exact command text to clipboard with visible "copied" feedback via existing [data-copy] machinery
- Parity check (scripts/distill-parity.mjs path / smoke spec) passes with updated fixture where markup changed but text is identical; llms.txt / llms-full.txt output byte-identical