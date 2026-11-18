# Claude Code hook failure modes

Which hook mistakes are silent, which warn, and which fail open (the guarded command still runs), per version?

## Latest per item

| Item | Value | Measured | Source |
|---|---|---|---|
| A0 control matcher Bash | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A1 matcher bash (lowercase) | not fired; command ran; no warning; /hooks lists it outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A10 location repo-root settings.json | not fired; command ran; no warning; /hooks no hooks yet outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A11 trailing comma | not fired; command ran; interactive Settings Error; headless silent outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A12 bare entry without matcher group | not fired; command ran; interactive Settings Error; headless silent outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A13 Stop hook with matcher Bash | fired at stop; matcher ignored outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A2 matcher Bash|Edit | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A3 matcher * | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A4 matcher empty | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A5 matcher Ba.* | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A6 event PreToolUSE | not fired; command ran; interactive Settings Warning; headless silent outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A7 event pretooluse | not fired; command ran; interactive Settings Warning; headless silent outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A8 location .claude/settings.local.json | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| A9 location .claude/hooks.json | not fired; command ran; no warning; /hooks no hooks yet outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| B1 script path typo | not fired; command ran; interactive hook failed exit 127; headless informational outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| B2 script not executable | not fired; command ran; interactive hook failed Permission denied; headless informational outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| B3 no shebang | fired under dash; [[ not found; exit 0; command ran; silent outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| B4 relative path after cd | not fired from subdir; command ran; headless informational outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| B5 timeout 2s, script sleeps 5s | fired; command ran; headless informational timed out outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| B6 timeout + onFailure block | fired; blocked (timed out; blocking) outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| B7 path typo + onFailure block | not fired; blocked (failed; blocking) outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| C1 exit 1 | fired; command ran; interactive hook failed with stderr; headless silent outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| C2 top-level permissionDecision deny, exit 0 | fired; command ran; silent outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| C3 hookSpecificOutput deny, exit 0 | fired; blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| C4 matcher Write exit 2 | fired; Write blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| C5 PostToolUse exit 2 | fired; command ran; output reached model outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |
| E1 matcher edited bash to Bash mid-session | picked up without restart; next call blocked outcome | 2026-11-18 | loopnotes-lab notes/claude-code-hooks-not-firing (Claude Code 2.1.326, Linux) |

## Method

Fresh mktemp git repo per case with a fake .env and a PreToolUse guard script that logs its first line and exits 2 on .env; headless claude -p (haiku, stream-json, setting-sources project,local, bypassPermissions) plus a pty-driven interactive session for startup warnings and /hooks. One mistake per case, one run per case.

## Files

- `observations.csv`: 27 rows, one per measurement (date, item, value, unit, source)

## Articles that use it

- https://loopnotes.dev/claude-code-hooks-not-firing/
