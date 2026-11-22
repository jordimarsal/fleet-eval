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
R1: The `Scorer` port shall score one task output at a time: `score(*, task: Task, output: TaskOutput) -> Score`. The signature is keyword-only, references only core types, keeps the `metric: str` attribute, and replaces the `record: RunRecord` signature. The scorer returns one score per successful output; replicate aggregation stays outside the core.

R2: The core shall expose two frozen value types for next-token probabilities: `TokenAlternative` with `token: str` and `logprob: float`, and `TokenLogprob` with `token: str`, `logprob: float` and `top_logprobs: tuple[TokenAlternative, ...] = ()`. Both shall validate that the token is non-empty and the log-probability is finite and `<= 0`. `TokenLogprob` shall reject duplicate alternative token strings; the generated token may also appear in `top_logprobs`, and the order is preserved.

R3: `TaskOutput` shall carry an optional `logprobs: tuple[TokenLogprob, ...] | None = None`. `None` means log-probabilities were not requested; an empty tuple means they were requested but the engine returned no generated tokens. The field is additive and does not change `RunRecord` or the JSONL format.

R4: The core shall expose a frozen `TaskKL` type with `task_id: str`, `divergence: float`, `reference_mass: float` and `variant_mass: float`. `task_id` shall be non-empty, `divergence` finite and `>= 0`, and both masses finite in `[0, 1]`. The type carries the result of one KL estimate and the probability mass that the estimate retained on each side.

R5: `Report` shall carry three additive fields: `kl_divergence: float | None = None`, `task_kl: tuple[TaskKL, ...] = ()` and `kl_method: str | None = None`. They shall be all-or-nothing: either all absent/empty, or `task_kl` non-empty, `kl_divergence` finite and `>= 0`, and `kl_method` non-empty. `task_kl` task ids shall be unique and each shall exist in `deltas`; `kl_divergence` shall equal the arithmetic mean of the `TaskKL.divergence` values within an absolute tolerance of `1e-9`. A report with no KL fields shall remain valid.

R6: The serialized schema shall stay version `"1"`. A pre-feature `Report` JSON without the KL fields shall parse with the defaults; a new `Report` with KL fields shall round-trip through `to_json`/`from_json` unchanged; unknown fields shall still be rejected; `RunRecord`, `to_jsonl` and `parse_jsonl` shall be unchanged. ADR-008 shall record the additive policy and its relationship with ADR-001 and R12.

R7: `TokenAlternative`, `TokenLogprob` and `TaskKL` shall be exported from `quantdelta.core` and pinned by the public API snapshot; the `Scorer` signature change shall be pinned too. The core shall add no runtime dependency and shall keep its import boundary (no httpx, no I/O, no adapter vocabulary).

R8: Every invalid value shall raise `InvalidDataError` naming the offending field (or `<root>` only when no single field applies). At minimum: NaN/Inf/positive log-probabilities, empty tokens, duplicate alternative tokens, masses outside `[0, 1]`, negative or non-finite KL, duplicate `TaskKL` ids, a `TaskKL` id absent from `deltas`, a KL mean mismatch, and a partial KL field set. Tests shall cover each rule, the old-report compatibility, the new round-trip, the port signature and the public exports.

--- FEATURE TITLE ---
feat(core)!: score task outputs, carry logprobs and report KL

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
docs/decisions/llamacpp-backend-threading.md
docs/decisions/llamacpp-manifest-cache.md
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
tests/unit/backends/llamacpp/test_concurrency.py
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