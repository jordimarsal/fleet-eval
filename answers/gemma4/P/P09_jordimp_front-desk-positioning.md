FILES
src/data/types.ts
src/data/content.ts
src/pages/[lang]/departments/[dept].astro
tests/fixtures/parity.json

TASKS
T1: Update data types for new offer block
    depends_on: (none)
    refs: R4
T2: Update content with new copy and localized strings
    depends_on: T1
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R13
T3: Implement offer block rendering in department page template
    depends_on: T2
    refs: R14, R17
T4: Regenerate parity oracle and validate site integrity
    depends_on: T3
    refs: R15, R16

GATES
- Run `npm run build` to ensure no type errors or broken links.
- Execute `npm run test` (Vitest + Playwright) to verify all requirements and existing logic.
- Run `npm run build && node scripts/distill-parity.mjs` and verify the `git diff` of `tests/fixtures/parity.json` matches expected changes only.
- Verify `llms.txt` and `llms-full.txt` generation via snapshot tests.
- Manual visual check of Front Desk page for correct markup (`<mark>`, `<b>`) and layout using existing CSS classes.