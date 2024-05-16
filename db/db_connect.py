import sqlite3

class database:
    def __init__(self, name):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

    def insert(self, table, columns, values):
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns})")
        self._cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")

