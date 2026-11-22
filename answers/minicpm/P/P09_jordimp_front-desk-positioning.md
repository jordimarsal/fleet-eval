FILES
src/data/types.ts
src/data/content.ts
src/pages/[lang]/departments/[dept].astro
tests/fixtures/parity.json
src/lib/__snapshots__/llms-endpoint.spec.ts.snap

TASKS
T1: Update `HOME` content strings for kicker, h1, and stand in all locales.
    depends_on: (none)
    refs: R1, R2, R3
T2: Add the new typed `offer` block to `FrontdeskPageContent` in `types.ts` and populate `content.ts` with localized strings.
    depends_on: T1
    refs: R4
T3: Update `FRONTDESK_PAGE.cta`, `DEPTS.frontdesk.line`, `DEPTS.frontdesk.intro`, and `PAGES.frontdesk.description` in `content.ts`.
    depends_on: T2
    refs: R5, R6, R7, R10
T4: Update `FOOTER.line` and `PAGES.home.description` in `content.ts`.
    depends_on: T3
    refs: R8, R9
T5: Append the conflict-of-interest disclaimer to `DEPTS.telemetry.intro` in all locales.
    depends_on: T4
    refs: R11
T6: Verify `SITE.email` and `FRONTDESK_PAGE.how` steps are unchanged in `content.ts` and `config.ts`.
    depends_on: T5
    refs: R13, R12
T7: Ensure the Front Desk page renders the `offer` block using existing CSS classes.
    depends_on: T6
    refs: R14, R17
T8: Regenerate the parity oracle (`tests/fixtures/parity.json`) and verify the git diff scope.
    depends_on: T7
    refs: R15
T9: Update `llms.txt` and `llms-full.txt` snapshots to reflect new copy.
    depends_on: T8
    refs: R16

GATES
- Run `npm run build` to ensure successful compilation.
- Run `npm test` (vitest) for unit tests.
- Run `npx playwright test` for E2E tests (specifically departments.spec.ts, home.spec.ts, smoke.spec.ts).
- Verify `tests/fixtures/parity.json` diff only touches allowed fields with `_meta.counts` unchanged.
- Verify `src/lib/__snapshots__/llms-endpoint.spec.ts.snap` is updated correctly.
- Confirm no changes to `src/styles/site.css`, `src/config.ts` (email), or `FRONTDESK_PAGE.how` steps.