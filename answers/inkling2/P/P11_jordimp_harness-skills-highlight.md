FILES
src/data/content.ts
src/data/content.spec.ts

TASKS
T1: Add skills installability highlight and `6`/`skills` metric to `harness-standard` entry
    depends_on: (none)
    refs: R1, R2, R3, R4
T2: Extend content spec with F17 assertions for the three languages, metric shape, No-registry wording, and diff-boundary checks
    depends_on: T1
    refs: R1, R2, R3, R4

GATES
npm test -- src/data/content.spec.ts (F17 assertions pass)
full Vitest unit suite (all existing content-spec assertions stay green without modification — departments lists, positive tooling list, thesis-tier list)
Playwright tests/projects.spec.ts and tests/smoke.spec.ts green (no rendering regression on the touched entry)
reviewer inspection of added copy lines: no `Anthropic` or `registry`; only standalone `npx skills add jordimarsal/harness` claim
git diff restricted to highlights/metrics of the harness-standard entry plus the two listed files