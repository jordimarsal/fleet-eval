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

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- html_report.py (first 60 lines of 70088 bytes) ---
"""HTML report of the scoreboard -> results/report.html.

Single-page SELF-CONTAINED: inline CSS, zero dependencies, zero network (can be opened
with a double click or `xdg-open` offline). The scores are computed by the real harness
functions (report._scores / report._global_score with config.WEIGHTS) so that this page
and the CLI always say the same thing.

The scoreboard carries one small inline script: the ranking's order control (by global,
by a dimension, or by task set — MILLORA §C9). Without it the page reads correctly in the
server-side order (--sort), and every row states its test version (SET: label·task-set).

Also owns the model-vs-model compare page (MILLORA §4.4-4.5) -> results/compare.html:
same self-contained contract (inline CSS, zero deps, double click) plus a SMALL
inline JS picker (two selects + swap) that re-renders any pair client-side from the
embedded compact pool JSON (?a=slug,think&b=slug,think). Without JS the page still
shows the server-rendered pair.

Usage:  python3 -m ggufbench.html_report   (writes results/report.html and prints the path)
        or, after any run, python3 -m ggufbench.run --html (same output, one flag)
        python3 -m ggufbench.run --compare "slug,think" "slug,think"   (results/compare.html)
"""

import datetime
import html as _html
import json
import os
import re
import subprocess

from . import config, report as R


def _esc(s):
    return _html.escape(str(s), quote=True)


_RETIRED_STEMS = None


def _retired_stems():
    """Stems of the pruned fleet. Their pool rows stay as a record but render gray.
    Two sources, unioned: the tracked registry (config.RETIRED_FILE — survives the
    profiles being deleted outside the repo) and any profile still parked under
    models/retired/ (parking a profile there retires it by convention). Cached; tests
    reset html_report._RETIRED_STEMS or patch this function for determinism."""
    global _RETIRED_STEMS
    if _RETIRED_STEMS is None:
        _RETIRED_STEMS = _registry_stems() | _archived_profile_stems()
    return _RETIRED_STEMS


def _registry_stems():
    """Stems listed in the retired registry. A missing/corrupt file degrades to empty
    (the report is regenerated on machines that may not have it), never raises."""
    try:
        data = json.loads(config.RETIRED_FILE.read_text())
    except (OSError, ValueError):
        return set()
    stems = set()
    for entry in data.get("retired") or []:
--- tests/test_html_report.py (first 60 lines of 45679 bytes) ---
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from ggufbench import config, html_report, report


def _mk(name="models/foo.gguf", engine="llama", code_score=0.9, tools_score=0.75,
        thinking=None, code_excluded=0):
    """Minimal but complete result (the 4 dimensions + metadata).
    thinking=None -> no key (legacy row); "on"/"off" -> new (R4)."""
    r = {"model": name, "engine": engine, "ts": "2026-10-09T10:00:00",
            "context_mode": "fixed", "tasks_version": "v1", "server_build": "b1234",
            "model_config_flags": "-c 16384 --flash-attn auto",
            "speed": {"passed": True, "turns": 0, "trace": [], "score": 0,
                      "speed_ms": 100, "gen_tps": 100.0, "prompt_tps": 300.0},
            "tools": {"passed": True, "turns": 0, "trace": [], "score": tools_score,
                      "by_lang": {}},
            "code": {"passed": True, "turns": 0, "trace": [], "score": code_score,
                     "by_lang": {"python": code_score}, "excluded": code_excluded},
            "agent": {"passed": True, "turns": 0, "trace": [], "score": 0.5,
                      "by_lang": {"python": 0.5}}}
    if thinking is not None:
        r["thinking"] = thinking
    return r


