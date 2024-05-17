import sqlite3


class database:
    def __init__(self, name):
        db_path = "db/" + name
        self._conn = sqlite3.connect(db_path)
        self._cursor = self._conn.cursor()
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS RTX4090 (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            store TEXT,
            name TEXT,
            price REAL,
            datetime TEXT DEFAULT (datetime('now','localtime'))
        )""")
        self._conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

    def insert(self, store, name, price):
        self._cursor.execute(
            "INSERT INTO RTX4090 (store, name, price) VALUES (?, ?, ?)",
            (store, name, price)
        )
        self._conn.commit()
