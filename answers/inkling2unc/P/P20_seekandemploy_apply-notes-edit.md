FILES
src/seekandemploy/cli.py
src/seekandemploy/repository.py
src/seekandemploy/applications_report.py
tests/test_applications_cli.py

TASKS
T1: Add `--set`/`--clear` argument parsing with exactly-one requirement
    depends_on: (none)
    refs: R8
T2: Implement notes edit repository operation persisting text or NULL without side effects
    depends_on: (none)
    refs: R1, R2, R5, R6
T3: Wire `apply notes <id>` command handler: lookup, edit, not-found stderr/exit 1
    depends_on: T1, T2
    refs: R1, R2, R7
T4: Emit success stdout line in tracker-glance format followed by report path
    depends_on: T3
    refs: R3
T5: Regenerate HTML snapshot from current database at `--out` (default applications.html) on successful edit
    depends_on: T4
    refs: R4
GATES
pytest tests/test_applications_cli.py -q
pytest tests/test_applications_report.py -q
ruff check src/seekandemploy/cli.py src/seekandemploy/repository.py src/seekandemploy/applications_report.py
mypy src/seekandemploy (or project's configured typecheck gate)
end-to-end smoke: seekandemploy apply notes <existing-id> --set "note" and --clear against a scratch sqlite DB; verify persisted value, stdout line shape, regenerated --out file, exit codes 2 (both flags / neither) and 1 (unknown id with untouched snapshot), no application_event rows created