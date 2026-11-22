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
R1: The `/metrics` parser shall accept every numeric sample value legal in the Prometheus text format: decimal, scientific notation, a leading `+`, and the special tokens `NaN`, `+Inf` and `-Inf`.

R2: The `/metrics` parser shall accept an optional sample timestamp written as an integer or a decimal number (OpenMetrics).

R3: The `/metrics` parser shall accept label values that contain braces inside quotes, and escaped quotes inside label values.

R4: When a `/metrics` line still violates the exposition format, `metrics()` shall raise `LlamaCppMalformedResponseError` naming the offending line, as in R16 of feature 2.

R5: Memory recognition shall use only sample names ending in `_bytes`. The `"memory"` substring heuristic is removed: `memory_pool_count` or `process_memory_kib` never become a GiB value. Non-finite and negative samples remain unrecognized (feature 2, R14).

R6: `manifest()` shall cache the artifact sha256 across calls, but shall resolve `engine_version` on every call from the configuration pin or the most recent observed `system_fingerprint`. Repeated calls shall not re-hash the artifact and shall reflect a fingerprint observed after the first call. This supersedes the object-identity reading of R25 in feature 2; the closed feature 2 spec is not edited.

R7: A `LlamaCppBackend` instance shall be safe for concurrent `run()`, `metrics()` and `manifest()` calls from multiple threads: successful-run counters, the fingerprint and the artifact hash cache are updated under a lock, and concurrent `manifest()` calls compute the hash once. HTTP requests are never performed while holding the lock.

R8: `LlamaCppConfig` shall validate `base_url` with `urllib.parse`: scheme `http` or `https` case-insensitively and normalized to lower case, a non-empty hostname, an optional port in 1–65535, no whitespace, no query/fragment, and no userinfo (credentials). Path prefixes are preserved; trailing slashes are stripped.

R9: A chat completion with `finish_reason == "length"` or empty `content` shall be recorded as a success with its token counts and `error=None`. Truncation handling is the runner/scorer's responsibility and shall be documented in the adapter design; the frozen core contract is not changed.

R10: The amended R29 scope shall be documented and tested: the host, port, model identifier and file location come only from configuration, while the HTTP route suffixes and the sampling defaults are fixed adapter constants. This supersedes the literal wording of R29 in feature 2; the closed feature 2 spec is not edited.

R11: The test stub shall use a listen backlog of at least 512 and the suite shall include a 300-run, 64-thread concurrency test proving zero lost updates and an exact `tokens_per_second` ratio. The test runs offline and deterministically.

--- FEATURE TITLE ---
fix(llamacpp): harden the parser, manifest cache and concurrency

--- REPOSITORY FILE TREE (before implementation) ---
.gitignore
.opencode/agent/implementer.md
.opencode/agent/leader.md
.opencode/agent/reviewer.md
.opencode/agent/spec-author.md
AGENTS.md
HARNESS.md
README.md
docs/architecture.md
docs/clarity-style.md
docs/conventions.md
docs/decisions/core-contract-data-model-pydantic.md
docs/decisions/core-contract-shared-core-boundary.md
docs/decisions/llamacpp-backend-command-semantics.md
docs/decisions/llamacpp-backend-error-routing.md
docs/fleet.md
docs/gauntlet-protocol.md
docs/model-field-notes.md
docs/specs.md
docs/verification.md
opencode.json
pyproject.toml
src/quantdelta/__init__.py
src/quantdelta/backends/__init__.py
src/quantdelta/backends/llamacpp/__init__.py
src/quantdelta/backends/llamacpp/backend.py
src/quantdelta/backends/llamacpp/config.py
src/quantdelta/backends/llamacpp/errors.py
src/quantdelta/backends/llamacpp/manifest.py
src/quantdelta/core/__init__.py
src/quantdelta/core/errors.py
src/quantdelta/core/models.py
src/quantdelta/core/ports.py
src/quantdelta/core/serialization.py
tests/test_smoke.py
tests/unit/backends/llamacpp/conftest.py
tests/unit/backends/llamacpp/test_backend.py
tests/unit/backends/llamacpp/test_boundary.py
tests/unit/backends/llamacpp/test_config.py
tests/unit/backends/llamacpp/test_llamacpp_errors.py
tests/unit/backends/llamacpp/test_manifest.py
tests/unit/backends/llamacpp/test_metrics.py
tests/unit/backends/llamacpp/test_run.py
tests/unit/backends/llamacpp/test_stub_server.py
tests/unit/core/test_errors.py
tests/unit/core/test_import_boundary.py
tests/unit/core/test_models.py
tests/unit/core/test_public_api.py
tests/unit/core/test_serialization.py

Write ONLY the plan (the three sections). No prose outside them.