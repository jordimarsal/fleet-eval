FILES
src/config.ts
src/data/content.ts
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/lib/seo.ts
src/lib/llms.ts
src/config.spec.ts
src/data/content.spec.ts
src/lib/seo.spec.ts
src/lib/llms.spec.ts
src/lib/llms-endpoint.spec.ts
src/lib/__snapshots__/llms-endpoint.spec.ts.snap
tests/home.spec.ts
tests/departments.spec.ts
harness/progress/impl_contact-email.md

TASKS
T1: Define CONTACT_EMAIL and update references
    depends_on: (none)
    refs: R7, R6
T2: Update UI components to use mailto link and correct email display
    depends_on: T1
    refs: R2, R3
T3: Update SEO and LLMs generation logic
    depends_on: T1
    refs: R4, R5
T4: Update unit tests for config, data, seo, and llms
    depends_on: T1
    refs: R1, R4, R5, R7
T5: Update integration/e2e tests for home and departments pages
    depends_on: T2
    refs: R2, R3
T6: Refresh snapshots and verify no gmail.com remains
    depends_on: T4, T5
    refs: R1, R5
T7: Record provisioning evidence in harness
    depends_on: (none)
    refs: R6, R8

GATES
- `npm run test` passes all unit and integration tests.
- `rg -n "gmail" src dist` returns no matches.
- `rg -n "hello@jordimp.net" src dist` is empty if Task 0 evidence (R6/R8) is not yet recorded; otherwise it confirms the new address.
- `vitest -u` has been run to update `src/lib/__snapshots__/llms-endpoint.spec.ts.snap`.
- Manual verification of `harness/progress/impl_contact-email.md` contains MX/SPF dig output, inbox confirmation, provider name, and free tier details.