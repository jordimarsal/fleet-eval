The user wants me to implement **T3**: Add the `archived` field to `project_status` (both list and detail endpoints) + tests.

Let me analyze what's needed:

1. The test file `tests/test_api_archive.py` expects:
   - `/api/projects` returns items with `"archived": false/true`
   - `/api/projects/{pid}` (detail) returns `"archived": true/false`
   - Archive/unarchive endpoints work (but those are T2 — wait, let me re-read)

Wait, looking more carefully at the task breakdown:
- T1: archive.py module ✓ (already done)
- T2: POST /api/projects/{pid}/archive & /unarchive endpoints
- T3: camp archived a project_status (llista i detall) + tests

But the test file `tests/test_api_archive.py` contains BOTH T2 (the POST endpoints) AND T3 (the `archived` flag in responses). Let me look at what's actually being tested here...

Actually, looking at the current step description again: "T3: camp archived a project_status (llista i detall) + tests". This is specifically about adding the `archived` boolean field to the response payloads of both the list endpoint (`GET /api/projects`) and the detail endpoint (`GET /api/projects/{pid}`).

However, the test file `tests/test_api_archive.py` also tests the POST endpoints. Since T2 depends on T1 and T3 depends on T1, but the test file covers both... Let me check if T2 has already been implemented by looking at the API code.

Looking at the provided `src/atalaia/api.py`, I don't see any `/archive` or `/unarchive` routes defined. So T2 hasn't been implemented yet either. But my task is ONLY T3.

Wait - let me re-read the instructions: "Implement ONLY this" referring to T3. The evidence says `harness/logs/f4_archive/batch-1.log` which suggests batch 1 covered T1-T5 together perhaps? No, each task has its own evidence line pointing to batch-1.log for T1-T5.

Let me focus strictly on what T3 requires based on the tests that MUST pass:
- `test_list_includes_archived_flag_false_by_default`: GET /api/projects → items have `"archived": false`
- In `test_archive_and_unarchive_roundtrip`: after archiving, list shows `"archived": true`, detail shows `"archived": true`; after unarchiving, list shows `"archived": false`
- `test_unknown_id_404`: POST to unknown id returns 404 (this is T2)
- `test_archive_survives_new_client_instance`: archive state persists across client instances

Since the test file includes both T2 and T3 functionality, but I'm only implementing T3, I need to be careful. However, looking at the dependency chain: T3 depends_on T1 only. T2 also depends_on T1. They're parallel in terms of dependencies.

But practically, for the tests to pass, BOTH the endpoints AND the archived field must exist. Since my step is specifically "camp archived a project_status", let me implement just that part - adding the `archived` field to `project_status()` and `detail_payload()`.

Actually wait - re-reading more carefully. The plan says all tasks T1-T5 are marked `[x]` as done. But the current repository state doesn't show them implemented. This seems like the harness is asking me to implement them sequentially even though they're marked complete in the plan overview.

Let me focus on what T3 specifically needs:
1. Modify `src/atalaia/api.py` to include `"archived"` in `project_status()` response
2. Ensure it's also in `detail_payload()` (which calls `project_status`)
3. Create/update test file for this specific aspect

The key change is in `project_status()` function - add an `archived` boolean field by checking if the project ID is in the archive set.

Let me look at how `create_app` works to understand where projects come from and how I can inject the archive check.

Looking at the existing code structure, `project_status` takes a `Project` object and returns a dict. I need to add the `archived` field there. The simplest approach is to call `load_archived()` inside `project_status` or pass it in.

Since `project_status` is called per-project in the list endpoint, calling `load_archived()` each time would be inefficient but correct. Better to load once and pass down, but given the simple nature, let me just import and use it directly in the function since it reads from disk.

Actually, looking at the test more carefully - the tests monkeypatch `archive_module.STATE_DIR`, so as long as I import from `atalaia.archive`, the monkeypatching will work correctly.

Let me implement:
1. In `src/atalaia/api.py`: Add `"archived"` field to `project_status()` 
2. The test file already exists as shown (`tests/test_api_archive.py`) - but wait, that test file also requires T2 endpoints. Since I'm only doing T3, maybe I should create a separate focused test? 

Re-reading: "TESTS THE FINAL RESULT MUST PASS (they define the exact API)" - this shows ALL tests that must ultimately pass. But for THIS step, I should focus on what T3 delivers.

Given the constraint "Implement ONLY the current step", and T3 is specifically about the `archived` field in responses, I'll:
1. Modify `api.py` to add the `archived` field
2. The test file `tests/test_api_archive.py` covers both T2+T3, but since it's listed as required, and my changes need to make those specific assertions pass regarding the `archived` field...

I think the cleanest interpretation is: modify `api.py` to include `archived` in both list and detail payloads. The full test file will pass once T2 is also done, but my contribution here is making the `archived` field appear correctly.

Let me write the modified `api.py`.

<tool_call>
<function=Read>
<parameter=file_path>
src/atalaia/api.py
</parameter>
</function>
</tool_call>