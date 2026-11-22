FILES
src/data/content.ts

TASKS
T1: Update `harness-standard` highlights to include standalone skills installability message
    depends_on: (none)
    refs: R1, R4
T2: Add metrics entry to `harness-standard` with value `6` and label `skills` in all locales
    depends_on: T1
    refs: R2
T3: Verify no unintended modifications to `harness-standard` or other project entries
    depends_on: T2
    refs: R3

GATES
- Run `vitest` to ensure all content specs pass, including assertions for `harness-standard` highlights and metrics.
- Run Playwright tests (`tests/projects.spec.ts`, `tests/smoke.spec.ts`) to confirm page rendering remains intact.
- Inspect git diff to verify only `highlights` and `metrics` of `harness-standard` are modified.
- Confirm added highlight text does not contain `Anthropic` or `registry`.