import os
from urllib.parse import urlparse

import sqlite3


class SqliteDatabase:
    def __init__(self, db_path):
        assert os.path.exists(urlparse(db_path).path), f"{db_path} not found"
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path, uri=True)
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.connection is not None:
            self.connection.close()
        return False
