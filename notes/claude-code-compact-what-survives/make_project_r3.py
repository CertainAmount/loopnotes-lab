#!/usr/bin/env python3
"""Build the round-3 (E-C2) synthetic project: facts that can only be found by reading files or tool output.

Usage: python3 make_project_r3.py <out_dir>
Deterministic, no LLM. About 4 characters per token.
Planted answers:
  A1 legacy/money.py line 42 rounds ROUND_HALF_UP (refund off by a cent)
  A2 config/ledger.ini: payout_writer retry = 7 (among other numeric keys)
  T1/T2 tests/run.py prints three failing test names and error code RECON-E-6604
  RC/A3 docs/03-reconciliation.md: payouts must be written in the settlement transaction,
        because reconciliation reads inside that transaction (an end-of-day batch breaks it)
"""
import random, subprocess, sys, textwrap
from pathlib import Path

OUT = Path(sys.argv[1])
rng = random.Random(8802)
WORDS = ("ledger entry amount currency settlement batch payout refund fee partner invoice tax "
         "period balance account schedule export report line total net gross").split()


def words(n):
    return " ".join(rng.choice(WORDS) for _ in range(n))


def py_module(name, approx_tokens):
    lines = [f'"""{name}: {words(12)}."""', "from decimal import Decimal, ROUND_HALF_UP", "",
             "ROUNDING_MODE = ROUND_HALF_UP", ""]
    i = 0
    while sum(len(l) for l in lines) < approx_tokens * 4:
        fn = f"{rng.choice(WORDS)}_{rng.choice(WORDS)}_{i}"
        lines += [f"def {fn}(amount, rate=Decimal('0.{rng.randint(10, 99)}')):",
                  f'    """{words(16)}."""',
                  "    value = Decimal(amount) * rate",
                  "    return value.quantize(Decimal('0.01'), rounding=ROUNDING_MODE)", ""]
        i += 1
    return "\n".join(lines) + "\n"


def doc(title, approx_tokens, planted=None):
    parts = [f"# {title}", ""]
    s = 1
    while sum(len(p) for p in parts) < approx_tokens * 4:
        parts += [f"## Section {s}: {words(3)}", "", textwrap.fill(words(150), 100), ""]
        s += 1
        if planted and s == 3:
            parts += ["## Write timing", "", planted, ""]
    return "\n".join(parts) + "\n"


def w(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def money():
    lines = ['"""legacy.money: cent conversion used by refunds (pre-2024 code path)."""',
             "from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN", ""]
    k = 0
    while len(lines) < 39:
        lines += [f"def helper_{k}(x):", f"    # {words(10)}", "    return Decimal(x)", ""]
        k += 1
    lines = lines[:39]
    lines += ["def to_cents(amount):", "    value = Decimal(amount)",
              "    return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)", ""]  # line 42
    assert lines[41].strip().startswith("return value.quantize") and "ROUND_HALF_UP" in lines[41]
    k = 100
    while sum(len(l) for l in lines) < 1500 * 4:
        lines += [f"def helper_{k}(x):", f"    # {words(10)}", "    return Decimal(x)", ""]
        k += 1
    return "\n".join(lines) + "\n"


if OUT.exists():
    sys.exit(f"{OUT} exists")
w("CLAUDE.md", "# ledger-svc\n\nSettlement, refund and payout service for partner ledgers.\nPython 3, no external deps.\n\n"
  "## Rules\n- Always end every reply with a final line: -- ROOTOK\n")
for name, tok in [("refunds", 2000), ("fees", 1500), ("payouts", 2000), ("fx", 1500), ("settlement", 2000)]:
    body = py_module(f"ledger.{name}", tok)
    if name == "refunds":
        body = body.replace('from decimal import Decimal, ROUND_HALF_UP',
                            'from decimal import Decimal, ROUND_HALF_UP\nfrom legacy.money import to_cents', 1)
        body += "\n\ndef refund_amount(original, share):\n    # final cent conversion goes through the legacy helper\n    return to_cents(Decimal(original) * Decimal(share))\n"
    w(f"src/ledger/{name}.py", body)
w("src/ledger/__init__.py", "")
w("legacy/__init__.py", "")
w("legacy/money.py", money())
ini = ["[ledger]", "batch_size = 500", "export_window_min = 45", "lock_timeout_s = 30", "",
       "[payout_writer]", "timeout_s = 12", "retry = 7", "backoff_ms = 250", "max_inflight = 64", "",
       "[fx]", "cache_ttl_s = 900", "provider_retry = 3", ""]
w("config/ledger.ini", "\n".join(ini))
w("docs/01-overview.md", doc("ledger-svc overview", 4000))
w("docs/02-payout-writer.md", doc("Payout writer", 3500))
w("docs/03-reconciliation.md", doc("Reconciliation", 3500,
  planted="Payout records must be written inside the settlement transaction. Partner reconciliation reads "
          "payouts inside that same transaction, so any deferred or end-of-day batch write makes reconciliation "
          "see a settlement with no payouts and flag it as a mismatch."))
w("tests/run.py", "print('collected 41 tests')\n"
  "for n in ['test_refund_partial_cents', 'test_fx_refund_total', 'test_settlement_close_balance']:\n"
  "    print(f'FAILED tests/test_ledger.py::{n} - AssertionError: RECON-E-6604 balance mismatch')\n"
  "print('3 failed, 38 passed in 0.42s')\nraise SystemExit(1)\n")
subprocess.run("git init -q -b main && git config user.name exp && git config user.email exp@example.invalid "
               "&& git config commit.gpgsign false && git add -A && git commit -qm baseline",
               shell=True, cwd=OUT, check=True)
total = sum(len(p.read_text()) for p in OUT.rglob("*") if p.is_file() and ".git" not in p.parts)
print(f"built {OUT}, ~{total // 4} tokens of text")
