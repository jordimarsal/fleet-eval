FILES
src/mussol/jobs/enums.py
src/mussol/jobs/models.py
src/mussol/jobs/service.py
src/mussol/jobs/repository.py
src/mussol/jobs/processor.py
src/mussol/api/job_routes.py
tests/test_jobs_enum.py
tests/test_jobs_models.py
tests/test_jobs_service.py
tests/test_jobs_repository.py
tests/test_jobs_processor.py
tests/test_api_job_routes.py

TASKS
T1: Implement `JobStatus` enum and `DownloadJob` model with state validation
    depends_on: (none)
    refs: R1, R2
T2: Implement job repository for persistence and restart survival
    depends_on: T1
    refs: R2
T3: Implement job submission logic that resolves URLs to tracks and creates queued jobs
    depends_on: T1
    refs: R3, R8
T4: Implement job processor that drives stages (download, transcode, store) with progress tracking
    depends_on: T2
    refs: R4, R7
T5: Implement HTTP API routes for job submission, listing, and details with DTOs and error handling
    depends_on: T3
    refs: R5
T6: Configure HTTP server to bind only to `127.0.0.1`
    depends_on: T5
    refs: R6
T7: Add comprehensive tests for job lifecycle, state transitions, and API endpoints
    depends_on: T4
    refs: R1, R2, R3, R4, R5, R7, R8

GATES
- All unit tests pass (pytest)
- Integration tests verify job pipeline completion from queued to completed/failed
- API tests verify `problem+json` error format and correct HTTP status codes
- Security check confirms server binds only to `127.0.0.1`
- Traceability check (`harness/tools/check-traceability.py`) passes for all requirements R1-R8