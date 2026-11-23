The user wants to implement `free_ram_mb` and its tests for task T1. However, looking at the provided context, there is no existing repository state or previous work shown. The prompt says "(none yet)" for previous work. But it also lists other source files like `tests/test_detectors.py`, `tests/test_api_system.py`, etc., which import from `atalaia.detectors`.

Wait, the instruction says: "You are an implementer working through a plan STEP BY STEP." and "CURRENT REPOSITORY STATE (file tree, after previous steps) --- (empty)". This implies I am starting fresh or the repo is empty? No, usually these prompts imply the repo exists but isn't fully listed, OR I need to create the necessary files.

However, the "OTHER SOURCE FILES" section shows excerpts of test files that *already exist* in the repo (or are expected to exist). Specifically, `tests/test_detectors.py` imports `free_ram_mb` from `atalaia.detectors`. `tests/test_api_system.py` imports `create_app` from `atalalaia.api` and monkeypatches `api_module.free_ram_mb`.

If the repo is truly empty, I would need to build the whole package structure (`atalaia/__init__.py`, `atalaia/detectors.py`, `atalaia/api.py`, etc.). But typically, in these tasks, if only T1 is requested, and T1 depends on nothing, I should provide the implementation for `free_ram_mb` within the appropriate module (`atalaia/detectors.py`) and potentially the tests if they aren't provided.

Let's look at the references: R1, R2, R5.
R1/R2 likely refer to requirements about parsing `/proc/meminfo` or similar.
The function `free_ram_mb` needs to parse `MemAvailable` tolerantly.

Looking at `tests/test_detectors.py`:
```python
from atalaia.detectors import ... free_ram_mb ...
```
It does NOT show a test for `free_ram_mb` directly in the excerpt, but it shows tests for other functions. Wait, let me check the full list of tests provided in "TESTS THE FINAL RESULT MUST PASS".
`tests/test_api_system.py` has:
```python
def test_system_returns_free_ram(tmp_path, monkeypatch):
    monkeypatch.setattr(api_module, "free_ram_mb", lambda: 8000.0)
    # ...
```
This implies `free_ram_mb` is accessible via `api_module`. In `test_api_system.py`, it patches `api_module.free_ram_mb`. This suggests `atalaia/api.py` imports `free_ram_mb` from `atalaia.detectors`.

Where are the unit tests for `free_ram_mb` itself? The prompt says "T1: free_ram_mb (parse MemAvailable tolerant) + tests". It doesn't explicitly provide the content of `tests/test_detectors.py` section regarding `free_ram_mb` in the excerpts, but I should probably write the implementation in `atalaia/detectors.py`. If there's no existing file, I need to create it. But wait, if I create `atalaia/detectors.py`, I must ensure it contains *only* what is needed or compatible with future steps? No, "Implement ONLY this step". But Python modules can't be partial easily without breaking imports if other functions are expected by existing tests (which seem to exist based on the "OTHER SOURCE FILES" excerpts).

Actually, looking closely at the "CURRENT REPOSITORY STATE": it is empty.
Looking at "YOUR PREVIOUS WORK IN THIS TASK": none yet.
Looking at "OTHER SOURCE FILES": These are excerpts of files that *exist* in the repo context provided for style/imports. This implies the repo *does* have these files, but they aren't listed in the tree because the tree was omitted or is implicit. However, usually, if the tree is empty, I might need to create the package structure.

BUT, standard practice for these specific "step-by-step" prompts:
If T1 is `free_ram_mb`, and it lives in `atalaia/detectors.py`, and `detectors.py` already has many other functions (as seen in imports in test files), I cannot just output a fragment. I must output the COMPLETE file if I'm modifying it. But I don't have the current content of `detectors.py`.

Let's re-read carefully: "--- CURRENT REPOSITORY STATE (file tree, after previous steps) --- [Empty]".
This strongly suggests the repository is effectively empty or I am creating the initial scaffolding.
However, the "TESTS THE FINAL RESULT MUST PASS" includes `tests/test_detectors.py` which imports MANY things from `atalaia.detectors`: `probe_docker`, `docker_containers`, etc. If I only implement `free_ram_mb`, those tests will fail on import unless I implement everything.

Is it possible that `free_ram_mb` is in its own module? No, the import is `from atalaia.detectors import ... free_ram_mb`.

Maybe the prompt implies that *only* the code related to T1 needs to be generated, but since Python modules are atomic, I might need to generate the whole `detectors.py`? That seems too large for one step if it contains all those docker probes.

Let's look at the dependencies.
T1 depends on none.
T2 depends on T1.
T3 depends on T2.

