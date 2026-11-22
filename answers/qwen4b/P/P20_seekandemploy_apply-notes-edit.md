FILES
src/seekandemploy/cli.py
src/seekandemploy/models.py
src/seekandemploy/repository.py
src/seekandemploy/applications_report.py
tests/test_applications_cli.py
tests/test_applications_models.py
tests/test_repository.py

TASKS
T1: Implement `apply notes` command parsing and validation for `--set <text>` and `--clear`
    depends_on: (none)
    refs: R1, R2, R8
T2: Validate application ID existence and handle missing application case
    depends_on: T1
    refs: R7
T3: Update application's notes field in the database based on command flags
    depends_on: T2
    refs: R1, R2, R5, R6
T4: Generate and print tracker-glance format output upon successful edit
    depends_on: T3
    refs: R3
T5: Regenerate static HTML snapshot from current database state at specified path
    depends_on: T3
    refs: R4
T6: Ensure no row is appended to `application_event` table during notes update
    depends_on: T3
    refs: R5

GATES
- Verify that `seekandemploy apply notes <id> --set <text>` correctly persists `<text>` as the application's `notes` field.
- Confirm that `seekandemploy apply notes <id> --clear` sets the `notes` field to NULL.
- Validate that when a notes edit succeeds, the system prints the correct tracker-glance line followed by the report path.
- Ensure that the static HTML snapshot is regenerated at the specified `--out` path (defaulting to `applications.html`) after a successful notes edit.
- Confirm that no entry is added to the `application_event` table when editing notes.
- Verify that the application’s status, company, title, URL, salary expectation, currency, applied date, or source job-offer link remains unchanged.
- Test error handling for invalid IDs: ensure "error: application <id> not found" is printed and exit code 1 is returned without modifying the HTML snapshot.
- Validate command usage errors: confirm that both `--set` and `--clear` flags are rejected with exit code 2 if used together or omitted.