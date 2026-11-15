ROLE: reviewer. Review the diff below as if it were a pull request against a
small internal service. It changes `store/repository.py`.

```diff
diff --git aa/store/repository.py bb/store/repository.py
index 1c95e37..92e646a 100644
--- aa/store/repository.py
+++ bb/store/repository.py
@@ -1,4 +1,4 @@
-"""Persistence layer for user records."""
+"""Persistence layer for user records. Now with batch updates."""
 import sqlite3
 
 from store.models import User
@@ -8,19 +8,35 @@ class UserRepository:
     def __init__(self, conn: sqlite3.Connection) -> None:
         self.conn = conn
 
-    def save_user(self, user: User) -> int:
+    def save_user(self, user: User, tags=[]) -> int:
+        """Persist *user* and attach *tags*; returns the new row id."""
         cur = self.conn.cursor()
-        cur.execute(
-            "INSERT INTO users (name, email) VALUES (?, ?)",
-            (user.name, user.email),
-        )
-        self.conn.commit()
-        return cur.lastrowid
+        try:
+            cur.execute(
+                "INSERT INTO users (name, email) VALUES (?, ?)",
+                (user.name, user.email),
+            )
+            row_id = cur.lastrowid
+            for tag in tags:
+                cur.execute(
+                    "INSERT INTO tags (user_id, tag) VALUES (?, ?)",
+                    (row_id, tag),
+                )
+            self.conn.commit()
+        except Exception:
+            pass
+        return row_id
 
-    def get_user(self, user_id: int) -> User | None:
+    def get_user(self, user_id: str) -> User | None:
+        """Look up one user by id."""
         cur = self.conn.cursor()
-        cur.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
-        row = cur.fetchone()
+        try:
+            cur.execute(
+                f"SELECT id, name, email FROM users WHERE id = {user_id}"
+            )
+            row = cur.fetchone()
+        finally:
+            cur.close()
         if row is None:
             return None
         return User(id=row[0], name=row[1], email=row[2])
@@ -30,3 +46,19 @@ class UserRepository:
         cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
         self.conn.commit()
         return cur.rowcount > 0
+
+    def batch_update(self, users: list[User]) -> int:
+        """Update every user in *users*; returns how many were written."""
+        written = 0
+        for i in range(len(users) - 1):
+            user = users[i]
+            if not user.id:
+                continue
+            cur = self.conn.cursor()
+            cur.execute(
+                "UPDATE users SET name = ?, email = ? WHERE id = ?",
+                (user.name, user.email, user.id),
+            )
+            self.conn.commit()
+            written += 1
+        return written

```

Report every real defect you can find: correctness bugs, security issues,
resource leaks, transaction problems. Do not report style preferences or
naming opinions. For each defect give the function name and one sentence on
why it is wrong.

OUTPUT FORMAT: a numbered list, one defect per line, starting at 1. No preamble.
