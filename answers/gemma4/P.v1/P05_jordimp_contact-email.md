FILES
harness/progress/impl_contact-email.md
src/config.ts
src/data/content.ts
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/pages/[lang]/departments/[dept].astro
src/lib/seo.ts
src/lib/llms.ts
src/lib/__snapshots__/llms-endpoint.spec.ts.snap

TASKS
T1: Verify email deliverability and provisioning
    depends_on: (none)
    refs: R6, R8
T2: Define canonical CONTACT_EMAIL in config and content
    depends_on: T1
    refs: R7
T3: Update UI components to use CONTACT_EMAIL for pills and contact rows
    depends_on: T2
    refs: R2, R3
T4: Update SEO Person JSON-LD and LLMS endpoints
    depends_on: T2
    refs: R4, R5
T5: Final verification of source and build artifacts
    depends_on: T3, T4
    refs: R1

GATES
- Verify `harness/progress/impl_contact-email.md` contains MX/SPF `dig` evidence and provider details.
- Run `vitest` to ensure all unit tests (`config.spec.ts`, `content.spec.ts`, `seo.spec.ts`, `llms.spec.ts`, `llms-endpoint.spec.ts`) pass.
- Run `vitest -u` on snapshots and manually verify `src/lib/__snapshots__/llms-endpoint.spec.ts.snap` only changed the email string.
- Run `npm run qa:content` (or equivalent script calling `scripts/qa-content.mjs`) to scan `src/`, `tests/`, and `dist/**/*.html`.
- Execute `rg -n "gmail" src dist` and `rg -n "hello@jordimp.net" src dist` to confirm no leakage or incorrect hardcoding.