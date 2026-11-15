"""Persistence layer for user records."""
import sqlite3

from store.models import User


class UserRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def save_user(self, user: User) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user.name, user.email),
        )
        self.conn.commit()
        return cur.lastrowid

    def get_user(self, user_id: int) -> User | None:
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return User(id=row[0], name=row[1], email=row[2])

    def delete_user(self, user_id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        return cur.rowcount > 0
