FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Restructure panel markup to place CTA (and CV button for operations) between header/line and body content
    depends_on: (none)
    refs: R1, R2
T2: Add scoped CSS: filled yellow CTA at rest with fill-sweep disabled; quieter hover on in-panel cards; reduced sizing rules
    depends_on: T1
    refs: R2, R3, R4
T3: Verify built output across locales and home layout (dist scan + visual checks), confirm F16 tap targets and unchanged /projects index styling
    depends_on: T2
    refs: R1, R4, R5
T4: Regenerate parity fixture from new markup order and run full test suite to confirm no collateral changes
    depends_on: T3
    refs: R5

GATES
npm run build succeeds and a scan of dist/{en,es,ca}/index.html asserts every .dept-panel's first .btn occurs before its body container (.cards, .ledger, .prose, .pills or .q-plaque-copy) — verify R1 via script over all three locale pages
Inspect built CSS for the scoped rule `.dept-panel__cta .btn { background: var(--y1) }` plus its disabled ::before overlay, and for the card rules disabling `.dept-panel .card::before`, lowered hover transform (≤ 2px lift) and shadow (≤ 5px), reduced padding (12px), gap (8px), summary font-size 0.88rem — verify R2–R4
Visual pass on deployed home (CTA above cards filled yellow; in-panel cards quieter with visible affordance) and keyboard focus pass keeping a visible indicator — verify R1–R3
Confirm F16 tap targets respected (multi-line whole-card links remain ≥ 44px) and that /projects index cards styling is unchanged — verify R4, R5
Regenerate parity fixture via npm run distill:parity; git diff limited to src/components/site/DeptPanel.astro, src/styles/site.css, tests/fixtures/parity.json; llms.txt / llms-full.txt content unchanged — verify R5
Full npx vitest run green, including dist scan + visual confirmation of panel markup order — final gate