class TestRender(unittest.TestCase):
    def test_contains_model_dims_and_global(self):
        html = html_report.render([_mk()])
        self.assertIn("foo", html)
        self.assertIn("Weighted global", html)
        self.assertIn("90%", html)                       # code 0.9
        self.assertIn("75%", html)                       # tools 0.75
        # global = .3*.75 + .3*.9 + .25*.5 + .15*1.0 = 0.77 (speed: it is the minimum -> 1.0)
        self.assertIn("0.77", html)

    def test_self_contained_no_external_resources(self):
        """The promise of the module: double click and it works — offline, no dependency.
        It may carry the one inline script that orders the ranking, but nothing fetched:
        no src=, no external URL."""
        html = html_report.render([_mk()])
        self.assertLessEqual(html.count("<script"), 1)            # the order control
        self.assertIn('<script>', html)
        self.assertNotIn("<script src", html)
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)

    def test_sorted_by_global_desc(self):
        html = html_report.render([_mk(name="models/zzz-second.gguf", code_score=0.1, tools_score=0.1),
                                   _mk(name="models/aaa-first.gguf")])
        self.assertLess(html.index("aaa-first"), html.index("zzz-second"))

    def test_engine_badge_for_strata(self):
        html = html_report.render([_mk(name="strata-iq3_xxs", engine="strata")])
        self.assertIn("badge strata", html)

    def test_missing_lang_cell(self):
--- tests/test_report.py (first 60 lines of 37864 bytes) ---
import unittest, json, tempfile, shutil
from pathlib import Path
from ggufbench import report, config

W = {"tools": 0.30, "code": 0.30, "agent": 0.25, "speed": 0.15}


def mk(model, speed_ms=None, gen_tps=None, prompt_tps=None,
       tools=1.0, code=1.0, agent=1.0, code_lang=None, agent_lang=None,
       thinking=None, code_excluded=0):
    # thinking=None -> no key (legacy row, pre-thinking era); "on"/"off" -> new
    r = {"model": model, "context_mode": "fixed", "ts": "2026-08-03T00:00:00",
            "tasks_version": "x", "server_build": "10250",
            "speed": {"passed": True, "turns": 0, "trace": [],
                      "speed_ms": speed_ms, "gen_tps": gen_tps or 0, "prompt_tps": prompt_tps or 0},
            "tools": {"passed": True, "turns": 0, "trace": [], "score": tools, "by_lang": {}, "tasks": []},
            "code": {"passed": True, "turns": 0, "trace": [], "score": code, "by_lang": code_lang or {}, "tasks": [],
                     "excluded": code_excluded},
            "agent": {"passed": True, "turns": 0, "trace": [], "score": agent, "by_lang": agent_lang or {}, "tasks": []}}
    if thinking is not None:
        r["thinking"] = thinking
    return r


