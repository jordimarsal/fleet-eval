FILES
src/mussol/downloads/__init__.py
src/mussol/downloads/job_status.py
src/mussol/downloads/job.py
src/mussol/downloads/service.py
src/mussol/downloads/errors.py
src/mussol/api/download_routes.py
tests/test_job_status.py
tests/test_download_job.py
tests/test_download_service.py
tests/test_download_routes.py

TASKS
T1: Implement `JobStatus` enum and `DownloadJob` value object with state validation
    depends_on: (none)
    refs: R1, R2
T2: Implement `DownloadService` to drive jobs through download/transcode/store stages with progress tracking
    depends_on: T1
    refs: R3, R4, R7
T3: Implement HTTP API routes for job submission, listing, and details with DTOs and problem+json errors
    depends_on: T2
    refs: R5, R6, R8
T4: Add tests covering status transitions, service pipeline, and API endpoints
    depends_on: T3
    refs: R1, R2, R3, R4, R5, R6, R7, R8

GATES
- Run `python -m pytest` to verify all unit and integration tests pass.
- Run `harness/tools/check-traceability.py --all` to ensure all requirements (R1-R8) are traced to implementation and tests.
- Run `harness/tools/audit-security.sh --stack=python` to confirm no HIGH security findings.
- Verify the HTTP server binds only to `127.0.0.1` and returns `problem+json` error format.