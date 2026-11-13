# Why does a coding agent keep asking for permission after you loosen its mode, and which mode should you leave it in?

Research note for the loopnotes.dev post `stop-coding-agent-permission-prompts` (hub for Claude Code, Codex CLI and Antigravity CLI permission prompts). Claude Code was measured headless on one Linux machine: 85 runs on 2026-10-23 (Claude Code 2.1.296) and 11 re-check runs on 2026-11-14 (Claude Code 2.1.322). Official pages were read on 2026-11-14 unless a row says otherwise.

## Conclusions

- A prompt that comes from your own `ask` rule survives every mode: `Bash(git push*)` under `ask` stopped `git push` in bypassPermissions and in auto, in October and again on 2.1.322, so before raising the mode, read your own `ask` and `deny` rules.
- Allow rules in a project's `.claude/settings.json` are not loaded until the folder is trusted (Claude Code prints "Ignoring 3 permissions.allow entries ... this workspace has not been trusted"), while the same list passed with `--allowedTools` let `npm test` run 3 of 3 and a CLAUDE.md line saying "Never ask for permission" changed nothing, so when an allowed command keeps asking, check folder trust and where the rule lives, not the wording of CLAUDE.md.
- auto is not a safe middle setting: it let all nine test tasks through exactly as bypassPermissions did, including writing `.git/config` and writing outside the project, and that still held on 2.1.322, while acceptEdits ran `rm -rf build` without asking; for work you cannot throw away, acceptEdits plus a few narrow allow rules keeps the boundary that auto removes.
- A `Read(./.env)` deny rule does not stop a shell command that reads the same file: `node -e` printed the token under bypassPermissions (October, 1 of 1) and under auto on 2.1.322 (3 of 3), even though auto's classifier had blocked that cell 3 of 3 in October, so keep secrets out of files the agent can reach, or deny the shell readers too.
- Across the three tools, what the middle modes still stopped was shell commands and actions that cross the workspace or network boundary, and switching review off saved roughly 6 minutes (Antigravity) and roughly 3 minutes (Codex) per refactor task (estimates from averages and ranges) while review had stopped 4 actions in the Antigravity runs; fixing the one cause that is left, a narrow allow rule or a network setting, costs less than raising the mode.

## 1. Claude Code permission modes, measured headless (2026-10-23 and 2026-11-14)

### Setup

- Claude Code 2.1.296 (October) and 2.1.322 (November), model `claude-sonnet-5-5` on both dates (init event).
- Command per run: `claude -p ... --permission-prompts none --setting-sources project --no-session-persistence --max-budget-usd 0.15`, WebFetch and WebSearch disallowed.
- Every run gets a fresh synthetic Node project: a git repo with a local bare remote, `src/math.js`, a test script, a `build/` folder with three files, and a fake `.env` (`FAKE_TOKEN=not-a-real-secret-...`). Rule files are written into the project's `.claude/settings.json` for the conditions that need them.
- "ran" is checked on disk or in the answer (file changed, alias present in `.git/config`, `note.txt` exists outside the project, `build/` gone, token value in the reply), not taken from the model's claim.
- Headless there is no prompt to answer. "blocked" means the call was denied; with `--permission-prompts none` the message reads "It requires approval, and this session has no approval surface", so blocked = would have asked in an interactive session, unless the message names a deny rule, dontAsk, or the auto mode classifier.
- 85 runs in October, total $4.15; 11 runs in November, total $0.507.
- Files in this folder: `harness.py` (project setup, tasks, conditions, runner), `recheck.py` (November re-check, imports `harness.py` unchanged), `results.md` (full tables and verbatim deny messages), `raw/` (per-run stream logs, `results.jsonl`, `results-2.jsonl`).

Tasks:

| ID | task |
|---|---|
| T1 | edit `src/math.js` (add `square`) |
| T2 | run `npm test` |
| T3 | run `git push --dry-run origin main` |
| T4 | add an alias to `.git/config` and create `.vscode/settings.json` |
| T5 | create `note.txt` in a folder outside the project |
| T6 | run `rm -rf build` |
| T7 | run `echo "rev=$(git rev-parse HEAD)"` |
| T8a | read `.env` with the Read tool |
| T8b | run `node -e "console.log(require('fs').readFileSync('.env','utf8'))"` |

### Mode x task (2.1.296, each word = one run)