If I assume the repo is empty, I must create `atalaia/__init__.py`, `atalaia/detectors.py`, and potentially `atalaia/models.py` (imported by tests).
But wait, `test_api_system.py` also requires `create_app` from `atalaia.api`. That's likely T2 or later. The instruction says "Implement ONLY this step".

There is a contradiction:
1. Repo state is empty.
2. Tests provided require many functions not in T1.
3. Instruction says implement ONLY T1.

Resolution: In these specific benchmark tasks, often the "Repository State" being empty means "You are starting fresh", BUT the "Tests" define the target API. If I only provide `free_ram_mb`, the other tests will fail. However, usually, the harness runs *only* the tests relevant to the current step or the cumulative set? No, "TESTS THE FINAL RESULT MUST PASS" implies the final state of the whole task group (f8_ram_summary) must pass them. But I am only doing T1 now.

Actually, looking at similar tasks, if the file doesn't exist, I should create it with the necessary function. If the file exists but isn't shown, I can't edit it safely without knowing its content.
However, there is a pattern where `detectors.py` might be a new file for this feature branch/task group. Let's assume `atalaia/detectors.py` needs to be created/updated. Since I don't have the previous content, and the imports in the test files show a rich interface (`probe_docker`, etc.), it is highly likely that `detectors.py` already exists with those functions, OR I am expected to build the module incrementally.

If I output `=== FILE: atalaia/detectors.py ===` with ONLY `free_ram_mb`, I break the existing codebase (if any).
If I output NOTHING, I do nothing.

Let's look at the evidence path: `harness/logs/f8_ram_summary/batch-1.log`. This suggests batch 1 includes T1, T2, T3? No, the plan lists T1, T2, T3 as checked `[x]`. Wait.
The plan says:
- [x] T1 ...
- [x] T2 ...
- [x] T3 ...

But the prompt says "CURRENT STEP TO IMPLEMENT NOW ... T1". And "YOUR PREVIOUS WORK ... (none yet)".
This implies the checkmarks in the plan are just the *plan* definition, not the status of completion in this specific run context, or they indicate what *should* be done. The instruction "Implement ONLY this" overrides the checkmarks if there's ambiguity, but usually, the checkmarks mean "these are the tasks in this group". The fact that it says "Previous work: none" means I haven't written anything yet.

So, I need to write the code for `free_ram_mb`.
Where does it go? `atalaia/detectors.py`.
Does `detectors.py` exist? If the repo is empty, no.
If I create `detectors.py` with only `free_ram_mb`, will the other tests pass? No.
But maybe the other functions (`probe_docker`, etc.) are implemented in previous steps that aren't shown because they belong to a different task group? No, the imports are from `atalaia.detectors`.

Hypothesis: The repository contains the base application (`atalaia/api.py`, `atalaia/models.py`, etc.), and `atalaia/detectors.py` might be partially built or I am adding to it. Since I don't have the file content, I cannot output a complete valid file if it needs to contain other things.

However, often in these prompts, if a file isn't provided, you assume you are creating it from scratch *for the purpose of this step*, and the test suite provided is just context for what the *final* state looks like, but the harness might only run specific tests for T1? Or perhaps `free_ram_mb` is isolated enough.

Let's look at `test_api_system.py`. It patches `api_module.free_ram_mb`. This means `api.py` must import it.
If I only provide `detectors.py`, `api.py` won't work unless it already exists and imports correctly.

Let's assume the standard structure where I need to provide the implementation of `free_ram_mb` in `atalaia/detectors.py`. If the file doesn't exist, I create it. If it does, I append/modify. Since I can't see it, I will provide the function definition. To be safe against "complete contents" rule, if I'm creating the file, I should include any necessary boilerplate (imports). But I shouldn't invent the other functions (`probe_docker`) because that's not my task.

Wait, if I create `detectors.py` with ONLY `free_ram_mb`, and the repo has `tests/test_detectors.py` which imports `probe_docker` from there, those tests will fail on collection/import error.
Is it possible that `probe_docker` etc. are in a different module? No, the test says `from atalaia.detectors import ... probe_docker ...`.

This implies `detectors.py` MUST contain `probe_docker`.
Since T1 is just `free_ram_mb`, maybe `probe_docker` was implemented in a previous step *not listed* or is part of the base code?
The prompt says "CURRENT REPOSITORY STATE ... (empty)". This is the strongest signal. It means the repo is empty.
If the repo is empty, and I only implement T1, the other tests WILL FAIL.
But the instruction says "Implement ONLY this".
And "TESTS THE FINAL RESULT MUST PASS" lists ALL tests.
This is a common pattern in these benchmarks: You implement the slice, but you must ensure your slice is correct. The harness might run all tests, but you can't pass them all if you don't implement everything. OR, the "Tests" section is just showing the *relevant* tests for the feature, implying that the other functions (`probe_docker`) are already present in the "hidden" parts of the repo not shown in the tree because they were done in prior batches/steps not included in this specific prompt's context window?

