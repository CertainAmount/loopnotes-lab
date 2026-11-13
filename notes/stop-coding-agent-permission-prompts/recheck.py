#!/usr/bin/env python3
"""Re-check (2026-11-14) of the auto / acceptEdits results on the installed Claude Code version.
Reuses harness.py unchanged; writes to raw/results-2.jsonl and raw/recheck-2/, stops at $1 cumulative.
Usage: python3 recheck.py
"""
from pathlib import Path
import harness as h

h.RAW = h.HERE / "raw" / "recheck-2"; h.RAW.mkdir(parents=True, exist_ok=True)
h.RES = h.HERE / "raw" / "results-2.jsonl"
h.CAP_USD = 1.0

jobs = ([("C3", t, i) for t in ["T4", "T5", "T8b"] for i in (1, 2)]
        + [("C2", "T6", 1)]
        + [("C8", t, 1) for t in ["T3", "T8b"]])
h.run_many(jobs, workers=3)
print("cost", round(h.total_cost(), 3))
