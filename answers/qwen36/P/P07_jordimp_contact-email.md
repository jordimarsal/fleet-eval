FILES
src/config.ts
src/data/content.ts
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/pages/[lang]/departments/[dept].astro
src/lib/seo.ts
src/lib/llms.ts
src/pages/llms.txt.ts
src/pages/llms-full.txt.ts
harness/progress/impl_contact-email.md
tasks.md
src/config.spec.ts
src/data/content.spec.ts
tests/home.spec.ts
tests/departments.spec.ts
src/lib/seo.spec.ts
src/lib/llms.spec.ts
src/lib/llms-endpoint.spec.ts
src/lib/__snapshots__/llms-endpoint.spec.ts.snap

TASKS
T0: Provision free-tier mailbox and record evidence
    depends_on: (none)
    refs: R6, R8
T1: Define CONTACT_EMAIL literal in src/config.ts and wire SITE.email references
    depends_on: T0
    refs: R7
T2: Replace gmail.com occurrences in src/data/content.ts with SITE.email reference
    depends_on: T1
    refs: R1, R3
T3: Update FooterDesk.astro to use SITE.email for pill href and label
    depends_on: T1
    refs: R2
T4: Update DeptPanel.astro to use SITE.email for pill href
    depends_on: T1
    refs: R2
T5: Update front-desk department page to render SITE.email in contact row
    depends_on: T1
    refs: R3
T6: Update Person JSON-LD email property via seo.ts
    depends_on: T1
    refs: R4
T7: Update llms.txt and llms-full.txt builders to emit SITE.email
    depends_on: T1
    refs: R5
T8: Run qa:content gate and verify rg -n "gmail" src dist returns no match
    depends_on: T7
    refs: R1
T9: Refresh llms-endpoint snapshot and review diff
    depends_on: T7
    refs: R5

GATES
- `rg -n "gmail\.com" src/ tests/` returns zero matches (R1)
- `rg -n "hello@jordimp\.net" src/ dist/` returns zero matches if Task 0 evidence is absent; otherwise confirms presence only where intended (R6)
- `vitest run src/config.spec.ts` passes all assertions on CONTACT_EMAIL, CONFIG_SITE.email, CONTENT_SITE.email (R7)
- `playwright test tests/home.spec.ts` asserts mailto:hello@jordimp.net hrefs for /en/, /es/, /ca/ (R2)
- `playwright test tests/departments.spec.ts` asserts contact-row text and copy button data-copy for front-desk in all three locales (R3)
- `vitest run src/lib/seo.spec.ts` pins personJsonLd('en').email to the literal (R4)
- `vitest run src/lib/llms.spec.ts src/lib/llms-endpoint.spec.ts` pins literals in both builders (R5)
- `git diff src/lib/__snapshots__/llms-endpoint.spec.ts.snap | grep hello@jordimp.net` shows address-only change (R5)
- `harness/progress/impl_contact-email.md` contains dig MX/SPF output, forwarded-test confirmation, provider name, and free-tier statement (R6, R8)