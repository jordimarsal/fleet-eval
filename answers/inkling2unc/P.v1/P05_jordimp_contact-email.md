FILES
tasks.md
harness/progress/impl_contact-email.md
src/config.ts
src/config.spec.ts
src/data/content.ts
src/lib/seo.ts
src/lib/seo.spec.ts
src/lib/llms.ts
src/lib/llms.spec.ts
src/lib/llms-endpoint.spec.ts
src/lib/__snapshots__/llms-endpoint.spec.ts.snap
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/pages/[lang]/departments/[dept].astro
src/pages/llms.txt.ts
src/pages/llms-full.txt.ts
tests/home.spec.ts
tests/departments.spec.ts

TASKS
T0: Record hello@jordimp.net deliverability evidence (MX/SPF + test message received; provider free tier named)
    depends_on: (none)
    refs: R6, R8
T1: Define CONTACT_EMAIL literal and reference it from both SITE configs
    depends_on: T0
    refs: R7, R1
T2: Point footer and front-desk email pills at mailto:hello@jordimp.net with localized labels unchanged
    depends_on: T1
    refs: R2
T3: Render hello@jordimp.net as the department contact row value and data-copy target (all locales)
    depends_on: T1
    refs: R3
T4: Set Person JSON-LD email to mailto:hello@jordimp.net
    depends_on: T1
    refs: R4
T5: Emit hello@jordimp.net in llms.txt / llms-full.txt builders; refresh llms snapshot via vitest -u and review address-only diff
    depends_on: T1
    refs: R5
T6: Update/extend specs (config, home, departments, seo, llms, llms-endpoint) asserting the new literal across all three locales
    depends_on: T2, T3, T4, T5
    refs: R1, R2, R3, R4, R5

GATES
- Evidence gate before any work: tasks.md Task 0 records MX/SPF dig output + inbox confirmation + provider free tier; if absent, keep feature blocked and run nothing else.
- vitest: src/config.spec.ts, src/lib/seo.spec.ts, src/lib/llms.spec.ts, src/lib/llms-endpoint.spec.ts (and existing content/quality suites)
- npm run qa:content scans src/ + tests/ sources and visible text of every dist/**/*.html for `gmail.com` — no match.
- Build site, then manual check: rg -n "gmail" src dist returns no match; also confirm hello@jordimp.net appears only where intended and does not leak into unintended copy.
- Playwright e2e: tests/home.spec.ts asserts footer pill href="mailto:hello@jordimp.net" on /en/, /es/, /ca/; tests/departments.spec.ts asserts contact-row value and data-copy equals the address in all three locales.
- Review snapshot diff from `vitest -u` under src/lib/__snapshots__/llms-endpoint.spec.ts.snap — address-only change.
- Completion gate re-checks R6/R8: evidence file exists with provider name + free tier noted, and recorded before feature is marked done.