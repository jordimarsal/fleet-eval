FILES
src/data/content.ts
src/data/content.spec.ts

TASKS
T1: Update harness-standard entry with skills highlights and metrics
    depends_on: (none)
    refs: R1, R2, R3, R4
T2: Add content spec assertions for new highlights and metrics
    depends_on: T1
    refs: R1, R2, R3, R4

GATES
- Run `npm run test` to execute Vitest unit tests, ensuring `src/data/content.spec.ts` passes with new assertions for `harness-standard` highlights and metrics.
- Verify that existing content-spec assertions (department project lists, positive tooling list, thesis-tier list) remain green without modification.
- Inspect the diff of `src/data/content.ts` to confirm only `highlights` and `metrics` fields of the `harness-standard` entry are modified, preserving slug, name, github URL, dept, tier, and other entries.
- Review the added highlight copy in all three languages (en, es, ca) to ensure it claims standalone installability via `npx skills add jordimarsal/harness` and does not mention "Anthropic" or "registry".