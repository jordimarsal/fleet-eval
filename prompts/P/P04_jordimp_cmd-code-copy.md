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
R1: WHEN a rendered highlight contains the install command, the system SHALL wrap the command in a `<code>` element styled monospace with a background and border that distinguish it from surrounding prose.  Verification: dist scan of the project detail page and the tooling department page (en/es/ca) finds `<code` wrapping the command; built CSS contains the `.cmd-copy` rules (mono font, background, border).

R2: WHEN the pointer hovers the code element — or it receives keyboard focus — the system SHALL reveal a copy affordance (icon) that copies the exact command text to the clipboard on activation, with visible "copied" feedback.  Verification: markup contains the `data-copy` affordance bound to the command (both the code text and its copy control); manual pass: hover shows the icon, click writes the command to the clipboard and shows the copied label (existing `[data-copy]` machinery).

R3: The rendered line SHALL keep the command as selectable plain text, and the content source (`content.ts`) SHALL remain unchanged — the F17 content assertions stay green and `llms.txt`/`llms-full.txt` output is byte-identical.  Verification: full `npx vitest run` green without modifying F17 tests; `git diff` limited to the new util/spec/component, the two rendering surfaces, site.css and the parity fixture; llms snapshot untouched.

R4: The segmentation SHALL be a pure, unit-tested helper: given a highlight line, it returns the text before and after the command plus the command itself; lines without the command pass through unchanged; HTML-escaping stays the responsibility of the rendering components (Astro's default), not the helper.  Verification: colocated `cmd-code.spec.ts` lands red first, then green: match case, no-match case, command at line start/end.

--- FEATURE TITLE ---
feat(content): copyable install command in highlight lines (F19)

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