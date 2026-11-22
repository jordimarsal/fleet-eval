FILES
src/mussol/downloads/job_status.py
src/mussol/downloads/job.py
src/mussol/downloads/service.py
src/mussol/downloads/manager.py
src/mussol/api/dtos.py
src/mussol/api/app.py
tests/test_download_job.py
tests/test_download_service.py
tests/test_job_manager.py

TASKS
T1: Define JobStatus enum and DownloadJob state machine
    depends_on: (none)
    refs: R1, R2
T2: Implement job persistence and progress tracking logic
    depends_on: T1
    refs: R7
T3: Implement DownloadService to drive jobs through stages (download, transcode, store) with error handling
    depends_on: T1, T2
    refs: R4
T4: Implement URL submission logic to resolve tracks and create queued jobs
    depends_on: T3
    refs: R3, R8
T5: Implement JobManager to handle automatic execution of queued jobs and recovery after restarts
    depends_on: T4
    refs: R4
T6: Implement HTTP API for job submission, listing, and details using DTOs and problem+json
    depends_on: T5
    refs: R5
T7: Configure API server to bind strictly to 127.0.0.1
    depends_on: T6
    refs: R6

GATES
- Verify `JobStatus` enum contains all required members via unit tests.
- Verify `DownloadJob` rejects invalid state transitions (e.g., `completed` -> `downloading`) via unit tests.
- Verify that an unsupported URL returns a typed error and creates zero jobs in the database.
- Verify that a single URL resolves to multiple jobs if it contains multiple tracks.
- Verify that a job failure in any stage results in `failed` status without raising unhandled exceptions.
- Verify that progress values are correctly updated between 0 and 100 across stages.
- Verify that the API responds with `application/problem+json` on errors.
- Verify that the web server is unreachable from external IP addresses (bind check).
- Verify that restarting the application resumes `queued` or interrupted jobs.
- Run `harness/tools/check-traceability.py` to ensure all requirements are covered.