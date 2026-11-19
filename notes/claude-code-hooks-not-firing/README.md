# Why doesn't my Claude Code hook fire, or fire and not block?

Research note for the loopnotes.dev article on Claude Code hooks that don't fire. Measured on Linux with the Claude Code CLI: round 1 on 2026-11-18 (headless 2.1.326, interactive 2.1.327, one run per case), round 2 on 2026-11-19 (2.1.328, three runs per case, headless and interactive, plus what `"onFailure": "block"` covers). Model haiku. Each case is a guard that should block `cat .env` against a fake key.

## Conclusions

- Claude Code ran the guarded command whenever the hook did not hand back a "no" in a form it reads: in all 15 mistakes we tested, `cat .env` printed the fake key in every headless run, so a guard that let the command through is broken in one specific place, and the reader's job is to find which one.
- `/hooks` looked wrong (`no hooks yet`) only when the hook was in a file Claude Code doesn't read, the event name was misspelled or the JSON was broken; a lowercase `"bash"` matcher and every script-side mistake were listed exactly like a working hook, so a hook that shows in `/hooks` still needs a first-line log to tell "never called" (matcher spelling) from "called, but its answer didn't block".
- When the script could not start or exited 1, an interactive session showed `PreToolUse:Bash hook failed` under the tool call and then ran the command anyway; the shell error printed below that line (`not found`, `Permission denied`) names the fix.
- `claude -p` did run hooks (the working guard blocked 3/3) but printed none of the interactive warnings for the same broken folders; for a headless or CI run, rely on the hook's own log line or open the folder interactively once.
- Only two answers blocked: `exit 2` from a PreToolUse hook (stderr is the reason) or exit 0 with `hookSpecificOutput.permissionDecision: "deny"`; `exit 1`, a top-level `permissionDecision`, and `exit 2` from a PostToolUse hook all let the command run.
- `"onFailure": "block"` turned the failures Claude Code itself detects (missing script, no execute bit, timeout, `exit 1`) into blocks, but not a lowercase matcher, a script with no shebang or a misplaced `permissionDecision`; no setting proves a guard works, so after any fix ask for `cat .env` against a fake file and look for the block message.

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

- Rechecked 2026-11-19: both pages unchanged on every point above. [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md): 2.1.326 shows hook failures in red instead of grey and makes a hook's `"decision": "block"` hold in more cases (round 2 row C2b); 2.1.328 extends `onFailure` to `mcp_tool` hooks.

## Other people's reports (links only)

Read as reports from one person and one setup, not as facts. Titles checked 2026-11-18.

