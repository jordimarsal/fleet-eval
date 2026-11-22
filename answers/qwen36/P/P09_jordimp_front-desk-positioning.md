FILES
src/data/content.ts
src/data/types.ts
tests/departments.spec.ts
tests/fixtures/parity.json

TASKS
T1: Add `offer` block to `FrontdeskPageContent` in `src/data/types.ts`
    depends_on: (none)
    refs: R4
T2: Update `HOME.kicker`, `HOME.h1`, and `HOME.stand` across all locales in `src/data/content.ts`
    depends_on: T1
    refs: R1, R2, R3
T3: Localize `offer` strings (`openTitle`, `notOpenTitle`, `firmLine`, `howLine`, `deskLine`) and populate `openItems`/`notOpenItems` arrays for en/es/ca in `src/data/content.ts`
    depends_on: T1
    refs: R4
T4: Update `FRONTDESK_PAGE.cta` across all locales in `src/data/content.ts`
    depends_on: T2
    refs: R5
T5: Update `DEPTS.frontdesk.line` and `DEPTS.frontdesk.intro` across all locales in `src/data/content.ts`
    depends_on: T3
    refs: R6, R7
T6: Update `FOOTER.line` across all locales in `src/data/content.ts`
    depends_on: T2
    refs: R8
T7: Update `PAGES.home.description` plain-text form of R3 across all locales in `src/data/content.ts`
    depends_on: T2
    refs: R9
T8: Update `PAGES.frontdesk.description` across all locales in `src/data/content.ts`
    depends_on: T4
    refs: R10
T9: Append conflict-of-interest line to `DEPTS.telemetry.intro` for en/es/ca in `src/data/content.ts`
    depends_on: (none)
    refs: R11
T10: Verify no changes to `FRONTDESK_PAGE.how`, `SITE.email`, or `src/styles/site.css`
    depends_on: T2
    refs: R12, R13, R17
T11: Regenerate parity oracle via `npm run build && node scripts/distill-parity.mjs` and commit updated `tests/fixtures/parity.json`
    depends_on: T2, T4, T5, T9
    refs: R15
T12: Regenerate `llms.txt` and `llms-full.txt` and update llms unit snapshot
    depends_on: T5, T9
    refs: R16

GATES
- `npm run build` succeeds with zero warnings.
- `npm test` passes all unit tests (vitest).
- `npx playwright test` passes all e2e tests including `tests/departments.spec.ts` for the frontdesk department page rendering of the offer block (R14).
- `git diff tests/fixtures/parity.json` touches only title/description/h1/mainText on home routes, frontdesk routes, telemetry routes, and splash description; `_meta.counts` remains `{ "localeRoutes": 63, "pages": 65 }`.
- `git diff src/data/content.ts` confirms no changes to `FRONTDESK_PAGE.how`, `SITE.email`, or any stylesheet file.
- Rendered pages in en/es/ca contain the exact strings from R1–R10 (verified via parity oracle + manual spot-check on `/en/frontdesk/`).
- Telemetry intro includes the conflict-of-interest line in all three locales.
- `llms.txt` and `llms-full.txt` reflect updated Front Desk line/intro and Telemetry intro.