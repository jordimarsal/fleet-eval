FILES
src/atalaia/system.py
src/atalaia/api.py
web/app.js
tests/test_api_ram.py
harness/specs/f8_ram/tasks.md
harness/progress/impl_f8_ram.md
harness/progress/review_f8_ram.md

TASKS
T1: Implement `system.free_ram_mb` endpoint reading `/proc/meminfo` directly
    depends_on: (none)
    refs: R1, R2, R5
T2: Wire `GET /api/system` into FastAPI router and expose via existing API module
    depends_on: T1
    refs: R1
T3: Add top-bar RAM display to UI — sum of `ram_mb` from up entries + free RAM from system
    depends_on: T1
    refs: R3
T4: Render `—` for any unavailable value in the UI
    depends_on: T3
    refs: R4
T5: Write unit tests covering happy path, missing file, malformed file, and null propagation
    depends_on: T1
    refs: R1, R2
T6: Record task completion and review notes in harness progress files
    depends_on: T5
    refs: R1, R2, R3, R4, R5

GATES
- `python -m pytest tests/test_api_ram.py -v` passes all assertions.
- `curl http://127.0.0.1:8901/api/system` returns valid JSON with `free_ram_mb` key on a live `/proc/meminfo`.
- Simulate missing `/proc/meminfo` (rename it temporarily) and confirm response contains `"free_ram_mb": null` without HTTP error.
- Simulate malformed `/proc/meminfo` (inject garbage lines) and confirm same graceful null behavior.
- Open browser against local server; verify top bar shows sum of up-entry RAM plus free RAM, and that `—` appears when values are absent.
- Confirm no Docker subprocess calls or external dependencies appear in `src/atalaia/system.py`.