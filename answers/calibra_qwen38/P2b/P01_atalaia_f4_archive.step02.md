The user wants me to implement T2: POST `/api/projects/{pid}/archive` and `/unarchive` endpoints with 404 for unknown projects and 202 idempotent responses.

Let me analyze what's needed:

1. **T1 is done**: `src/atalaia/archive.py` exists with `load_archived`, `save_archived`, `archive`, `unarchive`. Tests pass.

2. **T2 requires**: Adding two new API endpoints to `src/atalaia/api.py`:
   - `POST /api/projects/{pid}/archive` → returns 202 `{"status": "archived"}` if project known, 404 if unknown
   - `POST /api/projects/{pid}/unarchive` → returns 202 `{"status": "unarchived"}` if project known, 404 if unknown

3. Looking at the test file `tests/test_api_archive.py`, I need to understand how the app is created and how projects are resolved. Let me look at the existing `create_app` function in `api.py` more carefully.

From the excerpts, I can see `create_app` takes a `discover` parameter (and possibly `web_dir`). The tests use:
```python
def client_for(*projects):
    return TestClient(create_app(discover=lambda roots: list(projects)))
```

So `create_app` accepts a `discover` callable that returns a list of `Project` objects.

I need to see the full `api.py` to understand the current structure. Let me read it first.

<tool_call>
<function=Read>
<parameter=file_path>
/home/user/src/atalaia/api.py
</parameter>
</function>
</tool_call>