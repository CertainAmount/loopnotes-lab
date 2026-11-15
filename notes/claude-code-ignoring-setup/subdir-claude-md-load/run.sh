#!/bin/bash
# usage: run.sh <label> <prompt>
S=$(cd "$(dirname "$0")/.." && pwd)
W=$(mktemp -d "$S/w.XXXXXX"); cd "$W"
git init -q . && mkdir -p src/main src/test
printf 'Small demo project. Code in src/main, tests in src/test.\n' > CLAUDE.md
printf 'Rule for this folder: the first line of every file created in src/test must be exactly: // TESTRULE-OK\n' > src/test/CLAUDE.md
printf 'export const sample = [1, 2];\n' > src/test/helpers.js
printf 'export function add(a,b){return a+b}\n' > src/main/add.js
git add -A && git -c user.email=t@t -c user.name=t commit -qm base
env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT claude -p "$2" --model haiku --output-format stream-json --verbose --max-turns 6 --no-session-persistence --setting-sources project --permission-mode acceptEdits --allowedTools "Read Write Edit Glob Grep" > "$S/$1.stream.jsonl" 2>"$S/$1.err"
for f in src/test/*; do [ "$f" = src/test/CLAUDE.md ] && continue; echo "$1 $f first-line: $(head -1 "$f")"; done
grep -o 'TESTRULE-OK[^"]\{0,0\}' "$S/$1.stream.jsonl" | wc -l | sed "s/^/$1 TESTRULE mentions in stream: /"
