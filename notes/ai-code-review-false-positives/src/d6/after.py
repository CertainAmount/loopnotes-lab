"""accounts/names.py"""


def initials(name):
    parts = name.split()
    return "".join(p[0].upper() for p in parts)


def short_name(name, n=12):
    if len(name) <= n:
        return name
    parts = name.split()
    if len(parts) == 1:
        return name[: n - 1] + "…"
    first, last = parts[0], parts[-1]
    s = f"{first} {last[0]}."
    if len(s) <= n:
        return s
    return first[: n - 1] + "…"
