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
R1: WHEN the pool holds both live and retired rows, the report SHALL render a tab bar with two panes — Board (live rows only) and Retired (retired rows only) — both present in the single document, one visible at a time.

R2: WHEN the report is opened, the Board pane SHALL be the visible one by default (no storage, no JavaScript needed to reach it).

R3: WHILE the pool holds no retired rows, the report SHALL render the board content without a tab bar and without the retired pane.

R4: The Retired pane SHALL NOT contain the Recommendations section nor the KPI strip: it is a record, and a retired model can neither be recommended nor win a live headline.

R5: The KPI strip (Best overall, Fastest (gen), Lowest latency, Newest model) SHALL be computed from the live rows only — no headline figure may come from a model that was deleted.

R6: The Recommendations section SHALL appear after the KPI strip and before the "Weighted global" section.

R7: Within every per-dimension list of the report (code, agent, tools, speed in ms, gen t/s, prompt t/s) the rows SHALL run from best performer to worst — descending for the higher-is-better scores and throughputs, ascending for latency — including the lists of the Retired pane.

R8: The Board pane SHALL NOT render any retired row (the gray styling and the "retired" badge stay, inside the Retired pane).

R9: The Retired pane SHALL state that these models are a record only — retired from the bench, unable to run again.

R10: WHILE the pool holds retired rows, the header "models" chip SHALL state the two counts separately (e.g. `18 models (+16 retired)`); without retired rows it SHALL keep the single total.

R11: The "task sets" chip SHALL link only to set blocks rendered in the Board pane; a signature that exists only among retired rows SHALL be named as text, never as a link to a block that cannot be seen.

R12: The report SHALL remain self-contained — no external resource, at most the existing single inline script — and the two panes SHALL stay switchable with JavaScript disabled (pure CSS).

--- FEATURE TITLE ---
chore(progress): close report_polish (feature 8 done, report published)

