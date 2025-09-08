import sqlite3
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'accounts.db')

def get_connection():
    """
    Establish and return a connection to the SQLite database.
    Includes a timeout to avoid 'database is locked' errors.
    """
    return sqlite3.connect(DB_PATH, timeout=10)

def initialize_database():
    """
    Create the accounts table if it doesn't already exist.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                number TEXT NOT NULL UNIQUE,
                balance REAL NOT NULL
            );
        """)
        conn.commit()