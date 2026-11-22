FILES
src/data/content.ts
src/data/types.ts
tests/fixtures/parity.json
src/lib/__snapshots__/llms-endpoint.spec.ts.snap

TASKS
T1: Update `SITE.role` and `SITE.tagline` in `src/data/content.ts`.
    depends_on: (none)
    refs: R1
T2: Add `offer` block to `FrontdeskPageContent` type definition in `src/data/types.ts`.
    depends_on: (none)
    refs: R4
T3: Populate `FRONTDESK_PAGE.offer` with English strings in `src/data/content.ts`.
    depends_on: T2
    refs: R4
T4: Localize `FRONTDESK_PAGE.offer` for Spanish (`es`) and Catalan (`ca`) in `src/data/content.ts`.
    depends_on: T3
    refs: R4
T5: Set `HOME.kicker`, `HOME.h1`, and `HOME.stand` in `src/data/content.ts`.
    depends_on: (none)
    refs: R1, R2, R3
T6: Set `PAGES.home.description` in `src/data/content.ts`.
    depends_on: T5
    refs: R9
T7: Set `FRONTDESK_PAGE.cta` in `src/data/content.ts`.
    depends_on: (none)
    refs: R5
T8: Set `DEPTS.frontdesk.line` and `DEPTS.frontdesk.intro` in `src/data/content.ts`.
    depends_on: (none)
    refs: R6, R7
T9: Set `FOOTER.line` in `src/data/content.ts`.
    depends_on: (none)
    refs: R8
T10: Set `PAGES.frontdesk.description` in `src/data/content.ts`.
    depends_on: (none)
    refs: R10
T11: Append conflict-of-interest line to `TELEMETRY_PAGE.intro` for all locales in `src/data/content.ts`.
    depends_on: (none)
    refs: R11
T12: Verify `SITE.email` remains unchanged in `src/config.ts` and `src/data/content.ts`.
    depends_on: (none)
    refs: R13
T13: Regenerate parity oracle using `npm run build && node scripts/distill-parity.mjs`.
    depends_on: T1-T12
    refs: R15
T14: Update `llms-endpoint.spec.ts.snap` to match new Front Desk/Telemetry content.
    depends_on: T13
    refs: R16

GATES
- `npm test`: All unit tests pass.
- `npm run build`: Build succeeds without errors.
- `npx playwright test`: All E2E tests pass, specifically verifying the rendered text on Home, Front Desk, and Telemetry pages matches requirements.
- `git diff tests/fixtures/parity.json`: Confirms changes are limited to title/description/h1/mainText of specified routes and `_meta.counts` is unchanged.
- `git diff src/lib/__snapshots__/llms-endpoint.spec.ts.snap`: Confirms llms snapshot update matches generated output.