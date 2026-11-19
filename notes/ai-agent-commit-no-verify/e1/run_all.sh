#!/bin/bash
cd /tmp/e1
for C in none claudemd guard deny; do for N in 1 2 3 4 5; do
  [ "$C-$N" = none-1 ] && continue
  ./run_one.sh $C $N
  tot=$(cat logs/*.jsonl | grep '"type":"result"' | python3 -c "import sys,json;print(sum(json.loads(l).get('total_cost_usd',0) for l in sys.stdin))")
  echo "$C-$N total=$tot"
  python3 -c "import sys; sys.exit(0 if float('$tot')<1.8 else 1)" || { echo STOP; exit 1; }
done; done
