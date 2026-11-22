FILES
src/styles/tokens.css
src/layouts/BaseLayout.astro
src/pages/index.astro
src/lib/i18n.ts
src/i18n/ui.ts
src/content.config.ts
src/env.d.ts
src/components/SEO.astro
src/components/LocaleSwitcher.astro
src/components/ThemeToggle.astro
src/components/ProjectCard.astro
src/pages/[lang]/projects/index.astro
src/pages/[lang]/projects/[slug].astro
tsconfig.json
package.json

TASKS
T1: Lock tsconfig to strict and verify zero errors/warnings
    depends_on: (none)
    refs: R1
T2: Define design tokens in src/styles/tokens.css with locked palette, fonts, spacing/radius/container/prose scales
    depends_on: T1
    refs: R5
T3: Wire global.css to import tokens.css and use CSS variables for body/card/muted/chips styling
    depends_on: T2
    refs: R5
T4: Implement BaseLayout with html[lang] slotting logo/nav/actions/default/footer; inject inline head script for theme from localStorage/prefers-color-scheme
    depends_on: T3
    refs: R6, R7, R8
T5: Add ThemeToggle component wired into BaseLayout actions slot; inline toggle handler sets data-theme and persists to localStorage
    depends_on: T4
    refs: R9
T6: Implement L() fallback helper in src/lib/i18n.ts returning en value when requested locale lacks a key
    depends_on: T4
    refs: R10
T7: Enforce UiKey parity across en/es/ca dictionaries — no empty strings, compile-time Record<UiKey,string> on es/ca
    depends_on: T6
    refs: R11
T8: Build LocaleSwitcher rendering one link per locale with hreflang and aria-current="true" on active
    depends_on: T7
    refs: R12
T9: Define typed Astro content collections (projects/experience/skills) with Zod schemas and localized() requiring en+es+ca values
    depends_on: T8
    refs: R13
T10: Ship 11 project entries (5 featured, 6 not) in src/content/projects/*.json
    depends_on: T9
    refs: R14
T11: Render projects index through BaseLayout with featured/secondary sections sorted featured-first then year desc then name asc
    depends_on: T10
    refs: R15
T12: Add stack filter buttons (All + one per distinct tag) to projects index with data-stack and aria-pressed state
    depends_on: T11
    refs: R16
T13: Inline toggle handler for stack filters updating card visibility and button aria-pressed together
    depends_on: T12
    refs: R17
T14: Wire reset (All) button clearing active tags and reapplying
    depends_on: T13
    refs: R18
T15: Emit individual project pages rendering name/year/localized summary/problem/highlights/stack/metrics/github link
    depends_on: T14
    refs: R19
T16: Inject SEO component into BaseLayout providing title/meta description/canonical pointing at https://jordimp.net/{lang}/{path}
    depends_on: T15
    refs: R20
T17: Strip owner phone number from all built pages; ban 9-digit runs in ui dictionary strings via vitest
    depends_on: T16
    refs: R21

GATES
- `npm run check` reports 0 errors, 0 warnings (R1)
- `npm run build && test -d dist/en` succeeds; removing a required field from any src/content/projects/*.json causes Zod failure naming the file (R2)
- `ls dist/en/index.html dist/es/index.html dist/ca/index.html` exists; `grep -q 'url=/en/' dist/index.html` passes (R3)
- `find dist -name '*.html' ! -path 'dist/en/*' ! -path 'dist/es/*' ! -path 'dist/ca/*'` yields exactly one result: dist/index.html (R4)
- `grep -q '#0b1220' src/styles/tokens.css && grep -q '#2dd4bf' src/styles/tokens.css && grep -q '#0d9488' src/styles/tokens.css && grep -q "'Inter Variable'" src/styles/tokens.css` (R5)
- For each locale l ∈ {en,es,ca}: `grep -o "<html lang=\"$l\"" dist/$l/projects/index.html` matches once (R6)
- `grep -F "localStorage.getItem('theme')" dist/en/projects/index.html` finds inline head script before bundled scripts (R7)
- `grep -F "matchMedia('(prefers-color-scheme: light)')" dist/en/projects/index.html` confirms stored ?? matchMedia pattern (R8)
- `grep -rlF 'document.getElementById("theme-toggle")' dist/ | wc -l` → 36; `grep -rlF 'localStorage.setItem(t,e)' dist/ | wc -l` → 36 (R9)
- `npx vitest run` passes i18n spec for en fallback on missing locale (R10)
- `npm run check` compiles es/ca as Record<UiKey,string>; `npx vitest run` verifies key parity and non-empty values (R11)
- `grep -o 'hreflang="' dist/en/projects/index.html | wc -l` → 3; `grep -q 'aria-current="true"' dist/en/projects/index.html` (R12)
- `npm run build` green; deleting es key of a localized field in any content JSON fails the build (R13)
- `ls src/content/projects/*.json | wc -l` → 11; `grep -l '"featured": true' src/content/projects/*.json | wc -l` → 5 (R14)
- `grep -o 'href="/en/projects/[a-z0-9-]*/"' dist/en/projects/index.html | wc -l` → 11 cards; ordering verified featured before secondary (R15)
- `jq -r '.stack[]' src/content/projects/*.json | sort -u | wc -l` → 42 distinct stacks; `grep -o 'data-stack=' dist/en/projects/index.html | wc -l` → 53; `grep -q 'data-reset' dist/en/projects/index.html` (R16)
- Inline module script contains both card visibility and aria-pressed update logic: `grep -oF 'e.hidden=t.size>0&&!s.some(d=>t.has(d))' dist/en/projects/index.html` → 1; `grep -oF 'setAttribute("aria-pressed",String(t.has(e.dataset.stack??"")))' dist/en/projects/index.html` → 1 (R17)
- `grep -oF 't.clear(),o()' dist/en/projects/index.html` → 1 match for reset handler (R18)
- `ls dist/en/projects | wc -l` → 12; `grep -q 'github.com/jordimarsal/kafka-adapter-telemetry' dist/en/projects/kafka-adapter-telemetry/index.html`; `grep -q '>Problem<' dist/en/projects/kafka-adapter-telemetry/index.html` (R19)
- `grep -q 'rel="canonical" href="https://jordimp.net/en/projects/"' dist/en/projects/index.html` (R20)
- `! grep -rq '609 940 649' dist/` passes; `npx vitest run` bans any 9-digit run inside ui dictionary strings (R21)