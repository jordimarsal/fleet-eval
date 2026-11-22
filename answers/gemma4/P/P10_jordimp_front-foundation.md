FILES
src/styles/tokens.css
src/i18n/ui.ts
src/content.config.ts
src/content/projects/bible-text-analysis.json
src/content/projects/codebaserag.json
src/content/projects/harness-standard.json
src/content/projects/interview-simulator.json
src/content/projects/kafka-adapter-telemetry.json
src/content/projects/mcp-transparent-png.json
src/content/projects/md-mermaid-pdf.json
src/content/projects/product-offers.json
src/content/projects/redis-toolkit.json
src/content/projects/rustcut.json
src/content/projects/spring-boot-casino.json
src/layouts/BaseLayout.astro
src/components/ThemeToggle.astro
src/pages/index.astro
src/pages/[lang]/index.astro
src/pages/[lang]/projects/index.astro
src/pages/[lang]/projects/[slug].astro

TASKS
T1: Define design tokens and strict TypeScript config
    depends_on: (none)
    refs: R1, R5
T2: Implement i18n dictionary parity and fallback logic
    depends_on: T1
    refs: R10, R11, R21
T3: Configure content collections with localized Zod schemas
    depends_on: T2
    refs: R2, R13
T4: Populate project data with exact requirements
    depends_on: T3
    refs: R14
T5: Implement BaseLayout with SEO, theme script, and slots
    depends_on: T1
    refs: R6, R7, R8, R20
T6: Implement ThemeToggle component and persistence
    depends_on: T5
    refs: R9
T7: Implement LocaleSwitcher with hreflang and aria-current
    depends_on: T2
    refs: R12
T8: Implement root redirect page and locale routing
    depends_on: T5
    refs: R3, R4
T9: Build Projects Index with sorting and stack filtering
    depends_on: T4, T7
    refs: R15, R16, R17, R18
T10: Build Project Detail pages
    depends_on: T3, T5
    refs: R19

GATES
- `grep -q 'astro/tsconfigs/strict' tsconfig.json && npm run check` (R1)
- `npm run build && test -d dist/en` (R2)
- `npm run build && ls dist/en/index.html dist/es/index.html dist/ca/index.html && grep -q 'url=/en/' dist/index.html` (R3)
- `find dist -name '*.html' ! -path 'dist/en/*' ! -path 'dist/es/*' ! -path 'dist/ca/*' | wc -l` should be 1 (R4)
- `grep -q '#0b1220' src/styles/tokens.css && grep -q '#2dd4bf' src/styles/tokens.css && grep -q '#0d9488' src/styles/tokens.css` (R5)
- `for l in en es ca; do grep -o "<html lang=\"$l\"" dist/$l/projects/index.html; done` (R6)
- `grep -F "localStorage.getItem('theme')" dist/en/projects/index.html` (R7)
- `grep -F "matchMedia('(prefers-color-scheme: light)')" dist/en/projects/index.html` (R8)
- `grep -rlF 'document.getElementById("theme-toggle")' dist/ | wc -l` and `grep -rlF 'localStorage.setItem(t,e)' dist/ | wc -l` (R9)
- `npx vitest run` for i18n fallback and key parity (R10, R11)
- `grep -o 'hreflang="' dist/en/projects/index.html | wc -l` and `grep -q 'aria-current="true"' dist/en/projects/index.html` (R12)
- `ls src/content/projects/*.json | wc -l` and featured count check (R14)
- `grep -o 'href="/en/projects/[a-z0-9-]*/"' dist/en/projects/index.html | wc -l` and order check (R15)
- `jq -r '.stack[]' src/content/projects/*.json | sort -u | wc -l` and filter button count (R16)
- `! grep -rq '609 940 649' dist/` (R21)