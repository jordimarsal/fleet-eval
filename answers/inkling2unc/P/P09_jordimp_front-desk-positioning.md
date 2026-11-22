FILES
src/data/types.ts
src/data/content.ts
src/pages/[lang]/departments/[dept].astro
tests/fixtures/parity.json
src/lib/__snapshots__/llms-endpoint.spec.ts.snap

TASKS
T1: Add typed `offer` block to FrontdeskPageContent
    depends_on: (none)
    refs: R4
T2: Set home, front desk, footer, description and telemetry copy across en/es/ca (leaving FRONTDESK_PAGE.how steps and contact emails untouched)
    depends_on: T1
    refs: R1, R2, R3, R5, R6, R7, R8, R9, R10, R11, R12, R13
T3: Render the offer block on the Front Desk department page in all locales
    depends_on: T2
    refs: R14, R17
T4: Regenerate parity fixture and committed llms snapshot from the built site
    depends_on: T3
    refs: R15, R16
GATES
- npm run build && node scripts/distill-parity.mjs; confirm `git diff --stat tests/fixtures/parity.json` touches only title/description/h1/mainText of the three home routes, three Front Desk routes, three Telemetry routes and the splash description, with _meta.counts still { "localeRoutes": 63, "pages": 65 }; re-verify underline that src/styles/site.css is unchanged via git status and grep for styles
- npx astro check / typecheck (or project's lint+type gate as configured) plus unit suite (vitest) covering content shape — frontdesk offers non-empty, es/ca localized, 3 open items + 1 not-open item per locale
- Playwright departments/home/smoke specs pass locally (tests/departments.spec.ts, tests/home.spec.ts, tests/smoke.spec.ts) proving rendered offer block strings, `<mark>` in h1, `<b>2017</b>` in stand, preserved how steps, email constants unchanged at jordi.marsal@gmail.com in both src/data/content.ts and src/config.ts, and llms endpoints carrying updated line/intro values
- npm run test (full e2e including parity fixture assertion and llms snapshot match) green before closing