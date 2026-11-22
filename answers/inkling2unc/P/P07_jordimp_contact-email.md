FILES
harness/progress/impl_contact-email.md
src/config.ts
src/config.spec.ts
src/data/content.ts
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/pages/[lang]/departments/[dept].astro
src/lib/seo.ts
src/lib/seo.spec.ts
src/lib/llms.ts
src/lib/llms.spec.ts
src/lib/llms-endpoint.spec.ts
src/lib/__snapshots__/llms-endpoint.spec.ts.snap
tests/home.spec.ts
tests/departments.spec.ts

TASKS
T1: Confirm deliverability and record Task 0 evidence (mx/SPF via dig, forwarded test message receipt in owner inbox, free provider + tier per harness/progress/impl_contact-email.md)
    depends_on: (none)
    refs: R6, R8
T2: Define CONTACT_EMAIL literal once; point both config.ts and data/content.ts SITE.email at it; pin src/config.spec.ts
    depends_on: T1
    refs: R7
T3: Update pill rendering so FooterDesk and front-desk DeptPanel href is mailto:hello@jordimp.net while visible label stays localized FOOTER.email; add home.spec assertions on /en/ /es/ /ca/
    depends_on: T2
    refs: R2
T4: Ensure front-desk department page contact row shows hello@jordimp.net as value and button.copy-btn[data-copy] equals it; keep departments.spec using SITE.email resolving to the same address
    depends_on: T2
    refs: R3
T5: Set Person JSON-LD email to mailto:hello@jordimp.net; pin src/lib/seo.spec.ts personJsonLd('en').email to literal
    depends_on: T2
    refs: R4
T6: Emit hello@jordimp.net in llms.txt `- Email:` line and llms-full.txt `Contact:` line (both builders); update specs and refresh committed snapshot with vitest -u, review diff for address-only change
    depends_on: T2
    refs: R5
T7: Build site and verify content gate: run unit tests + qa:content scan of src/+tests/ and dist HTML text for gmail.com; confirm rg -n "gmail" src dist is empty
    depends_on: T3, T4, T5, T6
    refs: R1

GATES
pnpm test / vitest: config.spec.ts, content.spec.ts, seo.spec.ts, llms.spec.ts, llms-endpoint.spec.ts pass; full suite green.
Playwright e2e: home.spec.ts asserts .footer-desk .pill[href^="mailto:"] href="mailto:hello@jordimp.net" on /en/ /es/ /ca/; departments.spec.ts asserts contact row value and copy button data-copy equal the literal across all three locales.
Snapshot review: src/lib/__snapshots__/llms-endpoint.spec.ts.snap diff reviewed line-by-line (address-only).
Build + content QA: pnpm build succeeds; node scripts/qa-content.mjs scans src/+tests/ sources and visible text of every dist/**/*.html — no gmail.com anywhere; manual git-style check `rg -n "gmail" src dist` returns zero matches; also confirm rg for hello@jordimp.net shows no residual placeholder in src/ until evidence is recorded.
Evidence gate: harness/progress/impl_contact-email.md records MX/SPF dig output, test-message receipt confirmation, and provider + free tier named per R6/R8 before marking the feature unblocked; if absent, keep feature blocked with no implementation task run.