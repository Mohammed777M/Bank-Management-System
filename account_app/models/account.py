from database.db import get_connection
import sqlite3
from database.db import get_connection

def create_account(name, number, balance):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if account number exists
    cursor.execute("SELECT id FROM accounts WHERE number = ?", (number,))
    if cursor.fetchone():
        raise ValueError("Account number already exists.")
    
    cursor.execute(
        "INSERT INTO accounts (name, number, balance) VALUES (?, ?, ?)",
        (name, number, balance)
    )
    conn.commit()
    account_id = cursor.lastrowid
    conn.close()
    return account_id



def create_account(name, number, balance):
    conn = get_connection()
    cursor = conn.cursor()

    # Check for duplicate account number (optional but recommended)
    cursor.execute("SELECT id FROM accounts WHERE number = ?", (number,))
    if cursor.fetchone():
        raise ValueError("Account number already exists.")

    cursor.execute(
        "INSERT INTO accounts (name, number, balance) VALUES (?, ?, ?)",
        (name, number, balance)
    )
    conn.commit()

    # Get the id of the newly inserted account
    account_id = cursor.lastrowid

    conn.close()
    return account_id



def get_accounts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_account_by_id(account_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
    account = cursor.fetchone()
    conn.close()
    return account


def update_account(account_id, name, number, balance):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE accounts SET name = ?, number = ?, balance = ? WHERE id = ?",
        (name, number, balance, account_id)
    )
    conn.commit()
    conn.close()


def delete_account(account_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts WHERE id=?", (account_id,))
    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()
    return rows_deleted > 0