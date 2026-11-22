FILES
src/styles/tokens.css
src/lib/i18n.ts
src/content.config.ts
src/pages/index.astro
src/layouts/BaseLayout.astro
src/components/ThemeToggle.astro
src/components/LocaleSwitcher.astro
src/components/ProjectCard.astro
src/pages/[lang]/projects/index.astro
src/pages/[lang]/projects/[slug].astro
src/i18n/ui.ts
src/lib/i18n.spec.ts
harness/specs/f1-front-foundation/requirements.md
harness/feature_list.json

TASKS
T1: Define design tokens and global styles
    depends_on: (none)
    refs: R5
T2: Implement i18n utilities and UI dictionaries with tests
    depends_on: T1
    refs: R10, R11, R21
T3: Configure content collections with Zod schemas
    depends_on: T1
    refs: R13, R14
T4: Implement BaseLayout with SEO, theme toggle, and locale switcher
    depends_on: T1, T2
    refs: R6, R7, R8, R9, R12, R20
T5: Create root redirect page
    depends_on: T1
    refs: R3, R4
T6: Implement Projects Index page with filtering logic
    depends_on: T3, T4
    refs: R15, R16, R17, R18
T7: Implement Project Detail pages
    depends_on: T3, T4
    refs: R19
T8: Finalize TypeScript configuration and build verification
    depends_on: T2, T3, T4, T5, T6, T7
    refs: R1, R2

GATES
npm run check
npm run build && test -d dist/en
ls dist/en/index.html dist/es/index.html dist/ca/index.html && grep -q 'url=/en/' dist/index.html
find dist -name '*.html' ! -path 'dist/en/*' ! -path 'dist/es/*' ! -path 'dist/ca/*' | wc -l # Expect 1 (root index)
grep -q '#0b1220' src/styles/tokens.css && grep -q '#2dd4bf' src/styles/tokens.css && grep -q '#0d9488' src/styles/tokens.css && grep -q "'Inter Variable'" src/styles/tokens.css
for l in en es ca; do grep -o "<html lang=\"$l\"" dist/$l/projects/index.html; done
grep -F "localStorage.getItem('theme')" dist/en/projects/index.html
grep -F "matchMedia('(prefers-color-scheme: light)')" dist/en/projects/index.html
grep -rlF 'document.getElementById("theme-toggle")' dist/ | wc -l # Expect 36
npx vitest run
jq -r '.stack[]' src/content/projects/*.json | sort -u | wc -l # Expect 42
grep -o 'data-stack=' dist/en/projects/index.html | wc -l # Expect 53
ls src/content/projects/*.json | wc -l # Expect 11
grep -l '"featured": true' src/content/projects/*.json | wc -l # Expect 5
ls dist/en/projects | wc -l # Expect 12
grep -q 'github.com/jordimarsal/kafka-adapter-telemetry' dist/en/projects/kafka-adapter-telemetry/index.html
! grep -rq '609 940 649' dist/