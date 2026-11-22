FILES
src/data/content.ts
src/data/content.spec.ts

TASKS
T1: Update harness-standard project data
    depends_on: (none)
    refs: R1, R2, R3, R4
T2: Verify content requirements via unit tests
    depends_on: T1
    refs: R1, R2, R3, R4

GATES
- Run `vitest src/data/content.spec.ts` to ensure all requirement assertions pass.
- Run `playwright test tests/projects.spec.ts` to ensure no regressions in project rendering.
- Manual inspection of `src/data/content.ts` to confirm wording does not mention "Anthropic" or "registry".
- Verify that existing project counts and other entry fields remain unchanged in `src/data/content.spec.ts`.