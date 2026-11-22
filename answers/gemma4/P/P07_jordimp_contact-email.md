FILES
src/config.ts
src/data/content.ts
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/pages/[lang]/departments/[dept].astro
src/lib/seo.ts
src/lib/llms.ts
src/lib/llms-endpoint.ts
src/lib/__snapshots__/llms-endpoint.spec.ts.snap
harness/progress/impl_contact-email.md

TASKS
T1: Verify email deliverability and provisioning
    depends_on: (none)
    refs: R6, R8
T2: Define canonical CONTACT_EMAIL in config and content
    depends_on: T1
    refs: R7
T3: Update FooterDesk and DeptPanel to use mailto link
    depends_on: T2
    refs: R2
T4: Update Front Desk department page contact row
    depends_on: T2
    refs: R3
T5: Update SEO Person JSON-LD block
    depends_on: T2
    refs: R4
T6: Update LLMS text endpoints
    depends_on: T2
    refs: R5
T7: Final verification of string absence and test suite pass
    depends_on: T6
    refs: R1

GATES
- `rg -n "gmail" src dist` returns no matches (ensuring old email is gone).
- `rg -n "hello@jordimp.net" src dist` returns no matches (ensuring literal isn't hardcoded in source/dist, only via config/data references).
- `vitest run` passes all unit tests including `src/config.spec.ts`, `src/lib/seo.spec.ts`, `src/lib/llms.spec.ts`, and `src/data/content.spec.ts`.
- `playwright test` passes for `tests/home.spec.ts` and `tests/departments.spec.ts`.
- Manual check of `harness/progress/impl_contact-email.md` confirms MX/SPF evidence and provider details.
- `qa:content` gate (scanning `src/`, `tests/`, and `dist/**/*.html`) returns zero hits for `gmail.com`.