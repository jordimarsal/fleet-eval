FILES
src/mussol/downloads/__init__.py
src/mussol/downloads/job.py
src/mussol/downloads/service.py
src/mussol/api/app.py
src/mussol/api/dtos.py
tests/test_download_service.py
tests/test_api.py

TASKS
T1: Implement JobStatus enum and Job value object
    depends_on: (none)
    refs: R1
T2: Implement DownloadService state machine and pipeline logic
    depends_on: T1
    refs: R2, R4, R7
T3: Implement URL submission and job creation logic
    depends_on: T2
    refs: R3, R8
T4: Implement HTTP API endpoints and DTOs
    depends_on: T3
    refs: R5, R6
T5: Update tests for service and API
    depends_on: T4
    refs: R1, R2, R3, R4, R5, R6, R7, R8

GATES
- harness/tools/check-traceability.py --feature download_jobs
- pytest tests/test_download_service.py tests/test_api.py -v
- bash harness/tools/audit-security.sh