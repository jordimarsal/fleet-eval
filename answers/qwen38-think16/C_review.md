1. save_user: the mutable default `tags=[]` shares one list object across all calls that omit tags.
2. save_user: `except Exception: pass` silently swallows database and programming errors such as an invalid *tags* value.
3. save_user: `row_id` is referenced before assignment when the initial INSERT fails, causing UnboundLocalError instead of a handled error.
4. save_user: the cursor created in the method is never closed, leaking statement resources.
5. save_user: missing rollback after an exception leaves the connection in an open transaction with partially written data.
6. save_user: returning `row_id` after a swallowed exception reports success for data that was not committed.
7. get_user: interpolating `user_id` into SQL with an f-string enables SQL injection.
8. batch_update: `range(len(users) - 1)` skips the last element, so the advertised batch update does not process every user.
9. batch_update: incrementing `written` without checking `cur.rowcount` counts attempted updates even when no row actually matched.
10. batch_update: committing inside the loop makes the batch non-atomic and can leave partial updates if it fails midway.
11. batch_update: cursors created in each iteration are never closed on either success or error, leaking statement resources.
12. delete_user: the cursor created in the method is never closed, leaking statement resources.