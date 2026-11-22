ROLE: implementation planner. A feature has been approved. You get the
approved requirements and the repository file tree BEFORE implementation.
Write the implementation plan with EXACTLY these three sections:

FILES
<repo-relative path of every file you would create or modify, one per line>

TASKS
T1: <short title>
    depends_on: (none)
    refs: R1, R2
T2: <short title>
    depends_on: T1
    refs: R3
(... ordered so dependencies come first; every requirement must be covered
 by the refs of at least one task)

GATES
<the verification gates you would run before closing the feature>

--- APPROVED REQUIREMENTS ---
R1: The system shall not emit the string `gmail.com` in any source file under `src/`, any test file under `tests/`, or any built HTML file under `dist/`.  Verification: the unit test `src/config.spec.ts` pins the value; the `qa:content` gate scans both the `src/` + `tests/` sources and the visible text of every `dist/**/*.html` for `gmail.com`; the manual command `rg -n "gmail" src dist` returns no match.

R2: WHEN any page renders an email pill (the `FooterDesk` footer pill, or the front-desk `DeptPanel` pill on the home building page), the system shall set that pill's `href` to `mailto:hello@jordimp.net`, while the pill's visible label stays the localized `FOOTER.email` string in the page locale.  Verification: `tests/home.spec.ts` asserts, on each of `/en/`, `/es/`, `/ca/`, that `.footer-desk .pill[href^="mailto:"]` has `href="mailto:hello@jordimp.net"`.

R3: WHEN the front desk department page (`/{lang}/departments/front-desk/`) renders in any of the three locales, the system shall display `hello@jordimp.net` as the email contact-row value, and set the row's copy button `data-copy` to `hello@jordimp.net`.  Verification: `tests/departments.spec.ts` asserts, for all three locales, that the first `.contact-row .contact-row__v` has text `hello@jordimp.net` and that `button.copy-btn[data-copy]` equals `hello@jordimp.net` (the existing assertions already use `SITE.email`, which must resolve to the same value).

R4: WHEN a page emits the `Person` JSON-LD block, the system shall set its `email` property to `mailto:hello@jordimp.net`.  Verification: `src/lib/seo.spec.ts` pins `personJsonLd('en').email` to the literal.

R5: WHEN the site builds the `llms.txt` and `llms-full.txt` endpoints, the system shall emit `hello@jordimp.net` in the `llms.txt` contact block (`- Email:`) and in the `llms-full.txt` contact line (`Contact:`).  Verification: `src/lib/llms.spec.ts` and `src/lib/llms-endpoint.spec.ts` pin the literal in both builders; the committed oracle `src/lib/__snapshots__/llms-endpoint.spec.ts.snap` is refreshed with `vitest -u` and reviewed for the address-only change.

R6: WHILE the `hello@jordimp.net` mailbox is not verified deliverable — MX and SPF records present for `jordimp.net` and a forwarded test message received in the owner's inbox, with the evidence recorded in `harness/progress/impl_contact-email.md` — the system shall not emit `hello@jordimp.net` in `src/` or `dist/` (the contact-email feature stays `blocked`).  Verification: Task 0 of `tasks.md` records the evidence (the `dig` output for MX/SPF and a confirmation that the test message reached the inbox). If the evidence is absent, the `rg -n "hello@jordimp.net" src dist` check must be empty and no implementation task runs; the leader keeps the feature in `blocked`.

R7: The system shall define the canonical address exactly once as a `CONTACT_EMAIL` literal in `src/config.ts`, and have both `src/config.ts` `SITE.email` and `src/data/content.ts` `SITE.email` reference it.  Verification: `src/config.spec.ts` asserts `CONTACT_EMAIL === 'hello@jordimp.net'`, `CONFIG_SITE.email === CONTACT_EMAIL` and `CONTENT_SITE.email === CONTACT_EMAIL`.

R8: The receiving path for `hello@jordimp.net` shall be provisioned on a provider's free tier (no paid mail plan required) — either free custom-domain forwarding (e.g. ImprovMX, forwardemail.net, Cloudflare Email Routing) or a free real mailbox (e.g. Zoho Mail Free, DNSExit) — with the chosen provider and tier recorded in the Task 0 evidence.  Verification: `harness/progress/impl_contact-email.md` names the provider and states the free tier used (forwarding rule or mailbox plan); no billing/payment method is required. This is a human-evidence requirement, checked at the completion gate alongside R6.

