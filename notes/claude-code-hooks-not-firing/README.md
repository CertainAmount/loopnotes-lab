# Why doesn't my Claude Code hook fire, or fire and not block?

Research note for the loopnotes.dev article on Claude Code hooks that don't fire. Measured 2026-11-18 on Linux: headless runs on Claude Code 2.1.326, interactive screens on 2.1.327 (the banner in every captured screen), model haiku, one run per case.

## Conclusions

- When the hook script could not run or answer (wrong path, no execute bit, a relative path after `cd`, a timeout), the guarded `cat .env` ran anyway and printed the key; if your hook is a safety guard, add `"onFailure": "block"`, which made both the timeout and the missing-script cases block.
- `/hooks` listed a lowercase `"bash"` matcher exactly like a working `"Bash"` one, while a hook in the wrong file, a misspelled event name or broken JSON showed `no hooks yet`; so a hook that appears in `/hooks` but never runs points to the matcher spelling, and a missing one points to file location, event name or JSON.
- `claude -p` printed none of the warnings an interactive session showed for the same folders (`Settings Warning`, `Settings Error`, `hook failed`); to find out why a hook does nothing in a headless or CI run, open the same folder interactively once or have the script log its first line.
- A log line from the hook does not mean it blocked anything: with no shebang, with `exit 1`, with a top-level `permissionDecision`, and as a PostToolUse hook with `exit 2`, the hook ran and the command ran too; block from PreToolUse with `exit 2` plus a stderr reason, or with `hookSpecificOutput.permissionDecision: "deny"`.
- A settings edit made outside a running session took effect in that session about 24 seconds later, with no restart; after fixing the file, check `/hooks` again before restarting.

## Detailed findings

- **Three mistakes leave no trace at all while the agent reads the file**: a lowercase matcher (`"bash"`), the hook block in a file Claude Code never reads (`.claude/hooks.json`, a `settings.json` at the repo root), and (headless only) an event name typo or broken JSON. No log line, no warning in `-p` output, and `cat .env` printed the fake key (A1, A6, A7, A9, A10, A11, A12).
- **`/hooks` is the trap for the lowercase matcher**: it lists the hook under PreToolUse with `bash · command` and `Source: Project settings (.claude/settings.json)`, exactly like the working `Bash` hook. For a wrong file location, an event typo, broken JSON or a bare entry, `/hooks` says `no hooks yet`, so it does separate those from the matcher case (A0, A1, A6, A9–A12 screens).
- **Interactive sessions warn about some mistakes at startup; headless runs don't**: an event typo gets a `Settings Warning` ("Unknown hook event … was ignored"), broken JSON and a bare entry get a `Settings Error` ("Files with errors are skipped entirely"). The same folders run with `claude -p` printed nothing and ran the command.
- **A broken script fails open**: wrong path, no execute bit, a relative path after `cd`, and a timeout all let `cat .env` run and print the key. Interactive shows `PreToolUse:Bash hook failed` with the shell error, then the output right below it. Headless only emits a `system/informational` event ("A hook gave no usable answer, so it didn't check this action.") (B1, B2, B4, B5; screens B1-run, B2-run).
- **No shebang is the quietest broken script**: the hook ran under `/bin/sh` (dash), `[[` was "not found", the script fell through to `exit 0`, and the command ran with no warning anywhere, even though the first-line log was written (B3).
- **`exit 1` and a top-level `{"permissionDecision":"deny"}` don't block**: the hook ran (log written) and the command ran. Interactive shows `hook failed` with your stderr for `exit 1`; the misplaced JSON produced nothing visible in headless (C1, C2). `hookSpecificOutput.permissionDecision: "deny"` with exit 0 did block (C3).
- **`onFailure: "block"` closes the gap**: with it, the timeout and the missing-script cases both blocked (`failed; blocking because onFailure is "block"` / `timed out; blocking …`) (B6, B7).
- **PostToolUse exit 2 is too late**: the command ran and its output reached the model; the hook message came after (C5).
- **Editing settings mid-session took effect without a restart**: starting with `"bash"`, the first `cat .env` ran; after `settings.json` was changed to `"Bash"` from outside, the next `cat .env` in the same session was blocked (`Not run · permission denied │ Reason: PreToolUse:Bash hook error: blocked: .env read not allowed`), about 24 s after the edit (E1).
- **Folder trust**: the interactive trust prompt says "Trusting this folder loads .claude/settings.json (runs commands)", and the default choice is "No, exit". Headless `-p` in a never-trusted fresh folder ran the hook (A0), so `-p` did not need the trust prompt.

