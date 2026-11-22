FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts
src/styles/site.css
tests/smoke.spec.ts
tests/departments.spec.ts

TASKS
T1: Implement command extraction and segmentation helper
    depends_on: (none)
    refs: R1, R4
T2: Add copy affordance to code element with keyboard/hover support
    depends_on: T1
    refs: R2
T3: Verify rendering parity and content integrity across locales
    depends_on: T1, T2
    refs: R1, R3
T4: Update tests for new cmd-code logic and copy behavior
    depends_on: T1, T2
    refs: R1, R2, R3, R4

GATES
- dist scan of project detail page and tooling department page (en/es/ca) confirms `<code>` wrapping around install commands with `.cmd-copy` CSS rules  
- manual verification shows hover/keyboard focus reveals copy icon; clicking copies text to clipboard and displays "copied" feedback  
- full `npx vitest run` passes green; `git diff` limited to new files and modified rendering components; F17 assertions remain green; llms.txt/llms-full.txt byte-identical  
- unit test suite in `cmd-code.spec.ts` passes all cases: command at start/end, middle, no command  
- existing rendering surfaces (e.g., departments, projects) show correct plain-text selection and unmodified source content in `content.ts`