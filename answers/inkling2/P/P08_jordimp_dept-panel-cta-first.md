FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Move department CTA (and operations CV button) above panel body in DeptPanel.astro
    depends_on: (none)
    refs: R1
T2: Add scoped filled-yellow CTA styles with fill-sweep disabled in site.css
    depends_on: T1
    refs: R1, R2
T3: De-emphasize and shrink project cards inside panels (no sweep overlay, reduced lift/shadow, smaller sizing)
    depends_on: T2
    refs: R3, R4
T4: Regenerate parity fixture and run verification scan over built output
    depends_on: T3
    refs: R5, R1, R2, R3, R4

GATES
npm run build succeeds; dist scan across dist/{en,es,ca}/index.html asserts the first .btn inside every dept-panel occurs before .cards / .ledger / .prose / .pills / .q-plaque-copy; built CSS contains `.dept-panel__cta .btn { background: var(--y1) }` with its ::before sweep disabled, plus the panel card rules disabling `.dept-panel .card::before`, reducing hover transform/shadow, and setting 12px padding / 8px gap / 0.88rem summary font while whole-card link height stays ≥ 44px; keyboard focus pass shows a visible indicator on panel cards and CTA buttons; visual pass on deployed home confirms filled CTAs above body copy in all seven departments; full `npx vitest run` green; `npm run distill:parity` produces tests/fixtures/parity.json whose diff covers only panel markup order; git diff limited to src/components/site/DeptPanel.astro, src/styles/site.css and tests/fixtures/parity.json (llms.txt / llms-full.txt content unchanged, /projects index styling untouched)