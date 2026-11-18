#!/usr/bin/env bash
# Repeats (2026-11-19): conditions A, B, C, E, six diffs, runs r2 and r3. Same command and flags as run_e3.sh.
# Run 1 stays in outputs/dN-X.*; repeats go to outputs/rN/dN-X.*. Each run is memory-capped and sequential.
set -u
E="$(cd "$(dirname "$0")" && pwd)"
WORK="${E3_WORKDIR:?set E3_WORKDIR to an empty directory}"
cd "$WORK"
for r in r2 r3; do mkdir -p "$E/outputs/$r"; for d in d1 d2 d3 d4 d5 d6; do for c in A B C E; do
  o="$E/outputs/$r/$d-$c"
  [ -s "$o.json" ] && continue
  systemd-run --user --scope -q -p MemoryMax=2G -p MemorySwapMax=0 \
    timeout 300 claude -p "$(cat "$E/prompts/$d-$c.txt")" --tools "" --setting-sources "" --output-format json </dev/null >"$o.json" 2>/dev/null
  python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['result'])" "$o.json" >"$o.txt"
  echo "$r $d-$c done"
done; done; done
