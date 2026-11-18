"""search/paging.py"""


def total_pages(n, size):
    return (n + size - 1) // size
