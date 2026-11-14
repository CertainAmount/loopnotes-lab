"""Price gaps between cheap and strong tiers, from official list prices read 2026-11-14.

USD per 1M tokens, standard (uncached) input and output. Run: python3 calc.py
"""
from fractions import Fraction as F

# (cheap name, cheap in, cheap out, strong name, strong in, strong out)
PAIRS = [
    ("gpt-6-luna", F("0.10"), F("0.50"), "gpt-6-sol", F("2"), F("10")),
    ("gpt-6-luna >272K", F("0.20"), F("0.75"), "gpt-6-sol >272K", F("4"), F("15")),
    ("Haiku 5.5 <=100K", F("0.10"), F("0.50"), "Sonnet 5.5", F("2"), F("10")),
    ("Haiku 5.5 >100K", F("0.50"), F("2.50"), "Sonnet 5.5", F("2"), F("10")),
    ("gpt-6.1-terra", F("1"), F("5"), "gpt-6-sol", F("2"), F("10")),
    ("Sonnet 5.5", F("2"), F("10"), "Opus 5.5", F("4"), F("20")),
]

print("| Cheap | Strong | Input gap | Output gap | Tries to equal one strong call | Cheap-first failure rate that loses money |")
print("|---|---|---|---|---|---|")
for cn, ci, co, sn, si, so in PAIRS:
    gi, go = si / ci, so / co
    assert gi == go, (cn, sn)  # same gap on input and output -> any input:output mix gives the same gap
    r = gi
    print(f"| {cn} | {sn} | {float(gi):g}x | {float(go):g}x | {float(r):g} | above {float(1 - 1 / r):.0%} |")
