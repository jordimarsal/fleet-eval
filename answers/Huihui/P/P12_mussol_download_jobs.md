FILES
src/mussol/downloads/__init__.py
src/mussol/downloads/job_status.py
src/mussol/downloads/errors.py
src/mussol/downloads/job.py
src/mussol/downloads/service.py
src/mussol/api/dtos.py
src/mussol/api/app.py
tests/test_download_job.py
tests/test_download_service.py
tests/test_api.py

TASKS
T1: Define JobStatus enum and state transition logic
    depends_on: (none)
    refs: R1, R2
T2: Implement DownloadJob entity with behavior methods
    depends_on: T1
    refs: R2, R7
T3: Implement DownloadService for job creation and execution pipeline
    depends_on: T2
    refs: R3, R4, R7, R8
T4: Update API DTOs and HTTP endpoints for jobs
    depends_on: T3
    refs: R5, R6, R8
T5: Write unit tests for job state machine and service logic
    depends_on: T2, T3
    refs: R1, R2, R3, R4, R7, R8
T6: Write integration tests for API endpoints
    depends_on: T4
    refs: R5, R6, R8

GATES
- Run `pytest tests/` to ensure all new and existing tests pass.
- Verify that `DownloadJob` state transitions reject invalid moves via unit tests.
- Confirm that submitting an unsupported URL returns a typed error and creates no jobs.
- Validate that the HTTP server binds to 127.0.0.1 only.
- Check that job progress is updated between 0 and 100 during the pipeline stages.