1. save_user — mutable default argument `tags=[]` means tags persist across calls and leak between users.
2. save_user — bare `except Exception: pass` swallows failures (including partial tag inserts) while returning a possibly unbound or misleading `row_id`.
3. save_user — on failure nothing rolls back the connection, leaving it in an open/incomplete transaction even though the error is suppressed.
4. get_user — type changed to `str` and SQL built with f-string interpolation of `user_id` into `WHERE id = {user_id}`, allowing SQL injection and breaking normal int callers.
5. batch_update — loop bound `range(len(users) - 1)` skips the last user entirely.
6. batch_update — commits once per row inside the loop instead of atomically for the whole batch, so partial updates survive mid-batch failures.
7. batch_update — increments `written` without checking cursor rowcount, reporting success even when no row was updated.