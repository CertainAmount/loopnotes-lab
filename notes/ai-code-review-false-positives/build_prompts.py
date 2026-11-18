"""Build the 18 E3 prompts (6 diffs x conditions A/B/C) from diffs/ and src/."""
from pathlib import Path

HERE = Path(__file__).parent
BASE = "Review this diff. List each issue as one comment.\nFormat: one comment per line, each line starting with \"- \". No other text."
SCOPE = ("Only comment on security, concurrency, error handling, data integrity, "
         "or performance/resource usage. Skip style and naming.")
RULES = (HERE / "prompts/team-rules.txt").read_text().strip()

for i in range(1, 7):
    d = f"d{i}"
    diff = (HERE / f"diffs/{d}.diff").read_text().rstrip()
    caller = (HERE / f"src/{d}/caller.py").read_text().rstrip()
    a = f"{BASE}\n\n```diff\n{diff}\n```\n"
    b = (f"{BASE}\n\n```diff\n{diff}\n```\n\n"
         f"Callers of the changed code (unchanged files, for context):\n```python\n{caller}\n```\n\n{RULES}\n")
    c = f"{BASE}\n{SCOPE}\n\n```diff\n{diff}\n```\n"
    for cond, text in (("A", a), ("B", b), ("C", c)):
        (HERE / f"prompts/{d}-{cond}.txt").write_text(text)
print("ok")
