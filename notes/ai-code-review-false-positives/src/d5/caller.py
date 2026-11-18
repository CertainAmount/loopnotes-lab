"""api/quote_server.py (unchanged, shown for context)"""
from concurrent.futures import ThreadPoolExecutor

from pricing.cache import billing_report, get_rate_counted

CURRENCIES = {"USD", "EUR", "JPY", "KRW"}
pool = ThreadPoolExecutor(max_workers=16)


def quote(cur, amount):
    if cur not in CURRENCIES:
        raise ValueError("unsupported currency")
    # requests are served concurrently from this pool
    return pool.submit(lambda: amount * get_rate_counted(cur)).result()


def close_month():
    return billing_report()