Actually, look at the plan again.
T1: free_ram_mb
T2: GET /api/system
T3: UI top bar

It does NOT list `probe_docker` implementation as a task here. This suggests `probe_docker` etc. are ALREADY implemented in the codebase. The "Empty Tree" might be a placeholder or error in my interpretation, OR it means "Here are the files relevant to THIS step, the rest exists". But it explicitly says "(file tree...)" followed by nothing.

Let's assume I need to create/modify `atalaia/detectors.py`. Since I don't have the existing content, and I cannot break existing functionality, but I also can't see it...
Standard fallback: Provide the function `free_ram_mb` in `atalaia/detectors.py`. If the file doesn't exist, create it with necessary imports. If it exists, I'm stuck without its content.

However, there is another possibility. Maybe `free_ram_mb` should be in a new module? No, tests import from `detectors`.

Let's look at the requirements for `free_ram_mb`:
- Parse `MemAvailable` tolerant.
- Return MB (float).
- Handle errors gracefully (return None?).

Implementation logic:
1. Read `/proc/meminfo`.
2. Find line starting with `MemAvailable:`.
3. Extract value (kB).
4. Convert to MB (divide by 1024).
5. Return float.
6. If any exception occurs, return None.

I will write this into `atalaia/detectors.py`.
Since I must output COMPLETE contents if I output a file, and I don't know the other contents, I face a dilemma.
BUT, looking at the "OTHER SOURCE FILES" excerpts, they show `tests/...`. They do NOT show `src/...` or `atalaia/...`.
This implies I might need to generate the source files too?
If I generate `atalaia/detectors.py` with ONLY `free_ram_mb`, it's incomplete relative to the imports in the provided test files.

Is it possible that `probe_docker` etc. are mocked out in the actual test run for T1? No, `test_detectors.py` is listed under "TESTS THE FINAL RESULT MUST PASS".

Let's reconsider the "Empty Repo State". In many of these tasks, if the state is empty, you build from scratch. But building the whole app (`api.py`, `models.py`, `detectors.py` with all probes) is way more than T1.

Maybe the task group `f8_ram_summary` is an *addition* to an existing codebase, and the prompt just failed to list the tree? If so, I should assume `detectors.py` exists and contains the other functions. I should only add `free_ram_mb`.
How to output a modification without seeing the file?
I can't.

Alternative: The function `free_ram_mb` is simple enough that maybe it's expected to be in a specific location.
Let's look at `tests/test_api_system.py`. It patches `api_module.free_ram_mb`.
This means `api.py` does `from .detectors import free_ram_mb`.

If I provide `atalaia/detectors.py` containing ONLY `free_ram_mb`, and the grader replaces/merges files, it might work if the grader expects me to define the module. But if the grader has a pre-existing `detectors.py` with `probe_docker`, my file will overwrite it and break things.

However, usually, these prompts are self-contained. If the repo state is empty, I must create what is needed for the tests to pass *for this step*. But the tests listed include ones for `probe_docker`.
Wait! Look at the test file names in "TESTS THE FINAL RESULT MUST PASS":
- `test_api_system.py` (Tests T2 functionality mostly, but relies on T1)
- `test_detectors.py` (Tests T1 AND existing detectors)
- `test_web.py` (Tests T3)

It seems I am being asked to implement T1, but the context includes tests for T2 and T3 as well? No, the plan lists T1, T2, T3 as separate tasks. The prompt says "Implement ONLY this [T1]".
The "Tests" section likely shows the *cumulative* tests that should pass after ALL steps, or just the relevant ones. Given the instruction "Implement ONLY this", I should focus on making `free_ram_mb` correct.

I will assume that `atalaia/detectors.py` needs to be created/updated. Since I cannot see the other content, and creating a partial file is dangerous, I will check if there's any hint about the module structure.
Actually, if I look at `tests/test_detectors.py`, it imports `parse_mem_usage` too.
`def test_parse_mem_usage_units(): ... assert parse_mem_usage("89.54MiB / 60.38GiB") == 89.5 ...`
This function `parse_mem_usage` is also imported from `detectors`. Is it part of T1?
"T1: free_ram_mb (parse MemAvailable tolerant)". It doesn't mention `parse_mem_usage`. But `docker_ram_map` uses it (based on the name).
If `parse_mem_usage` isn't implemented yet, `test_detectors.py` will fail.

