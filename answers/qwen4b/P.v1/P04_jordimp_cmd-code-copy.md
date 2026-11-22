FILES  
src/lib/cmd-code.ts  
src/components/content/HighlightLine.astro  
src/styles/site.css  
tests/unit/cmd-code.spec.ts  

TASKS  
T1: Implement cmd-code helper to extract command and surrounding text  
    depends_on: (none)  
    refs: R1, R4  
T2: Update HighlightLine component to wrap install commands in `<code>.cmd-copy`  
    depends_on: T1  
    refs: R1, R2  
T3: Add copy affordance with keyboard/hover support and clipboard feedback  
    depends_on: T2  
    refs: R2  
T4: Verify content source integrity and F17 test parity  
    depends_on: T2  
    refs: R3  
T5: Write unit tests for cmd-code helper covering all edge cases  
    depends_on: T1  
    refs: R4  

GATES  
- Dist scan of project detail and tooling department pages (en/es/ca) confirms `<code>` wrapping of install commands  
- Built CSS includes `.cmd-copy` rules with monospace font, background, and border  
- Manual verification: hover shows copy icon, click copies command and displays "copied" feedback  
- Full `npx vitest run` passes; no changes to F17 assertions or llms.txt/llms-full.txt output  
- Unit test suite for `cmd-code.spec.ts` passes all cases (match, no-match, start/end)  
- `git diff` limited to new files and rendering components; no unintended modifications