"""Which GPU memory limit do Macs report by default? Count the `recommendedMaxWorkingSetSize = N MB`
lines that people pasted into public llama.cpp GitHub issues.

Fetch (2026-11-14): gh api -X GET search/issues -f q='repo:ggml-org/llama.cpp recommendedMaxWorkingSetSize'
  -f per_page=100 -f page=1..3  > s1.json s2.json s3.json
Usage: mac_limit_survey.py s1.json s2.json s3.json  -> mac-limit-survey.csv + summary

llama.cpp prints the value / 1e6 in current builds and / 2^20 in older ones, so both are tried.
A value is matched to an installed-memory size only when it is 3/4 or 2/3 of a standard Apple size
within 0.4%; that match is an inference, not the reporter's stated RAM. Values that match neither
(raised limits via iogpu.wired_limit_mb, other macOS versions) stay "unmatched".
"""
import csv, json, os, re, sys, collections

RAM = [8, 16, 18, 24, 32, 36, 48, 64, 96, 128, 192, 256, 512]
items = []
for f in sys.argv[1:]:
    items += json.load(open(f))["items"]
rows, seen = [], set()
for it in items:
    body = it.get("body") or ""
    for m in re.finditer(r"recommendedMaxWorkingSetSize\s*=\s*([\d.]+)\s*MB", body):
        v = float(m.group(1))
        if (it["number"], v) in seen:
            continue
        seen.add((it["number"], v))
        hit = ("", "", "")
        for unit, ub in (("1e6", 1e6), ("MiB", 2 ** 20)):
            gib = v * ub / 2 ** 30
            for r in RAM:
                for name, t in (("3/4", 0.75), ("2/3", 2 / 3)):
                    if abs(gib / r - t) < 0.004:
                        hit = (r, name, unit)
        rows.append({"issue": it["number"], "created": it["created_at"][:10], "value_mb": v,
                     "value_gib_if_1e6": round(v * 1e6 / 2 ** 30, 2), "inferred_ram_gb": hit[0],
                     "ratio": hit[1], "unit": hit[2]})
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mac-limit-survey.csv")
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
c = collections.Counter((r["inferred_ram_gb"], r["ratio"]) for r in rows)
print(len(items), "issues,", len(rows), "distinct (issue, value) lines")
for k in sorted(c, key=lambda k: (k[0] == "", k[0] or 0)):
    print(k, c[k])
