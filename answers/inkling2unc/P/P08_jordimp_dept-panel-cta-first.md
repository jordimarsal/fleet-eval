FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Reorder panel markup so the department CTA renders above panel body content
    depends_on: (none)
    refs: R1
T2: Scope filled-yellow CTA styling and disable its fill-sweep inside panels
    depends_on: (none)
    refs: R2
T3: Calm down in-panel project cards (disable sweep overlay; reduce lift/shadow; keep focus outline; apply reduced sizing)
    depends_on: (none)
    refs: R3, R4
T4: Build, verify dist output, regenerate parity fixture and confirm suite is green
    depends_on: T1, T2, T3
    refs: R1, R2, R3, R4, R5

GATES
- `npm run build` succeeds for en/es/ca locales.
- Scan of `dist/{en,es,ca}/index.html` asserts that inside every `dept-panel`, the first `.btn` appears before any panel body container (`.cards`, `.ledger`, `.prose`, `.pills`, `.q-plaque-copy`) — both department CTAs and operations CV button covered.
- Built CSS contains the scoped rule `.dept-panel__cta .btn { background: var(--y1) }` with its `::before` fill-sweep disabled.
- Built CSS contains scoped rules disabling `.dept-panel .card::before`, reducing the hover transform to ≤2px and shadow to ≤5px inside panels while the keyboard focus outline remains unchanged; visual pass on deployed home.
- Built CSS contains scoped sizing rules (padding 12px, gap 8px, summary font-size 0.88rem) applied only within `.dept-panel`; cards remain multi-line links taller than 44px (F16 tap-target respected); dist scan + visual pass recorded.
- Outside panels unchanged: /projects index card styling untouched in code review of diff; `llms.txt`/`llms-full.txt` content unmodified (no source change); `git status`/diff limited to `DeptPanel.astro`, `site.css`, `tests/fixtures/parity.json`.
- `npx vitest run` fully green.
- `npm run distill:parity` produces a fixture whose diff covers only panel markup order; `tests/fixtures/parity.json` committed from that command (not hand-edited).