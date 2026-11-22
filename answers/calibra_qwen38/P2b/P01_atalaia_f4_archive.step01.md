The user wants me to implement **T1**: `archive.py` module with idempotent load/save and corrupt-tolerant behavior, plus tests.

Let me analyze the test files to understand the exact API required:

From `tests/test_archive.py`:
```python
import atalaia.archive as archive_module
from atalaia.archive import archive, load_archived, save_archived, unarchive

@pytest.fixture(autouse=True)
def isolated_state(monkeypatch, tmp_path):
    monkeypatch.setattr(archive_module, "STATE_DIR", tmp_path / "state")
    return tmp_path / "state"
```

So `archive_module` must have a `STATE_DIR` attribute that can be monkeypatched. The state dir is where `archived.json` lives.

Functions needed:
- `load_archived() -> set[str]` - returns empty set if no file, tolerates corrupt JSON, tolerates non-list JSON
- `save_archived(ids: set[str]) -> None` - saves to STATE_DIR/archived.json
- `archive(pid: str) -> None` - adds pid to archived (idempotent)
- `unarchive(pid: str) -> None` - removes pid from archived (succeeds even if not present)

The file path is `STATE_DIR / "archived.json"`.

Let me also check `tests/test_api_archive.py` which imports:
```python
import atalaia.archive as archive_module
from atalaia.api import create_app
from atalaia.archive import load_archived
```

This confirms the same module structure.

Now let me look at how other modules handle state directories for style consistency. Looking at `src/atalaia/actions.py` reference in tests:
```python
monkeypatch.setattr(actions_module, "STATE_DIR", tmp_path / "state")
```

So the pattern is a module-level `STATE_DIR` constant. Let me check what default value it should have. In actions, looking at the test setup, it's likely something like `Path.home() / ".atalaia" / "state"` or similar. But since we're just implementing T1 and the tests monkeypatch it, I need a reasonable default.

Looking at the project structure, there's no existing STATE_DIR definition visible in the excerpts. Let me use a sensible default that follows common patterns. Since this is a local dashboard tool, I'll use `~/.local/state/atalaia` or similar. Actually, let me keep it simple - the key requirement is that it's a module-level variable that can be monkeypatched.

Let me write the implementation:

```python
"""Archive state management (idempotent, corrupt-tolerant)."""

from __future__ import annotations

import json
from pathlib import Path

STATE_DIR = Path.home() / ".local" / "state" / "atalaia"


def _archive_file() -> Path:
    return STATE_DIR / "archived.json"


def load_archived() -> set[str]:
    """Load archived project IDs. Returns empty set on missing/corrupt file."""
    path = _archive_file()
    if not path.is_file():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return set()
    if not isinstance(data, list):
        return set()
    return {item for item in data if isinstance(item, str)}


def save_archived(ids: set[str]) -> None:
    """Persist archived project IDs to disk."""
    path = _archive_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sorted(ids)), encoding="utf-8")


def archive(pid: str) -> None:
    """Add a project ID to the archive (idempotent)."""
    current = load_archived()
    current.add(pid)
    save_archived(current)


def unarchive(pid: str) -> None:
    """Remove a project ID from the archive (no-op if absent)."""
    current = load_archived()
    current.discard(pid)
    save_archived(current)
```

Now let me verify against all test cases:

1. `test_load_empty_without_file`: No file → returns `set()` ✓
2. `test_save_and_load_roundtrip`: Save `{"abc123", "def456"}` → load returns same set ✓
3. `test_load_tolerates_corrupt_file`: File contains `{not json` → JSONDecodeError caught → `set()` ✓
4. `test_load_tolerates_non_list_json`: File contains `{"archived": true}` → not a list → `set()` ✓
5. `test_archive_is_idempotent`: Call archive twice with same pid → still just that one id ✓
6. `test_unarchive_non_archived_succeeds`: Unarchive non-existent → no error, empty set ✓
7. `test_unarchive_removes_only_target`: Archive two, unarchive one → only other remains ✓

All good. Now I need to also create the tests file since T1 says "+ tests". But wait - looking at the plan again, it says "Implement archive.py (load/save idempotent, corrupt-tolerant) + tests". The tests are already defined in the "TESTS THE FINAL RESULT MUST PASS" section as `tests/test_archive.py`. So I should output both files.

Let me double-check: the test file content is provided in full in the prompt. I'll include it exactly as given.

=== FILE: src/atalaia/archive.py ===
"""Archive state management (idempotent, corrupt-tolerant)."""

from __future__ import annotations

import json
from pathlib import Path

STATE_DIR = Path.home() / ".local" / "state" / "atalaia"


def _archive_file() -> Path:
    return STATE_DIR / "archived.json"


def load_archived() -> set[str]:
    """Load archived project IDs. Returns empty set on missing/corrupt file."""
    path = _archive_file()
    if not path.is_file():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return set()
    if not isinstance(data, list):
        return set()
    return {item for item in data if isinstance(item, str)}


def save_archived(ids: set[str]) -> None:
    """Persist archived project IDs to disk."""
    path = _archive_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sorted(ids)), encoding="utf-8")


def archive(pid: str) -> None:
    """Add a project ID to the archive (idempotent)."""
    current = load_archived()
    current.add(pid)
    save_archived(current)


def unarchive(pid: str) -> None:
    """Remove a project ID from the archive (no-op if absent)."""
    current = load_archived()
    current.discard(pid)
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