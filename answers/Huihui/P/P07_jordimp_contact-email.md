FILES
src/config.ts
src/data/content.ts
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/pages/[lang]/departments/[dept].astro
src/lib/seo.ts
src/lib/llms.ts
src/config.spec.ts
src/data/content.spec.ts
tests/home.spec.ts
tests/departments.spec.ts
src/lib/seo.spec.ts
src/lib/llms.spec.ts
src/lib/llms-endpoint.spec.ts
harness/progress/impl_contact-email.md

TASKS
T1: Define CONTACT_EMAIL and update config references
    depends_on: (none)
    refs: R7, R6
T2: Update content data to use canonical email
    depends_on: T1
    refs: R7, R1
T3: Implement email pill hrefs in Footer and DeptPanel
    depends_on: T1
    refs: R2
T4: Update Front Desk department page contact row
    depends_on: T1
    refs: R3
T5: Update SEO JSON-LD Person block
    depends_on: T1
    refs: R4
T6: Update LLMs text generation endpoints
    depends_on: T1
    refs: R5
T7: Update unit tests for new email literal
    depends_on: T1, T2, T5, T6
    refs: R1, R4, R5, R7
T8: Update E2E tests for email visibility and links
    depends_on: T3, T4
    refs: R2, R3
T9: Record implementation evidence and provider details
    depends_on: T1
    refs: R6, R8

GATES
- `npm run test` passes all unit tests.
- `npm run build` succeeds without errors.
- `rg -n "gmail" src dist` returns no matches (excluding node_modules).
- `rg -n "hello@jordimp.net" src dist` confirms the address is present in expected locations if unblocked, or empty if blocked per R6 logic (though R6 says it shall NOT emit while blocked, so this gate checks consistency with state). *Correction based on R6*: If blocked, `rg -n "hello@jordimp.net" src dist` must be empty. If unblocked, it should match. The plan assumes we are implementing the feature, so we verify presence where required by R2-R5.
- `node scripts/qa-content.mjs` passes, scanning `src/`, `tests/`, and `dist/**/*.html` for absence of `gmail.com`.
- Manual verification of `harness/progress/impl_contact-email.md` contains MX/SPF dig output and provider name (R6, R8).
- Playwright E2E suite (`npx playwright test`) passes, specifically verifying mailto links and contact rows in `home.spec.ts` and `departments.spec.ts`.