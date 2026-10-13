import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS = ROOT / "database/migrations"


class MigrationTests(unittest.TestCase):
    def test_expand_migrate_contract(self):
        with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
            with sqlite3.connect(tmp.name) as db:
                db.execute("""
                    CREATE TABLE customers (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT
                    )
                """)
                db.execute(
                    "INSERT INTO customers (name, email) VALUES (?, ?)",
                    ("Test Customer", "test@example.com"),
                )
                db.commit()

                db.executescript(
                    (MIGRATIONS / "001_expand.sql").read_text()
                )
                db.execute("""
                    UPDATE customers
                    SET email_v2 = email
                    WHERE email_v2 IS NULL AND email IS NOT NULL
                """)
                self.assertEqual(
                    db.execute(
                        "SELECT email_v2 FROM customers WHERE id = 1"
                    ).fetchone()[0],
                    "test@example.com",
                )

                db.executescript(
                    (MIGRATIONS / "002_contract.sql").read_text()
                )
                columns = {
                    row[1]
                    for row in db.execute("PRAGMA table_info(customers)")
                }
                self.assertNotIn("email", columns)
                self.assertIn("email_v2", columns)
                self.assertEqual(
                    db.execute(
                        "SELECT email_v2 FROM customers WHERE id = 1"
                    ).fetchone()[0],
                    "test@example.com",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
