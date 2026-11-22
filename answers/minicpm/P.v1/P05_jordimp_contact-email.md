FILES
src/config.ts
src/data/content.ts
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/lib/seo.ts
src/pages/llms.txt.ts
src/pages/llms-full.txt.ts
src/config.spec.ts
tests/home.spec.ts
tests/departments.spec.ts
src/lib/seo.spec.ts
src/lib/llms.spec.ts
src/lib/llms-endpoint.spec.ts
harness/progress/impl_contact-email.md

TASKS
T1: Define CONTACT_EMAIL literal and wire up SITE.email references
    depends_on: (none)
    refs: R7
T2: Update FooterDesk component to use CONTACT_EMAIL for mailto href
    depends_on: T1
    refs: R2
T3: Update DeptPanel component to use CONTACT_EMAIL for mailto href
    depends_on: T1
    refs: R2
T4: Update department page contact row to use CONTACT_EMAIL value and copy button
    depends_on: T1
    refs: R3
T5: Update Person JSON-LD generator to use CONTACT_EMAIL for email property
    depends_on: T1
    refs: R4
T6: Update llms.txt and llms-full.txt builders to emit CONTACT_EMAIL
    depends_on: T1
    refs: R5
T7: Add verification tests for all components and literals
    depends_on: T1
    refs: R1, R2, R3, R4, R5, R7
T8: Document MX/SPF verification and provider selection in harness progress file
    depends_on: (none)
    refs: R6, R8

GATES
- Run `rg -n "gmail.com" src tests dist` to ensure no `gmail.com` strings remain.
- Run `rg -n "hello@jordimp.net" src dist` to verify the new address is present only where intended (and absent if R6 blocked state is active).
- Execute `vitest` to pass all updated unit tests (`config.spec.ts`, `home.spec.ts`, `departments.spec.ts`, `seo.spec.ts`, `llms.spec.ts`, `llms-endpoint.spec.ts`).
- Run `npm run build` and scan `dist/**/*.html` visible text for `gmail.com` (must be empty) and verify `hello@jordimp.net` appears correctly in rendered pages.
- Verify `harness/progress/impl_contact-email.md` contains MX/SPF dig output, test message confirmation, and provider/tier documentation.
- Manual check: `rg -n "gmail" src dist` returns no matches.