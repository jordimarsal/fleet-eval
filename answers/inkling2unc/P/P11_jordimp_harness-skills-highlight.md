FILES
src/data/content.ts
src/data/content.spec.ts

TASKS
T1: Add standalone-skills highlight and skills metric to harness-standard entry
    depends_on: (none)
    refs: R1, R2, R3
T2: Assert new highlights, metric and installability copy in the content spec
    depends_on: T1
    refs: R1, R2, R3, R4
T3: Review added copy for accuracy before closeout
    depends_on: T2
    refs: R4

GATES
Run `npx vitest run src/data/content.spec.ts` — existing project/department/tooling/tier list assertions stay green unmodified (R3) and the new harness-standard assertions pass (R1, R2, R4)
Grep `src/data/content.ts` diff for the feature branch: confirm only `highlights` and `metrics` of the `harness-standard` entry changed; no changes to slug, name, github URL, dept, tier, or any other entry
Reviewer inspection gate: added highlight lines contain no occurrence of `Anthropic` or `registry` and no claim beyond skills installability
Full unit suite `npm test` (or `npx vitest run`) plus a build/e2e smoke relevant to projects pages remain green with no baseline changes