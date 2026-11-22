FILES
docs/architecture.md
docs/fleet.md

TASKS
T1: Update architecture documentation with model field notes
    depends_on: (none)
    refs: R7, R12
T2: Add fleet link to documentation
    depends_on: T1
    refs: R8

GATES
- Verify that `docs/architecture.md` contains explicit descriptions for all required fields of `RunRecord` as specified in R7 (model/agent identity, backend name/version, command, seed, timestamps, scores, resource metrics).
- Verify that `docs/architecture.md` documents the `schema_version` field and its role in maintaining backward compatibility for JSONL files per R12.
- Verify that `docs/fleet.md` is linked from the main documentation index or relevant navigation points.
- Run a markdown linting check on modified files to ensure formatting consistency.
- Confirm no code changes were made to `src/quantdelta/core/` to preserve import boundaries and vocabulary constraints (R5, R6).