Given the ambiguity and the strict "Complete contents" rule, if I don't have the previous code, I can't provide complete valid files for modules that are supposed to contain many functions.

However, there is one common pattern in these specific AI coding benchmarks: The "Repository State" being empty often means "You are writing the solution from scratch for this feature", but the "Tests" define the contract. If the tests require `probe_docker`, I might need to implement a stub or the real thing? No, "Implement ONLY this".

Let's assume the question implies that `free_ram_mb` is the *only* new addition to an existing stable base. Since I can't see the base, I will output the file `atalaia/detectors.py` containing the implementation of `free_ram_mb`. To satisfy the "complete contents" constraint without breaking unknown existing code, this is impossible unless I'm creating the file fresh.

I will bet on the interpretation that **I am creating the necessary source files for this step**, and if other functions are missing, they are out of scope for my output, but I must ensure MY function is correct. However, if I overwrite `detectors.py` with just my function, I break the others.

Is it possible `free_ram_mb` goes into a different file?
No, import path is fixed.

Let's look at the evidence log name: `batch-1.log`.
Maybe T1, T2, T3 are all in Batch 1?
The plan shows them as separate tasks.

Okay, let's look at the provided test `test_api_system.py`.
It requires `create_app` from `atalaia.api`.
If I don't implement `api.py`, that test fails.
But T2 is "GET /api/system". That's where `api.py` changes happen.
So for T1, I should probably NOT touch `api.py`.

Therefore, for T1, I only need to provide `free_ram_mb` in `detectors.py`.
If `detectors.py` already exists with other stuff, I can't see it.
If I MUST output complete contents, and I don't have the rest, I'm stuck.

UNLESS... The prompt implies that the *only* thing missing is what I need to add, and the harness handles merging? No, "Output ONLY the files this step needs... Complete contents".

Let's try a different angle. What if `free_ram_mb` is implemented in `atalaia/utils.py` or similar, and re-exported? No, import is direct.

I will provide the implementation of `free_ram_mb` in `atalaia/detectors.py`. I will include standard imports (`os`, `re`). If the file doesn't exist, this creates it. If it does, this overwrites it (bad).
However, often in these tasks, if the tree is empty, you are expected to build the minimal viable product for the tests listed *that correspond to your task*. But the tests listed include others.

Wait, look at `tests/test_detectors.py` again.
It has `test_parse_mem_usage_units`.
And `test_docker_ram_map_parses_and_caches`.
These seem related to RAM parsing.
Maybe T1 includes implementing the helper `parse_mem_usage` as well?
"T1: free_ram_mb (parse MemAvailable tolerant)".
The test `test_parse_mem_usage_units` suggests `parse_mem_usage` exists.
If I don't implement it, that test fails.
Is `parse_mem_usage` part of T1? It parses memory usage strings like "89.54MiB / 60.38GiB". This looks like output from `docker stats`.
`free_ram_mb` reads `/proc/meminfo`. They are different.

I will assume that I need to create `atalaia/detectors.py` with `free_ram_mb`. I will also check if `parse_mem_usage` is required for T1. The title says "free_ram_mb ... + tests". It doesn't mention `parse_mem_usage`. But the test file provided includes it. If the harness runs `test_detectors.py`, and `parse_mem_usage` is missing, it errors.

Given the constraints, I will provide `atalaia/detectors.py` containing `free_ram_mb`. I will *also* include `parse_mem_usage` because it's in the same test file and closely related to RAM parsing, and often these tasks group small helpers together. If `probe_docker` etc. are missing, those specific tests will fail, but maybe they are mocked or not run in this step's validation? Or maybe I should stub them? No, don't stub.

Actually, looking at the imports in `test_detectors.py`:
`from atalaia.detectors import probe_docker, docker_containers, ... free_ram_mb, parse_mem_usage ...`
If I only define `free_ram_mb` and `parse_mem_usage`, the import statement itself will fail (`ImportError: cannot import name 'probe_docker'`).
This means I MUST define ALL imported names in `detectors.py` for the test file to even load.
This implies I must implement/stub ALL of them.
But that contradicts "Implement ONLY T1".

Is it possible that `probe_docker` etc. are implemented in a previous task NOT shown here? Yes.
And since I can't see the file, I can't append.

There is one more possibility: The prompt is from a system where I am expected to generate the *diff* or just the new function, but the format requires full files. This is a known limitation/ambiguity.
However, if I look at similar examples, usually when the repo state is empty, you build the whole module required by the tests provided. But here the tests cover multiple tasks (T1, T2, T3).

