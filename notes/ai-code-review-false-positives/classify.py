"""Apply the README rules to each comment in outputs/dN-X.txt (run 1) and outputs/rN/dN-X.txt (repeats r2, r3, 2026-11-19)
-> e3-classified.csv (one row per comment, with a run column), e3-summary.csv (run 1 per condition, unchanged)
and e3-summary-runs.csv (A, B, C, E per run, then mean and min-max across the 3 runs).
Labels below were assigned by reading each comment against the README rules (one judge).
Format per comment: (class, planted_hit, reason_tag, ambiguous, short_reason). Keys without a run prefix are run 1."""
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

 # repeats, 2026-11-19 (run_e3_repeats.sh; A, B, C, E only)
 "r2/d1-A": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",1,"N+1 batch"),(L,0,"",0,"batch fails on one"),(L,0,"",0,"team.name None fallback"),(L,0,"",0,"user.name None"),(L,0,"",0,"list comprehension"),(A,0,"",0,"tests for missing user/team")],
 "r2/d1-B": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",0,"batch fails on one"),(L,0,"",1,"N+1 batch")],
 "r2/d1-C": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",1,"N+1 batch"),(L,0,"",0,"batch fails on one"),(L,0,"",0,"uids size limit (security framing)"),(L,0,"",0,"team.name None fallback")],
 "r2/d1-E": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",1,"N+1 batch"),(L,0,"",0,"batch fails on one")],
 "r2/d2-A": [(A,1,"",0,"except returns True"),(A,0,"",0,"charged without order"),(L,0,"",1,"pending order before charge / crash between steps"),(L,0,"",1,"broad except types"),(L,0,"",0,"log.warning drops traceback"),(L,0,"",0,"no failure metric"),(L,0,"",1,"idempotency key"),(L,0,"",0,"intentional except is silent")],
 "r2/d2-B": [(A,1,"",0,"except returns True, 502 unreachable"),(A,0,"",0,"broad except lacks intentional marker (team rule 3)"),(A,0,"",0,"charged without order"),(L,0,"",1,"idempotency key"),(L,0,"",0,"log.warning drops traceback")],
 "r2/d2-C": [(A,1,"",0,"except returns True"),(A,0,"",0,"charged without order"),(L,0,"",1,"idempotency key"),(L,0,"",1,"broad except / ambiguous charge"),(L,0,"",0,"log.warning drops traceback"),(L,0,"",0,"exception text may leak payment data (security framing)")],
 "r2/d2-E": [(A,1,"",0,"except returns True"),(A,0,"",0,"charged without order"),(L,0,"",1,"idempotency key"),(L,0,"",1,"broad except / ambiguous charge")],
 "r2/d3-A": [(A,1,"",0,"conn leak on early return"),(A,0,"",0,"conn leak on exception"),(L,0,"",0,"with-connect does not close (advice)"),(L,0,"",0,"close right after fetchall"),(L,0,"",1,"stale file when empty"),(L,0,"",0,"fetchall memory"),(L,0,"",0,"no CSV header (pre-existing)"),(L,0,"",0,"write_rows newline (pre-existing)"),(L,0,"",0,"month column assumption"),(W,0,"already-handled-elsewhere",0,"month unvalidated"),(A,0,"",0,"tests for empty-month path"),(L,0,"",0,"docstring")],
 "r2/d3-B": [(A,1,"",0,"conn leak on early return"),(A,0,"",0,"conn leak on exception"),(L,0,"",1,"stale file when empty"),(L,0,"",0,"close right after fetchall")],
 "r2/d3-C": [(A,1,"",0,"conn leak on early return"),(A,0,"",0,"conn leak on exception"),(L,0,"",0,"fetchall memory"),(L,0,"",0,"close right after fetchall"),(L,0,"",1,"stale file when empty"),(L,0,"",1,"atomic temp-file write")],
 "r2/d3-E": [(A,1,"",0,"conn leak on early return"),(A,0,"",0,"conn leak on exception"),(L,0,"",0,"fetchall memory")],
 "r2/d4-A": [(A,1,"",0,"off-by-one end"),(W,0,"already-handled-elsewhere",0,"page not validated"),(L,0,"",1,"size<=0 (caller code, outside diff)"),(W,0,"already-handled-elsewhere",0,"page beyond total"),(L,0,"",0,"empty result 0 pages vs page 1"),(L,0,"",0,"needs materialized list"),(A,0,"",0,"boundary tests")],
 "r2/d4-B": [(A,1,"",0,"off-by-one end")],
 "r2/d4-C": [(A,1,"",0,"off-by-one end"),(W,0,"already-handled-elsewhere",0,"page not validated"),(L,0,"",1,"size<=0 (caller code, outside diff)"),(W,0,"already-handled-elsewhere",0,"size upper bound (caller caps at 100)"),(W,0,"already-handled-elsewhere",0,"page/size not type-checked (caller int())"),(L,0,"",0,"needs materialized list")],
 "r2/d4-E": [(A,1,"",0,"off-by-one end"),(W,0,"already-handled-elsewhere",0,"page not validated"),(L,0,"",1,"size<=0 (caller code, outside diff)")],
 "r2/d5-A": [(A,1,"",0,"non-atomic increment"),(L,0,"",1,"in-memory billing"),(L,0,"",1,"per-process counts (in-memory billing)"),(A,0,"",0,"never reset across months"),(L,0,"",0,"no partner id"),(L,0,"",0,"hits counts misses (naming)"),(W,0,"already-handled-elsewhere",0,"cur unvalidated"),(L,0,"",0,"get_rate stays public / unbilled path"),(L,0,"",0,"billing in cache module (design)"),(A,0,"",0,"dict changed size during iteration"),(A,0,"",0,"tests for counting"),(L,0,"",0,"use Counter")],
 "r2/d5-B": [(A,1,"",0,"non-atomic increment"),(A,0,"",0,"dict changed size during iteration"),(A,0,"",0,"never reset across months"),(L,0,"",1,"in-memory billing"),(L,0,"",0,"hits counts misses (naming)"),(L,0,"",0,"get_rate duplicate fetch (pre-existing)")],
 "r2/d5-C": [(A,1,"",0,"non-atomic increment"),(A,0,"",0,"dict changed size during iteration"),(L,0,"",0,"get_rate duplicate fetch (pre-existing)"),(L,0,"",1,"in-memory billing"),(A,0,"",0,"never reset across months"),(W,0,"already-handled-elsewhere",0,"cur unvalidated"),(L,0,"",1,"no TTL on rates (data integrity framing)")],
 "r2/d5-E": [(A,1,"",0,"non-atomic increment"),(A,0,"",0,"dict changed size during iteration"),(L,0,"",1,"in-memory billing"),(A,0,"",0,"never reset across months")],
 "r2/d6-A": [(W,0,"already-handled-elsewhere",0,"whitespace-only name"),(L,0,"",0,"ellipsis when first fits"),(L,0,"",0,"n not validated"),(L,0,"",1,"inconsistent normalization (leading/trailing part handled by route)"),(L,0,"",0,"grapheme clusters"),(L,0,"",0,"display width"),(L,0,"",0,"western name order"),(L,0,"",0,"byte length / non-ASCII ellipsis"),(L,0,"",0,"docstring"),(L,0,"",0,"tests")],
 "r2/d6-B": [(L,0,"",0,"ellipsis when first fits"),(L,0,"",0,"collisions (last initial dropped)"),(L,0,"",0,"n<=0"),(L,0,"",0,"grapheme clusters / display width"),(L,0,"",0,"tests")],
 "r2/d6-C": [(W,0,"already-handled-elsewhere",0,"whitespace-only name"),(L,0,"",0,"n not validated"),(W,0,"already-handled-elsewhere",0,"name None"),(L,0,"",0,"grapheme clusters")],
 "r2/d6-E": [(W,0,"already-handled-elsewhere",0,"whitespace-only name")],
 "r3/d1-A": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",1,"N+1 batch"),(L,0,"",0,"batch fails on one"),(L,0,"",0,"list comprehension"),(L,0,"",0,"team.name None fallback"),(L,0,"",0,"separator in service layer"),(A,0,"",0,"tests for missing user/team")],
 "r3/d1-B": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",0,"batch fails on one"),(L,0,"",1,"N+1 batch")],
 "r3/d1-C": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",1,"N+1 batch"),(L,0,"",0,"dedupe teams"),(L,0,"",0,"batch fails on one"),(L,0,"",0,"uids size limit (security framing)"),(L,0,"",0,"non-transactional reads (concurrency framing)")],
 "r3/d1-E": [(A,1,"",0,"user None"),(A,0,"",0,"team None"),(L,0,"",0,"batch fails on one"),(L,0,"",1,"N+1 batch")],
 "r3/d2-A": [(A,1,"",0,"except returns True"),(A,0,"",0,"charged without order"),(L,0,"",1,"idempotency key"),(L,0,"",1,"broad except types"),(L,0,"",0,"log.warning drops traceback"),(L,0,"",0,"intentional except is silent"),(L,0,"",0,"no failure metric"),(A,0,"",0,"tests for failure paths")],
 "r3/d2-B": [(A,1,"",0,"except returns True, 502 unreachable"),(A,0,"",0,"broad except lacks intentional marker (team rule 3)"),(A,0,"",0,"charged without order"),(L,0,"",1,"idempotency key"),(L,0,"",0,"log.warning drops traceback"),(A,0,"",0,"restates planted bug: 502 branch dead")],
 "r3/d2-C": [(A,1,"",0,"except returns True"),(A,0,"",0,"charged without order"),(L,0,"",1,"idempotency key"),(L,0,"",1,"broad except types"),(L,0,"",0,"log.warning drops traceback"),(L,0,"",1,"charge timeout / ambiguous charge")],
 "r3/d2-E": [(A,1,"",0,"except returns True"),(A,0,"",0,"charged without order"),(L,0,"",1,"idempotency key"),(L,0,"",0,"log.warning drops traceback")],
 "r3/d3-A": [(A,1,"",0,"conn leak on early return and on exception"),(L,0,"",0,"close right after fetchall"),(L,0,"",1,"stale file when empty"),(L,0,"",0,"no CSV header (pre-existing)"),(L,0,"",0,"fetchall memory"),(L,0,"",1,"month column assumption (+ month unvalidated aside)"),(L,0,"",0,"no ORDER BY"),(L,0,"",0,"write_rows newline (pre-existing)"),(A,0,"",0,"docstring + tests for empty-month path")],
 "r3/d3-B": [(A,1,"",0,"conn leak on early return"),(A,0,"",0,"conn leak on exception"),(L,0,"",0,"close right after fetchall"),(L,0,"",1,"stale file when empty"),(L,0,"",1,"atomic temp-file write"),(L,0,"",0,"no ORDER BY"),(L,0,"",0,"fetchall memory")],
 "r3/d3-C": [(A,1,"",0,"conn leak on early return"),(A,0,"",0,"conn leak on exception"),(L,0,"",0,"fetchall memory"),(L,0,"",1,"stale file when empty"),(L,0,"",1,"atomic temp-file write"),(W,0,"already-handled-elsewhere",0,"out_path traversal (caller builds from fixed dir; security framing)")],
 "r3/d3-E": [(A,1,"",0,"conn leak on early return"),(A,0,"",0,"conn leak on exception"),(L,0,"",0,"fetchall memory")],
 "r3/d4-A": [(A,1,"",0,"off-by-one end"),(W,0,"already-handled-elsewhere",0,"page not validated"),(L,0,"",1,"size<=0 (caller code, outside diff)"),(W,0,"already-handled-elsewhere",0,"page beyond total"),(L,0,"",0,"empty result 0 pages vs page 1"),(L,0,"",0,"needs materialized list"),(A,0,"",0,"boundary tests")],
 "r3/d4-B": [(A,1,"",0,"off-by-one end")],
 "r3/d4-C": [(A,1,"",0,"off-by-one end (framed as data integrity)"),(W,0,"already-handled-elsewhere",0,"page not validated"),(L,0,"",1,"size<=0 (caller code, outside diff)"),(W,0,"already-handled-elsewhere",0,"size upper bound (caller caps at 100)"),(W,0,"already-handled-elsewhere",0,"page beyond total"),(L,0,"",0,"needs materialized list")],
 "r3/d4-E": [(A,1,"",0,"off-by-one end"),(W,0,"already-handled-elsewhere",0,"page not validated"),(L,0,"",1,"size<=0 (caller code, outside diff)")],
 "r3/d5-A": [(A,1,"",0,"non-atomic increment"),(A,0,"",0,"dict changed size during iteration"),(L,0,"",1,"in-memory billing"),(A,0,"",0,"never reset across months"),(L,0,"",0,"no partner id"),(L,0,"",0,"hits counts misses (naming)"),(L,0,"",0,"get_rate stays public / unbilled path"),(L,0,"",0,"dict comprehension -> dict()"),(A,0,"",0,"tests for counting")],
 "r3/d5-B": [(A,1,"",0,"non-atomic increment"),(A,0,"",0,"dict changed size during iteration"),(A,0,"",0,"never reset across months"),(L,0,"",1,"in-memory billing"),(L,0,"",0,"get_rate duplicate fetch (pre-existing)"),(L,0,"",0,"hits counts misses (naming)")],
 "r3/d5-C": [(A,1,"",0,"non-atomic increment"),(L,0,"",0,"get_rate duplicate fetch (pre-existing)"),(L,0,"",1,"in-memory billing"),(A,0,"",0,"never reset across months"),(A,0,"",0,"dict changed size during iteration"),(L,0,"",0,"fetch_rate errors not handled"),(L,0,"",1,"no TTL on rates (data integrity framing)"),(W,0,"already-handled-elsewhere",0,"cur unvalidated"),(L,0,"",0,"no partner id")],
 "r3/d5-E": [(A,1,"",0,"non-atomic increment"),(A,0,"",0,"dict changed size during iteration"),(A,0,"",0,"never reset across months"),(L,0,"",1,"in-memory billing")],
 "r3/d6-A": [(W,0,"already-handled-elsewhere",0,"whitespace-only name"),(L,0,"",0,"n not validated"),(W,0,"already-handled-elsewhere",1,"leading/trailing whitespace kept (route strips)"),(L,0,"",0,"ellipsis when first fits"),(L,0,"",0,"collisions (last initial dropped)"),(L,0,"",0,"last initial not uppercased"),(L,0,"",0,"western name order"),(L,0,"",0,"grapheme clusters / display width"),(L,0,"",0,"byte length / non-ASCII ellipsis"),(L,0,"",0,"magic number n=12"),(L,0,"",0,"docstring + tests")],
 "r3/d6-B": [(L,0,"",0,"ellipsis when first fits"),(L,0,"",0,"n<=0"),(L,0,"",0,"inconsistent normalization (internal spaces)"),(L,0,"",0,"grapheme clusters / display width"),(L,0,"",0,"tests")],
 "r3/d6-C": [(W,0,"already-handled-elsewhere",0,"whitespace-only name"),(L,0,"",0,"n not validated"),(L,0,"",0,"grapheme clusters")],
 "r3/d6-E": [(W,0,"already-handled-elsewhere",0,"whitespace-only name")],
}
rows = []
for key, labs in LAB.items():
    lines = [l for l in (HERE / f"outputs/{key}.txt").read_text().splitlines() if l.startswith("- ")]
    assert len(lines) == len(labs), (key, len(lines), len(labs))
    run, dc = key.split("/") if "/" in key else ("r1", key)
    d, c = dc.split("-")
    cid = f"{dc}-{{}}" if run == "r1" else f"{run}-{dc}-{{}}"
    for i, (cls, hit, tag, amb, why) in enumerate(labs, 1):
        rows.append(dict(run=run, condition=c, diff=d, comment_id=cid.format(i), cls=cls, planted_hit=hit, reason_tag=tag, ambiguous=amb, note=why))
