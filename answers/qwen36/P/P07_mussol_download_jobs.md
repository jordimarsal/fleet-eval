FILES
src/mussol/download_jobs/__init__.py
src/mussol/download_jobs/job_status.py
src/mussol/download_jobs/download_job.py
src/mussol/download_jobs/service.py
src/mussol/download_jobs/errors.py
src/mussol/api/endpoints/downloads.py
src/mussol/api/dtos.py
src/mussol/api/app.py
harness/specs/download_jobs/design.md
harness/specs/download_jobs/requirements.md
harness/specs/download_jobs/tasks.md
tests/test_download_job.py
tests/test_download_service.py
tests/test_api.py
tests/test_web.py

TASKS
T1: Define `JobStatus` enum with queued, downloading, transcoding, completed, failed members
    depends_on: (none)
    refs: R1
T2: Implement `DownloadJob` value object with immutable state and behavior methods returning `Result` that reject invalid transitions
    depends_on: T1
    refs: R2
T3: Create download job error types for unsupported URLs and invalid transitions
    depends_on: T1
    refs: R8
T4: Build download service that creates one queued job per resolved track from a submitted URL
    depends_on: T2, T3
    refs: R3, R8
T5: Implement pipeline stages (download → transcode → store) in the service, updating status at each stage; failures mark job as failed without raising exceptions
    depends_on: T2, T4
    refs: R4
T6: Add per-job progress tracking between 0 and 100 across pipeline stages
    depends_on: T2, T5
    refs: R7
T7: Expose job submission, listing, and detail endpoints over HTTP using DTOs with problem+json errors
    depends_on: T4, T6
    refs: R5
T8: Bind HTTP server to 127.0.0.1 only
    depends_on: T7
    refs: R6
T9: Wire download service into app launcher so jobs run automatically on startup
    depends_on: T5, T8
    refs: feat(jobs): run submitted jobs automatically and survive restarts

GATES
- Unit tests for `JobStatus` enum values and transitions (R1, R2)
- Property-based tests verifying no invalid state transitions are possible through behavior methods (R2)
- Integration test submitting an unsupported URL returns typed error and creates zero jobs (R3, R8)
- End-to-end test of a full pipeline (queued → downloading → transcoding → completed) with status updates at each stage (R4)
- Failure injection test confirming any stage failure marks the job as failed without raising exceptions (R4)
- Progress tracking verification that per-job progress is reported between 0 and 100 across all stages (R7)
- API contract test validating submission, listing, and detail endpoints return correct DTOs and problem+json errors (R5)
- Network binding test confirming the server listens only on 127.0.0.1 (R6)
- Restart survival test: submit a job, stop the process, restart it, verify queued jobs resume execution (feat title)