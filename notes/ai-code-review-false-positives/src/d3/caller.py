"""jobs/monthly_export.py (unchanged, shown for context)"""
import os
import re

from reports.export import export_month

EXPORT_DIR = "/var/exports"
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")


def run(month):
    if not MONTH_RE.match(month):
        raise ValueError("month must look like 2026-11")
    out_path = os.path.join(EXPORT_DIR, f"payments-{month}.csv")
    # this job runs every hour for the current month, inside one long-lived worker
    return export_month("/var/data/payments.db", out_path, month)
