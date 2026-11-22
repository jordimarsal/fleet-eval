=== FILE: src/atalaia/archive.py ===
from __future__ import annotations

import json
import os
from pathlib import Path


STATE_DIR = Path(os.environ.get("ATALAIA_ARCHIVE_STATE_DIR") or (Path.home() / ".local" / "share" / "atalaia"))


def archived_file() -> Path:
    return STATE_DIR / "archived.json"


def load_archived() -> set[str]:
    try:
        data = json.loads(archived_file().read_text(encoding="utf-8"))
    except Exception:
        return set()
    if not isinstance(data, list):
        return set()
    return {item for item in data if isinstance(item, str)}


def save_archived(ids) -> None:
    clean = sorted({str(i) for i in ids if isinstance(i, str) and i})
    state_dir = archived_file().parent
    state_dir.mkdir(parents=True, exist_ok=True)
    archived_file().write_text(json.dumps(clean), encoding="utf-8")


def archive(project_id: str) -> set[str]:
    ids = load_archived()
    ids.add(project_id)
    save_archived(ids)
    return load_archived()


def unarchive(project_id: str) -> set[str]:
    ids = load_archived()
    before = len(ids)
    ids.discard(project_id)
    if len(ids) != before:
        save_archived(ids)
    else:
        from pathlib import Path

        path = archived_file()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                pass
        except Exception:
            pass
    return load_archived()


=== END FILE ===