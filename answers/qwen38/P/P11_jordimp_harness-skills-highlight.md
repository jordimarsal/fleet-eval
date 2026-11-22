FILES
src/data/content.ts
src/data/content.spec.ts

TASKS
T1: Update harness-standard entry with skills highlight and metric
    depends_on: (none)
    refs: R1, R2, R3, R4
T2: Add content spec assertions for new highlights and metrics
    depends_on: T1
    refs: R1, R2, R3, R4

GATES
Run `npm run test` to execute Vitest unit tests, ensuring `src/data/content.spec.ts` passes with new assertions for `harness-standard` highlights containing `/npx skills add jordimarsal\/harness/` in all locales and the specific metric `{ value: '6', label: { en: 'skills', es: 'skills', ca: 'skills' } }`.
Verify that existing content-spec assertions regarding project counts, slugs, and other fields remain green to satisfy R3.
Manually inspect the diff of `src/data/content.ts` to confirm only `highlights` and `metrics` were modified for `harness-standard`, and that no text implies Anthropic registry publication (R4).