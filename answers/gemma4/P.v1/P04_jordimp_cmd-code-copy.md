FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts
src/pages/[lang]/departments/[dept].astro
src/pages/[lang]/index.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Implement command segmentation utility and unit tests
    depends_on: (none)
    refs: R4
T2: Add CSS rules for `.cmd-copy` styling
    depends_on: T1
    refs: R1
T3: Update rendering surfaces to use helper and apply markup
    depends_on: T2
    refs: R1, R2, R3
T4: Verify parity and content integrity
    depends_on: T3
    refs: R3

GATES
- `npx vitest run src/lib/cmd-code.spec.ts` passes (R4)
- `git diff --stat` confirms no changes to `src/data/content.ts` or `src/lib/__snapshots__` (R3)
- `scripts/distill-parity.mjs` shows zero byte difference in LLM outputs (R3)
- Manual verification of hover/focus state on project detail and tooling pages (R2)
- Visual check of monospace background and border on rendered commands (R1)