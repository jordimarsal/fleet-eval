FILES
harness/progress/impl_contact-email.md
src/config.ts
src/data/content.ts
src/lib/llms-endpoint.spec.ts
src/lib/llms.spec.ts
src/lib/seo.spec.ts
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/pages/[lang]/departments/[dept].astro

TASKS
T1: Provision free email forwarding and record evidence
    depends_on: (none)
    refs: R6, R8
T2: Define CONTACT_EMAIL literal in src/config.ts
    depends_on: T1
    refs: R7
T3: Wire SITE.email in src/config.ts and src/data/content.ts to CONTACT_EMAIL
    depends_on: T2
    refs: R7
T4: Update FooterDesk.astro to use SITE.email for mailto href
    depends_on: T3
    refs: R2
T5: Update DeptPanel.astro to use SITE.email for mailto href
    depends_on: T3
    refs: R2
T6: Update [dept].astro contact row to use SITE.email value and copy button
    depends_on: T3
    refs: R3
T7: Update seo.ts JSON-LD builder to use SITE.email
    depends_on: T3
    refs: R4
T8: Update llms.ts and llms-endpoint.ts builders to use SITE.email
    depends_on: T3
    refs: R5
T9: Run qa:content gate and verify no gmail.com leakage
    depends_on: T8
    refs: R1

GATES
- `rg -n "gmail.com" src dist` returns empty (R1)
- `vitest run tests/home.spec.ts` passes assertions for mailto hrefs on /en/, /es/, /ca/ (R2)
- `vitest run tests/departments.spec.ts` passes assertions for contact-row text and data-copy attributes (R3)
- `vitest run src/lib/seo.spec.ts` passes assertion for personJsonLd email property (R4)
- `vitest run src/lib/llms.spec.ts src/lib/llms-endpoint.spec.ts` passes with updated snapshots containing hello@jordimp.net (R5)
- `harness/progress/impl_contact-email.md` contains MX/SPF dig output, test message confirmation, and provider name (R6, R8)