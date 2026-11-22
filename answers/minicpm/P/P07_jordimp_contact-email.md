FILES
src/config.ts
src/data/content.ts
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/lib/seo.ts
src/pages/llms.txt.ts
src/pages/llms-full.txt.ts
tests/home.spec.ts
tests/departments.spec.ts
src/lib/llms.spec.ts
src/lib/llms-endpoint.spec.ts
src/lib/seo.spec.ts
harness/progress/impl_contact-email.md

TASKS
T1: Provision external email forwarding and record evidence
    depends_on: (none)
    refs: R6, R8
T2: Define CONTACT_EMAIL literal and wire SITE.email references
    depends_on: T1
    refs: R7
T3: Update FooterDesk pill href to mailto:hello@jordimp.net
    depends_on: T2
    refs: R2
T4: Update DeptPanel pill href to mailto:hello@jordimp.net
    depends_on: T2
    refs: R2
T5: Update front-desk department page contact row value and copy button
    depends_on: T2
    refs: R3
T6: Update Person JSON-LD email property to mailto:hello@jordimp.net
    depends_on: T2
    refs: R4
T7: Update llms.txt and llms-full.txt endpoints to emit hello@jordimp.net
    depends_on: T2
    refs: R5
T8: Run verification gates and update snapshots
    depends_on: T7
    refs: R1, R2, R3, R4, R5, R7

GATES
- `rg -n "gmail.com" src tests dist` returns no matches
- `rg -n "hello@jordimp.net" src dist` returns matches only in intended files
- `vitest run src/config.spec.ts src/data/content.spec.ts tests/home.spec.ts tests/departments.spec.ts src/lib/seo.spec.ts src/lib/llms.spec.ts src/lib/llms-endpoint.spec.ts` passes all assertions
- `npm run build` completes successfully and `dist/**/*.html` contains no `gmail.com`
- `harness/progress/impl_contact-email.md` contains MX/SPF dig output, test message confirmation, and provider/tier documentation