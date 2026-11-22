FILES
src/data/types.ts
src/data/content.ts
src/pages/[lang]/departments/[dept].astro
tests/fixtures/parity.json
src/lib/__snapshots__/llms-endpoint.spec.ts.snap

TASKS
T1: Update FrontdeskPageContent types to include offer block
    depends_on: (none)
    refs: R4
T2: Implement new positioning copy in content data
    depends_on: T1
    refs: R1, R2, R3, R5, R6, R7, R8, R9, R10, R11, R12, R13
T3: Render offer block on Front Desk department page
    depends_on: T2
    refs: R14, R17
T4: Regenerate parity oracle and llms snapshots
    depends_on: T3
    refs: R15, R16

GATES
- `npm run build` completes successfully.
- `node scripts/distill-parity.mjs` generates a diff for `tests/fixtures/parity.json` that only touches the specified title/description/h1/mainText fields for home, front desk, telemetry routes, and splash description, with `_meta.counts` unchanged at `{ "localeRoutes": 63, "pages": 65 }`.
- `npx vitest run src/lib/llms-endpoint.spec.ts` passes with updated snapshot matching the generated `llms.txt` and `llms-full.txt` content.
- `npx playwright test tests/departments.spec.ts` verifies the Front Desk page renders the new offer block strings in all locales (en, es, ca).
- `git diff --name-only` confirms no changes to `src/styles/site.css` or other stylesheets.