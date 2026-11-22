FILES
src/mussol/downloads/__init__.py
src/mussol/downloads/job_status.py
src/mussol/downloads/download_job.py
src/mussol/downloads/service.py
src/mussol/api/dtos.py
src/mussol/api/routes/jobs.py
src/mussol/api/app.py
main.py
tests/test_download_job.py
tests/test_download_service.py
tests/test_api_jobs.py
tests/test_app_binding.py

TASKS
T1: Define JobStatus enum and DownloadJob state machine
    depends_on: (none)
    refs: R1, R2
T2: Implement download pipeline logic with progress tracking
    depends_on: T1
    refs: R4, R7
T3: Create job submission service handling URL resolution and errors
    depends_on: T2
    refs: R3, R8
T4: Expose HTTP endpoints for job submission, listing, and detail
    depends_on: T3
    refs: R5
T5: Configure application binding to 127.0.0.1
    depends_on: T4
    refs: R6
T6: Write unit tests for state transitions and pipeline execution
    depends_on: T2
    refs: R1, R2, R4, R7
T7: Write integration tests for API endpoints and error handling
    depends_on: T4
    refs: R3, R5, R8
T8: Verify network binding configuration
    depends_on: T5
    refs: R6

GATES
- Run `pytest` to ensure all new and existing tests pass.
- Execute `python -m src.mussol.api.app --host 127.0.0.1 --port 8000 &` and verify via `netstat` or `ss` that the process is listening only on `127.0.0.1`.
- Submit a valid YouTube URL via POST `/jobs` and verify one job per track is created with status `queued`.
- Monitor job progress via GET `/jobs/{id}` to confirm status transitions from `queued` -> `downloading` -> `transcoding` -> `completed` (or `failed`) and progress values between 0-100.
- Submit an unsupported URL (e.g., invalid domain) and verify a `problem+json` response is returned and no jobs are created in the database/store.
- Simulate a download failure (mocked) and verify the job status becomes `failed` without raising an unhandled exception in the API layer.