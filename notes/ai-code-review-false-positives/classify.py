"""Apply the README rules to each comment in outputs/dN-X.txt -> e3-classified.csv and e3-summary.csv.
Labels below were assigned by reading each comment against the README rules (one judge).
Format per comment: (class, planted_hit, reason_tag, ambiguous, short_reason)."""
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
A, W, L = "acted_on", "wrong", "right_low_value"
LAB = {
 "d1-A": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",1,"N+1 batch"),(L,0,"",0,"dedupe teams"),(L,0,"",0,"batch fails on one"),(L,0,"",0,"list comprehension"),(L,0,"",0,"empty short_label"),(L,0,"",0,"separator in service layer"),(A,0,"",0,"tests for missing user/team")],
 "d1-B": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",0,"batch fails on one"),(L,0,"",1,"N+1 batch")],
 "d1-C": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",0,"batch fails on one"),(L,0,"",1,"N+1 batch"),(L,0,"",0,"dedupe teams"),(L,0,"",0,"uids size limit (security framing)"),(L,0,"",1,"authorization check (speculative)")],
 "d2-A": [(A,1,"",0,"except returns True"),(A,0,"",0,"charged without order"),(L,0,"",1,"broad except types"),(L,0,"",0,"log.warning drops traceback"),(L,0,"",1,"idempotency key"),(L,0,"",0,"intentional except is silent"),(A,0,"",0,"tests for failure paths")],
 "d2-B": [(A,1,"",0,"except returns True, 502 unreachable"),(A,0,"",0,"broad except lacks intentional marker (team rule 3)"),(A,0,"",0,"charged without order"),(L,0,"",0,"log.warning drops traceback"),(L,0,"",1,"idempotency key")],
 "d2-C": [(A,1,"",0,"except returns True"),(A,0,"",0,"charged without order"),(L,0,"",1,"idempotency key"),(L,0,"",1,"broad except / ambiguous charge"),(L,0,"",0,"log.warning drops traceback")],
 "d3-A": [(A,1,"",0,"conn leak on early return"),(L,0,"",1,"no file when empty"),(L,0,"",0,"close right after fetchall"),(L,0,"",0,"fetchall memory"),(L,0,"",0,"no CSV header (pre-existing)"),(L,0,"",0,"month column assumption"),(W,0,"already-handled-elsewhere",0,"month unvalidated"),(L,0,"",0,"float amounts"),(A,0,"",0,"tests for empty-month path")],
 "d3-B": [(A,1,"",0,"conn leak on early return"),(A,0,"",0,"conn leak on exception"),(L,0,"",0,"close right after fetchall"),(L,0,"",1,"atomic temp-file write"),(L,0,"",1,"stale file when empty"),(L,0,"",0,"no CSV header")],
 "d3-C": [(A,1,"",0,"conn leak on early return"),(A,0,"",0,"conn leak on exception"),(L,0,"",0,"close right after fetchall"),(L,0,"",0,"fetchall memory"),(L,0,"",1,"atomic temp-file write"),(L,0,"",1,"stale file when empty"),(L,0,"",0,"CSV formula injection (numeric columns)")],
 "d4-A": [(A,1,"",0,"off-by-one end"),(W,0,"already-handled-elsewhere",0,"page not validated"),(L,0,"",1,"size<=0 (caller code, outside diff)"),(W,0,"already-handled-elsewhere",0,"page beyond total"),(L,0,"",0,"needs materialized list"),(A,0,"",0,"boundary tests"),(L,0,"",0,"docstring 1-indexed")],
 "d4-B": [(A,1,"",0,"off-by-one end")],
 "d4-C": [(A,1,"",0,"off-by-one end (framed as data integrity)"),(W,0,"already-handled-elsewhere",0,"page not validated"),(L,0,"",1,"size<=0 (caller code, outside diff)"),(W,0,"already-handled-elsewhere",0,"size upper bound (caller caps at 100)"),(L,0,"",0,"needs materialized list"),(W,0,"already-handled-elsewhere",0,"page beyond total")],
 "d5-A": [(A,1,"",0,"non-atomic increment"),(L,0,"",1,"in-memory billing"),(A,0,"",0,"never reset across months"),(L,0,"",0,"no partner id"),(A,0,"",0,"dict changed size during iteration"),(L,0,"",0,"hits counts misses (naming)"),(W,0,"already-handled-elsewhere",0,"cur unvalidated"),(L,0,"",0,"get_rate duplicate fetch (pre-existing)"),(L,0,"",0,"use Counter"),(A,0,"",0,"tests for counting")],
 "d5-B": [(A,1,"",0,"non-atomic increment"),(A,0,"",0,"dict changed size during iteration"),(A,0,"",0,"never reset across months"),(L,0,"",1,"in-memory billing"),(L,0,"",0,"get_rate duplicate fetch (pre-existing)"),(L,0,"",0,"hits counts misses (naming)")],
 "d5-C": [(A,1,"",0,"non-atomic increment"),(L,0,"",0,"get_rate duplicate fetch (pre-existing)"),(A,0,"",0,"dict changed size during iteration"),(A,0,"",0,"never reset across months"),(L,0,"",1,"in-memory billing"),(L,0,"",0,"fetch_rate errors not handled"),(L,0,"",1,"no TTL / unbounded keys if unvalidated")],
 "d6-A": [(W,0,"already-handled-elsewhere",0,"whitespace-only name"),(L,0,"",0,"n not validated"),(W,0,"already-handled-elsewhere",0,"name not stripped"),(L,0,"",0,"inconsistent normalization"),(L,0,"",0,"ellipsis when first fits"),(L,0,"",0,"grapheme clusters"),(L,0,"",0,"display width"),(L,0,"",0,"byte length"),(L,0,"",0,"western name order"),(L,0,"",0,"docstring"),(L,0,"",0,"tests")],
 "d6-B": [(L,0,"",0,"n<=0"),(L,0,"",0,"ellipsis when first fits"),(L,0,"",0,"grapheme clusters"),(L,0,"",0,"display width"),(L,0,"",0,"middle names dropped"),(L,0,"",0,"tests"),(L,0,"",0,"docstring")],
 "d6-C": [(W,0,"already-handled-elsewhere",0,"whitespace-only name"),(W,0,"already-handled-elsewhere",0,"name None"),(L,0,"",0,"n not validated"),(L,0,"",0,"grapheme clusters"),(L,0,"",0,"byte length"),(L,0,"",0,"collisions / impersonation (security framing)")],

 "d1-D": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",0,"batch fails on one")],
 "d2-D": [(A,1,"",0,"except returns True"),(A,0,"",0,"charged without order"),(L,0,"",1,"broad except types"),(L,0,"",0,"log.warning drops traceback"),(L,0,"",1,"idempotency key")],
 "d3-D": [(A,1,"",0,"conn leak on early return and on exception")],
 "d4-D": [(A,1,"",0,"off-by-one end"),(W,0,"already-handled-elsewhere",0,"page not validated"),(L,0,"",1,"size<=0 (caller code, outside diff)")],
 "d5-D": [(A,1,"",0,"non-atomic increment"),(A,0,"",0,"dict changed size during iteration"),(A,0,"",0,"never reset across months"),(L,0,"",1,"in-memory billing")],
 "d6-D": [(W,0,"already-handled-elsewhere",0,"whitespace-only name"),(L,0,"",0,"n not validated")],
 "d1-E": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",1,"N+1 batch"),(L,0,"",0,"batch fails on one")],
 "d2-E": [(A,1,"",0,"except returns True"),(A,0,"",0,"charged without order"),(L,0,"",1,"idempotency key"),(L,0,"",0,"log.warning drops traceback")],
 "d3-E": [(A,1,"",0,"conn leak on early return"),(A,0,"",0,"conn leak on exception"),(L,0,"",0,"fetchall memory")],
 "d4-E": [(A,1,"",0,"off-by-one end"),(W,0,"already-handled-elsewhere",0,"page not validated"),(L,0,"",1,"size<=0 (caller code, outside diff)")],
 "d5-E": [(A,1,"",0,"non-atomic increment"),(A,0,"",0,"dict changed size during iteration"),(L,0,"",1,"in-memory billing"),(A,0,"",0,"never reset across months"),(L,0,"",0,"get_rate duplicate fetch (pre-existing)")],
 "d6-E": [(W,0,"already-handled-elsewhere",0,"whitespace-only name")],
}
rows = []
for key, labs in LAB.items():
    lines = [l for l in (HERE / f"outputs/{key}.txt").read_text().splitlines() if l.startswith("- ")]
    assert len(lines) == len(labs), (key, len(lines), len(labs))
    d, c = key.split("-")
    for i, (cls, hit, tag, amb, why) in enumerate(labs, 1):
        rows.append(dict(condition=c, diff=d, comment_id=f"{key}-{i}", cls=cls, planted_hit=hit, reason_tag=tag, ambiguous=amb, note=why))
with open(HERE / "e3-classified.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["condition","diff","comment_id","cls","planted_hit","reason_tag","ambiguous","note"])
    w.writeheader(); w.writerows(rows)
with open(HERE / "e3-summary.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["condition","comments","acted_on","wrong","right_low_value","pct_acted","pct_wrong","pct_low","planted_hits_of_5","ambiguous"])
    for c in "ABCDE":
        r = [x for x in rows if x["condition"] == c]; k = Counter(x["cls"] for x in r); n = len(r)
        hits = len({x["diff"] for x in r if x["planted_hit"]})
        w.writerow([c, n, k[A], k[W], k[L], round(100*k[A]/n), round(100*k[W]/n), round(100*k[L]/n), hits, sum(x["ambiguous"] for x in r)])
print((HERE / "e3-summary.csv").read_text())
for c in "ABCDE":
    print(c, {d: sum(1 for x in rows if x["condition"]==c and x["diff"]==d) for d in ["d1","d2","d3","d4","d5","d6"]})