with open(HERE / "e3-classified.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["run","condition","diff","comment_id","cls","planted_hit","reason_tag","ambiguous","note"])
    w.writeheader(); w.writerows(rows)
with open(HERE / "e3-summary.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["condition","comments","acted_on","wrong","right_low_value","pct_acted","pct_wrong","pct_low","planted_hits_of_5","ambiguous"])
    for c in "ABCDE":
        r = [x for x in rows if x["condition"] == c and x["run"] == "r1"]; k = Counter(x["cls"] for x in r); n = len(r)
        hits = len({x["diff"] for x in r if x["planted_hit"]})
        w.writerow([c, n, k[A], k[W], k[L], round(100*k[A]/n), round(100*k[W]/n), round(100*k[L]/n), hits, sum(x["ambiguous"] for x in r)])
print((HERE / "e3-summary.csv").read_text())
for c in "ABCDE":
    print(c, {d: sum(1 for x in rows if x["condition"]==c and x["diff"]==d and x["run"]=="r1") for d in ["d1","d2","d3","d4","d5","d6"]})

# repeats: A, B, C, E x runs r1-r3
RUNS, DIFFS = ("r1", "r2", "r3"), ["d1","d2","d3","d4","d5","d6"]
KEYS = ["comments","acted_on","wrong","right_low_value","pct_acted","pct_wrong","pct_low","planted_hits_of_5","ambiguous","control_d6_comments"]
def stats(r):
    k = Counter(x["cls"] for x in r); n = len(r)
    return dict(comments=n, acted_on=k[A], wrong=k[W], right_low_value=k[L], pct_acted=round(100*k[A]/n), pct_wrong=round(100*k[W]/n),
                pct_low=round(100*k[L]/n), planted_hits_of_5=len({x["diff"] for x in r if x["planted_hit"]}),
                ambiguous=sum(x["ambiguous"] for x in r), control_d6_comments=sum(1 for x in r if x["diff"] == "d6"))
with open(HERE / "e3-summary-runs.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["condition","run"] + KEYS)
    for c in "ABCE":
        per = [stats([x for x in rows if x["condition"] == c and x["run"] == run]) for run in RUNS]
        for run, st in zip(RUNS, per):
            w.writerow([c, run] + [st[k] for k in KEYS])
        w.writerow([c, "mean"] + [round(sum(st[k] for st in per) / 3, 1) for k in KEYS])
        w.writerow([c, "min-max"] + [f"{min(st[k] for st in per)}-{max(st[k] for st in per)}" for k in KEYS])
print((HERE / "e3-summary-runs.csv").read_text())
for c in "ABCE":
    for run in RUNS:
        print(c, run, [sum(1 for x in rows if x["condition"]==c and x["diff"]==d and x["run"]==run) for d in DIFFS])
