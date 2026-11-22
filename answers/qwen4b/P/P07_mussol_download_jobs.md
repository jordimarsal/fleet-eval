FILES  
src/mussol/download_jobs/job_status.py  
src/mussol/download_jobs/download_job.py  
src/mussol/download_jobs/state_machine.py  
src/mussol/api/dtos/job.py  
src/mussol/api/routes/jobs.py  
src/mussol/shared/result.py  
harness/specs/download_jobs/tasks.md  
harness/progress/impl_download_jobs.md  

TASKS  
T1: Define JobStatus enum and validate transitions  
    depends_on: (none)  
    refs: R1, R2, R4  
T2: Implement DownloadJob state machine with guarded transitions  
    depends_on: T1  
    refs: R2, R3, R4, R7  
T3: Implement job creation from URL with track resolution logic  
    depends_on: T2  
    refs: R3, R8  
T4: Implement HTTP endpoints for job submission, listing, and detail  
    depends_on: T3  
    refs: R5, R6  
T5: Add per-job progress tracking across pipeline stages  
    depends_on: T2  
    refs: R7, R4  
T6: Ensure failure in any stage marks job as failed without exception  
    depends_on: T2  
    refs: R4, R2  

GATES  
- All requirements are traceable to at least one task via `refs`  
- Unit tests cover all state transitions and error paths in `tests/test_download_job.py`, `tests/test_api.py`  
- HTTP endpoint behavior matches specification in `harness/specs/download_jobs/requirements.md`  
- System binds only to `127.0.0.1` when running (verified in integration test)  
- Job status updates and progress tracking are logged and validated in harness checkpoints