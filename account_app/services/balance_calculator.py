# account_app/services/balance_calculator.py

import threading
from database.db import get_connection

def fetch_all_balances():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def calculate_total_balance_threaded():
    balances = fetch_all_balances()
    batch_size = 5
    results = []
    threads = []

    def worker(batch):
        results.append(sum(batch))

    for i in range(0, len(balances), batch_size):
        batch = balances[i:i+batch_size]
        t = threading.Thread(target=worker, args=(batch,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sum(results)
