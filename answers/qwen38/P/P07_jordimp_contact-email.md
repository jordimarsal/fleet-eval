FILES
src/config.ts
src/data/content.ts
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/pages/[lang]/departments/[dept].astro
src/lib/seo.ts
src/lib/llms.ts
src/lib/__snapshots__/llms-endpoint.spec.ts.snap
src/config.spec.ts
tests/home.spec.ts
tests/departments.spec.ts
harness/progress/impl_contact-email.md

TASKS
T1: Provision mailbox and record evidence
    depends_on: (none)
    refs: R6, R8
T2: Define CONTACT_EMAIL literal in config
    depends_on: T1
    refs: R7
T3: Update content data to reference CONTACT_EMAIL
    depends_on: T2
    refs: R7
T4: Implement email pill hrefs in FooterDesk and DeptPanel
    depends_on: T2
    refs: R2
T5: Update front-desk department page contact row
    depends_on: T2
    refs: R3
T6: Update Person JSON-LD email property
    depends_on: T2
    refs: R4
T7: Update llms.txt and llms-full.txt builders
    depends_on: T2
    refs: R5
T8: Refresh snapshots and update unit tests
    depends_on: T2, T3, T4, T5, T6, T7
    refs: R1, R2, R3, R4, R5, R7
T9: Verify no gmail.com leakage and final QA gates
    depends_on: T8
    refs: R1

GATES
- `rg -n "gmail" src dist` returns no match.
- `vitest run` passes all unit tests, including `src/config.spec.ts`, `src/lib/seo.spec.ts`, `src/lib/llms.spec.ts`.
- `playwright test` passes all e2e tests, including `tests/home.spec.ts` and `tests/departments.spec.ts`.
- `node scripts/qa-content.mjs` passes (scans for `gmail.com`).
- `harness/progress/impl_contact-email.md` contains MX/SPF dig output, inbox confirmation, and provider details.