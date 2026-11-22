FILES
src/data/types.ts
src/data/content.ts
src/pages/[lang]/departments/[dept].astro
tests/fixtures/parity.json
src/lib/__snapshots__/llms-endpoint.spec.ts.snap

TASKS
T1: Update FrontdeskPageContent type definition
    depends_on: (none)
    refs: R4
T2: Update content data for Home, Front Desk, Telemetry, and Footer
    depends_on: T1
    refs: R1, R2, R3, R5, R6, R7, R8, R9, R10, R11, R12, R13
T3: Implement Offer Block rendering in Front Desk page
    depends_on: T2
    refs: R14, R17
T4: Regenerate parity oracle and llms snapshots
    depends_on: T3
    refs: R15, R16

GATES
npm run build && node scripts/distill-parity.mjs
git diff --exit-code tests/fixtures/parity.json src/lib/__snapshots__/llms-endpoint.spec.ts.snap
npx vitest run
npx playwright test