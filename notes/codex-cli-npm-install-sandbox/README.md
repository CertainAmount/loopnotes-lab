# Why does npm install fail inside Codex CLI when file edits work?

Research note for the loopnotes.dev article "Codex CLI npm install Fails? It's Sandbox Network Access". It collects what OpenAI's official Codex pages say about the workspace-write sandbox and network access, how those pages changed between two reads, the open macOS report, the earlier timing measurement from the author's original Korean post, and what the top search results cover. Everything below was read on 2026-11-13 unless a row says otherwise. GitHub issues and blog posts are other people's reports, not our experience and not an official diagnosis.

## Conclusions

1. OpenAI's Approvals & security page says the workspace-write sandbox keeps network access off by default, while the Sandbox page that defines the modes does not say so, so a reader whose file edits work but whose `npm install` fails should treat it as the sandbox's network switch before touching npm's registry, proxy or cache settings.
2. The same page documents both fixes: a permanent `network_access = true` under `[sandbox_workspace_write]` in `~/.codex/config.toml`, and, since our previous read on 2026-10-30, a one-run override `codex -c 'features.network_proxy=true' -c 'sandbox_workspace_write.network_access=true'`, so a reader can open the network for one run without editing the config file, or keep it closed and approve the single command under `on-request`.
3. The page also says `approval_policy = "never"` can be combined with any sandbox mode, meaning it stops the questions and leaves the sandbox boundary in place, so a reader should not switch to `never` to get an install through.
4. `approval_policy = "untrusted"` was removed (PR #39630, merged 2026-08-20, from 0.149.0) and can stop Codex from starting, so a reader who pasted it from an old tutorial removes that line; the project setting `trust_level = "untrusted"` is a different, still valid key.
5. The report that macOS's Seatbelt sandbox ignores `network_access = true` (openai/codex #10390) has been open since 2026-02-02 with no maintainer reply and no merged fix as of 2026-11-13, so a Mac reader who set the key and still sees the same failure approves that one command instead of editing the config further.
6. In the author's earlier timing test (same refactor, 5 runs, macOS Apple Silicon, September 2026), workspace-write with on-request took 14-16 minutes with 2-4 approval stops versus 11-13 minutes with none for full access in an isolated environment, so keeping the sandbox on the host costs minutes per task, not hours, and a reader can weigh that against letting a mistake reach outside the workspace.

## 1. Official pages compared

| # | Source | Read | What it says that matters here |
|---|---|---|---|
| 1 | [OpenAI docs: Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security) | 2026-11-13 (page carries no date) | workspace-write has network access off by default; turn it on with `[sandbox_workspace_write]` / `network_access = true`; one-run example `codex -c 'features.network_proxy=true' -c 'sandbox_workspace_write.network_access=true'`; `on-request` asks before edits outside the workspace and before network commands; approval values `on-request`, `never`, `granular`; `never` combines with any sandbox mode; `approval_policy = "untrusted"` is not supported and can block startup; `trust_level = "untrusted"` (project trust) still exists; on launch a version-controlled folder starts in Auto (workspace-write + on-request), otherwise read-only, and an untrusted directory can start read-only; `/permissions`, `--profile`; `--dangerously-bypass-approvals-and-sandbox` (`--yolo`); macOS Seatbelt (`sandbox-exec`); a network proxy with a domain allowlist (`features.network_proxy`, deny wins over allow). |
| 2 | [OpenAI docs: Sandbox](https://learn.chatgpt.com/docs/sandboxing) | 2026-11-13 | Defines read-only, workspace-write and danger-full-access; danger-full-access removes the filesystem and network boundaries; implementation is Seatbelt on macOS, bubblewrap on Linux and WSL2 (a bundled helper if bubblewrap is missing), a native sandbox on Windows. **No sentence about workspace-write's network default.** |
| 3 | [openai/codex releases](https://github.com/openai/codex/releases) | 2026-11-13 | Latest 0.168.0 (2026-11-13), previous 0.167.2 (2026-11-11). The 0.168.0 notes have no network_access, Seatbelt or approval_policy entry. |
| 4 | [openai/codex PR #39630](https://github.com/openai/codex/pull/39630) | 2026-10-30 (past event, not re-read) | Removes `approval_policy = "untrusted"`; merged 2026-08-20; included from 0.149.0. |
| 5 | [npm docs: config](https://docs.npmjs.com/cli/v11/using-npm/config) and [npm docs: logging](https://docs.npmjs.com/cli/v11/using-npm/logging) | 2026-11-13 | Defaults `fetch-retries` 2, `fetch-retry-mintimeout` 10000 (10 s), `fetch-retry-maxtimeout` 60000 (1 min), `fetch-retry-factor` 10; npm retries read requests to the registry on network failures. `loglevel` defaults to `notice`; `http` comes after `notice` in the level order, so http-level lines are not shown by default. With the retry module's timeout = min(10 s x 10^n, 60 s), the two retries wait 10 s and then 60 s, about 70 s before npm gives up. |

What the comparison concludes: a blocked install in the sandbox prints nothing for about 70 seconds at npm's default log level (row 5), which is why it looks hung rather than failed. The reason `npm install` fails (network off by default) is stated only on the Approvals & security page, not on the Sandbox page a reader is likely to open first for "sandbox network access". The key name uses an underscore table name, `sandbox_workspace_write`.

## 2. The same page on two dates

| Item | 2026-10-30 read | 2026-11-13 read |
|---|---|---|
| `-c` example on Approvals & security | only `-c approvals_reviewer=auto_review`; no network example | `codex -c 'features.network_proxy=true' -c 'sandbox_workspace_write.network_access=true'` |
| Network proxy and domain allowlist | not recorded | documented (`features.network_proxy`, allowlist, deny over allow) |
| Latest release | 0.166.0 (2026-10-29) | 0.168.0 (2026-11-13) |
| #10390 status | open | open, no maintainer reply, no merged fix |

What it concludes: a one-run network override is now an official, documented form; older posts that say no network example exists are out of date. The documented example sets the proxy flag together with the network key.

## 3. Open macOS report

| Report | Opened | Status on 2026-11-13 | Claim |
|---|---|---|---|
| [openai/codex #10390: "macOS: network_access = true in config.toml silently ignored by seatbelt sandbox"](https://github.com/openai/codex/issues/10390) | 2026-02-02 | open; no maintainer reply; no merged fix | Setting `network_access = true` has no effect under Seatbelt on macOS. |

This is a user report. We have not reproduced it on a Mac, and the article does not state it as a confirmed bug.

## 4. Earlier measurement (the author's original post)

From the author's Korean original post (2026-09-24), which the article links. Same refactoring task repeated 5 times in a personal/POC repository on macOS Apple Silicon; only the sandbox and approval settings changed.

| Setting | Time per run (range over 5 runs) | Approval stops |
|---|---|---|
| workspace-write + on-request (host) | 14-16 min | 2-4 |
| danger-full-access (isolated environment) | 11-13 min | none |

The stops were mostly at commands that needed the network or files outside the workspace. Times were not taken with precise timestamps; this is five personal runs, not a general speed figure, and the gap depended on how much the task needed outside the sandbox. Time per single approval was not measured.

## 5. What the top results cover

Query: "codex cli npm install fails sandbox network access workspace-write", 2026-11-13.

| # | Result | One-line summary |
|---|---|---|
| 1 | smartscope.blog, "Fix Codex CLI 'Network Access Restricted' in 2 Commands (2026)" | About 280 words; the config key and a one-run override, based on the docs, with no own test (it says so). |
| 2 | codex.danielvaughan.com, "Codex CLI Troubleshooting Field Guide" | A symptom list for several Codex problems. |
| 3 | toolnavs.com, "Codex installation dependencies always fail? First check whether the task allows network" | About 350-400 words (2026-07-31); tells readers to tell DNS, timeout and refusal apart and not to jump to full access. |

None of the three shows an actual npm error line, a test that separates a sandbox block from an npm problem, a cost figure for approving versus opening access, or the macOS report.

Google autocomplete (hl=en, 2026-11-13) for the main stems: "codex npm install" → command, windows, latest, fails, update, mac, cli, 403, version; "codex sandbox network" → access, disabled, disabled=1, internet access, allow network, cli sandbox network access, sandbox workspace write.network access; "codex cli network access" → restricted, internet access, enable, allow, no network access; "codex workspace-write" → not working, never, sandbox_workspace_write, config toml workspace write. Many "codex npm install" completions come from people installing Codex itself with npm, not from installs run inside Codex.

## Limits

- No sandbox test was run on our machine for this version of the note; the error code npm prints inside the sandbox and whether the `-c` override works on its own (without the proxy flag) are not covered here. The planned test: install `@openai/codex@0.168.0` locally on Linux (bubblewrap), run `npm ping` and `npm install is-number` in an empty project under workspace-write with the network off, with the `-c` override alone, with the documented proxy form, and without the sandbox, three times each, recording exit code, npm error line and time to failure, plus a `touch` file-write check.
- The macOS behaviour rests on one open user report (#10390); we have not reproduced it.
- The 5-run timing comes from personal runs on one Mac in September 2026 and is not a benchmark.
- The official pages carry no dates; "read" dates are when we fetched them. Key names and flags in Codex have changed between releases, so check the Approvals & security page against your installed version.
- Codex cloud, Windows, and installs that fail with HTTP 403 are outside this note.

## 6. Reader check additions (2026-11-13)

A cold reader asked how to check the current mode, what the proxy flag in the one-run example does, and how to fix an EACCES global install without sudo. Pages read on 2026-11-13:

| # | Source | What it says that matters here |
|---|---|---|
| 6 | [OpenAI docs: Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security), network proxy part | "The feature changes how enabled network access is enforced; it does not grant network access by itself." Network off + proxy on: network stays off. Network on + proxy off: unrestricted direct outbound access. Network on + proxy on: traffic constrained by the network policy. With `domains` unset the proxy "uses allowlist behavior, so no external destinations are allowed until you add allow rules." Explicit start flags: `codex --sandbox workspace-write --ask-for-approval on-request`. The page does not describe the approval prompt's layout or answer options, and gives no user-facing way to ask for a single-command escalation. |
| 7 | [OpenAI docs: CLI slash commands](https://learn.chatgpt.com/docs/cli/slash-commands/) | `/status`: "Display session configuration and token usage"; review it for the active model, approval policy, writable roots and token usage. `/permissions` switches presets (Auto, Read Only) mid-session. `/approve` only retries an action the automatic reviewer denied, so it is not the route for a sandbox-blocked install. |
| 8 | [npm docs: Resolving EACCES permissions errors when installing packages globally](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally) | Option 1 (recommended): reinstall npm with a Node version manager; the current Node need not be removed first. Option 2 (not Windows): `npm config set prefix ~/.local`, add `PATH=~/.local/bin:$PATH` to `~/.profile` (zsh: also `source ~/.profile` in `~/.zprofile`), `source ~/.profile`, then a global install without sudo. |

What it concludes:

- The official one-run example `codex -c 'features.network_proxy=true' -c 'sandbox_workspace_write.network_access=true'` turns on the proxy with no domain rules, which by the page's own table allows no external destination; for an npm install the network key alone (`-c 'sandbox_workspace_write.network_access=true'`, matching the config.toml block) is the form that gives direct outbound access. We did not run either form on a machine; this follows the page's text. The article now gives the key alone plus `--sandbox workspace-write`, and says why the proxy flag is left out.
- No Codex page documents the approval prompt's options; the article describes it only as the author saw it (the prompt names the command and, in the date-fns task, the reason) and gives the reader a plain instruction to type when Codex does not ask on its own. The author's own instruction wording in September was not recorded, so the article's example line is advice for the reader, not a quote.
- The npm retry count, said precisely: `fetch-retries` 2 means one first try plus two retries, three tries in all, waiting 10 s and then 60 s (about 70 s before npm gives up). The article now says "three times in all ... a little over a minute after the first" so the reader does not have to reconcile attempts with retries.

## 7. Moved out of the article body (reader check, 2026-11-13)

These sentences were in the body and moved here because they proved the method rather than changed a reader's step:

- "OpenAI's Agent approvals & security page is where the default is written down: `workspace-write` keeps network access off. The Sandbox page describes the mode without mentioning the network, which makes it easy to go digging through npm's registry, proxy and cache settings instead." (the body keeps the default and the link)
- "In September I repeated the same refactoring task five times in a personal/POC repository on an Apple Silicon Mac, changing only the sandbox and approval settings" (setup of the 5-run table; section 4 above)
- "I won't turn that into 'full access is 20% faster': the gap depended heavily on how much the task needed outside the sandbox, and this is five personal runs without precise timestamps." (the body keeps one clause: the gap depends on how much the task reaches outside the sandbox)
- npm retry waits "after 10 and then 60 seconds" and the http-level lines "attempt 1, 2 and 3, ending about 70 seconds in" (section 1 row 5; the body says three tries, a little over a minute)
- `approval_policy = "untrusted"` "retired in 0.149.0" (section 1 row 4; the body keeps the PR link)
- Dates of the two scenes: the blocked install in September 2026, the first `npm ci`-first task (dayjs to date-fns) in late October 2026, about six functions into the edits (author interview).

## 8. Reader check 2 additions (2026-11-13)

A second cold reader asked how to confirm the network is on after the `-c` or config.toml route (the docs describe `/status` as showing approval policy and writable roots, not network), and what the approval prompt looks like. The docs pages do not answer either, so we read the Codex TUI source on the main branch (commit `5045589550122ec4f073d10e3d66a0813bcb7be0`, 2026-11-13). The latest release at that time was 0.168.0; labels on main can be ahead of a release.

| # | Source | What it says that matters here |
|---|---|---|
| 9 | [codex-rs/tui/src/status/card.rs](https://github.com/openai/codex/blob/5045589550122ec4f073d10e3d66a0813bcb7be0/codex-rs/tui/src/status/card.rs) | `/status` prints a `Permissions` line. For workspace-write it reads `Workspace (<approval>)` when the network is off and `Workspace with network access (<approval>)` when the permission summary contains "(network access enabled)"; with no built-in profile active it reads `Custom (workspace with network access, <approval>)`. Under `on-request` the approval part is shown as `Ask for approval`. |
| 10 | [codex-rs/tui/src/bottom_pane/approval_overlay.rs](https://github.com/openai/codex/blob/5045589550122ec4f073d10e3d66a0813bcb7be0/codex-rs/tui/src/bottom_pane/approval_overlay.rs) | Command approval answers: `Yes, proceed` (or `Yes, just this once` when the request comes from the network proxy), `Yes, and don't ask again for commands that start with <prefix>` (an exec-policy amendment), `Yes, and don't ask again for this command in this session`, `No, continue without running it`, `No, and tell Codex what to do differently`. Which answers appear depends on the request. |

What it concludes:

- After either network route, the reader checks that the `/status` Permissions line contains `with network access` before retrying the install; if it does and the install still fails, the setting is not what blocks it (on a Mac, #10390), so approving the one command is the next step.
- The one-command approval the author used matches `Yes, proceed`; the `don't ask again` answers widen it to later runs of that command or every command with that prefix, which is the opposite of the author's rule of reading each package name.
- We did not run Codex to see these lines on screen; they come from the source.

Moved or reduced in the body at this check: the npm retry count ("three times in all") and timing ("a little over a minute after the first") are said as "retries without printing anything ... looks hung until the last try gives up" (section 1 row 5 and section 6 keep the numbers); issue and PR numbers moved off the link text into Sources.

Article: [Codex CLI npm install Fails? It's Sandbox Network Access](https://loopnotes.dev/codex-cli-npm-install-sandbox/)
