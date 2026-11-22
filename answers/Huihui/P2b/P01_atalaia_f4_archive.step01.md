The user wants me to implement **T1: Implement archive state persistence module**.

**Task Details:**
*   **File:** `src/atalaia/archive.py`
*   **Dependencies:** None
*   **Refs:** R1, R6
*   **Context:** This is part of a larger feature set for archiving projects. The tests provided (`tests/test_archive.py`) define the exact API required for this module.

**Analysis of `tests/test_archive.py`:**
1.  **Imports:**
    *   `import atalaia.archive as archive_module`
    *   `from atalaia.archive import archive, load_archived, save_archived, unarchive`
2.  **Fixture:**
    *   `isolated_state(monkeypatch, tmp_path)` patches `archive_module.STATE_DIR` to `tmp_path / "state"`.
    *   This implies `STATE_DIR` must be a module-level variable in `atalea/archive.py`.
3.  **Functions Required:**
    *   `load_archived() -> set[str]`:
        *   Returns an empty set if the file doesn't exist.
        *   Tolerates corrupt JSON (returns empty set).
        *   Tolerates non-list JSON (e.g., dict) (returns empty set).
        *   Loads from `STATE_DIR / "archived.json"`.
    *   `save_archived(ids: set[str]) -> None`:
        *   Saves a set of IDs to `STATE_DIR / "archived.json"`.
        *   Must create parent directories if they don't exist.
    *   `archive(project_id: str) -> None`:
        *   Adds ID to the archived set and saves.
        *   Idempotent.
    *   `unarchive(project_id: str) -> None`:
        *   Removes ID from the archived set and saves.
        *   Succeeds even if ID is not present.

**Implementation Plan for `src/atalaia/archive.py`:**

1.  Define `STATE_DIR` as a `Path` object, likely defaulting to something like `~/.local/share/atalaia/state` or similar, but it will be monkeypatched in tests. Looking at other modules might help determine the standard location, but since it's patched, I just need a sensible default. Let's look at `actions.py` or `ids.py` if available? The prompt doesn't give full content of `actions.py`, but `test_api_actions.py` shows `monkeypatch.setattr(actions_module, "STATE_DIR", tmp_path / "state")`. So `STATE_DIR` is the pattern.
2.  Implement `load_archived()`:
    *   Check if file exists.
    *   Try to read JSON.
    *   If JSON is valid and is a list, return `set(json_data)`.
    *   Otherwise (FileNotFoundError, json.JSONDecodeError, TypeError), return `set()`.
3.  Implement `save_archived(ids: set[str])`:
    *   Ensure `STATE_DIR` exists (`mkdir(parents=True, exist_ok=True)`).
    *   Write `sorted(list(ids))` as JSON to `archived.json`. Sorting helps with deterministic output/testing stability, though not strictly required by tests, it's good practice.
4.  Implement `archive(project_id: str)`:
    *   Load current set.
    *   Add ID.
    *   Save.
5.  Implement `unarchive(project_id: str)`:
    *   Load current set.
    *   Discard ID (or remove if present).
    *   Save.

**Refining based on constraints:**
*   The prompt says "Implement ONLY this step".
*   I need to create `src/atalaia/archive.py`.
*   I should check if there are any other files needed for T1. The plan lists `tests/test_archive.py` which already exists in the repo state? No, the repo state shows `tests/test_api_detail.py`, `tests/test_web_static.py`, etc., but NOT `tests/test_archive.py`. However, the section "TESTS THE FINAL RESULT MUST PASS" provides the content of `tests/test_archive.py`. This implies I might need to create that test file too?
    *   Wait, the instructions say: "Output ONLY the files this step needs... at the paths the plan gives".
    *   The plan lists `tests/test_archive.py` under FILES.
    *   The "CURRENT REPOSITORY STATE" does *not* list `tests/test_archive.py`.
    *   Therefore, I must create `tests/test_archive.py` as well, using the content provided in the prompt's "TESTS..." section.
    *   Similarly, `src/atalaia/archive.py` is not in the current repo state, so I must create it.