- [anthropics/claude-code #30143](https://github.com/anthropics/claude-code/issues/30143): PreToolUse/PostToolUse hooks reported not to fire in `-p` mode. Opened 2026-03-02, closed as completed 2026-03-03. A repository collaborator replied that the report's matcher `Bash(*)` is an invalid regular expression and "silently matches nothing", and suggested `"matcher": "Bash"`; the reporter agreed the matcher was wrong and pointed to #20063 for the headless question. Checked 2026-11-19 (issue page via the GitHub API). Our headless control (A0) did fire and block on 2.1.326 and 2.1.328.
- [anthropics/claude-code #49990](https://github.com/anthropics/claude-code/issues/49990): a bare `{type, command}` entry reported to break the whole hooks config silently. Matches A12 headless; interactive showed a `Settings Error`.
- [anthropics/claude-code #80697](https://github.com/anthropics/claude-code/issues/80697): what a hook that fails to launch does. Our runs (B1, B2) failed open.
- [anthropics/claude-code #79480](https://github.com/anthropics/claude-code/issues/79480): project `.claude/settings.json` hooks reported as silently not registered. A9 and A10 (wrong file) look like this.
- dev.to/rulestack (top search result for "claude code hooks not firing", 2026-07): a checklist built from the docs, no own runs. It says PermissionRequest hooks are skipped in `-p`; the current hooks guide says they still run outside dontAsk mode. We did not measure PermissionRequest.

## Search demand

Google autocomplete (English, 2026-11-18) for "claude code hooks not firing" suggested: not working, not running, stop hook not working, notification hook not working. "claude code hook error" suggested PreToolUse, Bash, Stop, PostToolUse, UserPromptSubmit and SessionStart variants, which is why the table records the exact on-screen wording of each case. Rechecked 2026-11-19: "claude code hooks not working" and "claude code hook not blocking" returned the same suggestions; "how to debug claude code hooks" appeared as a new variant with the same intent; "claude code hook failed" suggested the same per-event "hook error" variants plus "stop hook error json validation failed" (not measured here).

Top results for "claude code hooks not firing" on 2026-11-19: a dev.to checklist built from the docs with no own runs, then GitHub issue mirrors ([#15585](https://github.com/anthropics/claude-code/issues/15585), [#20265](https://github.com/anthropics/claude-code/issues/20265), [#55644](https://github.com/anthropics/claude-code/issues/55644), #30143), each one person's report. None of them shows which mistake leaves which trace. The search summary repeated #30143's claim that project hooks don't fire under `-p`; our headless control blocked 3/3 on 2.1.328.

No Naver counts: this is an English developer-tool question, and Korean search data was not used.

## Limits

- Round 1: one run per case; round 2 (2026-11-19, 2.1.328): three runs per case for the rows in the round 2 table. One OS (Linux), the CLI only. VS Code, the desktop app, Windows and plugin hooks were not tested.
- The user-level `~/.claude/settings.json` location was not measured.
- Interactive screens were captured for the cases listed in `screens/` only. The timeout case (B5) was rerun interactively on 2026-11-18 (reader fix r3, below); its full ten-minute default was not waited out, only `"timeout": 2`.
- Headless and interactive runs reported different patch versions (2.1.326 and 2.1.327). Results can change with later versions; the dataset `claude-code-hooks` in this repository keeps the rows per version so they can be re-measured.
- The model's reply text (for example, whether it retried) varies between runs; the log line and whether `FAKE_KEY` appeared in the tool result are the measured values.

## Config shape and timeout default (official, checked 2026-11-18, reader fix r1)

- [Hooks reference](https://code.claude.com/docs/en/hooks): configuration has three levels, hook event → **matcher group** (`{"matcher": ..., "hooks": [...]}`) → hook handlers (`{"type": "command", "command": ...}`). A handler placed straight in the event's array (A12) is the "bare entry" case; the interactive error was `Hook matcher "hooks" must be an array of hook entries`.
- Same page, common handler fields: `timeout` is "Seconds before canceling", set on the handler; defaults 600 for `command`, `http` and `mcp_tool` (30 for `prompt`, 60 for `agent`; lowered to 30 on UserPromptSubmit/PreModelSwitch/PostModelSwitch and 10 on MessageDisplay). B5 used `"timeout": 2` to make the case quick.
- E1 timing: the edit from `"bash"` to `"Bash"` took effect about 24 seconds later in the same session (the article says only that no restart was needed).

## Version check and details moved out of the article (reader fix r2, 2026-11-18)

- [CLI reference](https://code.claude.com/docs/en/cli-reference), checked 2026-11-18: `--version`, `-v` "Output the version number"; `claude update` "Update to latest version". On the test machine `claude --version` printed `2.1.327 (Claude Code)`. The article points readers to these for the `onFailure` 2.1.295+ requirement.
- Full wording under a wrong hook path (B1, interactive screen in `screens/`): `not found`, then `Exit 127, likely a missing program: The check may not have run. See /hooks.` The article keeps only `not found`, which is enough to route the reader.
- Headless control (A0): with `"Bash"` the hook blocked `cat .env` under `claude -p` in a fresh folder that had never been trusted. The article keeps only the conclusion that hooks run under `-p`.
- Log-line equivalents for non-bash hooks (Python `open(...).write`, Node `fs.appendFileSync`) are standard library calls given for readers; only the bash form was run in this test.

## Timeout in an interactive session and other details moved out (reader fix r3, 2026-11-18)

- **B5 interactive** (Claude Code 2.1.327, same folder setup, `"timeout": 2`, script logs then sleeps 5): while the hook ran, the tool call showed `$ cat .env (running PreToolUse hook · 1s)`; after the timeout the command ran and printed `FAKE_KEY=test-not-real` with no `hook failed`, no `hook error` and no other hook text. The first-line log was written (`fired`). Raw stream with ANSI codes stripped: `screens/B5-run.txt`. So a timed-out hook routes the reader to "log written, command ran", not to `hook failed`; headless (B5 above) adds only the informational event "A hook didn't answer in time, so it didn't check this action."
- **Stop ignores the matcher** (A13, cut from the article as off the PreToolUse reader's path): a Stop hook with `"matcher": "Bash"` still ran when Claude stopped, matching the hooks reference (https://code.claude.com/docs/en/hooks, checked 2026-11-18).
- First-screen line removed from the article: "Every guard I broke so it couldn't start or answer in time let `cat .env` print the key." The fact stays in the article's `hook failed` section (wrong path, no execute bit, relative path after `cd`: B1, B2, B4) and the timeout paragraph (B5).

Article: [Claude Code Hooks Not Firing: Which Mistakes Fail Silently](https://loopnotes.dev/claude-code-hooks-not-firing/)

## Round 2: three runs per case and what `onFailure` covers (2026-11-19, Claude Code 2.1.328)

Same method as above, rebuilt as scripts in `harness/` (`cases.py` builds each case folder, `headless.py` runs `claude -p`, `interactive.py` drives a 150x50 pseudo-terminal and renders screens with pyte). Every run under `systemd-run --user --scope -p MemoryMax=2G`. Headless summaries per run: `raw2/<case>-r<n>.txt`; interactive screens: `screens2/<case>-run-r<n>.txt` (startup, answer) and `screens2/<case>-hooks-r1.txt` (`/hooks`, no prompt). Headless and interactive both reported 2.1.328. Headless cost for the 72 runs: about $0.21.

"Log" = the guard's first line was written; "key" = `FAKE_KEY` appeared after the prompt (the guarded `cat .env` ran). Counts are out of 3.

| Case | Mistake | Headless: log / key | Headless text | Interactive: key | Interactive text | `/hooks` (1 run) |
|---|---|---|---|---|---|---|
| A0 | control `"Bash"` | 3 / 0 | `PreToolUse:Bash hook error: […]: blocked: .env read not allowed` | – | – | – |
| A1 | matcher `"bash"` | 0 / 3 | none | 3 | none | listed: `bash · command` |
| A6 | event `"PreToolUSE"` | 0 / 3 | none | 3 | `Settings Warning` 3/3 | (round 1: `no hooks yet`) |
| A7 | event `"pretooluse"` | 0 / 3 | none | – | – | (round 1: `no hooks yet`) |
| A9 | `.claude/hooks.json` | 0 / 3 | none | 3 | none | (round 1: `no hooks yet`) |
| A10 | root `settings.json` | 0 / 3 | none | – | – | (round 1: `no hooks yet`) |
| A11 | trailing comma | 0 / 3 | none | 3 | `Settings Error` `Invalid or malformed JSON (line 10, column 11)` 3/3 | (round 1: `no hooks yet`) |
| A12 | bare entry | 0 / 3 | none | 3 | `Settings Error` 3/3 (wording changed, below) | (round 1: `no hooks yet`) |
| B1 | path typo | 0 / 3 | `hook_no_verdict` "A hook gave no usable answer, so it didn't check this action." | 3 | `PreToolUse:Bash hook failed` / `not found` / `Exit 127 …` 3/3 | listed: `Bash · command` (typo path shown) |
| B2 | no execute bit | 0 / 3 | `hook_no_verdict` (same) | 3 | `hook failed` / `Permission denied` 3/3 | listed |
| B3 | no shebang | 3 / 3 | none | 3 | none | listed |
| B4 | relative path, `cd sub` first | 3 / 3 (second call) | `hook_no_verdict` (same) | **1** | 1/3 `hook failed` / `not found` + key; 2/3 blocked: `1 action not run · permission denied` / `Reason: PreToolUse:Bash hook error: blocked: .env read not allowed` | listed |
| B5 | `"timeout": 2`, sleeps 5 | 3 / 3 | "A hook didn't answer in time, so it didn't check this action." | 3 | none (only the transient `running PreToolUse hook` counter) | listed |
| B6 | B5 + `onFailure` | 3 / 0 | `timed out; blocking because onFailure is "block"` (Claude retried once each run) | – | – | – |
| B7 | B1 + `onFailure` | 0 / 0 | `failed; blocking because onFailure is "block"` | – | – | – |
| C1 | `exit 1` | 3 / 3 | none | 3 | `PreToolUse:Bash hook failed` + the script's stderr 3/3 | listed |
| C2 | top-level `permissionDecision` | 3 / 3 | none | 3 | none | listed |
| C2b | top-level `{"decision":"block","reason":…}`, exit 0 | 3 / 0 | `PreToolUse:Bash hook error: blocked: .env read not allowed` | – | – | – |
| C5 | PostToolUse, exit 2 | 3 / 3 | none | – | – | listed under PostToolUse |
| **O1** | A1 + `onFailure` | 0 / 3 | none | – | – | – |
| **O2** | B3 + `onFailure` | 3 / 3 | none | – | – | – |
| **O3** | C1 + `onFailure` | 3 / 0 | `failed; blocking because onFailure is "block"` + stderr | – | – | – |
| **O4** | C2 + `onFailure` | 3 / 3 | none | – | – | – |
| **O5** | B2 + `onFailure` | 0 / 0 | `failed; blocking because onFailure is "block"` + `Permission denied` | – | – | – |

What round 2 settles:

- Every round 1 result held 3/3 on 2.1.328, headless and interactive, except B4 interactive (below).
- `/hooks` listed every B and C case exactly like a working hook (`Bash · command`), including the misspelled script path. Of the mistakes that let `cat .env` run, `/hooks` looked wrong only for the file location, event name and JSON cases (A6, A7, A9-A12, round 1 screens). It does not tell a working guard from a broken one.
- `onFailure: "block"` turned every mistake Claude Code itself counts as a failure into a block: script missing (B7), no execute bit (O5), timeout (B6), `exit 1` (O3). It did nothing for the three mistakes where nothing failed from Claude Code's side: a matcher that never matched (O1, no log line), a script with no shebang that fell through to `exit 0` (O2), and a deny decision written outside `hookSpecificOutput` with exit 0 (O4). In all three the key printed 3/3 with no message.
- C2b (new): a top-level `"decision": "block"` with a `reason` and exit 0 did block (3/3) on 2.1.328. Only a top-level `permissionDecision` (C2) is ignored. The CHANGELOG for 2.1.326 mentions making `"decision": "block"` hold in more cases.
- B4 interactive split 2/3 blocked, 1/3 failed open. In the two blocked runs the relative hook path still resolved after `cd sub`; in the third it did not (`not found`) and the key printed. Headless failed open 3/3. A relative hook path is therefore not a reliable guard; whether it breaks depends on the session's working directory at that moment.
- A12 interactive wording on 2.1.328: `Hook matcher "hooks" must be an array of hook entries; received undefined — a PreToolUse/PermissionRequest hook that cannot be loaded may be what guards the permissions declared beside it, so nothing it sits in is applied until the entry is fixed or removed.` The Settings Error dialog now offers `1. Fix with Claude / 2. Exit and fix manually / 3. Continue without these settings`; the runs above chose 3.

## What `/status` flags (2026-11-19, Claude Code 2.1.328)

The CHANGELOG for 2.1.327 says `/status` now lists "hook matchers that never match". One interactive `/status` per folder, screens in `screens2/A1-status-r1.txt` and `screens2/A1x-status-r1.txt` (harness mode `status`; session and account lines removed):

- A1, lowercase `"bash"` matcher: the Status tab showed no diagnostics section at all. A lowercase tool name is a valid pattern that matches no tool, and `/status` did not flag it.
- A1x (control), matcher `Bash(*)` as in issue #30143: the Status tab added "System diagnostics" with `PreToolUse hook matcher Bash(*) isn't a valid regular expression`.

So `/status` catches a matcher that isn't a valid regular expression, not one that is valid but names no tool. For the lowercase case the first-line log stays the check.


## Moved out of the article (reader fix r1 on the 2026-11-19 rewrite)

- Scope line from the first paragraph: fifteen mistakes in a `.env` guard, Claude Code 2.1.328 on Linux, three runs each (round 2 table above). The article now says only that each common mistake let `claude -p` print the fake key.
- Issue #30143 ("hooks don't fire under `-p`"): opened 2026-03-02, closed 2026-03-03; the maintainer traced it to `Bash(*)`, a matcher that silently matched nothing (see "Other people's reports" and "What `/status` flags"). The article keeps the conclusion: hooks do run under `-p`, and the working guard blocked there in every run.
- `onFailure` version: the option needs Claude Code 2.1.295 or later (`claude --version`); kept in the article's Sources line only.
- The author's `onFailure` scene in full (author interview): with the option on, the day the guard broke with `exit 1`, `git status` stopped with `PreToolUse:Bash hook error: … failed; blocking because onFailure is "block"` and `No stderr output` under it. Deleting the option line let the same `git status` print the branch at once, while the hook log showed the script still running. The author left the option out because the lowercase matcher the author had tripped on gets past it anyway; deny rules and a narrowly scoped key guard the keys first, and the hook is a layer after those.
- `hook_no_verdict` coverage (round 2 headless rows): emitted for a script that couldn't start (B1 path typo, B2 no execute bit, B4 relative path) and for a timeout (B5, with `"timed_out": true` and the text "A hook didn't answer in time, so it didn't check this action."). `exit 1` (C1), the lowercase matcher (A1), settings-file mistakes (A6-A12), no shebang (B3), top-level `permissionDecision` (C2) and PostToolUse (C5) left no event. The article now says a CI step can grep for it and that `exit 1` and the other rows leave nothing.
- Where `Settings Warning` / `Settings Error` appear (screens2/A6-run-r1.txt, A11-run-r1.txt): a dialog at startup, before the first prompt, with options (Warning: Continue / Fix with Claude / Exit and fix manually; Error: Fix with Claude / Exit and fix manually / Continue without these settings). After Continue the normal prompt screen shows with no trace of the warning.
- `timeout` fix (official, see "Config shape and timeout default"): `timeout` is set in seconds on the handler next to `command`; 600 when omitted for `command` hooks.

## Matcher syntax, the startup dialog and `hook_no_verdict` shape (reader fix r2 on the 2026-11-19 rewrite)

- [Hooks reference](https://code.claude.com/docs/en/hooks), matcher table, checked 2026-11-19: `"*"`, `""` or no matcher matches every occurrence; a matcher made only of letters, digits, `_`, `-`, spaces, `,` and `|` is an exact string or a list of exact strings separated by `|` or `,` (`Edit|Write` and `Edit, Write` each match either tool); any other character makes it an unanchored JavaScript regular expression (`^Notebook`, `mcp__memory__.*`). The article tells the reader to write `"Bash"` and gives `"Bash|Read"` for several tools. Case sensitivity is cited from the hooks guide, as before.
- Startup dialog: `Settings Warning` (A6) and `Settings Error` (A11, A12) appeared in 3/3 interactive runs, each a fresh `claude` start in the same folder (`screens2/A6-run-r*.txt`, `A11-run-r*.txt`). So after Continue the warning is gone for that session and returns on the next start until the file is fixed; the article tells the reader to quit and start `claude` again.
- `hook_no_verdict` event as captured by the harness (`raw2/B1-r1.txt`, re-serialized from `--output-format stream-json --verbose`): `{"type": "system", "subtype": "informational", "content": "A hook gave no usable answer, so it didn't check this action.", "level": "warning", "tag": "hook_no_verdict", "hook_no_verdict": {"hook_event": "PreToolUse", "tool_use_id": "…", "timed_out": false}}`; the timeout case (B5) has `"timed_out": true` and "A hook didn't answer in time, so it didn't check this action." The article gives `grep -q hook_no_verdict` (a plain string, so it does not depend on JSON spacing).
- Moved out of the article: the first-screen line "Each common mistake I tried in a `.env` guard let `claude -p` print the fake key" (the round 2 table holds every row), the B4 run split for the relative path (2/3 held, 1/3 broke interactively), the `timeout` default of 600 seconds (still in Sources), the list of what `onFailure` catches (Image 3 and the O rows above), and the author's line "a hook in `/hooks` means registered to me".

## Minimal guard and where the exit-2 message goes (reader fix r3 on the 2026-11-19 rewrite)

- The article now shows a minimal guard: log line, `jq -r '.tool_input.command // ""'` from stdin, `exit 2` with the reason on stderr when the command contains `.env`, else `exit 0`. Same checks as `harness/cases.py` `GUARD_BODY` (which reads stdin into a variable first); the article's version was run by hand on 2026-11-19: `cat .env` input → stderr `blocked: .env read not allowed`, exit 2; `git status` input → exit 0.
- Hand run without a shebang (2026-11-19, audit-final fix): the same `[[ … ]]` guard run from bash exits 2 (bash interprets a shebang-less file itself), but through `sh` it prints `[[: not found` and exits 0, which is what Claude Code's `/bin/sh` does. So a hand-run exit 2 clears the script only when it starts with `#!/bin/bash`.
- [Hooks reference, exit code output table and "Exit code 2"](https://code.claude.com/docs/en/hooks#exit-code-2), checked 2026-11-19: "The message that comes with the block is your hook's stderr"; plain-text stdout with exit 2 is still a "Blocking error. Your stderr is the reason". So a guard that echoes its message to stdout and exits 2 still blocks, with an empty reason. The article says this in one sentence under the guard.
- Removed from the article: the line describing the Image 1 capture (misspelled guard path, fake key under the warning); the caption says the same.
