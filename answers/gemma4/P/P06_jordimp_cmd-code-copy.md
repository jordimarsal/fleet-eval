FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts
src/styles/site.css
src/pages/[lang]/departments/[dept].astro

TASKS
T1: Implement command segmentation utility
    depends_on: (none)
    refs: R4
T2: Add unit tests for segmentation utility
    depends_on: T1
    refs: R4
T3: Update CSS with `.cmd-copy` styles and hover affordance rules
    depends_on: (none)
    refs: R1, R2
T4: Integrate segmentation and copyable markup into Department page rendering
    depends_on: T2, T3
    refs: R1, R2, R3
T5: Verify parity and content integrity
    depends_on: T4
    refs: R3

GATES
- `npx vitest run src/lib/cmd-code.spec.ts` must pass (R4)
- `git diff --stat` shows no changes to `src/data/content.ts`, `llms.txt`, or `llms-full.txt` (R3)
- `npx vitest run src/data/content.spec.ts` must remain green (R3)
- Manual check: Hovering a command in the Tooling department page reveals the icon; clicking copies text to clipboard (R2)
- Dist scan: Check build output for `<code class="cmd-copy">` wrapping install commands on project and tooling pages (R1)