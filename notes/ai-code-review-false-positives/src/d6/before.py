"""accounts/names.py"""


def initials(name):
    parts = name.split()
    return "".join(p[0].upper() for p in parts)