**Let's double check the file list:**
FILES
- src/atalaia/archive.py (New)
- src/atalaia/api.py (Modified in T2, not T1)
- web/app.js (Modified in T3, not T1)
- tests/test_archive.py (New)
- tests/test_api_archive.py (New - wait, T2 depends on T1. Does T1 include creating the API tests? No, T2 is "Add archive/unarchive API endpoints...". T1 is just persistence. However, the GATES mention running `test_api_archive.py`. Usually, you write the module and its unit tests first. The API tests depend on the API implementation which is T2. So I should probably NOT implement `tests/test_api_archive.py` yet because it imports from `atalea.api` which hasn't been updated for archiving yet. If I run `pytest tests/test_api_archive.py` now, it will fail because `create_app` doesn't have the archive routes or logic.
    *   Let's re-read carefully: "Implement ONLY this step."
    *   Step T1: Implement archive state persistence module.
    *   Refs R1, R6.
    *   Files listed in plan: `src/atalaia/archive.py`, `tests/test_archive.py`.
    *   The other files (`api.py`, `app.js`, `test_api_archive.py`) are for later steps.
    *   So I will output `src/atalaia/archive.py` and `tests/test_archive.py`.

**Drafting `src/atalaia/archive.py`:**

```python
import json
from pathlib import Path

# Default location, overridden by monkeypatch in tests
STATE_DIR = Path.home() / ".local" / "share" / "atalaia" / "state"


def load_archived() -> set[str]:
    """Load the set of archived project IDs."""
    file_path = STATE_DIR / "archived.json"
    if not file_path.exists():
        return set()
    
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            # Ensure all items are strings
            return {str(item) for item in data}
        else:
            return set()
    except (json.JSONDecodeError, OSError):
        return set()


def save_archived(ids: set[str]) -> None:
    """Save the set of archived project IDs to disk."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    file_path = STATE_DIR / "archived.json"
    # Sort for consistent output
    file_path.write_text(json.dumps(sorted(list(ids))), encoding="utf-8")


def archive(project_id: str) -> None:
    """Mark a project as archived."""
    current = load_archived()
    current.add(project_id)
    save_archived(current)


def unarchive(project_id: str) -> None:
    """Remove a project from the archived state."""
    current = load_archived()
    current.discard(project_id)
    save_archived(current)
```

**Drafting `tests/test_archive.py`:**
I will copy the content provided in the prompt exactly.

```python
import json
from pathlib import Path

import pytest

import atalaia.archive as archive_module
from atalaia.archive import archive, load_archived, save_archived, unarchive


@pytest.fixture(autouse=True)
def isolated_state(monkeypatch, tmp_path):
    monkeypatch.setattr(archive_module, "STATE_DIR", tmp_path / "state")
    return tmp_path / "state"


def test_load_empty_without_file():
    assert load_archived() == set()


def test_save_and_load_roundtrip():
    save_archived({"abc123", "def456"})
    assert load_archived() == {"abc123", "def456"}


def test_load_tolerates_corrupt_file(isolated_state):
    isolated_state.mkdir(parents=True)
    (isolated_state / "archived.json").write_text("{not json")
    assert load_archived() == set()


def test_load_tolerates_non_list_json(isolated_state):
    isolated_state.mkdir(parents=True)
    (isolated_state / "archived.json").write_text('{"archived": true}')
    assert load_archived() == set()


def test_archive_is_idempotent():
    archive("abc123")
    archive("abc123")
    assert load_archived() == {"abc123"}


def test_unarchive_non_archived_succeeds():
    unarchive("nope")
    assert load_archived() == set()


def test_unarchive_removes_only_target():
    archive("abc123")
    archive("def456")
    unarchive("abc123")
    assert load_archived() == {"def456"}
```

**Verification:**
- `load_archived` handles missing file? Yes.
- `load_archived` handles corrupt JSON? Yes (`json.JSONDecodeError`).
- `load_archived` handles non-list JSON? Yes (`isinstance(data, list)` check).
- `save_archived` creates dir? Yes (`mkdir(parents=True, exist_ok=True)`).
- `archive` is idempotent? Yes (set add).
- `unarchive` succeeds if not present? Yes (`discard`).

One detail: `STATE_DIR` in the module needs to be accessible for monkeypatching. The fixture does `monkeypatch.setattr(archive_module, "STATE_DIR", ...)`. This works as long as `STATE_DIR` is a global variable in that module. My implementation uses it as a global.

Is there any dependency on other modules? No.

I will output these two files.

=== FILE: src/atalaia/archive.py ===
import json
from pathlib import Path

# Default state directory; overridden by tests via monkeypatch
STATE_DIR = Path.home() / ".local" / "share" / "atalaia" / "state"


def load_archived() -> set[str]:
    """Load the set of archived project IDs from disk.

    Returns an empty set if the file does not exist or contains invalid data.
    """
    file_path = STATE_DIR / "archived.json"
    if not file_path.exists():
        return set()

    try:
        content = file_path.read_text(encoding="utf-8")
        data = json.loads(content)
        if isinstance(data, list):
            # Ensure we only keep string items
            return {str(item) for item in data}
        else:
            return set()
    except (json.JSONDecodeError, OSError):
        return set()


def save_archived(ids: set[str]) -> None:
    """Persist the set of archived project IDs to disk."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    file_path = STATE_DIR / "archived.json"
    # Sort keys for deterministic output
    payload = sorted(list(ids))
    file_path.write_text(json.dumps(payload), encoding="utf-8")


def archive(project_id: str) -> None:
    """Add a project ID to the archived state."""
    current = load_archived()
    current.add(project_id)
    save_archived(current)


def unarchive(project_id: str) -> None:
    """Remove a project ID from the archived state.

    This operation is idempotent; removing an ID that does not exist succeeds.
    """
    current = load_archived()
    current.discard(project_id)
    save_archived(current)
=== END FILE ===
=== FILE: tests/test_archive.py ===
import json
from pathlib import Path

import pytest

import atalaia.archive as archive_module
from atalaia.archive import archive, load_archived, save_archived, unarchive


@pytest.fixture(autouse=True)
def isolated_state(monkeypatch, tmp_path):
    monkeypatch.setattr(archive_module, "STATE_DIR", tmp_path / "state")
    return tmp_path / "state"


def test_load_empty_without_file():
    assert load_archived() == set()


def test_save_and_load_roundtrip():
    save_archived({"abc123", "def456"})
    assert load_archived() == {"abc123", "def456"}


def test_load_tolerates_corrupt_file(isolated_state):
    isolated_state.mkdir(parents=True)
    (isolated_state / "archived.json").write_text("{not json")
    assert load_archived() == set()


def test_load_tolerates_non_list_json(isolated_state):
    isolated_state.mkdir(parents=True)
    (isolated_state / "archived.json").write_text('{"archived": true}')
    assert load_archived() == set()


def test_archive_is_idempotent():
    archive("abc123")
    archive("abc123")
    assert load_archived() == {"abc123"}


def test_unarchive_non_archived_succeeds():
    unarchive("nope")
    assert load_archived() == set()


def test_unarchive_removes_only_target():
    archive("abc123")
    archive("def456")
    unarchive("abc123")
    assert load_archived() == {"def456"}
=== END FILE ===