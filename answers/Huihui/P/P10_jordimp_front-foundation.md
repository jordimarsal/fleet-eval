FILES
src/styles/tokens.css
src/lib/i18n.ts
src/lib/i18n.spec.ts
src/content.config.ts
src/pages/index.astro
src/layouts/BaseLayout.astro
src/components/ThemeToggle.astro
src/components/LocaleSwitcher.astro
src/components/SEO.astro
src/pages/[lang]/projects/index.astro
src/pages/[lang]/projects/[slug].astro
harness/feature_list.json

TASKS
T1: Define design tokens and global styles
    depends_on: (none)
    refs: R5
T2: Implement i18n utilities with fallback logic
    depends_on: T1
    refs: R10, R11
T3: Configure content collections with Zod validation
    depends_on: T1
    refs: R13, R14
T4: Create root redirect page
    depends_on: T1
    refs: R3, R4
T5: Build BaseLayout with SEO and theme initialization
    depends_on: T1, T2
    refs: R6, R7, R8, R9, R20
T6: Implement LocaleSwitcher component
    depends_on: T5
    refs: R12
T7: Implement Projects Index page with filtering
    depends_on: T3, T5, T6
    refs: R15, R16, R17, R18
T8: Implement Project Detail page
    depends_on: T3, T5
    refs: R19, R20
T9: Finalize feature list status
    depends_on: T1, T2, T3, T4, T5, T6, T7, T8
    refs: R1

GATES
npm run check
npm run build && test -d dist/en
ls dist/en/index.html dist/es/index.html dist/ca/index.html && grep -q 'url=/en/' dist/index.html
find dist -name '*.html' ! -path 'dist/en/*' ! -path 'dist/es/*' ! -path 'dist/ca/*' | wc -l
grep -q '#0b1220' src/styles/tokens.css && grep -q '#2dd4bf' src/styles/tokens.css && grep -q '#0d9488' src/styles/tokens.css && grep -q "'Inter Variable'" src/styles/tokens.css
for l in en es ca; do grep -o "<html lang=\"$l\"" dist/$l/projects/index.html; done
grep -F "localStorage.getItem('theme')" dist/en/projects/index.html
grep -F "matchMedia('(prefers-color-scheme: light)')" dist/en/projects/index.html
grep -rlF 'document.getElementById("theme-toggle")' dist/ | wc -l
npx vitest run
jq -r '.stack[]' src/content/projects/*.json | sort -u | wc -l
grep -o 'data-stack=' dist/en/projects/index.html | wc -l
grep -oF 'e.hidden=t.size>0&&!s.some(d=>t.has(d))' dist/en/projects/index.html
grep -oF 'setAttribute("aria-pressed",String(t.has(e.dataset.stack??"")))' dist/en/projects/index.html
grep -oF 't.clear(),o()' dist/en/projects/index.html
ls dist/en/projects | wc -l
grep -q 'github.com/jordimarsal/kafka-adapter-telemetry' dist/en/projects/kafka-adapter-telemetry/index.html
grep -q '>Problem<' dist/en/projects/kafka-adapter-telemetry/index.html
grep -q 'rel="canonical" href="https://jordimp.net/en/projects/"' dist/en/projects/index.html
! grep -rq '609 940 649' dist/