ROLE: implementation planner. A feature has been approved. You get the
approved requirements and the repository file tree BEFORE implementation.
Write the implementation plan with EXACTLY these three sections:

FILES
<repo-relative path of every file you would create or modify, one per line>

TASKS
T1: <short title>
    depends_on: (none)
    refs: R1, R2
T2: <short title>
    depends_on: T1
    refs: R3
(... ordered so dependencies come first; every requirement must be covered
 by the refs of at least one task)

GATES
<the verification gates you would run before closing the feature>

--- APPROVED REQUIREMENTS ---
R1: WHEN a client requests `GET /api/system`, the system shall return `free_ram_mb` taken from `MemAvailable` in `/proc/meminfo` (converted to MB).

R2: IF `/proc/meminfo` is missing or malformed, THEN the system shall return `free_ram_mb` as null without failing the request.

R3: The UI top bar shall display the sum of `ram_mb` of every `up` entry and the free RAM from `/api/system`, refreshed on every poll.

R4: WHEN any value is unavailable, the UI shall display `—` for that value.

R5: The system summary read shall not require Docker or subprocess calls (direct file read of `/proc/meminfo`).

--- FEATURE TITLE ---
f8_ram_summary review APPROVED (5/5)

--- REPOSITORY FILE TREE (before implementation) ---
.opencode/agent/implementer.md
.opencode/agent/leader.md
.opencode/agent/reviewer.md
.opencode/agent/spec-author.md
AGENTS.md
HARNESS.md
README.md
dashboard.yaml
design-system/atalaia/MASTER.md
docs/architecture.md
docs/conventions.md
docs/specs.md
docs/verification.md
harness/CHECKPOINTS.md
harness/feature_list.json
harness/init.sh
harness/progress/current.md
harness/progress/history.md
harness/progress/impl_f1_scanner.md
harness/progress/impl_f2_ui.md
harness/progress/impl_f3_actions.md
harness/progress/impl_f4_archive.md
harness/progress/impl_f5_truth_containers.md
harness/progress/impl_f6_ram.md
harness/progress/impl_f7_stop_all.md
harness/progress/review_f1_scanner.md
harness/progress/review_f2_ui.md
harness/progress/review_f3_actions.md
harness/progress/review_f4_archive.md
harness/progress/review_f5_truth_containers.md
harness/progress/review_f6_ram.md
harness/progress/review_f7_stop_all.md
harness/specs/f1_scanner/APPROVAL
harness/specs/f1_scanner/design.md
harness/specs/f1_scanner/requirements.md
harness/specs/f1_scanner/review.md
harness/specs/f1_scanner/tasks.md
harness/specs/f2_ui/APPROVAL
harness/specs/f2_ui/design.md
harness/specs/f2_ui/requirements.md
harness/specs/f2_ui/review.md
harness/specs/f2_ui/tasks.md
harness/specs/f3_actions/APPROVAL
harness/specs/f3_actions/design.md
harness/specs/f3_actions/requirements.md
harness/specs/f3_actions/review.md
harness/specs/f3_actions/tasks.md
harness/specs/f4_archive/APPROVAL
harness/specs/f4_archive/design.md
harness/specs/f4_archive/requirements.md
harness/specs/f4_archive/review.md
harness/specs/f4_archive/tasks.md
harness/specs/f5_truth_containers/APPROVAL
harness/specs/f5_truth_containers/design.md
harness/specs/f5_truth_containers/requirements.md
harness/specs/f5_truth_containers/review.md
harness/specs/f5_truth_containers/tasks.md
harness/specs/f6_ram/APPROVAL
harness/specs/f6_ram/design.md
harness/specs/f6_ram/requirements.md
harness/specs/f6_ram/review.md
harness/specs/f6_ram/tasks.md
harness/specs/f7_stop_all/design.md
harness/specs/f7_stop_all/requirements.md
harness/specs/f7_stop_all/review.md
harness/specs/f7_stop_all/tasks.md
harness/tools/audit-security.sh
harness/tools/check-traceability.py
harness/tools/validate-feature-list.py
opencode.json
pyproject.toml
scripts/e2e_actions_demo.py
scripts/e2e_archive_demo.py
scripts/e2e_stopall_demo.py
src/atalaia/__init__.py
src/atalaia/actions.py
src/atalaia/api.py
src/atalaia/archive.py
src/atalaia/detail.py
src/atalaia/detectors.py
src/atalaia/ids.py
src/atalaia/models.py
src/atalaia/scanner.py
tests/test_actions.py
tests/test_actions_stopall.py
tests/test_api.py
tests/test_api_actions.py
tests/test_api_archive.py
tests/test_api_containers.py
tests/test_api_detail.py
tests/test_api_ram.py
tests/test_api_stopall.py
tests/test_archive.py
tests/test_detail.py
tests/test_detectors.py
tests/test_ids.py
tests/test_scanner.py
tests/test_web.py
tests/test_web_static.py
web/app.js
web/index.html
web/style.css

Write ONLY the plan (the three sections). No prose outside them.