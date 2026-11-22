FILES
tsconfig.json
src/styles/tokens.css
src/content.config.ts
src/lib/i18n.ts
src/i18n/ui.ts
src/layouts/BaseLayout.astro
src/pages/index.astro
src/components/LocaleSwitcher.astro
src/components/ThemeToggle.astro
src/pages/[lang]/index.astro
src/pages/[lang]/projects/index.astro
src/pages/[lang]/projects/[slug].astro
vitest.config.ts
src/lib/i18n.spec.ts

TASKS
T1: Configure strict TypeScript and build baseline
    depends_on: (none)
    refs: R1, R3, R4
T2: Implement design tokens in CSS
    depends_on: T1
    refs: R5
T3: Validate content collections with Zod schemas
    depends_on: T1
    refs: R2, R13
T4: Implement i18n localization with English fallback
    depends_on: T1
    refs: R10, R11
T5: Build BaseLayout with SEO and theme script
    depends_on: T2, T3, T4
    refs: R6, R7, R8, R9, R20
T6: Implement root redirect page
    depends_on: T5
    refs: R3, R4
T7: Implement LocaleSwitcher component
    depends_on: T5
    refs: R12
T8: Implement ThemeToggle functionality
    depends_on: T5
    refs: R9
T9: Populate project content entries
    depends_on: T3
    refs: R14
T10: Implement projects index page with filtering
    depends_on: T5, T7, T8, T9
    refs: R15, R16, R17, R18
T11: Implement project detail pages
    depends_on: T5, T7, T8, T9
    refs: R19
T12: Security and compliance verification
    depends_on: T10, T11
    refs: R21

GATES
- Run `npm run check` to verify 0 TypeScript errors/warnings (R1).
- Run `npm run build` to verify successful build and Zod validation (R2).
- Verify emitted files: `dist/en/index.html`, `dist/es/index.html`, `dist/ca/index.html`, and `dist/index.html` with redirect (R3).
- Verify no HTML pages exist outside locale-prefixed routes except root redirect (R4).
- Verify `src/styles/tokens.css` contains required design token values (R5).
- Verify `BaseLayout` renders correct `html[lang]` attributes for all locales (R6).
- Verify inline theme script in `<head>` uses `localStorage` and `prefers-color-scheme` (R7, R8).
- Verify theme toggle script is inlined and persists state (R9).
- Run `npx vitest run` to verify i18n fallback and UI key parity (R10, R11).
- Verify `LocaleSwitcher` renders correct `hreflang` and `aria-current` attributes (R12).
- Verify content collections validate at build time with negative tests (R13).
- Verify exactly 11 project entries with correct featured counts (R14).
- Verify projects index renders 11 cards with correct sorting and filter buttons (R15, R16).
- Verify stack filter logic updates card visibility and button states (R17, R18).
- Verify project detail pages render all required fields and links (R19).
- Verify SEO meta tags (`title`, `description`, `canonical`) are present (R20).
- Verify no phone number appears in built files (R21).