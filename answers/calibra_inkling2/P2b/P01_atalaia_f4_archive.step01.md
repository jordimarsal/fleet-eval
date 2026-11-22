=== FILE: src/atalaia/archive.py ===
"""Persistent store of archived project ids.

Load/save operations are   idempotent and tolerant of corrupt state files:
any mismatch falls back to an empty set rather than raising.
"""

from __future__ import annotations

import json
from pathlib import Path


STATE_DIR = Path(__file__).resolve().parents[2] / "state"


def _archived_path() -> Path:
    return Path(STATE_DIR) / "archived.json"


def load_archived() -> set[str]:
    try:
        raw = _archived_path().read_text(encoding="utf-8")
        data = json.loads(raw)
    except Exception:
        return set()
    if not isinstance(data, list):
        return set()
    return {item for item in data if isinstance(item, str)}


def save_archived(ids) -> None:
    path = _archived_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    unique = sorted({i for i in ids if isinstance(i, str) and i})
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(unique), encoding="utf-8")
    tmp.replace(path)


def archive(pid: str) -> None:
    current = load_archived()
    current.add(pid)
    save_archived(current)


def unarchive(pid: str) -> None:
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