#!/usr/bin/env bash
# Runs every point of E4 in priority order, one claude process at a time,
# stopping when the summed cost passes $2.70.
cd "$(dirname "$0")"
M=haiku
cost() { python3 -c "import csv;print(sum(float(r['total_cost_usd'] or 0) for r in csv.DictReader(open('runs.csv'))))" 2>/dev/null || echo 0; }
go() { # cfg req set n ts rep
  c=$(cost); python3 -c "import sys;sys.exit(0 if float('$c')<2.7 else 1)" || { echo "SKIP budget $*" >> logs/skipped.txt; return; }
  python3 run.py "$@" $M
}
R="R1 R2 R3 R4 R5"
for rep in 1 2 3; do for n in 10 25 50 100; do for r in $R; do go $n-lookalike $r lookalike $n on $rep; done; done; done
for rep in 1 2 3; do for n in 10 100; do for r in $R; do go $n-clean $r clean $n on $rep; done; done; done
for rep in 1 2 3; do for n in 10 100; do for r in $R; do go $n-lookalike $r lookalike $n off $rep; done; done; done
for rep in 1 2 3; do for r in $R; do go fixa-$r $r fixa 100 on $rep; go fixb-$r $r fixb 10 on $rep; done; done
for rep in 1 2 3; do for n in 25 50; do for r in $R; do go $n-clean $r clean $n on $rep; done; done; done
echo DONE total=$(cost)
