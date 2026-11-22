FILES
src/config.ts
src/data/content.ts
harness/progress/impl_contact-email.md

TASKS
T1: Provision free email forwarding for hello@jordimp.net and record evidence
    depends_on: (none)
    refs: R6, R8
T2: Define CONTACT_EMAIL literal in src/config.ts
    depends_on: T1
    refs: R7
T3: Update SITE.email in src/data/content.ts to reference CONTACT_EMAIL
    depends_on: T2
    refs: R7
T4: Update SEO JSON-LD email property to use SITE.email
    depends_on: T3
    refs: R4
T5: Update LLMs endpoint builders to emit SITE.email
    depends_on: T3
    refs: R5
T6: Verify all source and dist files no longer contain gmail.com or hardcoded old email
    depends_on: T5
    refs: R1

GATES
- `rg -n "gmail.com" src dist` returns empty output.
- `vitest run src/config.spec.ts src/lib/seo.spec.ts src/lib/llms.spec.ts src/lib/llms-endpoint.spec.ts` passes.
- `playwright test tests/home.spec.ts tests/departments.spec.ts` passes.
- `node scripts/qa-content.mjs` scans `dist/**/*.html` for visible text `hello@jordimp.net` and absence of `gmail.com`.
- Review `harness/progress/impl_contact-email.md` confirms free tier provider and MX/SPF evidence.