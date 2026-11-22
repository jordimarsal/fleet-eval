FILES
src/data/content.ts
src/data/content.spec.ts

TASKS
T1: Add standalone skills highlight to harness-standard highlights in all languages
    depends_on: (none)
    refs: R1, R4
T2: Add metrics entry with value "6" and label "skills" to harness-standard in all languages
    depends_on: T1
    refs: R2, R3
T3: Verify no modifications to project slug, name, github URL, dept, tier, or other fields
    depends_on: T2
    refs: R3

GATES
- Content spec passes assertion for `harness-standard.highlights.en`, `highlights.es`, and `highlights.ca` containing `/npx skills add jordimarsal\/harness/`
- Content spec passes assertion that `harness-standard.metrics` contains `{ value: '6', label: { en: 'skills', es: 'skills', ca: 'skills' } }`
- Existing content-spec assertions (department project lists, positive tooling list, thesis-tier list) remain green; diff shows only changes to `highlights` and `metrics` of `harness-standard`
- Reviewer confirms added copy does not mention or imply Anthropic registry or publication