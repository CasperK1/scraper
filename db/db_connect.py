import sqlite3
import logging


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
        self._duplicate_count = {"verkkokauppa": 0, "datatronic": 0, "jimms": 0}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info(f"Duplicate prices {self._duplicate_count}.")
        self._conn.close()

    def insert(self, store, name, price):
        try:
            cursor = self._conn.cursor()

            # Check if the same product from the store with the same price already exists
            cursor.execute(
                "SELECT COUNT(*) FROM RTX4090 WHERE store = ? AND name = ? AND price = ?",
                (store, name, price)
            )
            count = cursor.fetchone()[0]
            if count > 0:
                self._duplicate_count[store] += 1
                return

            cursor.execute(
                "INSERT INTO RTX4090 (store, name, price) VALUES (?, ?, ?)",
                (store, name, price)
            )
            self._conn.commit()

        except sqlite3.IntegrityError:
            logging.error("IntegrityError: Attempted to insert a duplicate value.")

        except sqlite3.OperationalError:
            logging.error("OperationalError: An error occurred that's related to the database's operation.")
