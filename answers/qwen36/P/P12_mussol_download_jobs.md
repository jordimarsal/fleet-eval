FILES
src/mussol/downloads/__init__.py
src/mussol/downloads/errors.py
src/mussol/downloads/job_status.py
src/mussol/downloads/job.py
src/mussol/downloads/service.py
src/mussol/downloads/runner.py
src/mussol/api/endpoints/download_jobs.py
tests/test_download_job.py
tests/test_download_service.py
tests/test_download_endpoints.py

TASKS
T1: Define JobStatus enum and job error types
    depends_on: (none)
    refs: R1
T2: Implement DownloadJob value object with immutable state transitions
    depends_on: T1
    refs: R2
T3: Build DownloadRunner that drives a single job through download → transcode → store stages
    depends_on: T2
    refs: R4, R7
T4: Create DownloadService with fan-out per-track logic and persistence for restart survival
    depends_on: T3
    refs: R3, R5, R8
T5: Wire HTTP endpoints under /api/jobs with DTOs, problem+json errors, and 127.0.0.1 binding
    depends_on: T4
    refs: R5, R6