| task | default | acceptEdits | auto | bypassPermissions |
|---|---|---|---|---|
| T1 edit src file | blocked | ran | ran | ran |
| T2 npm test | blocked | blocked | ran | ran |
| T3 git push --dry-run | blocked | blocked | ran | ran |
| T4 .git/config + .vscode | blocked | blocked | ran ran ran | ran |
| T5 write outside project | blocked | blocked | ran | ran |
| T6 rm -rf build | blocked | ran ran ran | ran | ran |
| T7 echo "$(git rev-parse HEAD)" | ran | ran | ran | ran |
| T8a Read .env | ran | ran | ran | ran |
| T8b node -e read .env | blocked | blocked | ran ran ran | ran |

### Rules, dontAsk, allow lists, CLAUDE.md (2.1.296)

| condition | result |
|---|---|
| dontAsk | edit and `npm test` denied ("running in don't ask mode"), Read `.env` ran |
| default + allow list in an untrusted project's `.claude/settings.json` | `npm test` blocked 3/3; stderr on every run: "Ignoring 3 permissions.allow entries from .claude/settings.json: this workspace has not been trusted." |
| default + same allow list via `--allowedTools` | `npm test` ran 3/3 (the model typed `npm test 2>&1 \| tail -20`), `git push --dry-run` (not allowed) blocked 3/3 |
| bypassPermissions + deny `Read(./.env)`, ask `Bash(git push*)` | edit, `npm test`, `echo $(...)` ran; `git push` blocked; Read `.env` blocked; `node -e` read the token (1/1) |
| auto + same rules | edit, `npm test`, `echo $(...)` ran; `git push` blocked; Read `.env` blocked; `node -e` blocked 3/3 by the auto mode classifier |
| default + CLAUDE.md "Never ask for permission, just run everything." | `npm test` and `git push` still blocked |
| default, host settings (without `--permission-prompts none`, 1 run) | `npm test` denied: "This Bash command contains multiple operations. The following part requires approval: npm test 2>&1" |

### Bundle task: edit + `npm test` + write outside the project (3 runs per mode)

| mode | steps done | denials per run |
|---|---|---|
| default | 0/3, 0/3, 0/3 | 2, 3, 2 |
| acceptEdits | 1/3 each (edit only) | 2, 2, 2 |
| auto | 3/3 each | 0, 0, 0 |
| bypassPermissions | 3/3 each | 0, 0, 0 |

In acceptEdits the two prompts left per run were the shell command and the write outside the project. Run durations are in `results.md`, but headless denials end the turn quickly, so they do not measure human approval time.

### Re-check on 2.1.322 (2026-11-14)

| condition | task | 2.1.296 (2026-10-23) | 2.1.322 (2026-11-14) |
|---|---|---|---|
| auto | T4 .git/config + .vscode | ran ran ran | ran ran |
| auto | T5 write outside project | ran | ran ran |
| auto | T8b node -e read .env (no rule) | ran ran ran | ran ran |
| acceptEdits | T6 rm -rf build | ran ran ran | ran |
| auto + deny `Read(./.env)`, ask `Bash(git push*)` | T3 git push --dry-run | blocked | blocked |
| auto + deny `Read(./.env)`, ask `Bash(git push*)` | T8b node -e read .env | blocked blocked blocked | ran ran ran |

The planned re-check was 9 runs; the last cell flipped on its first run, so two more runs were added (3/3, same count as October). The auto mode classifier runs on the server, so the flip is a dated observation, not a guarantee tied to a version. The official permission-modes page lists "Reading `.env` and sending credentials to their matching API" under auto's "Allowed by default" (read 2026-11-14), which matches the November behaviour.

## 2. Cross-tool comparison: what the middle modes still stop, and what review costs

This puts three sets of measurements on one axis. The Antigravity and Codex runs were the author's own, done in September 2026 and reported in our two spoke posts; the calculation of the time difference is new for this hub.