--- FEATURE TITLE ---
Merge feature/f14-contact-email: publish hello@jordimp.net from a single CONTACT_EMAIL literal

--- REPOSITORY FILE TREE (before implementation) ---
.github/workflows/deploy.yml
.github/workflows/qa.yml
.github/workflows/quality.yml
.gitignore
AGENTS.md
README.md
astro.config.mjs
docs/architecture.md
docs/conventions.md
docs/deploy-dns-checklist.md
docs/iteration-protocol.md
docs/specs.md
docs/superpowers/plans/2026-09-16-portfolio-phase0-1-front.md
docs/superpowers/plans/2026-09-22-contact-email.md
docs/superpowers/plans/2026-09-22-external-brand-hygiene.md
docs/superpowers/plans/2026-09-22-external-public-artifacts.md
docs/superpowers/plans/2026-09-22-front-desk-positioning.md
docs/superpowers/plans/2026-09-22-millores-master.md
docs/superpowers/plans/2026-09-22-rag-eval-article.md
docs/superpowers/plans/2026-09-22-showcase-curation.md
docs/superpowers/specs/2026-09-16-portfolio-web-design.md
docs/verification.md
lighthouserc.json
package.json
playwright.config.ts
public/CNAME
public/cv/Jordi-Marcal-Poy-CV-EN.pdf
public/cv/Jordi-Marcal-Poy-CV-ES.pdf
public/robots.txt
scripts/check-links.mjs
scripts/collect-quality.mjs
scripts/distill-parity.mjs
scripts/qa-content.mjs
src/components/Analytics.astro
src/components/SEO.astro
src/components/site/BackBuilding.astro
src/components/site/Breadcrumb.astro
src/components/site/Building.astro
src/components/site/CaseMotif.astro
src/components/site/DeptCard.astro
src/components/site/DeptPanel.astro
src/components/site/DeptStrip.astro
src/components/site/FooterDesk.astro
src/components/site/Navbar.astro
src/components/site/ProjectCard.astro
src/components/site/SecHead.astro
src/components/site/Ticker.astro
src/config.ts
src/data/content.spec.ts
src/data/content.ts
src/data/quality.json
src/data/types.ts
src/env.d.ts
src/layouts/SiteLayout.astro
src/lib/__snapshots__/llms-endpoint.spec.ts.snap
src/lib/analytics.spec.ts
src/lib/analytics.ts
src/lib/building-svg.spec.ts
src/lib/building-svg.ts
src/lib/case-svg.spec.ts
src/lib/case-svg.ts
src/lib/dept-blocks.spec.ts
src/lib/dept-blocks.ts
src/lib/dept-svg.spec.ts
src/lib/dept-svg.ts
src/lib/font-face.spec.ts
src/lib/font-face.ts
src/lib/i18n.spec.ts
src/lib/i18n.ts
src/lib/links.spec.ts
src/lib/links.ts
src/lib/llms-endpoint.spec.ts
src/lib/llms.spec.ts
src/lib/llms.ts
src/lib/night-boot.spec.ts
src/lib/night-boot.ts
src/lib/paths.spec.ts
src/lib/paths.ts
src/lib/quality.spec.ts
src/lib/quality.ts
src/lib/seo.spec.ts
src/lib/seo.ts
src/lib/sitemap.spec.ts
src/lib/sitemap.ts
src/pages/404.astro
src/pages/[lang]/cv.astro
src/pages/[lang]/departments/[dept].astro
src/pages/[lang]/index.astro
src/pages/[lang]/projects/[slug].astro
src/pages/[lang]/projects/index.astro
src/pages/[lang]/writing/rag-eval-gate.astro
src/pages/index.astro
src/pages/llms-full.txt.ts
src/pages/llms.txt.ts
src/robots.spec.ts
src/scripts/building.ts
src/scripts/copy.ts
src/scripts/filter.ts
src/scripts/theme.ts
src/styles/contrast.spec.ts
src/styles/site.css
tests/cases.spec.ts
tests/cv.spec.ts
tests/departments.spec.ts
tests/fixtures/parity.json
tests/home.spec.ts
tests/interactions.spec.ts
tests/notfound.spec.ts
tests/projects.spec.ts
tests/seo-head.spec.ts
tests/smoke.spec.ts
tests/splash.spec.ts
tsconfig.json
vitest.config.ts

Write ONLY the plan (the three sections). No prose outside them.