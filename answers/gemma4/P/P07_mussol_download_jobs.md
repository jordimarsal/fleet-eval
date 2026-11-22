FILES
src/mussol/downloads/__init__.py
src/mussol/downloads/domain.py
src/mussol/downloads/service.py
src/mussol/downloads/worker.py
src/mussol/api/dtos.py
src/mussol/api/app.py
tests/test_downloads.py

TASKS
T1: Define JobStatus enum and DownloadJob domain model with state transition logic
    depends_on: (none)
    refs: R1, R2
T2: Implement DownloadService for job submission, track resolution, and status retrieval
    depends_on: T1
    refs: R3, R8
T3: Implement background worker to drive jobs through download, transcode, and store stages
    depends_on: T2
    refs: R4, R7
T4: Implement HTTP API endpoints for job management using DTOs and problem+json errors
    depends_on: T3
    refs: R5
T5: Configure API server to bind strictly to 127.0.0.1
    depends_on: T4
    refs: R6

GATES
- Unit tests for `DownloadJob` state transitions (ensuring invalid transitions return `Result.failure`)
- Integration test for URL submission: verify one job per resolved track is created or error returned if unsupported
- End-to-end test of the pipeline: submit URL -> check status changes (queued -> downloading -> transcoding -> completed) -> verify progress increments
- API test verifying `problem+json` response format on invalid inputs
- Network test verifying the server rejects connections from non-loopback interfaces