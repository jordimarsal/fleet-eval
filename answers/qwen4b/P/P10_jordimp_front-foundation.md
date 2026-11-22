FILES
src/content/projects/index.json
src/i18n/ui.es.ts
src/i18n/ui.ca.ts
src/lib/i18n.ts
src/pages/[lang]/projects/index.astro
src/pages/[lang]/projects/[slug].astro
src/styles/tokens.css

TASKS
T1: Validate and scaffold locale-specific project index pages
    depends_on: (none)
    refs: R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21
T2: Implement Zod schema validation for content collections with localized fields
    depends_on: T1
    refs: R2, R3, R5, R10, R11, R13, R14
T3: Verify theme toggle logic and localStorage persistence in BaseLayout
    depends_on: T2
    refs: R7, R8, R9
T4: Ensure proper fallback behavior for missing localized values
    depends_on: T3
    refs: R10, R11
T5: Confirm correct rendering of LocaleSwitcher and hreflang links
    depends_on: T4
    refs: R12, R6, R20
T6: Validate HTML output structure and content accuracy
    depends_on: T5
    refs: R15, R16, R17, R18, R19

GATES
npm run check && npm run build && ls dist/en/index.html dist/es/index.html dist/ca/index.html && grep -q 'url=/en/' dist/index.html && find dist -name '*.html' ! -path 'dist/en/*' ! -path 'dist/es/*' ! -path 'dist/ca/*' | wc -l = 1 && grep -q '#0b1220' src/styles/tokens.css && grep -q '#2dd4bf' src/styles/tokens.css && grep -q '#0d9488' src/styles/tokens.css && grep -q "'Inter Variable'" src/styles/tokens.css && for l in en es ca; do grep -o "<html lang=\"$l\"" dist/$l/projects/index.html; done && grep -F "localStorage.getItem('theme')" dist/en/projects/index.html && grep -F "matchMedia('(prefers-color-scheme: light)')" dist/en/projects/index.html && grep -rlF 'document.getElementById("theme-toggle")' dist/ | wc -l = 36 && grep -rlF 'localStorage.setItem(t,e)' dist/ | wc -l = 36 && grep -o 'hreflang="' dist/en/projects/index.html | wc -l = 3 && grep -q 'aria-current="true"' dist/en/projects/index.html && grep -o 'data-stack=' dist/en/projects/index.html | wc -l = 53 && grep -q 'data-reset' dist/en/projects/index.html && grep -oF 'e.hidden=t.size>0&&!s.some(d=>t.has(d))' dist/en/projects/index.html && grep -oF 'setAttribute("aria-pressed",String(t.has(e.dataset.stack??"")))' dist/en/projects/index.html && grep -oF 't.clear(),o()' dist/en/projects/index.html && ls dist/en/projects | wc -l = 12 && grep -q 'github.com/jordimarsal/kafka-adapter-telemetry' dist/en/projects/kafka-adapter-telemetry/index.html && grep -q '>Problem<' dist/en/projects/kafka-adapter-telemetry/index.html && ! grep -rq '609 940 649' dist/ && npx vitest run