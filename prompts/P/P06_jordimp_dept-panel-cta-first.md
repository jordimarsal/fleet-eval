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
R1: WHEN a department panel renders on the home page, the system SHALL render the department CTA — and, for the operations panel, the CV button too — between the panel header/line and the panel body content (cards, pills, ledger, principles or inspections copy).  Verification: after `npm run build`, a scan over `dist/{en,es,ca}/index.html` asserts that inside every `dept-panel` the first `.btn` occurs before the panel body (` .cards`, `.ledger`, `.prose`, `.pills` or `.q-plaque-copy`).

R2: The department CTA buttons inside panels SHALL render with a filled yellow background (`var(--y1)`) at rest, with the fill-sweep overlay disabled, distinct from project cards.  Verification: built CSS contains the scoped rule (`.dept-panel__cta .btn { background: var(--y1) }` and its `::before` disabled); visual pass on the deployed home.

R3: WHEN a project card inside a department panel is hovered or focused, the system shall not render the yellow fill-sweep overlay; the card SHALL keep a visible hover/focus affordance (lift ≤ 2px, hard shadow ≤ 5px, focus outline unchanged).  Verification: built CSS contains the scoped rules disabling `.dept-panel .card::before` and reducing the hover transform/shadow inside panels; keyboard focus pass keeps a visible indicator.

R4: Project cards inside department panels SHALL render reduced sizing: padding 12px, gap 8px, summary font-size 0.88rem (currently 18px/16px padding, 12px gap, 0.92rem). Whole-card link heights stay ≥ 44px.  Verification: built CSS contains the scoped sizing rules; dist scan + visual pass; the F16 tap-target rule is respected (cards are multi-line links, height > 44px).

R5: Outside the department panels the system shall not change: `/projects` index cards keep their current styling; `llms.txt` / `llms-full.txt` content is unchanged; all existing tests stay green. The parity fixture (`tests/fixtures/parity.json`) SHALL be regenerated to match the new panel markup order.  Verification: full `npx vitest run` green; `npm run distill:parity` produces a fixture whose diff covers only panel markup order; `git diff` limited to `DeptPanel.astro`, `site.css` and fixtures.

--- FEATURE TITLE ---
feat(ui): department CTA above cards, filled; calmer smaller panel cards (F18)

--- REPOSITORY FILE TREE (before implementation) ---
.githooks/pre-push
.github/workflows/deploy.yml
.github/workflows/qa.yml
.github/workflows/quality.yml
.gitignore
AGENTS.md
README.md
astro.config.mjs
dashboard.yaml
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
public/harness/install.sh
public/robots.txt
scripts/check-links.mjs
scripts/collect-quality.mjs
scripts/distill-parity.mjs
scripts/install-hooks.mjs
scripts/lib/offhost-links.mjs
scripts/og-building.mjs
scripts/qa-content.mjs
scripts/sync-install-sh.sh
sonar-project.properties
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
src/config.spec.ts
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
src/lib/post-blocks.spec.ts
src/lib/post-blocks.ts
src/lib/quality.spec.ts
src/lib/quality.ts
src/lib/seo.spec.ts
src/lib/seo.ts
src/lib/sitemap.spec.ts
src/lib/sitemap.ts
src/pages/404.astro
src/pages/[lang]/blog/[slug].astro
src/pages/[lang]/blog/index.astro
src/pages/[lang]/contact.astro
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