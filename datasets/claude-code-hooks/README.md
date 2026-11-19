# Claude Code hook failure modes

Which hook mistakes are silent, which warn, and which fail open (the guarded command still runs), per version?

## Latest per item

| Item | Value | Measured | Source |
|---|---|---|---|
| A0 control matcher Bash | fired 3/3; blocked 3/3 outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| A1 matcher bash (lowercase) | not fired 3/3; command ran 3/3; no warning; /hooks lists it outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| A10 location repo-root settings.json | not fired; command ran; no warning; /hooks no hooks yet outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A10 settings.json at repo root | not fired 3/3; ran 3/3 (headless) outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| A11 trailing comma | not fired 3/3; ran 3/3; interactive Settings Error 3/3 outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| A12 bare entry | not fired 3/3; ran 3/3; interactive Settings Error 3/3 outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| A12 bare entry without matcher group | not fired; command ran; interactive Settings Error; headless silent outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A13 Stop hook with matcher Bash | fired at stop; matcher ignored outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A2 matcher Bash|Edit | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A3 matcher * | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A4 matcher empty | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A5 matcher Ba.* | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A6 event PreToolUSE | not fired 3/3; ran 3/3; interactive Settings Warning 3/3 outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| A7 event pretooluse | not fired 3/3; ran 3/3 (headless) outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| A8 location .claude/settings.local.json | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A9 hook in .claude/hooks.json | not fired 3/3; ran 3/3; no warning outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| A9 location .claude/hooks.json | not fired; command ran; no warning; /hooks no hooks yet outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| B1 script path typo | ran 3/3; interactive hook failed 3/3; headless hook_no_verdict; /hooks lists it outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| B2 no execute bit | ran 3/3; interactive hook failed + Permission denied 3/3; /hooks lists it outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| B2 script not executable | not fired; command ran; interactive hook failed Permission denied; headless informational outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| B3 no shebang | fired 3/3; ran 3/3; no message anywhere; /hooks lists it outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| B4 relative path after cd | headless ran 3/3; interactive ran 1/3, blocked 2/3 outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| B5 timeout 2s | fired 3/3; ran 3/3; interactive no message; headless hook_no_verdict timed_out outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| B5 timeout 2s, script sleeps 5s | fired; command ran; headless informational timed out outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| B6 timeout + onFailure block | blocked 3/3 (timed out; blocking) outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| B7 path typo + onFailure block | blocked 3/3 (failed; blocking) outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| C1 exit 1 | fired 3/3; ran 3/3; interactive hook failed + stderr 3/3 outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| C2 top-level permissionDecision | fired 3/3; ran 3/3; no message outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| C2 top-level permissionDecision deny, exit 0 | fired; command ran; silent outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| C2b top-level decision block | fired 3/3; blocked 3/3 outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| C3 hookSpecificOutput deny, exit 0 | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| C4 matcher Write exit 2 | fired; Write blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| C5 PostToolUse exit 2 | fired 3/3; ran 3/3 outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| E1 matcher edited bash to Bash mid-session | picked up without restart; next call blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| O1 lowercase matcher + onFailure block | not fired 3/3; ran 3/3; no message outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| O2 no shebang + onFailure block | fired 3/3; ran 3/3; no message outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| O3 exit 1 + onFailure block | fired 3/3; blocked 3/3 outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| O4 top-level permissionDecision + onFailure block | fired 3/3; ran 3/3; no message outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |
| O5 no execute bit + onFailure block | blocked 3/3 outcome | 2026-11-19 | loopnotes-lab notes/claude-code-hooks-not-firing round 2 (Claude Code 2.1.328, Linux, 3 runs) |

## Method

Fresh mktemp git repo per case with a fake .env and a PreToolUse guard script that logs its first line and exits 2 on .env; headless claude -p (haiku, stream-json, setting-sources project,local, bypassPermissions) plus a pty-driven interactive session for startup warnings and /hooks. One mistake per case, one run per case.

## Files

- `observations.csv`: 51 rows, one per measurement (date, item, value, unit, source)

## Articles that use it

- https://loopnotes.dev/claude-code-hooks-not-firing/