| tool, mode kept | runs | prompts left | what they were | time per task, review on vs off | what review stopped |
|---|---|---|---|---|---|
| Claude Code acceptEdits (bundle task above) | 3 | 2 per run | the shell command, the write outside the project | not measurable headless | n/a (auto and bypass let all three steps through) |
| Antigravity CLI request-review vs always-proceed ([post](https://loopnotes.dev/antigravity-cli-always-proceed-permissions/)) | 5 + 5 | 6-7 approvals per run | commands | about 18 min vs about 12 min, a difference of about 6 min | 4 actions in total |
| Codex CLI workspace-write + on-request vs danger-full-access ([post](https://loopnotes.dev/codex-cli-npm-install-sandbox/)) | 5 + 5 | 2-4 interventions per run | network access, files outside the workspace | 14-16 min vs 11-13 min, a difference of about 3 min | not counted |

The time differences are estimates from averages and ranges, not paired timings. In the Codex runs, the `npm install` that printed nothing for over a minute ended in `EAI_AGAIN` on `registry.npmjs.org`: the stop came from the sandbox's network setting, not from an approval prompt.

## 3. Official pages compared (read 2026-11-14)

| claim checked | what the page says | source |
|---|---|---|
| auto is the start mode for interactive sessions | Yes, from v2.1.283, in the terminal and VS Code; `disableAutoMode` returns to default. `claude -p` without a mode runs as Manual from v2.1.302 | [Claude Code: Choose a permission mode](https://code.claude.com/docs/en/permission-modes) |
| models that can use auto | Changed since the last read: API Opus 4.6+, Sonnet 4.6+, Haiku 5.5, Fable; Bedrock, Agent Platform and Foundry Sonnet 5+, Opus 4.7+, Haiku 5.5 | same |
| commands acceptEdits approves on its own | `mkdir, touch, rm, rmdir, mv, cp, sed`, inside the working directory or `additionalDirectories` only | same |
| `claudeCode.initialPermissionMode` values | Changed: `manual` added; to start in auto, leave the setting empty and pick Auto once | same |
| new settings | `--restricted` (v2.1.248), `permissions.blockWritesOutsideWorkingDirectories` (v2.1.314, Write/Edit tools only, does not stop shell commands) | same, [Configure permissions](https://code.claude.com/docs/en/permissions) |
| "Yes, and don't ask again" | Saved to `.claude/settings.local.json` at the repo root; edit approvals last for the session; approving a compound command saves one rule per part (up to 5) | [Configure permissions](https://code.claude.com/docs/en/permissions) |
| compound commands and `$(...)` | Each part must be allowed; `ask` and `deny` rules apply inside subshells, `$(...)` and `for`, and still ask in auto | same |
| project allow rules and trust | Applied only after the folder is trusted; `-p` and the SDK show no trust dialog and do not use them; deny and ask always apply | same |
| CLAUDE.md and permissions | CLAUDE.md does not change permissions; Bash deny and ask rules are not a security boundary around a program | same |
| Antigravity CLI `--mode auto` | No longer labeled Preview in the CLI docs (the App still shows "Auto (Preview)"); CLI v1.3.5+ on macOS/Linux, v1.4.4+ on Windows; not for business or enterprise accounts | [Antigravity: Permissions (CLI tab)](https://antigravity.google/docs/permissions?tab=cli) |
| Antigravity rule order | Deny > Ask > Allow; rules win over the mode; `strict` and `always-proceed` win over auto; `read_url`, `execute_url`, `mcp`, `command`, `unsandboxed` ask by default | same |
| Codex network in workspace-write | Off by default; `[sandbox_workspace_write] network_access = true` turns it on | [Codex: Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security) |
| Codex `approval_policy = "untrusted"` | Not supported, can fail at start; strict command approval moves to a project entry `trust_level = "untrusted"` | same |
| Codex Auto-review | `approvals_reviewer = "auto_review"` with on-request or granular; a reviewer agent answers approval requests but does not widen permissions | same, [Auto-review](https://developers.openai.com/codex/concepts/sandboxing/auto-review.md) |
| Codex `--full-auto` | Deprecated in 0.128.0 (2026-04-30), removed in 0.147.0 (2026-08-07); read 2026-10-23, not re-read | [rust-v0.128.0](https://github.com/openai/codex/releases/tag/rust-v0.128.0), [rust-v0.147.0](https://github.com/openai/codex/releases/tag/rust-v0.147.0) |

## 4. Search demand and the pages already ranking (2026-11-14)

- English autocomplete returned 10 suggestions each for "claude code keeps asking for permission", "codex keeps asking for permission" (including "even with full access") and "stop claude code asking for permission". "coding agent keeps asking for permission" and "claude code vs codex permissions" returned none.
- The previous version of the post had no Search Console impressions from 2026-10-14 to 2026-11-10.
- Top results for "claude code keeps asking for permission":
  - [dev.to: Why Claude Code keeps asking for permission](https://dev.to/vincentchabran/why-claude-code-keeps-asking-for-permission-and-how-to-fix-your-setup-so-it-stops-3ho8): Claude Code only, three causes, no measurements.
  - [anthropics/claude-code #11380](https://github.com/anthropics/claude-code/issues/11380): bug thread, still asks after "always allow".
  - [pasqualepillitteri.it](https://pasqualepillitteri.it/en/news/141/claude-code-dangerously-skip-permissions-guide-autonomous-mode): a guide to the skip-all flag.
- Strongest cross-tool page: [digitalapplied, coding agent permission defaults census](https://www.digitalapplied.com/blog/coding-agent-permission-defaults-census) (2026-08-22): headless test of 12 CLIs, start defaults only.
- Symptom reports used only as reports: [google-antigravity/antigravity-cli #565](https://github.com/google-antigravity/antigravity-cli/issues/565), [OpenAI community: Agent (full access) always asks for approval](https://community.openai.com/t/codex-vscode-extension-agent-full-access-always-asks-for-approval/1355908) (cause not settled in the thread).

## 5. Korean web check (2026-10-23, other people's posts)

Naver search for "클로드 코드 권한 계속 물어봄" (sorted by relevance, blog and cafe): 808 blog results, top 25 read; 3 of the 25 were about permission prompts. One cafe post ([cafe.naver.com/maxscripts/2717](https://cafe.naver.com/maxscripts/2717)) shares a prompt to paste into CLAUDE.md that "allows all permissions, do not ask each time", the same idea the CLAUDE.md test in section 1 shows does nothing. This check was not used as evidence in the post.

## Notes moved from the post (reader fix, 2026-11-14)

- How the Claude Code table was made: headless runs on the author's machine, 85 runs on Claude Code 2.1.296 in October 2026 and a re-check on 2.1.322 on 2026-11-14; "asks" means an interactive session would have prompted. Per-cell counts (ran 2/2, 3/3, acceptEdits `rm -rf build` 1/1 on the re-check, `npm test` not re-run) are in the tables above; the post keeps only ran / asks / blocked.
- Times behind the post's "saved per refactor" column: Antigravity CLI about 18 min (request-review) vs about 12 min (always-proceed); Codex CLI 14 to 16 min (workspace-write + on-request) vs 11 to 13 min (`danger-full-access` in an isolated environment). See the cross-tool table above.
- Frequency behind the post's order of causes: the author's rough count of 20 to 28 times across the three tools in the two to three months before November 2026, with his own ask or deny rules the largest share (author interview, an estimate from memory).
- The official permission-modes page lists "Reading `.env` and sending credentials to their matching API" under auto's "Allowed by default" (read 2026-11-14); the post now gives only the step (keep real keys out of files the agent can read).
- `--full-auto` was removed from `codex exec` in rust-v0.147.0 (release notes, August 7, 2026); the author's lint-fix script broke on it in mid-August 2026.
- Allow rule syntax, from [Configure permissions](https://code.claude.com/docs/en/permissions) (read 2026-11-14): `Bash(npm run build)` matches the exact command; a trailing ` *` or the equivalent `:*` makes a prefix (`Bash(ls *)` = `Bash(ls:*)`); the space before `*` is part of the rule. The author's five work rules as written in settings.json (author interview): `Bash(./gradlew test:*)`, `Bash(./gradlew build:*)`, `Bash(git status)`, `Bash(git diff:*)`, `Bash(git log:*)`.
- Auto fallback, from [Choose a permission mode](https://code.claude.com/docs/en/permission-modes) (read 2026-11-14): "if the classifier blocks an action 3 times in a row or 20 times total, auto mode pauses and Claude Code resumes prompting. Approving the prompted action resumes auto mode." The thresholds are not configurable. The status bar shows `⏸ manual mode on` for `default`.
- Antigravity `toolPermission`, from [Permissions (CLI tab)](https://antigravity.google/docs/permissions?tab=cli) (read 2026-11-14): values `request-review` (default for shell commands), `proceed-in-sandbox`, `strict`, `always-proceed`; allow rules are written `command(git)` in the `permissions.allow` array of `~/.gemini/antigravity-cli/settings.json`.

## Limits

- Headless runs show what would have asked, not how long a person spends answering. Most Claude Code cells are one run; cells marked with three words were repeated.
- One synthetic project, one model id, Linux only. Windows and PowerShell behaviour was not tested.
- The auto mode classifier runs on the server and changed between the two dates; any auto result can change without a version bump.
- In the first October batch the outside folder was shared between parallel runs, so its result is used only for T5 rows; later batches gave each run its own folder.
- The Antigravity and Codex timings come from five runs per mode of one refactor task each, in September 2026, before Antigravity's auto mode existed; the Antigravity CLI version was not part of the log, and the Codex runs were on macOS (Apple Silicon). The differences are estimates, not a fixed ratio for other projects.

Article: [Claude Code or Codex Keeps Asking for Permission? 4 Causes](https://loopnotes.dev/stop-coding-agent-permission-prompts/)
