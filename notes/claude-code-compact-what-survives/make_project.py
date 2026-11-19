#!/usr/bin/env python3
"""Build the synthetic ledger-svc project for the /compact experiment (deterministic, no LLM).

Usage: python3 make_project.py <out_dir>
Sizes are approximate (about 4 characters per token).
"""
import random, subprocess, sys, textwrap
from pathlib import Path

OUT = Path(sys.argv[1])
rng = random.Random(7731)
WORDS = ("ledger entry amount currency settlement batch payout refund fee partner invoice tax "
         "rounding period balance account reconcile schedule export report line total net gross").split()


def words(n):
    return " ".join(rng.choice(WORDS) for _ in range(n))


def py_module(name, approx_tokens, uses_rounding=True):
    lines = [f'"""{name}: {words(12)}."""', "from decimal import Decimal, ROUND_HALF_UP", ""]
    if uses_rounding:
        lines += ["ROUNDING_MODE = ROUND_HALF_UP", ""]
    i = 0
    while sum(len(l) for l in lines) < approx_tokens * 4:
        fn = f"{rng.choice(WORDS)}_{rng.choice(WORDS)}_{i}"
        body = [f"def {fn}(amount, rate=Decimal('0.{rng.randint(10, 99)}')):",
                f'    """{words(18)}."""',
                f"    # {words(14)}",
                "    value = Decimal(amount) * rate",
                (f"    return value.quantize(Decimal('0.01'), rounding=ROUNDING_MODE)" if uses_rounding
                 else "    return value"), ""]
        lines += body
        i += 1
    return "\n".join(lines) + "\n"


def doc(title, approx_tokens):
    parts = [f"# {title}", ""]
    s = 1
    while sum(len(p) for p in parts) < approx_tokens * 4:
        parts += [f"## Section {s}: {words(3)}", "", textwrap.fill(words(160), 100), ""]
        s += 1
    return "\n".join(parts) + "\n"


def w(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


if OUT.exists():
    sys.exit(f"{OUT} exists")
w("CLAUDE.md", "# ledger-svc\n\nSettlement and payout service for partner ledgers.\nPython 3, no external deps; run tests with `python tests/run.py`.\n\n"
  "## Rules\n- Always end every reply with a final line: -- ROOTOK\n")
w("billing/CLAUDE.md", "# billing/\n\n- When you mention anything about billing/, include the code word HERON.\n")
w("billing/invoice.py", py_module("billing.invoice", 3500, uses_rounding=False))
w("billing/tax.py", py_module("billing.tax", 3500, uses_rounding=False))
for name, tok in [("rounding", 2500), ("settlement", 3000), ("fees", 2500), ("payouts", 3000),
                  ("refunds", 2500), ("report_templates", 7000), ("fx", 2500)]:
    w(f"src/ledger/{name}.py", py_module(f"ledger.{name}", tok))
w("src/ledger/__init__.py", "")
w("legacy/old_rounding.py", py_module("legacy.old_rounding", 1500))
for i, t in enumerate(["Architecture overview", "Settlement pipeline", "Partner integration",
                       "Payout scheduling", "Reporting and exports"], 1):
    w(f"docs/{i:02d}-{t.lower().replace(' ', '-')}.md", doc(t, 5000))
w("scripts/migrate.py", "import sys\nprint('E_LOCK_9472: migration lock held by pid 31337', file=sys.stderr)\nsys.exit(1)\n")
w("tests/test_rounding.py", "from decimal import Decimal\nfrom src.ledger import rounding\n\n\ndef test_mode_exists():\n    assert rounding.ROUNDING_MODE is not None\n")
w("tests/run.py", "import sys, importlib, pathlib\nsys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))\n"
  "ok = 0\nfor f in sorted(pathlib.Path(__file__).parent.glob('test_*.py')):\n    m = importlib.import_module('tests.' + f.stem)\n"
  "    for n in dir(m):\n        if n.startswith('test_'):\n            getattr(m, n)(); ok += 1\nprint(f'{ok} passed')\n")
w("tests/__init__.py", "")
w(".claude/settings.json", '{\n  "hooks": {\n    "SessionStart": [\n      {"matcher": "compact", "hooks": [{"type": "command", "command": "echo \\"OWL-HOOK: hook context after compaction\\""}]}\n    ]\n  }\n}\n')
subprocess.run("git init -q -b main && git config user.name exp && git config user.email exp@example.invalid "
               "&& git config commit.gpgsign false && git add -A && git commit -qm baseline",
               shell=True, cwd=OUT, check=True)
total = sum(len(p.read_text()) for p in OUT.rglob("*") if p.is_file() and ".git" not in p.parts)
print(f"built {OUT}, ~{total // 4} tokens of text")
