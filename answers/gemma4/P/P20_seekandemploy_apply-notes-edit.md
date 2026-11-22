FILES
src/seekandemploy/cli.py
src/seekandemploy/repository.py
tests/test_applications_cli.py

TASKS
T1: Implement `update_job_offer_notes` in repository
    depends_on: (none)
    refs: R1, R2, R5, R6
T2: Add CLI command `apply notes` to `cli.py` with argument validation
    depends_on: T1
    refs: R1, R2, R7, R8
T3: Implement post-edit side effects (stdout reporting and HTML regeneration)
    depends_on: T2
    refs: R3, R4
T4: Add unit tests for CLI logic and repository updates
    depends_on: T3
    refs: R1, R2, R3, R4, R5, R6, R7, R8

GATES
- Verify `seekandemploy apply notes <id> --set "text"` updates notes and regenerates HTML.
- Verify `seekandemploy apply notes <id> --clear` sets notes to NULL and regenerates HTML.
- Verify error exit code 2 when both or neither `--set`/`--clear` are provided.
- Verify error exit code 1 and stderr message when ID is not found.
- Verify stdout format matches `[<id>] <status> <company> - <title>` followed by `report: <path>`.
- Verify no new rows are added to `application_event` table after a notes edit.
- Verify other application fields remain unchanged after a notes edit.