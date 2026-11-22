FILES
src/seekandemploy/cli.py
src/seekandemploy/repository.py
src/seekandemploy/applications_report.py
tests/test_applications_cli.py

TASKS
T1: Implement CLI argument parsing for `apply notes` command
    depends_on: (none)
    refs: R8
T2: Implement database persistence logic for `notes` field (set/clear)
    depends_on: T1
    refs: R1, R2
T3: Implement application lookup and error handling for missing IDs
    depends_on: T2
    refs: R7
T4: Implement success output formatting (tracker-glance + report path)
    depends_on: T2
    refs: R3
T5: Implement static HTML snapshot regeneration on successful edit
    depends_on: T4
    refs: R4
T6: Ensure no side effects on `application_event` table or other application fields
    depends_on: T2
    refs: R5, R6
T7: Write integration tests for `apply notes` command covering all requirements
    depends_on: T5
    refs: R1, R2, R3, R4, R5, R6, R7, R8

GATES
- Run `pytest tests/test_applications_cli.py` to verify all CLI behavior and error cases.
- Verify that `applications.html` is regenerated with updated content after a successful notes edit.
- Confirm that `application_event` table remains unchanged after notes editing.
- Check that stderr output and exit codes match requirements for invalid IDs and usage errors.