FILES
src/data/content.ts

TASKS
T1: Add `npx skills add jordimarsal/harness` highlight to `harness-standard` in all locales
    depends_on: (none)
    refs: R1, R4
T2: Add `{ value: '6', label: { en: 'skills', es: 'skills', ca: 'skills' } }` metric to `harness-standard`
    depends_on: T1
    refs: R2
T3: Verify no other project fields were modified and existing assertions remain green
    depends_on: T2
    refs: R3

GATES
- `npm run test -- src/data/content.spec.ts` passes (content spec asserts highlights regex match for each locale, metrics shape, and that only `highlights`/`metrics` of `harness-standard` changed)
- `npm run build` succeeds without new warnings or errors
- `npm run lint` passes with zero violations
- `git diff` shows changes limited to `src/data/content.ts`, touching only `highlights` and `metrics` arrays of the `harness-standard` entry; no slug/name/github/dept/tier modifications