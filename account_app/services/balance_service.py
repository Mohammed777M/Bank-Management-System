import threading
from models.account import get_all_accounts



def calculate_total_balance_threaded():
    accounts = get_all_accounts()
    total = 0
    lock = threading.Lock()

    def worker(acc):
        nonlocal total
        with lock:
            total += acc['balance']

    threads = []
    for acc in accounts:
        t = threading.Thread(target=worker, args=(acc,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return total