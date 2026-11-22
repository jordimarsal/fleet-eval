FILES
docs/model-field-notes.md
docs/fleet.md

TASKS
T1: Add model field notes to docs/model-field-notes.md
    depends_on: (none)
    refs: R7
T2: Update docs/fleet.md with the new fleet link
    depends_on: T1
    refs: (none)

GATES
- `opencode run --feature docs-model-field-notes` completes without errors and produces a diff that adds only the two files above
- `grep -r 'gguf\|llama\|kv[-_ ]?cache' docs/` returns no matches (R6 applies to all project text, not just src/)
- The new `docs/model-field-notes.md` contains at least one paragraph describing the model identity field on RunRecord (verifies R7 coverage)
- The updated `docs/fleet.md` includes a valid markdown link to the fleet endpoint (verifies the feature title intent)
- `git diff --stat` shows exactly 2 changed files under `docs/` and nothing else