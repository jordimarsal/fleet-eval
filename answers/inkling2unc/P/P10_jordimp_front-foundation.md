FILES
tsconfig.json
package.json
src/styles/tokens.css
src/lib/i18n.ts
src/lib/i18n.spec.ts
src/i18n/ui.ts
src/content.config.ts
src/layouts/BaseLayout.astro
src/components/SEO.astro
src/components/ThemeToggle.astro
src/components/LocaleSwitcher.astro
src/components/ProjectCard.astro
src/pages/index.astro
src/pages/[lang]/index.astro
src/pages/[lang]/projects/index.astro
src/pages/[lang]/projects/[slug].astro
harness/feature_list.json
docs/specs.md

TASKS
T1: TypeScript strict config, package scripts, and toolchain
    depends_on: (none)
    refs: R1

T2: Design tokens with locked palette values
    depends_on: T1
    refs: R5

T3: i18n core — L() fallback, locale typing, and runtime spec
    depends_on: T1
    refs: R10

T4: ui dictionary key parity (UiKey exactly en/es/ca, no empty strings) plus vitest checks
    depends_on: T3
    refs: R11, R21

T5: Content collections + localized() helper schema validation
    depends_on: T1
    refs: R13

T6: Root redirect page emitting dist/index.html meta-refresh to /en/
    depends_on: T1
    refs: R3, R4

T7: BaseLayout foundation — html[lang], logo/nav/actions slots, inline pre-paint theme script, canonical title/description, page scoping
    depends_on: T2, T3, T4
    refs: R2, R3, R4, R6, R7, R8, R9, R20, R21

T8: LocaleSwitcher hreflang links with aria-current on active locale
    depends_on: T7
    refs: R12

T9: Projects content data audit — exactly 11 entries with 5 featured
    depends_on: T5
    refs: R14, R2

T10: Projects index page — sort order, featured/secondary sections, filter buttons (All + stacks), inlined filter behavior
    depends_on: T7, T8, T9, T3
    refs: R15, R16, R17, R18

T11: Project detail pages rendering localized fields and repo link
    depends_on: T7, T9, T3
    refs: R19

GATES
npm run check → 0 errors / 0 warnings
grep -q 'astro/tsconfigs/strict' tsconfig.json && npm run check
npm run build (exit 0; Zod validation of every projects entry) then test -d dist/en
Negative: remove a required field from src/content/projects/*.json → build fails with named Zod error; restore file
ls dist/en/index.html dist/es/index.html dist/ca/index.html && grep -q 'url=/en/' dist/index.html
find dist -name '*.html' ! -path 'dist/en/*' ! -path 'dist/es/*' ! -path 'dist/ca/*' → exactly dist/index.html
grep -q '#0b1220' src/styles/tokens.css && grep -q '#2dd4bf' src/styles/tokens.css && grep -q '#0d9488' src/styles/tokens.css && grep -q "'Inter Variable'" src/styles/tokens.css
for l in en es ca; do grep -o "<html lang=\"$l\"" dist/$l/projects/index.html; done (1 match each)
grep -F "localStorage.getItem('theme')" dist/en/projects/index.html and before any bundled script
grep -F "matchMedia('(prefers-color-scheme: light)')" — actually check literal skeleton: the inlined head script implements stored ?? prefers-color-scheme fallback on every BaseLayout page
Theme toggle counts: grep -rlF 'document.getElementById("theme-toggle")' dist/ | wc -l → 36 and grep -rlF 'localStorage.setItem(t,e)' dist/ | wc -l → 36 (regenerate after layout changes so count matches built pages)
npx vitest run (L() missing-locale fallback + UiKey parity + non-empty values + no 9-digit phone numbers)
Negative: delete es key of a localized field in any content JSON → npm run build fails with Zod error naming file; restore
ls src/content/projects/*.json | wc -l → 11; grep -l '"featured": true' src/content/projects/*.json | wc -l → 5
find five featured slugs appear before secondary ones: grep -o 'href="/en/projects/[a-z0-9-]*/"' dist/en/projects/index.html (count = 11 cards, ordering verified between sections)
jq -r '.stack[]' src/content/projects/*.json | sort -u | wc -l → 42; grep -o 'data-stack=' dist/en/projects/index.html | wc -l → 53; grep -q 'data-reset' dist/en/projects/index.html
grep -oF 'e.hidden=t.size>0&&!s.some(d=>t.has(d))' dist/en/projects/index.html → 1 and grep -oF 'setAttribute("aria-pressed",String(t.has(e.dataset.stack??"")))' → 1 and grep -oF 't.clear(),o()' → 1 (adjust for actual esbuild output if identifiers differ; assert behavior via tests)
ls dist/en/projects | wc -l → 12; grep -q 'github.com/jordimarsal/kafka-adapter-telemetry' dist/en/projects/kafka-adapter-telemetry/index.html && grep -q '>Problem<' the same page
grep -q 'rel="canonical" href="https://jordimp.net/en/projects/"' dist/en/projects/index.html on a sample of pages per locale
! grep -rq '609 940 649' dist/ and vitest phone-number ban over ui strings
harness/tools/validate-feature-list.py --json harness/feature_list.json and check-traceability pass for this feature once impl notes are written