import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class MediaRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS media_items (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    stored_filename TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                )
                '''
            )

    def create(
        self,
        media_id: str,
        title: str,
        tags: str,
        original_filename: str,
        stored_filename: str,
        content_type: str,
        size_bytes: int,
    ) -> dict[str, Any]:
        created_at = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                '''
                INSERT INTO media_items (
                    id, title, tags, original_filename, stored_filename,
                    content_type, size_bytes, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    media_id,
                    title,
                    tags,
                    original_filename,
                    stored_filename,
                    content_type,
                    size_bytes,
                    created_at,
                ),
            )
        return {
            "id": media_id,
            "title": title,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
            "original_filename": original_filename,
            "stored_filename": stored_filename,
            "content_type": content_type,
            "size_bytes": size_bytes,
            "created_at": created_at,
        }

    def search(self, q: str, page: int, limit: int) -> dict[str, Any]:
        offset = (page - 1) * limit
        pattern = f"%{q.strip()}%"
        with self._connect() as conn:
            if q.strip():
                where = "WHERE title LIKE ? OR tags LIKE ? OR original_filename LIKE ?"
                params: tuple[Any, ...] = (pattern, pattern, pattern)
            else:
                where = ""
                params = ()

            total = conn.execute(
                f"SELECT COUNT(*) FROM media_items {where}", params
            ).fetchone()[0]

            rows = conn.execute(
                f'''
                SELECT * FROM media_items
                {where}
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
                ''',
                (*params, limit, offset),
            ).fetchall()

        items = [
            {
                "id": r["id"],
                "title": r["title"],
                "tags": [t.strip() for t in r["tags"].split(",") if t.strip()],
                "original_filename": r["original_filename"],
                "stored_filename": r["stored_filename"],
                "content_type": r["content_type"],
                "size_bytes": r["size_bytes"],
                "created_at": r["created_at"],
            }
            for r in rows
        ]
        pages = math.ceil(total / limit) if total > 0 else 1
        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
        }

    def delete(self, media_id: str) -> str | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT stored_filename FROM media_items WHERE id = ?", (media_id,)
            ).fetchone()
            if not row:
                return None
            conn.execute("DELETE FROM media_items WHERE id = ?", (media_id,))
            return str(row["stored_filename"])
