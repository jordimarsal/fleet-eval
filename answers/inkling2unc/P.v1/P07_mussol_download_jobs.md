FILES
src/mussol/downloads/__init__.py
src/mussol/downloads/status.py
src/mussol/downloads/errors.py
src/mussol/downloads/job.py
src/mussol/downloads/service.py
src/mussol/downloads/runner.py
src/mussol/downloads/repository.py
src/mussol/api/app.py
src/mussol/api/dtos.py
main.py
tests/test_downloads_status.py
tests/test_downloads_job.py
tests/test_downloads_service.py
tests/test_downloads_runner.py
tests/test_downloads_http.py

TASKS
T1: Define JobStatus enum and typed errors for the downloads module
    depends_on: (none)
    refs: R1, R8
T2: Implement DownloadJob with Result-returning behavior methods
    depends_on: T1
    refs: R2
T3: Implement submission service creating one queued job per resolved track; unsupported URL yields typed error with no jobs created
    depends_on: T2
    refs: R3, R8
T4: Run pipeline worker driving download/transcode/store stages with ordered status updates, bounded progress, and failure containment
    depends_on: T2
    refs: R4, R7
T5: Expose submit/list/detail HTTP endpoints with DTOs, problem+json errors, bound to 127.0.0.1 only
    depends_on: T3
    refs: R5, R6
T6: Add durable repository and startup reload so pending jobs survive restarts
    depends_on: T3
    refs: R3, R4

GATES
- Unit tests pass for the new or modified downloads modules plus existing test suite (tests/test_downloads_*.py, tests/test_api.py, tests/test_web.py) without skipped failures.
- Concurrency check confirmed by tests: each submitted supported URL produces exactly one queued job per resolved track (R3) and zero jobs on an unsupported URL (R8).
- Job state transitions verified: invalid transition is rejected via Result, never escapes as exception; stage failure marks the job failed without escaping (R2/R4).
- Progress range validated to remain within [0,100] across stages (R7) — including completing a 100% terminal state.
- HTTP smoke checks: routes respond with JSON/problem+json bodies for list, detail, and submission success/error paths; application binds to 127.0.0.1 only at runtime.
- Restart recovery gate: stop the process after queueing jobs, restart the app, confirm persisted queued jobs are visible again through listing and resumed pipeline execution.