FILES
src/data/content.ts
src/data/content.spec.ts

TASKS
T1: Add standalone skills highlight to `harness-standard` in all locales
    depends_on: (none)
    refs: R1, R4
T2: Add `skills` metric with value `6` to `harness-standard`
    depends_on: T1
    refs: R2
T3: Verify no other fields of `harness-standard` are modified and existing assertions pass
    depends_on: T2
    refs: R3

GATES
- Run `npm run test:unit` to ensure `content.spec.ts` assertions for `highlights` regex match and metric structure pass.
- Run `npm run test:e2e` to verify department lists and project listings remain green (R3).
- Manual inspection of generated HTML/JSON for `harness-standard` to confirm absence of "Anthropic" or "registry" in highlights (R4).