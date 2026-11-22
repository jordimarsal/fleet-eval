FILES
src/content.config.ts
src/i18n/ui.ts
src/layouts/BaseLayout.astro
src/lib/i18n.spec.ts
src/pages/index.astro
src/styles/tokens.css

TASKS
T1: Configure strict TypeScript and Astro content collections
    depends_on: (none)
    refs: R1, R13
T2: Define design tokens in CSS variables
    depends_on: T1
    refs: R5
T3: Implement i18n logic with `en` fallback for missing keys
    depends_on: T1
    refs: R10, R11
T4: Update BaseLayout to include SEO tags, theme toggle script, and slots
    depends_on: T2, T3
    refs: R6, R7, R8, R9, R20
T5: Implement root redirect page
    depends_on: T4
    refs: R3, R4
T6: Verify project data integrity and locale parity
    depends_on: T3
    refs: R11, R14
T7: Run full build verification suite
    depends_on: T1, T2, T4, T5, T6
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21

GATES
- `npm run check` returns 0 errors/warnings.
- `npm run build` exits 0; removing a required field from a project JSON fails the build with a Zod error naming the file.
- `ls dist/en/index.html dist/es/index.html dist/ca/index.html` succeeds.
- `grep -q 'url=/en/' dist/index.html`.
- `find dist -name '*.html' ! -path 'dist/en/*' ! -path 'dist/es/*' ! -path 'dist/ca/*'` yields exactly one result (`dist/index.html`).
- `grep -q '#0b1220' src/styles/tokens.css && grep -q '#2dd4bf' src/styles/tokens.css && grep -q '#0d9488' src/styles/tokens.css && grep -q "'Inter Variable'" src/styles/tokens.css`.
- For each locale in en es ca: `grep -o "<html lang=\"$l\"" dist/$l/projects/index.html` matches once.
- `grep -F "localStorage.getItem('theme')" dist/en/projects/index.html` finds inline script before bundled scripts.
- `grep -F "matchMedia('(prefers-color-scheme: light)')" dist/en/projects/index.html` confirms fallback logic.
- `grep -rlF 'document.getElementById("theme-toggle")' dist/ | wc -l` equals 36; `grep -rlF 'localStorage.setItem(t,e)' dist/ | wc -l` equals 36.
- `npx vitest run` passes i18n spec (R10, R11).
- `grep -o 'hreflang="' dist/en/projects/index.html | wc -l` equals 3; `grep -q 'aria-current="true"' dist/en/projects/index.html`.
- `ls src/content/projects/*.json | wc -l` equals 11; `grep -l '"featured": true' src/content/projects/*.json | wc -l` equals 5.
- `grep -o 'href="/en/projects/[a-z0-9-]*/"' dist/en/projects/index.html | wc -l` equals 12 (index nav + 11 cards); featured slugs appear before secondary ones.
- `jq -r '.stack[]' src/content/projects/*.json | sort -u | wc -l` equals 42; `grep -o 'data-stack=' dist/en/projects/index.html | wc -l` equals 53; `grep -q 'data-reset' dist/en/projects/index.html`.
- Filter logic in minified HTML contains `e.hidden=t.size>0&&!s.some(d=>t.has(d))` and `setAttribute("aria-pressed",String(t.has(e.dataset.stack??"")))`; reset handler contains `t.clear(),o()`.
- `ls dist/en/projects | wc -l` equals 12; project detail pages contain expected content (problem, highlights, stack, metrics, github link).
- `grep -q 'rel="canonical" href="https://jordimp.net/en/projects/"' dist/en/projects/index.html`.
- `! grep -rq '609 940 649' dist/`.