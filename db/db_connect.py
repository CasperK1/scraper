import sqlite3
import logging

class Database:
    def __init__(self, name):
        db_path = "db/" + name
        self._conn = sqlite3.connect(db_path)
        self._cursor = self._conn.cursor()
        self._create_tables()
        self._duplicate_count = {"verkkokauppa": 0, "datatronic": 0, "jimms": 0, "proshop": 0}

    def _create_tables(self):
        try:
            self._cursor.execute("""CREATE TABLE IF NOT EXISTS RTX4090 (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                store TEXT,
                name TEXT,
                datetime TEXT DEFAULT (datetime('now','localtime'))
            )""")
            self._cursor.execute("""CREATE TABLE IF NOT EXISTS RTX4090PriceHistory (
                price_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                price REAL,
                datetime TEXT DEFAULT (datetime('now','localtime')),
                FOREIGN KEY (product_id) REFERENCES RTX4090 (product_id)
            )""")
            self._conn.commit()

        except sqlite3.Error as e:
            logging.error(f"Error creating tables: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info(f"Duplicate prices {self._duplicate_count}.")
        self._conn.close()



    def insert(self, store, name, price):
        try:
            cursor = self._conn.cursor()
            # Check if the product already exists in the RTX4090 table
            cursor.execute(
                "SELECT product_id FROM RTX4090 WHERE store = ? AND name = ?",
                (store, name)
            )
            result = cursor.fetchone()

            if result:
                # Product exists, retrieve its product_id
                product_id = result[0]

                # Check if the same price already exists in the price history for this product
                cursor.execute(
                    "SELECT COUNT(*) FROM RTX4090PriceHistory WHERE product_id = ? AND price = ?",
                    (product_id, price)
                )
                count = cursor.fetchone()[0]
                if count > 0:
                    self._duplicate_count[store] += 1
                    return

                # Insert new price into RTX4090PriceHistory table
                cursor.execute(
                    "INSERT INTO RTX4090PriceHistory (product_id, price) VALUES (?, ?)",
                    (product_id, price)
                )

            else:
                # Product does not exist, insert it into RTX4090 table
                cursor.execute(
                    "INSERT INTO RTX4090 (store, name) VALUES (?, ?)",
                    (store, name)
                )
                product_id = cursor.lastrowid

                # Insert initial price into RTX4090PriceHistory table
                cursor.execute(
                    "INSERT INTO RTX4090PriceHistory (product_id, price) VALUES (?, ?)",
                    (product_id, price)
                )

            self._conn.commit()

        except sqlite3.IntegrityError:
            logging.error("IntegrityError: Attempted to insert a duplicate value.")

        except sqlite3.OperationalError as e:
            logging.error(f"OperationalError: An error occurred that's related to the database's operation. Details: {e}")


