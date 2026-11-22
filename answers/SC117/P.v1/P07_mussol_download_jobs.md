FILES
src/mussol/download_jobs/enums.py
src/mussol/download_jobs/models.py
src/mussol/download_jobs/stores.py
src/mussol/download_jobs/service.py
src/mussol/api/routes.py
src/mussol/api/dtos.py
src/mussol/shared/process.py
tests/test_download_jobs_enums.py
tests/test_download_jobs_models.py
tests/test_download_jobs_stores.py
tests/test_download_jobs_service.py
tests/test_api_routes.py

TASKS
T1: Define JobStatus enum and DownloadJob model with state machine logic
    depends_on: (none)
    refs: R1, R2
T2: Implement persistence layer for job states to survive restarts
    depends_on: T1
    refs: R7
T3: Implement URL resolution and job creation service
    depends_on: T1
    refs: R3, R8
T4: Implement download/transcode/store pipeline with progress tracking
    depends_on: T2
    refs: R4, R7
T5: Expose HTTP endpoints for submission, listing, and details
    depends_on: T3, T4
    refs: R5
T6: Configure HTTP server to bind to 127.0.0.1 only
    depends_on: T5
    refs: R6

GATES
- Unit tests pass for all new modules in src/mussol/download_jobs/ and src/mussol/api/routes.py
- Integration test verifies end-to-end flow: submit URL -> create jobs -> run pipeline -> update status -> store result
- Verification that invalid state transitions raise errors (R2)
- Verification that unsupported URLs return typed error without creating jobs (R8)
- Verification that HTTP server binds exclusively to 127.0.0.1 (R6)
- Verification that job progress updates correctly between 0 and 100 during stages (R7)
- Verification that job states persist across simulated restarts (implied by "survive restarts" feature title)