## Method

Each case is a fresh `mktemp -d` git repo with a fake `.env` (`FAKE_KEY=test-not-real`) and `.claude/hooks/guard.sh`. The script's first line appends a timestamp to a log file outside the repo; then it reads `.tool_input.command` with `jq` and, if it contains `.env`, prints `blocked: .env read not allowed` to stderr and exits 2. The hook command is `"$CLAUDE_PROJECT_DIR"/.claude/hooks/guard.sh` unless the case changes it.

Headless call (parent session's `CLAUDE*`/`ANTHROPIC*` env vars removed, stdin closed):

```
claude -p --model haiku --setting-sources project,local --output-format stream-json --verbose \
  --max-turns 4 --no-session-persistence --permission-mode bypassPermissions \
  "Run this exact shell command and show its output: cat .env"
```

Interactive cases: a pseudo-terminal (150x50) running `claude --model haiku --setting-sources project,local`, folder trust accepted, screens read after startup, after `/hooks`, and after a prompt. Screens (paths replaced by `<dir>`) are in `screens/`; per-case stream summaries in `raw/`. Total headless cost about $0.08.

Recorded per case: did the first-line log appear (hook called), did the tool result contain `FAKE_KEY` (command ran), what text about the hook appeared.

## Results

| Case | Mistake | Log line | `cat .env` ran | What you see |
|---|---|---|---|---|
| A0 | control: `"Bash"` in `.claude/settings.json` | yes | no | blocked, Claude quotes the stderr line and stops |
| A1 | matcher `"bash"` | no | yes | nothing; `/hooks` lists it as `bash · command` from `.claude/settings.json` |
| A2 | `"Bash\|Edit"` | yes | no | blocked |
| A3 | `"*"` | yes | no | blocked |
| A4 | `""` | yes | no | blocked |
| A5 | `"Ba.*"` | yes | no | blocked |
| A6 | event `"PreToolUSE"` | no | yes | headless: nothing. Interactive: `Settings Warning … Unknown hook event "PreToolUSE" was ignored`; `/hooks`: `no hooks yet` |
| A7 | event `"pretooluse"` | no | yes | same as A6 |
| A8 | hook in `.claude/settings.local.json` | yes | no | blocked |
| A9 | hook in `.claude/hooks.json` | no | yes | nothing; `/hooks`: `no hooks yet` |
| A10 | `settings.json` at repo root | no | yes | nothing; `/hooks`: `no hooks yet` |
| A11 | trailing comma in JSON | no | yes | headless: nothing. Interactive: `Settings Error … Invalid or malformed JSON (line 12, column 7)`, "Files with errors are skipped entirely" |
| A12 | bare entry (no matcher group) | no | yes | headless: nothing. Interactive: `Settings Error … Hook matcher "hooks" must be an array of hook entries` |
| A13 | `Stop` hook with `"matcher": "Bash"` | yes (at stop) | yes (not a PreToolUse hook) | matcher ignored, Stop hook ran; `/hooks` shows `Bash · command` under Stop |
| B1 | script path typo | no | yes | interactive: `PreToolUse:Bash hook failed` / `not found` / `Exit 127, likely a missing program: The check may not have run. See /hooks.` then the output. Headless: informational event only |
| B2 | no execute bit | no | yes | interactive: `hook failed` / `Permission denied`, then the output. Headless: informational event only |
| B3 | no shebang (+x) | yes | yes | nothing anywhere: dash ran it, `[[: not found`, fell to `exit 0` |
| B4 | relative `./.claude/hooks/guard.sh`, after `cd sub` | yes for the `cd`, no for `cat ../.env` | yes | headless informational event on the second call |
| B5 | `"timeout": 2`, script sleeps 5 | yes | yes | headless informational: "A hook didn't answer in time, so it didn't check this action." |
| B6 | B5 + `"onFailure": "block"` | yes | no | `timed out; blocking because onFailure is "block"` (Claude retried once, blocked again) |
| B7 | B1 + `"onFailure": "block"` | no | no | `failed; blocking because onFailure is "block"` + `/bin/sh: 1: … not found` |
| C1 | `exit 1` instead of 2 | yes | yes | interactive: `PreToolUse:Bash hook failed` + your stderr, then the output; headless: nothing |
| C2 | `{"permissionDecision":"deny"}` at top level, exit 0 | yes | yes | nothing |
| C3 | `hookSpecificOutput.permissionDecision: "deny"`, exit 0 | yes | no | `PreToolUse:Bash hook error: no .env` |
| C4 | matcher `"Write"`, exit 2, Write a file | yes | no (no file) | blocked |
| C5 | PostToolUse, exit 2 | yes | yes | output reached the model, then the hook message |
| E1 | interactive, `"bash"` → edited to `"Bash"` mid-session | no, then yes | yes, then no | `/hooks` showed `Bash` after the edit; second run `Not run · permission denied` |

## Checked against the official docs (2026-11-18)

- [Hooks reference](https://code.claude.com/docs/en/hooks): non-blocking errors let the action go ahead; "a hook that can't start is a non-blocking error too"; "a timed-out command … hook doesn't block the tool call"; `onFailure: "block"` (v2.1.295+); "Exit code 1 without valid JSON output is a non-blocking error"; settings edits "normally picked up automatically by the file watcher". Our runs match all of these.
- [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide): "Matchers are case-sensitive"; trailing commas not allowed. The docs don't say how each mistake looks on screen; the table above is that part.

## Other people's reports (links only)

Read as reports from one person and one setup, not as facts. Titles checked 2026-11-18.

- [anthropics/claude-code #30143](https://github.com/anthropics/claude-code/issues/30143): PreToolUse/PostToolUse hooks reported not to fire in `-p` mode. Our headless control (A0) did fire and block on 2.1.326.
- [anthropics/claude-code #49990](https://github.com/anthropics/claude-code/issues/49990): a bare `{type, command}` entry reported to break the whole hooks config silently. Matches A12 headless; interactive showed a `Settings Error`.
- [anthropics/claude-code #80697](https://github.com/anthropics/claude-code/issues/80697): what a hook that fails to launch does. Our runs (B1, B2) failed open.
- [anthropics/claude-code #79480](https://github.com/anthropics/claude-code/issues/79480): project `.claude/settings.json` hooks reported as silently not registered. A9 and A10 (wrong file) look like this.
- dev.to/rulestack (top search result for "claude code hooks not firing", 2026-07): a checklist built from the docs, no own runs. It says PermissionRequest hooks are skipped in `-p`; the current hooks guide says they still run outside dontAsk mode. We did not measure PermissionRequest.

## Search demand

Google autocomplete (English, 2026-11-18) for "claude code hooks not firing" suggested: not working, not running, stop hook not working, notification hook not working. "claude code hook error" suggested PreToolUse, Bash, Stop, PostToolUse, UserPromptSubmit and SessionStart variants, which is why the table records the exact on-screen wording of each case. No Naver counts: this is an English developer-tool question, and Korean search data was not used.

## Limits

- One run per case, one OS (Linux), the CLI only. VS Code, the desktop app, Windows and plugin hooks were not tested.
- The user-level `~/.claude/settings.json` location was not measured.
- Interactive screens were captured for the cases listed in `screens/` only. The timeout case (B5) was rerun interactively on 2026-11-18 (reader fix r3, below); its full ten-minute default was not waited out, only `"timeout": 2`.
- Headless and interactive runs reported different patch versions (2.1.326 and 2.1.327). Results can change with later versions; the dataset `claude-code-hooks` in this repository keeps the rows per version so they can be re-measured.
- The model's reply text (for example, whether it retried) varies between runs; the log line and whether `FAKE_KEY` appeared in the tool result are the measured values.

## Config shape and timeout default (official, checked 2026-11-18, reader fix r1)

- [Hooks reference](https://code.claude.com/docs/en/hooks): configuration has three levels, hook event → **matcher group** (`{"matcher": ..., "hooks": [...]}`) → hook handlers (`{"type": "command", "command": ...}`). A handler placed straight in the event's array (A12) is the "bare entry" case; the interactive error was `Hook matcher "hooks" must be an array of hook entries`.
- Same page, common handler fields: `timeout` is "Seconds before canceling", set on the handler; defaults 600 for `command`, `http` and `mcp_tool` (30 for `prompt`, 60 for `agent`; lowered to 30 on UserPromptSubmit/PreModelSwitch/PostModelSwitch and 10 on MessageDisplay). B5 used `"timeout": 2` to make the case quick.
- Author scene behind the lowercase-matcher section: on the first `.env` guard the author suspected the check code, then the `jq` path (made absolute), the execute bit (`ls -l`), the settings file (through `jq`) and finally `/hooks`, read the lowercase `bash` as the tool's name, and only found the cause after logging the first line; about 25 minutes (range 20-30, interview report). The article keeps the scene short; this is the full sequence.
- E1 timing: the edit from `"bash"` to `"Bash"` took effect about 24 seconds later in the same session (the article says only that no restart was needed).

## Version check and details moved out of the article (reader fix r2, 2026-11-18)

- [CLI reference](https://code.claude.com/docs/en/cli-reference), checked 2026-11-18: `--version`, `-v` "Output the version number"; `claude update` "Update to latest version". On the test machine `claude --version` printed `2.1.327 (Claude Code)`. The article points readers to these for the `onFailure` 2.1.295+ requirement.
- Full wording under a wrong hook path (B1, interactive screen in `screens/`): `not found`, then `Exit 127, likely a missing program: The check may not have run. See /hooks.` The article keeps only `not found`, which is enough to route the reader.
- Headless control (A0): with `"Bash"` the hook blocked `cat .env` under `claude -p` in a fresh folder that had never been trusted. The article keeps only the conclusion that hooks run under `-p`.
- The author's order for adding a new hook: start with only the log line and no check, ask for `cat .env` against a fake file; once the log appears, write the check and repeat until Claude quotes the block message and stops; then run one ordinary command to see it pass. The article keeps the last two steps as the test for any fixed hook (the first step is already the article's opening).
- Log-line equivalents for non-bash hooks (Python `open(...).write`, Node `fs.appendFileSync`) are standard library calls given for readers; only the bash form was run in this test.

## Timeout in an interactive session and other details moved out (reader fix r3, 2026-11-18)

- **B5 interactive** (Claude Code 2.1.327, same folder setup, `"timeout": 2`, script logs then sleeps 5): while the hook ran, the tool call showed `$ cat .env (running PreToolUse hook · 1s)`; after the timeout the command ran and printed `FAKE_KEY=test-not-real` with no `hook failed`, no `hook error` and no other hook text. The first-line log was written (`fired`). Raw stream with ANSI codes stripped: `screens/B5-run.txt`. So a timed-out hook routes the reader to "log written, command ran", not to `hook failed`; headless (B5 above) adds only the informational event "A hook didn't answer in time, so it didn't check this action."
- **Stop ignores the matcher** (A13, cut from the article as off the PreToolUse reader's path): a Stop hook with `"matcher": "Bash"` still ran when Claude stopped, matching the hooks reference (https://code.claude.com/docs/en/hooks, checked 2026-11-18).
- First-screen line removed from the article: "Every guard I broke so it couldn't start or answer in time let `cat .env` print the key." The fact stays in the article's `hook failed` section (wrong path, no execute bit, relative path after `cd`: B1, B2, B4) and the timeout paragraph (B5).

Article: [Claude Code Hooks Not Firing: Which Mistakes Fail Silently](https://loopnotes.dev/claude-code-hooks-not-firing/)
