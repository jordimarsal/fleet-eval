FILES
harness/progress/impl_contact-email.md
src/config.ts
src/data/content.ts
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/lib/seo.ts
src/lib/llms.ts
src/pages/llms-full.txt.ts
src/pages/llms.txt.ts
src/config.spec.ts
src/data/content.spec.ts
src/components/site/FooterDesk.spec.ts
src/components/site/DeptPanel.spec.ts
src/lib/seo.spec.ts
src/lib/llms.spec.ts
src/lib/llms-endpoint.spec.ts
tests/home.spec.ts
tests/departments.spec.ts

TASKS
T1: Provision free-tier mailbox and record evidence
    depends_on: (none)
    refs: R6, R8
T2: Define CONTACT_EMAIL literal in src/config.ts and wire SITE.email references
    depends_on: T1
    refs: R7
T3: Update FooterDesk to use mailto:hello@jordimp.net for href while keeping localized label
    depends_on: T2
    refs: R2
T4: Update DeptPanel to use mailto:hello@jordimp.net for href while keeping localized label
    depends_on: T2
    refs: R2
T5: Update front-desk department page contact row to display hello@jordimp.net with copy button
    depends_on: T2
    refs: R3
T6: Update Person JSON-LD email property to mailto:hello@jordimp.net
    depends_on: T2
    refs: R4
T7: Update llms.txt builder to emit hello@jordimp.net in contact block
    depends_on: T2
    refs: R5
T8: Update llms-full.txt builder to emit hello@jordimp.net in contact line
    depends_on: T2
    refs: R5
T9: Run qa-content gate and verify no gmail.com leakage across src/tests/dist
    depends_on: (none)
    refs: R1

GATES
- `rg -n "gmail\.com" src tests dist` returns zero matches
- `rg -n "hello@jordimp\.net" src dist` returns matches only where expected (config, components, lib, pages); grep of test files confirms assertions reference the literal
- `vitest run src/config.spec.ts src/data/content.spec.ts src/components/site/FooterDesk.spec.ts src/components/site/DeptPanel.spec.ts src/lib/seo.spec.ts src/lib/llms.spec.ts src/lib/llms-endpoint.spec.ts tests/home.spec.ts tests/departments.spec.ts` all pass
- `npm run build && rg -n "gmail\.com" dist` returns zero matches; `rg -n "hello@jordimp\.net" dist` shows the address in rendered HTML at expected locations
- `harness/progress/impl_contact-email.md` contains MX/SPF dig output and confirmation that a forwarded test message reached the owner's inbox