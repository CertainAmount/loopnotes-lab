"""reports/export.py"""
import csv
import sqlite3


def write_rows(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        for r in rows:
            w.writerow(r)


def export_month(db_path, out_path, month):
    conn = sqlite3.connect(db_path)
    cur = conn.execute(
        "SELECT id, amount, created_at FROM payments WHERE month = ?", (month,)
    )
    rows = cur.fetchall()
    if not rows:
        return 0
    write_rows(out_path, rows)
    conn.close()
    return len(rows)
