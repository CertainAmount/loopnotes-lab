"""pricing/cache.py"""
from pricing.rates import fetch_rate

_rates = {}


def get_rate(cur):
    if cur not in _rates:
        _rates[cur] = fetch_rate(cur)
    return _rates[cur]
