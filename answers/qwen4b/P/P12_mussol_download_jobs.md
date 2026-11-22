FILES
src/mussol/downloads/job_status.py
src/mussol/downloads/job.py
src/mussol/downloads/service.py
src/mussol/api/dtos.py
harness/progress/impl_download_jobs.md
harness/specs/download_jobs/tasks.md

TASKS
T1: Define JobStatus enum and validate transitions
    depends_on: (none)
    refs: R1, R2
T2: Implement DownloadJob state machine with guarded transitions
    depends_on: T1
    refs: R2, R4, R7
T3: Implement job creation from URL with track resolution
    depends_on: T2
    refs: R3, R8
T4: Implement HTTP endpoints for job submission, listing, and detail
    depends_on: T3
    refs: R5, R6
T5: Integrate progress tracking across pipeline stages
    depends_on: T2
    refs: R7
T6: Ensure failure propagation without exception escape
    depends_on: T2
    refs: R4

GATES
- Run check-traceability.py to verify all requirements are covered in implementation tasks
- Validate feature_list.json against schema using harness/tools/validate-feature-list.py
- Confirm no new security vulnerabilities via audit-security.sh
- Verify HTTP endpoints return problem+json errors per requirement R5