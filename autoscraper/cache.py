"""
Simple caching layer for AutoScraper results.
"""

import sqlite3
import json
import logging
import os

logger = logging.getLogger(__name__)


class ScraperCache:
    def __init__(self, db_path="scraper_cache.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS cache (url TEXT PRIMARY KEY, result TEXT)"
        )
        self.conn.commit()

    def get(self, url):
        cursor = self.conn.execute(
            "SELECT result FROM cache WHERE url = ?", (url,)
        )
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return None

    def set(self, url, result):
        data = json.dumps(result)
        self.conn.execute(
            "INSERT OR REPLACE INTO cache (url, result) VALUES (?, ?)",
            (url, data),
        )
        self.conn.commit()

    def delete_old_entries(self, days):
        try:
            self.conn.execute(
                "DELETE FROM cache WHERE created_at < datetime('now', ? || ' days')",
                (f"-{days}",),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logger.warning("Failed to delete old cache entries: %s", e)

    def export_all(self, output_path):
        cursor = self.conn.execute("SELECT url, result FROM cache")
        rows = cursor.fetchall()
        with open(output_path, "w") as f:
            for url, _ in rows:
                f.write("%s\n" % url)

    def close(self):
        self.conn.close()
