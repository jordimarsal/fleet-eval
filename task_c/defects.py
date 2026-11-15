"""Contract for task C: the seeded defects this diff must be caught for."""
# Each entry: (id, where, what a correct review must mention)
DEFECTS = [
    ("D1", "save_user",
     "mutable default argument `tags=[]` shared across every call"),
    ("D2", "save_user",
     "bare `except Exception: pass` swallows the DB error and reports success"),
    ("D3", "get_user",
     "f-string used as a SQL query -> injection via `user_id`"),
    ("D4", "get_user",
     "connection/cursor never closed on the error path (resource leak)"),
    ("D5", "batch_update",
     "off-by-one: `range(len(users) - 1)` skips the last user"),
    ("D6", "batch_update",
     "`is not None` / truthiness bug: a user id of 0 is falsy and skipped"),
    ("D7", "batch_update",
     "each update runs in its own transaction with no rollback on failure "
     "(partial update)"),
]
