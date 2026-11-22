FILES
src/mussol/downloads/__init__.py
src/mussol/downloads/errors.py
src/mussol/downloads/job_status.py
src/mussol/downloads/job.py
src/mussol/downloads/repository.py
src/mussol/downloads/progress.py
src/mussol/downloads/service.py
src/mussol/api/app.py
src/mussol/api/dtos.py
main.py
tests/test_download_job.py
tests/test_download_service.py
tests/test_downloads_recovery.py
tests/test_api.py

TASKS
T1: JobStatus enum and DownloadJob behavior methods with Result-returning transitions
    depends_on: (none)
    refs: R1, R2
T2: Persistent per-job repository that survives restarts
    depends_on: T1
    refs: R3
T3: Submission fan-out into one queued job per resolved track; typed error on unsupported URL without creating jobs
    depends_on: T2
    refs: R3, R8
T4: Staged pipeline driver (download -> transcode -> store) with stage status updates, failure marking without exception escape, per-job progress 0-100
    depends_on: T3
    refs: R4, R7
T5: HTTP API (submit/list/detail) with DTOs, problem+json errors, bound to 127.0.0.1; startup recovery of pending jobs
    depends_on: T4
    refs: R5, R6

GATES
- python3 -m pytest tests/test_download_job.py tests/test_download_service.py tests/test_downloads_recovery.py tests/test_api.py -v
- python3 -m pytest (full suite, including module boundaries and quality gates)
- bash harness/tools/audit-security.sh (no HIGH findings)
- python3 harness/tools/check-traceability.py --feature download_jobs (all requirements done, tests resolve)
- binding check: server starts only on 127.0.0.1; manual smoke test via main entry point confirming queued jobs survive a restart