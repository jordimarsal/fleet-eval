FILES
src/mussol/downloads/__init__.py
src/mussol/downloads/status.py
src/mussol/downloads/job.py
src/mussol/downloads/errors.py
src/mussol/downloads/store.py
src/mussol/downloads/service.py
src/mussol/downloads/pipeline.py
src/mussol/api/dtos.py
src/mussol/api/app.py
main.py
tests/test_download_jobs_domain.py
tests/test_download_jobs_service.py
tests/test_download_jobs_pipeline.py
tests/test_download_jobs_http.py

TASKS
T1: DownloadJob status enum and guarded transitions
    depends_on: (none)
    refs: R1, R2
T2: Persisted job creation per resolved track
    depends_on: T1
    refs: R3, R8
T3: Pipeline worker driving stages and bounded progress
    depends_on: T2
    refs: R4, R7
T4: HTTP submission/listing/detail with problem+json errors
    depends_on: T2
    refs: R5
T5: Startup recovery and loopback-only binding
    depends_on: T2, T3
    refs: R6
GATES
pytest tests/test_download_jobs_domain.py tests/test_download_jobs_service.py tests/test_download_jobs_pipeline.py tests/test_download_jobs_http.py -q
pytest -q
python harness/tools/check-traceability.py
bash harness/tools/audit-security.sh
manual verification that the running service binds only to 127.0.0.1