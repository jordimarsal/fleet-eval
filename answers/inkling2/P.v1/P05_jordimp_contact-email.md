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
src/config.spec.ts
src/lib/seo.spec.ts
src/lib/llms.spec.ts
src/lib/llms-endpoint.spec.ts
src/lib/__snapshots__/llms-endpoint.spec.ts.snap
tests/home.spec.ts
tests/departments.spec.ts
harness/progress/impl_contact-email.md

TASKS
T0: Record mailbox Task 0 evidence (MX/SPF dig + test message received + provider/tier) in impl_contact-email.md; feature remains blocked and no other task runs until this passes (gated R6, R8)
    depends_on: (none)
    refs: R6, R8
T1: Define CONTACT_EMAIL once in src/config.ts and route both config SITE.email and content data SITE.email through it; remove previous freeform contact literals along the way
    depends_on: T0
    refs: R7, R1
T2: Wire FooterDesk pill href and home building-page DeptPanel pill href to mailto using shared constant while keeping localized label; smoke tests on /en/, /es/, /ca/ keep assertions consistent
    depends_on: T1
    refs: R2
T3: Ensure front-desk department page renders hello@jordimp.net as contact-row value with copy button data-copy set from the shared constant (all locales)
    depends_on: T1
    refs: R3
T4: Set Person JSON-LD email property to mailto with quoted literal pinned by spec
    depends_on: T1
    refs: R4
T5: Emit agreed address in llms.txt contact block and llms-full.txt Contact line via builders; regenerate endpoint snapshot with vitest -u and review for address-only change
    depends_on: T1
    refs: R5
T6: Final sweep — confirm no `gmail` or prior-address occurrence remains under src/tests; report removal list so dist scan can pass at QA time
    depends_on: T2, T3, T4, T5
    refs: R1

GATES
- Task 0 evidence present in harness/progress/impl_contact-email.md covering both MX and SPF records plus received test message and provider/free tier selection (R6 + R8 human signoff before close)
- Feature must remain blocked if any of that evidence is absent; do not run further implementation tasks and keep leader blocking state until resolved
- Unit tests green: src/config.spec.ts (CONTACT_EMAIL === 'hello@jordimp.net'; CONFIG_SITE.email === CONTACT_EMAIL; CONTENT_SITE.email === CONTACT_EMAIL), src/lib/seo.spec.ts, src/lib/llms.spec.ts, src/lib/llms-endpoint.spec.ts including refreshed committed snapshot reviewed as address-only diff
- Full vitest suite plus Playwright assertions for /en/, /es/, /ca/ home pages (footer pill href via .footer-desk .pill[href^=mailto] with exact mailto string) and departments spec contact rows (first .contact-row__v text hello@jordimp.net and button.copy-btn[data-copy] only the shared value) across all three locales
- qa:content gate scans src/+tests sources and visible text of every dist/**/*.html for `gmail.com` returning zero matches after fresh build
- rg -n "gmail" src dist returns no match
- Manual confirmation that rg -n "hello@jordimp.net" src dist emits exactly one literal occurrence source per requirement usage and no other addresses remain except docs references unrelated to feature delivery