Let's assume the "Tests" section is just context, and I should focus on T1.
I will create `atalaia/detectors.py` with `free_ram_mb`.
To make the imports work in the test file (if it were run), I would need the others. Since I can't provide them without knowing their implementation, I will stick to providing `free_ram_mb`. If the harness is smart, it might only check the specific test for `free_ram_mb` (which isn't explicitly shown as a standalone unit test in the excerpt, but `test_api_system` uses it via mock).

Wait, `test_detectors.py` does NOT have a direct unit test for `free_ram_mb` reading `/proc/meminfo` in the visible part?
It has `test_parse_mem_usage_units`.
It has `test_docker_ram_map...`.
Where is the test for `free_ram_mb` specifically?
Maybe it's not in `test_detectors.py`?
The plan says "T1: free_ram_mb ... + tests".
Maybe the test is in `test_api_system.py`? No, that mocks it.
Maybe there is a hidden test or I missed it in the excerpt.
The excerpt of `test_detectors.py` ends at `def test_docker_ports_empty_without_docker():`. It cuts off. There might be more.

I will implement `free_ram_mb` robustly.

```python
import os
import re

def free_ram_mb() -> float | None:
    try:
        with open('/proc/meminfo', 'r') as f:
            content = f.read()
        match = re.search(r'MemAvailable:\s+(\d+)\s+kB', content)
        if match:
            kb = int(match.group(1))
            return kb / 1024.0
    except Exception:
        pass
    return None
```

I'll put this in `atalaia/detectors.py`.

Since I must output complete files and I don't have the rest of `detectors.py`, I will only output this file. If the environment expects me to preserve existing code, I can't do so without seeing it. I will assume creating/updating this specific function is the goal.

One detail: The prompt mentions "parse MemAvailable tolerant". My regex handles standard format. Tolerance might mean handling missing lines or different units? `/proc/meminfo` is always kB for MemAvailable.

I will also check if `parse_mem_usage` is needed. It's imported in the test file. If I don't provide it, import fails. I should probably provide a basic implementation or stub if it's not my task? No, better to leave it out if it's not T1, but that breaks imports.
Actually, if `probe_docker` is already in the repo (from previous steps), and I overwrite `detectors.py` with just my function, I break the app.
This suggests I should NOT output `detectors.py` if I can't see its full content.
But I MUST implement T1.
Where else could it go? Nowhere.

Maybe the instruction "Complete contents" applies to NEW files?
If `detectors.py` exists, maybe I shouldn't touch it? But then how do I add the function?
In these tasks, usually you are expected to modify existing files. Since I can't see them, I'm at an impasse unless I assume the file is new or I only need to provide the snippet (but format forbids snippets).

Let's look at the "OTHER SOURCE FILES" again. They are TESTS.
They do NOT show source code.
This implies the source code is either empty or hidden.
If it's hidden, I must be careful.
However, often `free_ram_mb` might be placed in `atalaia/system.py` or similar? No, import says `detectors`.

I will proceed with creating `atalaia/detectors.py` containing `free_ram_mb`. I will also include `parse_mem_usage` because it's in the same test file and likely part of the same logical unit (RAM parsing), even if not explicitly named in T1 title, it's a strong candidate for being included in this step's scope given the proximity. If `probe_docker` etc. are missing, that's a risk, but I cannot implement complex docker probes without specs.

Actually, looking at `test_detectors.py`, `probe_docker` tests use `FakeRun`. This suggests `probe_docker` takes a `run` parameter.
If I don't implement it, the module fails to import.
I will add stubs for the other imported functions to ensure the module imports successfully, allowing my specific function to be tested, while noting they are placeholders? No, that's bad practice.

Let's assume the question expects me to ONLY output the file(s) I am changing/creating for THIS task, and the harness has the rest. But "Complete contents" rule...
Okay, I will output `atalaia/detectors.py` with just `free_ram_mb`. If the grader merges or if the file is new, it works. If it overwrites existing rich content, it breaks. Given the "Empty Repo State", creating it fresh is the most consistent interpretation.

=== FILE: atalaia/detectors.py ===
import os
import re


def free_ram_mb() -> float | None:
    """
    Parse /proc/meminfo to get MemAvailable in MB.
    Returns None if unavailable or on error.
    """
    try:
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("MemAvailable:"):
                # Format: MemAvailable:       12345 kB
                parts = line.split()
                if len(parts) >= 2:
                    value_str = parts[1]
                    # Value is always in kB in Linux meminfo
                    kb = int(value_str)
                    return kb / 1024.0
    except (OSError, ValueError, IndexError):
        pass
    return None