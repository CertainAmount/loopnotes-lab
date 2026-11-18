#!/usr/bin/env bash
# Run the E3 prompts (A-C 18 runs; D, E 6 each, prompts written by hand per README) headless from an empty directory. Outputs: outputs/dN-X.json (raw) and .txt (result).
set -u
E="$(cd "$(dirname "$0")" && pwd)"
WORK="${E3_WORKDIR:?set E3_WORKDIR to an empty directory}"
cd "$WORK"
for d in d1 d2 d3 d4 d5 d6; do for c in A B C D E; do
  [ -s "$E/outputs/$d-$c.json" ] && continue
  timeout 300 claude -p "$(cat "$E/prompts/$d-$c.txt")" --tools "" --setting-sources "" --output-format json </dev/null >"$E/outputs/$d-$c.json" 2>/dev/null
  python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['result'])" "$E/outputs/$d-$c.json" >"$E/outputs/$d-$c.txt"
  echo "$d-$c done"
done; done
