FILES
src/data/types.ts
src/data/content.ts
src/pages/[lang]/departments/[dept].astro
tests/fixtures/parity.json
src/lib/__snapshots__/llms-endpoint.spec.ts.snap

TASKS
T1: Add typed offer block to FrontdeskPageContent and set all copy strings in central data
    depends_on: (none)
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R13 (verify email constants unchanged — no edit), R12 (verify how steps untouched — no edit)
T2: Render the offer block on the Front Desk page (localized CTA tagline, openTitle + items, notOpenTitle + items, firmLine/howLine/deskLine) using existing classes only
    depends_on: T1
    refs: R5, R14, R17
T3: Regenerate parity fixture from built site and llms snapshot; verify diff scope
    depends_on: T2
    refs: R15, R16
GATES
- npm run build && node scripts/distill-parity.mjs, then confirm git diff touches only title/description/h1/mainText of home, frontdesk and telemetry routes plus splash description, with _meta.counts = { "localeRoutes": 63, "pages": 65 }
- npm test (vitest unit suite incl. llms endpoint snapshot update check) and playwright suites tests/departments.spec.ts, tests/home.spec.ts, tests/smoke.spec.ts pass
- localization completeness lint over all locales for HOME/FRONTDESK_PAGE/FOOTER/PAGES descriptions/offer strings (non-empty in en/es/ca, exact markup preservation `<mark>`/`<b>2017</b>`, offer openItems=3 / notOpenItems=1 per locale)
- assert FRONTDESK_PAGE.how steps and SITE.email/config email remain unchanged

Note: no new files are created — the plan reuses existing components and classes, adds no styles, and changes content data only.