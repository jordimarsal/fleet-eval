FILES
src/mussol/downloads/__init__.py
src/mussol/downloads/job_status.py
src/mussol/downloads/job.py
src/mussol/downloads/errors.py
src/mussol/downloads/service.py
src/mussol/api/dtos.py
src/mussol/api/app.py
tests/test_download_job.py
tests/test_download_service.py
tests/test_api.py

TASKS
T1: Define JobStatus enum and DownloadJob state machine
    depends_on: (none)
    refs: R1, R2
T2: Implement DownloadService pipeline logic
    depends_on: T1
    refs: R3, R4, R7, R8
T3: Update API layer with DTOs and problem+json errors
    depends_on: T2
    refs: R5, R6
T4: Write unit tests for job state transitions
    depends_on: T1
    refs: R1, R2
T5: Write integration tests for service pipeline
    depends_on: T2
    refs: R3, R4, R7, R8
T6: Write API endpoint tests
    depends_on: T3
    refs: R5, R6

GATES
- Run `pytest` to ensure all new and existing tests pass.
- Verify that `DownloadJob` state transitions strictly follow the defined valid paths and return `Err` on invalid attempts.
- Confirm that submitting an unsupported URL returns a 400/422 status with `application/problem+json` content type and no jobs are created in the database.
- Validate that the HTTP server binds exclusively to `127.0.0.1`.
- Check that progress values remain within [0, 100] throughout the download/transcode/store stages.