class TestReport(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        # RESULTS_RUNS too: save_result writes the receipt (and the agent sidecar)
        # there, and overriding only POOL_FILE dropped junk receipts into the real
        # results/runs/ (docs/conventions.md §Testing).
        self.enterContext(config.override(POOL_FILE=self.tmpdir / "pool.jsonl",
                                          RESULTS_RUNS=self.tmpdir / "runs"))

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_receipts_land_in_the_isolated_results_dir(self):
        """The isolation contract (docs/conventions.md §Testing): POOL_FILE alone is not
        enough — save_result also writes the receipt under RESULTS_RUNS."""
        report.save_result(mk("m", thinking="off"))
        self.assertEqual(len(list((self.tmpdir / "runs").glob("*-m-off.json"))), 1)

    def test_save_result_does_not_touch_the_real_results_dir(self):
        """Regression guard: the suite used to drop junk receipts (m-na.json,
        solo-na.json…) into the real results/runs/, because those tests overrode
        POOL_FILE but not RESULTS_RUNS. This is the test that would have caught it."""
        real = config.RESULTS_DIR / "runs"
        before = sorted(p.name for p in real.glob("*.json")) if real.is_dir() else []
        report.save_result(mk("m", thinking="off"))
        report.save_result(mk("multi", thinking="on"))
        after = sorted(p.name for p in real.glob("*.json")) if real.is_dir() else []
        self.assertEqual(before, after)

    def test_save_and_load(self):
        r = mk("m", speed_ms=100)
        report.save_result(r)
        pool = report.load_pool()
        self.assertEqual(len(pool), 1)
        self.assertEqual(pool[0]["model"], "m")

--- tests/test_graders.py (first 60 lines of 36085 bytes) ---
import contextlib
import json
import io
import unittest
import urllib.error
import tempfile
import shutil
from pathlib import Path
from unittest import mock

from ggufbench import config, executors, graders, token_budget

HAS_SANDBOX = executors._probe_sandbox()

class FakeClient:
    """Client that can be scripted with a sequence of responses per task."""
    def __init__(self, responses):
        self.responses = list(responses); self.i = 0
    def chat(self, *a, **k):
        r = self.responses[self.i % len(self.responses)]; self.i += 1
        return r

class TestToolsGrader(unittest.TestCase):
    def test_pass_and_fail(self):
        tasks = [
            {"id":"t1","prompt":"x","tools":[],"expected":{"name":"f","arguments":{"a":1}}},
            {"id":"t2","prompt":"y","tools":[],"expected":{"name":"g","arguments":{}}},
        ]
        resp_pass = {"choices":[{"finish_reason":"tool_calls","message":{"tool_calls":[
            {"function":{"name":"f","arguments":'{"a":1}'}}]}}]}
        resp_fail = {"choices":[{"finish_reason":"tool_calls","message":{"tool_calls":[
            {"function":{"name":"g","arguments":'{"b":2}'}}]}}], "timings":{}}
        r = graders.grade_tools(FakeClient([resp_pass, resp_fail]), tasks)
        self.assertEqual(r["score"], 0.5)
        self.assertEqual(r["by_lang"], {})  # tools has no by_lang
    def test_noop_case(self):
        tasks = [{"id":"noop","prompt":"hi","tools":[],"expected":None}]  # None = must not call
        resp = {"choices":[{"finish_reason":"stop","message":{"content":"hi!"}}]}
        r = graders.grade_tools(FakeClient([resp]), tasks)
        self.assertEqual(r["score"], 1.0)
    def test_expected_without_arguments_checks_name_only(self):
        # EXPECTED without an 'arguments' key: only the name is checked. Before, the
        # absence required ABSENT arguments and no model ever passed (get_env asks for
        # 'any variable' with var_name required in the schema: impossible).
        tasks = [{"id":"get_env","prompt":"x","tools":[],
                  "expected":{"name":"get_env"}}]
        resp = {"choices":[{"finish_reason":"tool_calls","message":{"tool_calls":[
            {"function":{"name":"get_env","arguments":'{"var_name":"PATH"}'}}]}}]}
        r = graders.grade_tools(FakeClient([resp]), tasks)
        self.assertEqual(r["score"], 1.0)
    def test_expected_empty_arguments_still_strict(self):
        # 'arguments': {} still requires a call without arguments: a call
        # with arguments is not equal to an empty one.
        tasks = [{"id":"get_time","prompt":"x","tools":[],
                  "expected":{"name":"get_time","arguments":{}}}]
        resp = {"choices":[{"finish_reason":"tool_calls","message":{"tool_calls":[
            {"function":{"name":"get_time","arguments":'{"tz":"UTC"}'}}]}}]}
        r = graders.grade_tools(FakeClient([resp]), tasks)
        self.assertEqual(r["score"], 0.0)

--- tests/test_run_cli.py (first 60 lines of 33473 bytes) ---
import contextlib
import io
import json
import platform
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from ggufbench import config, run, report


def _mk(model="m"):
    return {"model": model, "context_mode": "fixed", "ts": "t", "tasks_version": "x",
            "server_build": "b", "speed": {"passed": True, "turns": 0, "trace": [], "score": 0},
            "tools": {"passed": True, "turns": 0, "trace": [], "score": 0},
            "code": {"passed": True, "turns": 0, "trace": [], "score": 0},
            "agent": {"passed": True, "turns": 0, "trace": [], "score": 0}}


class TestForgetCLI(unittest.TestCase):
    """--forget must report honestly: it cannot say 'removed' if it removes nothing."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        # RESULTS_RUNS too: save_result writes the receipt there, and overriding only
        # POOL_FILE dropped junk receipts into the real results/runs/
        # (docs/conventions.md §Testing).
        self.enterContext(config.override(POOL_FILE=self.tmpdir / "pool.jsonl",
                                          RESULTS_RUNS=self.tmpdir / "runs"))

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _run(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            run.main(argv)
        return out.getvalue() + err.getvalue()

    def test_forget_reports_when_nothing_matches(self):
        # With no matching entry: it must NOT say "removed".
        out = self._run(["--forget", "aixonoexisteix"])
        self.assertNotIn("removed", out)
        self.assertIn("no model matching", out)

    def test_forget_reports_actual_removal(self):
        report.save_result(_mk("m"))
        out = self._run(["--forget", "m"])
        self.assertIn("removed", out)
        self.assertEqual(len(report.load_pool()), 0)


class TestParseWeights(unittest.TestCase):
    def test_parse_weights(self):
        w = run.parse_weights("tools=0.4,code=0.3,agent=0.2,speed=0.1")
        self.assertAlmostEqual(w["tools"], 0.4)
        self.assertAlmostEqual(sum(w.values()), 1.0)
--- report.py (first 60 lines of 27422 bytes) ---
import hashlib
import json
import datetime
import os
import statistics
from typing import Any

from . import config


def task_signature(result):
    """Task set a result was measured with: the graded counts per dimension
    ('tools/code/agent', e.g. '16/60/60'), from the recorded field or derived from the
    traces ('?' for a dimension that was not measured).

    The suite version (config.TASKS_VERSION) is a label and cannot describe the set: v3
    covered four different counts because the C3 additions never bumped it, so two rows
    could share a version and still be incomparable. The signature comes from the data,
    which is why the scoreboard and the compare page compare signatures."""
    stored = result.get("task_signature")
    if stored:
        return str(stored)
    counts = (len((result.get(d) or {}).get("trace") or [])
              for d in ("tools", "code", "agent"))
    return "/".join(str(n) if n else "?" for n in counts)


def signature_counts(pool):
    """{task_signature: number of rows}, most frequent first. More than one entry means
    the pool mixes task sets — the drift the report must announce instead of hiding."""
    counts = {}
    for r in pool:
        sig = task_signature(r)
        counts[sig] = counts.get(sig, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def baseline_flags() -> str:
    """The baseline a row is measured under, as text: the harness' common flags
    (`config.baseline_argv()` = SERVER_FLAGS + CACHE_FLAGS) — never the per-model profile,
    which is already recorded as `model_config_flags`. It is a CONDITION (§C10): ADR-0008
    switched the KV cache q4_0 -> q8_0, so rows measured before it are not comparable with
    rows measured after, and nothing else in the data says so."""
    return " ".join(config.baseline_argv())


def baseline_id(row) -> str:
    """Short id of the baseline recorded in a row (the flags themselves live in config; the
    id is what the board prints). '?' when the row predates the field: the baseline was
    never recorded, and inventing one would turn an unknown condition into a
    seemingly known one."""
    flags = row.get("baseline_flags")
    if not isinstance(flags, str) or not flags:
        return "?"
    return hashlib.sha1(flags.encode("utf-8")).hexdigest()[:8]


def _engine_label(row) -> str:
    """Engine and build as ONE value: the pair is the condition (a build change is what
    makes two rows incomparable), and the engine name alone would hide it."""
--- run.py (first 60 lines of 27114 bytes) ---
import argparse
import datetime
import urllib.request
import difflib
import json
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

from . import config, server as S, client as C, graders as G, tasks_loader as T, report as R, html_report


def parse_weights(s):
    if not s:
        return dict(config.WEIGHTS)
    w = {}
    for part in s.split(","):
        k, v = part.split("=")
        w[k.strip()] = float(v)
    return w


def resolve_models(spec, engine="llama"):
    """all -> glob of the models directory. Otherwise, each item (comma-separated)
    can be:
      - an existing path (used as is),
      - a short or partial file name ('Ornith-...APEX-MTP-Quality[.gguf]'),
        resolved against models/*.gguf (same spirit as --forget);
        if it matches more than one file, a warning is printed and it is skipped (ambiguous),
      - a nonexistent path: passes through as is and llama-server will report the error.

    With ``engine='strata'`` the 'model' is a config: 'iq3_xxs' ->
    Strata/strata-iq3_xxs.json (and 'all' = every strata-*.json)."""
    if engine == "strata":
        return _resolve_strata_models(spec)
    if spec == "all":
        return sorted(str(p) for p in config.MODELS_DIR.glob("*.gguf"))
    if isinstance(spec, str):
        spec = [x.strip() for x in spec.split(",") if x.strip()]
    resolved = []
    for item in spec:
        if Path(item).is_file():
            resolved.append(item)
            continue
        matches = sorted(config.MODELS_DIR.glob(f"*{item}*"))
        if len(matches) == 1:
            resolved.append(str(matches[0]))
        elif len(matches) > 1:
            names = ", ".join(m.name for m in matches)
            print(f"⚠️  '{item}' is ambiguous ({names}); no unique match, ignored",
                  file=sys.stderr, flush=True)
        else:
            resolved.append(item)
    return resolved


def _resolve_strata_models(spec):
--- graders.py (first 60 lines of 25874 bytes) ---
from typing import Any

import statistics
import sys
import urllib.error

from . import config
from . import agent as A, client as C, code_extract, executors, token_budget

SPEED_MAX_TOKENS = 128
# A single generous budget (ADR-0002; R3 thinking_batches: starts at 32768 by the
# reviewer's decision — the expert tasks need it). With fixed seed/temp, max_tokens is a
# ceiling, not a target: it does not penalize concise models (they stop at EOS anyway).
# Environment precondition: every model in the pool must have context for prompt + 32768.
# CONTEXT_FIXED is 32768 (the whole budget, no room for the prompt), so a profile without
# -c does NOT meet this precondition: it needs its own -c or the context audit (SPEC §2).
# Output tokens are recorded in the trace (out_tokens) as an efficiency
# metric, not a penalty.
CODE_MAX_TOKENS = 32768
CODE_LADDER = [CODE_MAX_TOKENS]

# Transient server/network errors (500, timeouts, dropped connection...).
# Isolate them per task: a 500 response must only fail that task, not abort the whole run.
_TRANSIENT = (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError)


def grade_speed(client_mod, tasks, on_task=None):
    results = []
    for task in tasks:
        speed_ms_values, gen_tps_values, prompt_tps_values = [], [], []
        for _ in range(3):
            try:
                resp = client_mod.chat([{"role": "user", "content": task["prompt"]}],
                                       max_tokens=SPEED_MAX_TOKENS)
                t = C.parse_timings(resp)
                if not t:
                    continue
                if t.get("completion_ms"):
                    speed_ms_values.append(t["completion_ms"])
                if t.get("gen_tps"):
                    gen_tps_values.append(t["gen_tps"])
                if t.get("prompt_tps"):
                    prompt_tps_values.append(t["prompt_tps"])
            except _TRANSIENT:
                pass  # sample discarded; another one can compensate
        avg = lambda xs: statistics.mean(xs) if xs else 0
        entry = {
            "passed": True,
            "turns": 0,
            "trace": [],
            "speed_ms": int(avg(speed_ms_values)) if speed_ms_values else 0,
            "gen_tps": round(avg(gen_tps_values), 1) if gen_tps_values else 0,
            "prompt_tps": round(avg(prompt_tps_values), 1) if prompt_tps_values else 0,
        }
        results.append(entry)
        if on_task:
            on_task("speed", {"id": task["id"], "ms": entry["speed_ms"], "gen_tps": entry["gen_tps"]})
    ms_vals = [r["speed_ms"] for r in results if r["speed_ms"]]
    total_speed_ms = statistics.mean(ms_vals) if ms_vals else 0
    def _mean_field(field):

Write ONLY the plan (the three sections). No prose outside them.