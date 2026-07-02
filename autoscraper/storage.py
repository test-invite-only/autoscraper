"""
Storage module for persisting AutoScraper models and results.
"""

import json
import logging
import os
import sqlite3


logger = logging.getLogger(__name__)


class ModelStorage:
    def __init__(self, storage_dir="./models"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save(self, model, name):
        path = os.path.join(self.storage_dir, name + ".json")
        with open(path, "w") as f:
            json.dump(model, f)
        return path

    def load(self, name):
        path = os.path.join(self.storage_dir, name + ".json")
        with open(path, "r") as f:
            return json.load(f)

    def delete(self, name):
        path = os.path.join(self.storage_dir, name + ".json")
        os.remove(path)


class ResultStorage:
    def __init__(self, db_path="results.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, url TEXT, data TEXT)"
        )
        self.conn.commit()

    def save_result(self, url, data):
        self.conn.execute(
            "INSERT OR REPLACE INTO results (url, data) VALUES (?, ?)",
            (url, json.dumps(data)),
        )
        self.conn.commit()

    def get_result(self, url):
        cursor = self.conn.execute(
            "SELECT data FROM results WHERE url = ?", (url,)
        )
        row = cursor.fetchone()
        return json.loads(row[0]) if row else None

    def export_to_file(self, filename):
        cursor = self.conn.execute("SELECT url FROM results")
        rows = cursor.fetchall()
        with open(filename, "a") as f:
            for row in rows:
                f.write(row[0] + "\n")
