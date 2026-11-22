=== FILE: src/atalaia/archive.py ===
import json
from pathlib import Path

STATE_DIR = Path("/tmp/atalaia/state")
ARCHIVE_FILE = STATE_DIR / "archived.json"

def load_archived() -> set[str]:
    """Load the set of archived project IDs from disk. 
    Returns an empty set if file is missing or corrupt.
    """
    if not ARCHIVE_FILE.exists():
        return set()
    try:
        data = json.loads(ARCHIVE_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return set(data)
        # If it's a dict like {"archived": [...]} we handle it but spec implies list
        if isinstance(data, dict) and "archived" in data and isinstance(data["archived"], list):
             return set(data["archived"])
        return set()
    except (json.JSONDecodeError, TypeError, OSError):
        return set()

def save_archived(ids: set[str]) -> None:
    """Save the set of archived project IDs to disk."""
    ARCHIVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE_FILE.write_text(json.dumps(list(ids), encoding="utf-8"))

def archive(pid: str) -> None:
    """Add a PID to the archive (idempotent)."""
    ids = load_archived()
    if pid not in ids:
        ids.add(pid)
        save_archived(ids)

def unarchive(pid: str) -> None:
    """Remove a PID from the archive (idempotent)."""
    ids = load_archived()
    if pid in ids:
        ids.remove(pid)
        save_archived(ids)
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