--- REPOSITORY FILE TREE (before implementation) ---
.github/workflows/ci.yml
.gitignore
.opencode/agent/implementer.md
.opencode/agent/leader.md
.opencode/agent/reviewer.md
.opencode/agent/spec-author.md
AGENTS.md
HARNESS.md
LICENSE
README.md
__init__.py
agent.py
benchmarks/__init__.py
benchmarks/test_bench_code_extract.py
benchmarks/test_bench_html.py
benchmarks/test_bench_report.py
benchmarks/test_bench_tasks.py
client.py
code_extract.py
config.py
docs/SPEC.md
docs/architecture.md
docs/conventions.md
docs/plan.md
docs/security-audit.md
docs/specs.md
docs/verification.md
docs/writeups/which-local-model-for-coding-agents.ca.md
docs/writeups/which-local-model-for-coding-agents.es.md
docs/writeups/which-local-model-for-coding-agents.md
executors.py
graders.py
harness/CHECKPOINTS.md
harness/baselines.json
harness/decisions/0001-code-timeout-token-budget.md
harness/decisions/0002-single-code-token-budget.md
harness/decisions/0003-stdlib-only-harness.md
harness/decisions/0004-fixed-seed-temp-baselines.md
harness/decisions/0005-second-engine-strata.md
harness/decisions/0006-thinking-off-by-default.md
harness/decisions/0007-fixed-infra-ports.md
harness/decisions/0008-cache-q8_0-baseline.md
harness/decisions/0009-pool-identity-file-name.md
harness/decisions/_template.md
harness/feature_list.json
harness/init.sh
harness/logs/remeasure_pool/strata-0.1.41-rows.json
harness/progress/current.md
harness/progress/history.md
harness/progress/impl_c10.md
harness/progress/impl_discriminative_tasks.md
harness/progress/impl_hard_code_tier.md
harness/progress/impl_remeasure_pool.md
harness/progress/impl_single_token_budget.md
harness/progress/impl_thinking_batches.md
harness/progress/impl_timeout_scaling.md
harness/retired.json
harness/specs/discriminative_tasks/APPROVAL
harness/specs/discriminative_tasks/completion-gate.md
harness/specs/discriminative_tasks/design.md
harness/specs/discriminative_tasks/requirements.md
harness/specs/discriminative_tasks/review.md
harness/specs/discriminative_tasks/smoke-r5.md
harness/specs/discriminative_tasks/spec-gate.md
harness/specs/discriminative_tasks/tasks.md
harness/specs/discriminative_tasks/traceability-check.txt
harness/specs/hard_code_tier/APPROVAL
harness/specs/hard_code_tier/completion-gate.md
harness/specs/hard_code_tier/design.md
harness/specs/hard_code_tier/requirements.md
harness/specs/hard_code_tier/spec-gate.md
harness/specs/hard_code_tier/tasks.md
harness/specs/hard_code_tier/traceability-check.txt
harness/specs/lora_eval/design.md
harness/specs/lora_eval/requirements.md
harness/specs/lora_eval/tasks.md
harness/specs/remeasure_pool/APPROVAL
harness/specs/remeasure_pool/blocked.md
harness/specs/remeasure_pool/design.md
harness/specs/remeasure_pool/requirements.md
harness/specs/remeasure_pool/review.md
harness/specs/remeasure_pool/spec-gate.md
harness/specs/remeasure_pool/tasks.md
harness/specs/remeasure_pool/traceability-check.txt
harness/specs/single_token_budget/APPROVAL
harness/specs/single_token_budget/design.md
harness/specs/single_token_budget/requirements.md
harness/specs/single_token_budget/spec-gate.md
harness/specs/single_token_budget/tasks.md
harness/specs/single_token_budget/traceability-check.txt
harness/specs/thinking_batches/APPROVAL
harness/specs/thinking_batches/completion-gate.md
harness/specs/thinking_batches/design.md
harness/specs/thinking_batches/requirements.md
harness/specs/thinking_batches/review.md
harness/specs/thinking_batches/tasks.md
harness/specs/thinking_batches/traceability-check.txt
harness/specs/timeout_scaling/APPROVAL
harness/specs/timeout_scaling/design.md
harness/specs/timeout_scaling/requirements.md
harness/specs/timeout_scaling/spec-gate.md
harness/specs/timeout_scaling/tasks.md
harness/specs/timeout_scaling/traceability-check.txt
harness/tools/audit-security.sh
harness/tools/bench.sh
harness/tools/check-task.py
harness/tools/check-traceability.py
harness/tools/commit-msg
harness/tools/context-audit.py
harness/tools/probe-context.py
harness/tools/publish-report.sh
harness/tools/validate-feature-list.py
html_report.py
mypy.ini
opencode.json
pyproject.toml
report.py
run.py
server.py
tasks/agent/bash/add_feature.py
tasks/agent/bash/archive_verify.py
tasks/agent/bash/config_file_parser.py
tasks/agent/bash/csv_quoted_fields.py
tasks/agent/bash/csv_transform.py
tasks/agent/bash/debug.py
tasks/agent/bash/document.py
tasks/agent/bash/fix_bug.py
tasks/agent/bash/log_level_filter.py
tasks/agent/bash/log_triage.py
tasks/agent/bash/multi_file_aggregation.py
tasks/agent/bash/optimize.py
tasks/agent/bash/parallel_safe_tempfiles.py
tasks/agent/bash/refactor.py
tasks/agent/bash/retry_backoff.py
tasks/agent/bash/retry_pipeline.py
tasks/agent/bash/signal_trap_cleanup.py
tasks/agent/bash/space_traps.py
tasks/agent/java/add_feature.py
tasks/agent/java/add_interface_method.py
tasks/agent/java/builder_pattern_retrofit.py
tasks/agent/java/checked_exception_plumbing.py
tasks/agent/java/debug.py
tasks/agent/java/document.py
tasks/agent/java/equals_hashcode_contract.py
tasks/agent/java/feature_flag_end_to_end.py
tasks/agent/java/fix_bug.py
tasks/agent/java/fix_compile_error.py
tasks/agent/java/generics_wildcard_fix.py
tasks/agent/java/interface_mismatch.py
tasks/agent/java/invoice_dup_merge.py
tasks/agent/java/optimize.py
tasks/agent/java/optional_migration.py
tasks/agent/java/refactor.py
tasks/agent/java/shape_area_contract.py
tasks/agent/java/stream_api_migration.py
tasks/agent/python/add_feature.py
tasks/agent/python/cli_dry_run_feature.py
tasks/agent/python/cli_exit_code.py
tasks/agent/python/config_migration.py
tasks/agent/python/dataclasses_migration.py
tasks/agent/python/debug.py
tasks/agent/python/dependency_order.py
tasks/agent/python/document.py
tasks/agent/python/exception_safety.py
tasks/agent/python/fix_bug.py
tasks/agent/python/input_validation_layer.py
tasks/agent/python/invoice_dup_merge.py
tasks/agent/python/logging_retrofit.py
tasks/agent/python/optimize.py
tasks/agent/python/refactor.py
tasks/agent/python/refactor_guard.py
tasks/agent/python/stock_alert_thresholds.py
tasks/agent/python/test_driven_fix.py
tasks/agent/typescript/add_feature.py
tasks/agent/typescript/add_feature_type_discipline.py
tasks/agent/typescript/async_ordering.py
tasks/agent/typescript/async_queue_ordering.py
tasks/agent/typescript/csv_row_validator.py
tasks/agent/typescript/debug.py
tasks/agent/typescript/discriminated_union_exhaustiveness.py
tasks/agent/typescript/document.py
tasks/agent/typescript/error_union_handling.py
tasks/agent/typescript/feature_flag_end_to_end.py
tasks/agent/typescript/fix_bug.py
tasks/agent/typescript/namespace_to_module.py
tasks/agent/typescript/optimize.py
tasks/agent/typescript/order_merge_duplicates.py
tasks/agent/typescript/promise_rejection_handling.py
tasks/agent/typescript/readonly_deep_refactor.py
tasks/agent/typescript/refactor.py
tasks/agent/typescript/strict_null_fix.py
tasks/code/bash/access_agg_expert.py
tasks/code/bash/bubble_sort.py
tasks/code/bash/count_lines_hard.py
tasks/code/bash/count_words.py
tasks/code/bash/csv_stats_expert.py
tasks/code/bash/dedup_hard.py
tasks/code/bash/fibonacci.py
tasks/code/bash/format_duration_expert.py
tasks/code/bash/is_prime.py
tasks/code/bash/log_filter_debug_expert.py
tasks/code/bash/num_report_expert.py
tasks/code/bash/parse_size_hard.py
tasks/code/bash/remove_duplicates.py
tasks/code/bash/reverse_string.py
tasks/code/bash/simple_math.py
tasks/code/bash/subst_hard.py
tasks/code/bash/sum_col_hard.py
tasks/code/bash/sum_list.py
tasks/code/java/bracket_validator_hard.py
tasks/code/java/bubble_sort.py
tasks/code/java/count_words.py
tasks/code/java/csv_index_expert.py
tasks/code/java/csv_stats_expert.py
tasks/code/java/fibonacci.py
tasks/code/java/interval_codec_expert.py
tasks/code/java/is_prime.py
tasks/code/java/ledger_debug_expert.py
tasks/code/java/lower_upper_bound_hard.py
tasks/code/java/min_stack_hard.py
tasks/code/java/parse_size_hard.py
tasks/code/java/remove_duplicates.py
tasks/code/java/reverse_string.py
tasks/code/java/roman_to_int_hard.py
tasks/code/java/schedule_slots_expert.py
tasks/code/java/simple_math.py
tasks/code/java/sum_list.py
tasks/code/python/bubble_sort.py
tasks/code/python/count_words.py
tasks/code/python/fibonacci.py
tasks/code/python/fix_apply_discount_hard.py
tasks/code/python/is_prime.py
tasks/code/python/ledger_fifo_expert.py
tasks/code/python/lru_cache_hard.py
tasks/code/python/merge_intervals_hard.py
tasks/code/python/metrics_debug_expert.py
tasks/code/python/parse_size_hard.py
tasks/code/python/readings_etl_expert.py
tasks/code/python/remove_duplicates.py
tasks/code/python/reverse_string.py
tasks/code/python/simple_math.py
tasks/code/python/sum_list.py
tasks/code/python/ttl_cache_debug_expert.py
tasks/code/python/two_sum_count_hard.py
tasks/code/python/vault_engine_expert.py
tasks/code/typescript/bubble_sort.py
tasks/code/typescript/count_words.py
tasks/code/typescript/csv_stats_expert.py
tasks/code/typescript/deep_equal_hard.py
tasks/code/typescript/diff_objects_expert.py
tasks/code/typescript/event_debug_expert.py
tasks/code/typescript/event_emitter_hard.py
tasks/code/typescript/fibonacci.py
tasks/code/typescript/flatten_depth_hard.py
tasks/code/typescript/is_prime.py
tasks/code/typescript/jsonl_agg_expert.py
tasks/code/typescript/memo_fib_hard.py
tasks/code/typescript/parse_size_hard.py
tasks/code/typescript/proc_registry_expert.py
tasks/code/typescript/remove_duplicates.py
tasks/code/typescript/reverse_string.py
tasks/code/typescript/simple_math.py
tasks/code/typescript/sum_list.py
tasks/speed/hello.py
tasks/tools/archive_not_delete.py
tasks/tools/check_solution.py
tasks/tools/check_then_read.py
tasks/tools/get_env.py
tasks/tools/get_time.py
tasks/tools/list_files.py
tasks/tools/nested_filter_args.py
tasks/tools/noop.py
tasks/tools/pick_weather.py
tasks/tools/read_config_then_save.py
tasks/tools/read_file.py
tasks/tools/refuse_delete_protected.py
tasks/tools/save_file.py
tasks/tools/save_no_optional.py
tasks/tools/schedule_event.py
tasks/tools/search.py
tasks/tools/tags_exact.py
tasks/tools/toggle_bool.py
tasks_loader.py
tests/__init__.py
tests/test_agent.py
tests/test_agent_tasks.py
tests/test_client.py
tests/test_code_extract.py
tests/test_config.py
tests/test_context_audit.py
tests/test_executors.py
tests/test_expert_tasks.py
tests/test_graders.py
tests/test_hard_tasks.py
tests/test_html_report.py
tests/test_probe_context.py
tests/test_report.py
tests/test_run_cli.py
tests/test_server.py
tests/test_smoke.py
tests/test_smoke_evidence.py
tests/test_tasks_loader.py
tests/test_token_budget.py
tests/test_tools_tasks.py
token_budget.py

Write ONLY the plan (the three sections). No prose outside them.