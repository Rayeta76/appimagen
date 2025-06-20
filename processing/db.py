from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import sqlite3
from typing import Iterable, List

DB_PATH = Path("db/imagenes.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

@dataclass
class ImageRecord:
    title: str
    description: str
    path: str
    thumbnail: str

@dataclass
class TagRecord:
    name: str

class DBManager:
    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                """CREATE TABLE IF NOT EXISTS images (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        description TEXT,
                        path TEXT,
                        thumbnail TEXT
                    )"""
            )
            c.execute(
                """CREATE TABLE IF NOT EXISTS tags (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE
                    )"""
            )
            c.execute(
                """CREATE TABLE IF NOT EXISTS image_tags (
                        image_id INTEGER,
                        tag_id INTEGER,
                        PRIMARY KEY (image_id, tag_id),
                        FOREIGN KEY(image_id) REFERENCES images(id),
                        FOREIGN KEY(tag_id) REFERENCES tags(id)
                    )"""
            )
            conn.commit()

    def insert_image(self, record: ImageRecord, tags: Iterable[str]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO images(title, description, path, thumbnail) VALUES (?, ?, ?, ?)",
                (record.title, record.description, record.path, record.thumbnail),
            )
            image_id = c.lastrowid
            tag_ids: List[int] = []
            for tag in tags:
                c.execute("INSERT OR IGNORE INTO tags(name) VALUES (?)", (tag,))
                c.execute("SELECT id FROM tags WHERE name=?", (tag,))
                tag_id = c.fetchone()[0]
                tag_ids.append(tag_id)
            for tid in tag_ids:
                c.execute(
                    "INSERT OR IGNORE INTO image_tags(image_id, tag_id) VALUES (?, ?)",
                    (image_id, tid),
                )
            conn.commit()

    def search(self, text: str) -> List[ImageRecord]:
        wildcard = f"%{text}%"
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                """SELECT images.title, images.description, images.path, images.thumbnail
                   FROM images
                   LEFT JOIN image_tags ON images.id = image_tags.image_id
                   LEFT JOIN tags ON tags.id = image_tags.tag_id
                   WHERE images.title LIKE ? OR images.description LIKE ? OR tags.name LIKE ?
                   GROUP BY images.id""",
                (wildcard, wildcard, wildcard),
            )
            rows = c.fetchall()
            return [ImageRecord(*row) for row in rows]
