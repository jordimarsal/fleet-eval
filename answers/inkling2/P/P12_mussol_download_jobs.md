FILES
src/mussol/downloads/__init__.py
src/mussol/downloads/errors.py
src/mussol/downloads/job_status.py
src/mussol/downloads/job.py
src/mussol/downloads/service.py
src/mussol/downloads/store.py
src/mussol/api/dtos.py
src/mussol/api/app.py
main.py
tests/test_download_job.py
tests/test_download_service.py
tests/test_api.py

TASKS
T1: JobStatus enum and transition behaviors on DownloadJob
    depends_on: (none)
    refs: R1, R2
T2: Fan-out submission, staged run, failure marking, unsupported URL rejection
    depends_on: T1
    refs: R3, R4, R7, R8
T3: Persisted job store and restart recovery
    depends_on: T2
    refs: R3, R7
T4: HTTP API with DTOs, loopback bind, problem+json errors
    depends_on: T3
    refs: R5, R6

GATES
- python3 -m pytest tests/test_download_job.py tests/test_download_service.py tests/test_api.py -q (all transitions, fan-out/failure/unsupported/progress checks green)
- python3 -m pytest -q (full suite unchanged except the three files)
- Verify each of R1–R8 has a test in one of the modified test files; grep test names/covers before closing
- Start app via main.py, confirm it binds to 127.0.0.1 only (not 0.0.0.0 or ::) and that an interrupted queued job is resumed on startup before accepting traffic
- bash harness/tools/audit-security.sh reports no new HIGH findings for the downloads module