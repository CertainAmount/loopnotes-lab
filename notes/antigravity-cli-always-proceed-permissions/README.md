# Why does Antigravity CLI keep asking for permission in Always Proceed, and is it worth leaving on?

Research note for the loopnotes.dev post `antigravity-cli-always-proceed-permissions`. Official Antigravity pages and the CLI release notes were read on 2026-11-22 unless a row says otherwise. The run comparison was done by the author in September 2026 on his own machine; Antigravity CLI (`agy`) is not installed on the machine that compiled this note, so nothing here was re-run for this round.

## Conclusions

- The CLI docs say explicit rules always take precedence over modes and that modes apply only to operations no rule covers (order Deny > Ask > Allow), so a prompt under Always Proceed points to an `ask` line in `~/.gemini/antigravity-cli/settings.json` (the docs' own sample puts `command(*)` under `ask`); open that file before restarting, reinstalling or installing an auto-click extension.
- Rules match word by word as a prefix, so `command(git)` also covers `git push`, and allowing `git diff` also allows `git diff --output=<file>`, which writes a file (checked on git 2.34.1); allow subcommands one by one and put the few you never want run, such as push, under `deny`.
- Since v1.5.7 (2026-11-12) the CLI starts in `auto` wherever auto is available, and `strict` and `always-proceed` override auto, so on a fresh install the prompt may be auto's sandbox-escape review rather than a broken Always Proceed; check the mode in `/config` before changing rules.
- In 5 runs per mode of the same refactor, Always Proceed cut the average from about 18 to about 12 minutes (about 30%) and removed 6-7 approvals per run, but `request-review` had stopped 4 commands or changes the author had not approved; turn it on only in an environment you can throw away.
- None of the top English results (forum threads, GitHub #565) and none of the 25 Korean Naver posts reviewed report a timed comparison or name rule precedence as the cause; their fixes are restart, reinstall or third-party auto-approval, which do not touch an `ask` rule.

## 1. Official pages compared (read 2026-11-22)

| Page | What it says that this note relies on |
|---|---|
| [Antigravity Permissions, CLI tab](https://antigravity.google/docs/permissions?tab=cli) | "Deny > Ask > Allow"; "Fine-grained rules always take precedence over modes. Modes and toolPermission apply only to operations not covered by an explicit rule"; `always-proceed` = `--dangerously-skip-permissions` (no `--yolo` flag); `strict` and `always-proceed` take priority over auto; auto needs v1.3.5+ on macOS/Linux or v1.4.4+ on Windows, a sandbox, and a non-business/enterprise account, otherwise the CLI uses `default` (`request-review`); word-by-word prefix matching, `regex:` rules, exact matching on Windows; the sample settings put `command(*)` under `ask`; settings path `~/.gemini/antigravity-cli/settings.json` |
| [Antigravity Permissions, App tab](https://antigravity.google/docs/permissions) | the desktop app and IDE use a separate Permission Settings screen; "Auto (Preview)" applies to v2.29.0 and below |
| [Antigravity CLI releases](https://github.com/google-antigravity/antigravity-cli/releases) | entries below (the page shows no year; footer 2026) |
| [Google Codelabs: Antigravity CLI hands-on](https://codelabs.developers.google.com/antigravity-cli-hands-on) | the skip flag "will auto approve all tool permissions"; Artifact Review is a separate `/config` item (read 2026-11-10, not re-read this round) |

Permission-related release entries, 2026-11-10 to 2026-11-21:

| Version | Date | Change |
|---|---|---|
| 1.5.6 | before 11-12 | auto allowed for pay-as-you-go ADC accounts; not for Gemini Enterprise |
| 1.5.7 | 2026-11-12 | default Agent Mode changes from Default to Auto, headless `-p` included; `strict` now also overrides accept-edits |
| 1.5.8 | 2026-11-13 | fixes Windows bypass of always-allow rules (cmd and PowerShell exact match); fixes `mcp(...)` deny/ask rules being ignored for early-loaded MCP tools |
| 1.5.10 | 2026-11-17 | fixes the "always allow" option being selectable when an ask rule or hook requires confirmation every time (Remote Control screen) |
| 1.5.14 | 2026-11-21 | latest at reading; in auto, reads outside the workspace no longer need approval (writes still ask); ask and deny rules still apply |

## 2. Run comparison: request-review vs always-proceed (author's machine, September 2026)

Setup: one mid-sized refactor (explored about 20 files, changed 6-8 files, ran tests and lint, same scope in both modes), in a separate Git worktree of a personal repository with a Docker container for tests. Production credentials, the home directory and SSH keys were blocked, and `read_file`/`write_file` were not opened beyond the workspace. Published in the author's original Korean post on 2026-09-16.

| | `request-review` | `always-proceed` |
|---|---|---|
| Runs | 5 | 5 |
| Human approvals per run (average) | 6-7 | 0 (proceeds automatically) |
| Time to finish (average) | about 18 min | about 12 min |
| Commands or changes stopped at approval | 4 in total | 0 (would have run unattended) |

Calculation: 18 - 12 = about 6 minutes per run; 6 / 18 = about 33%, reported as about 30% because both times are rounded averages.

## 3. Prefix matching and `git diff --output`

- Word-by-word prefix matching (CLI tab): a rule `command(git)` matches every command whose words start with `git`, including `git push`; `command(git diff)` matches `git diff --output=out.patch`.
- `git diff --output=<file>` writes the diff to that file instead of stdout; reproduced on git 2.34.1. An allowed read-only-looking command can therefore write to the workspace.

## 4. What the top results say (query "why does antigravity keep asking for permission", 2026-11-22)

- [Forum 173114, "Antigravity always asks for permission"](https://discuss.ai.google.dev/t/antigravity-always-asks-for-permission/173114) — IDE/app users after v2.2.1 (from 2026-06-30); staff could not reproduce; screen auto-click workaround; unresolved (about 400 words, 8 posts, last 10-15).
- [Forum 118636, "still ask permission even command is already on allowed list"](https://discuss.ai.google.dev/t/bug-antigravity-still-ask-permission-even-command-is-already-on-allowed-list/118636) — multi-page bug thread; one user fixed by restarting; third-party auto-approve extension suggested.
- [GitHub #565](https://github.com/google-antigravity/antigravity-cli/issues/565) — CLI on Windows 11, always-proceed + trusted workspace + allow list still shows "Run command?"; opened 2026-07-08, closed 2026-07-14 with no fix recorded (search snippet, 2026-11-22).
- [Forum 188925, "Auto (preview) approval mode is highly ineffective"](https://discuss.ai.google.dev/t/auto-preview-approval-mode-is-highly-ineffective/188925) — one reply quotes rules sitting above presets and describes auto's sandbox-escape review (snippet only).
- Other related threads seen: [135514](https://discuss.ai.google.dev/t/135514), [127416](https://discuss.ai.google.dev/t/127416), [127846](https://discuss.ai.google.dev/t/127846), [120290](https://discuss.ai.google.dev/t/120290), [171183](https://discuss.ai.google.dev/t/171183).

Reports kept out of the article because they answer a different question (what leaks, not why it asks):

- [GitHub #36](https://github.com/google-antigravity/antigravity-cli/issues/36) — report that the skip flag also approves sandbox escape (open on 2026-11-10).
- [Forum 174516](https://discuss.ai.google.dev/t/antigravity-cli-workspace-permission-vs-env-permission/174516) — agent read `.env` without asking.
- [OWASP LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/), [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — general background.

## 5. Naver search counts (Korean web, other people's reports; searched 2026-11-10, sort by relevance)

| Search term | Types | Results |
|---|---|---|
| 안티그래비티 CLI 권한 승인 ("Antigravity CLI permission approval") | blog, cafe, kin, news | blog 103, cafe 4, kin 0, news 6 |
| agy always proceed 계속 물어봄 ("agy always proceed keeps asking") | blog, cafe, kin | blog 2, cafe 0, kin 0 |

Of the top 25 blog posts for the first term: 4 are auto-approval setup guides, 2 explain allow/ask/deny, 0 measure time or approval counts or test a block. The 2 blog results for the second term are general Antigravity introductions; none is about Always Proceed still asking.

Top 25 blog posts, first term (date, link):

- 2026-09-16 [최적 셋팅 바이블](https://blog.naver.com/wetshaver/224413454520)
- 2026-11-07 [처음 5분 세팅과 장점 4가지](https://blog.naver.com/snsbox2023/224468357584)
- 2026-10-15 [코딩 에이전트 5곳 비교](https://blog.naver.com/ksj0073/224442206156)
- 2026-09-08 [안티그래비티 소개](https://blog.naver.com/jenni-jenni/224404795194)
- 2026-10-19 [윈도우 앱부터 무료로 시작](https://blog.naver.com/hag2s/224445469683)
- 2026-09-08 [자동 승인 3단계 셋업](https://blog.naver.com/ainote_/224405071919)
- 2026-11-02 [플러그인 마켓플레이스](https://blog.naver.com/captainai/224462680569)
- 2026-08-15 [Antigravity IDE에서 Codex CLI](https://blog.naver.com/pkre500514/224379022651)
- 2026-11-06 [기본기 가이드](https://blog.naver.com/slowlymature/224466842522)
- 2026-06-24 [2.0 입문 4편: 코드를 보호하는 법](https://blog.naver.com/totorowo/224325484378)
- 2026-10-19 [맥북 설치 및 초기 설정](https://blog.naver.com/explojh/224446693849)
- 2026-11-06 [원격 AI, PC를 꺼도 일할까](https://blog.naver.com/wekinu/224467419419)
- 2026-09-23 [코드를 직접 짜고 검증하는 에이전트](https://blog.naver.com/goldenplanet/224420739028)
- 2026-08-24 [승인창 없애기](https://blog.naver.com/chukbok_papa/224388825668)
- 2026-10-06 [/config의 Tool Permission 옵션](https://blog.naver.com/aimldl/224432996312)
- 2026-09-01 [고객관리 앱 만들기](https://blog.naver.com/parkjuim90/224396824133)
- 2026-08-06 [자주 사용하는 명령들](https://blog.naver.com/dioyong/224369889480)
- 2026-09-17 [2.0 완벽 가이드](https://blog.naver.com/bpgun/224414704681)
- 2026-07-26 [2.0 설치 방법, 화면 바뀐 이유](https://blog.naver.com/backeclub/224358171412)
- 2026-06-30 [Gemini CLI에서 안티그래비티로 이사](https://blog.naver.com/clarkesquare/224331432784)
- 2026-11-06 [실전 가이드: 에이전트 워크플로](https://blog.naver.com/slowlymature/224467615786)
- 2026-11-02 [T3 Code 사용법](https://blog.naver.com/noppaku/224462164324)
- 2026-08-27 [좋은 AI 에이전트 Antigravity IDE](https://blog.naver.com/minerva3/224392314249)
- 2026-11-07 [음성 모드로 승인](https://blog.naver.com/p-cher/224468314955)
- 2026-09-15 [Gemini CLI 설치 및 API 키 설정](https://blog.naver.com/code_comma/224410185905)

## 6. Details moved out of the post (reader check, 2026-11-22)

- `/config` (Google Codelabs, [Antigravity CLI hands-on](https://codelabs.developers.google.com/antigravity-cli-hands-on), read 2026-11-22): the settings screen lists Color Scheme, Tool permission, telemetry and more, plus Agent Mode and Artifact Review as separate items; Tool Permission offers `request-review`, `proceed-in-sandbox`, `always-proceed` and `strict`, with the current value marked "(current)"; all settings are stored in `~/.gemini/antigravity-cli/settings.json`. The skip flag "will auto approve all tool permissions" and "There will be no prompt asking you for permissions."
- Permissions CLI tab (read 2026-11-22): "`strict` and `always-proceed` (`--dangerously-skip-permissions`) take precedence over `auto` mode"; to go back to request-review, "select `default` in `/config`, or set `agentMode` to `""`". The page's sample narrows npm with `command(regex:npm run (build|lint|test))` under `allow` while its `ask` list holds `command(*)`.
- App and IDE: permissions live under Settings > General > Global Permissions as presets, and the same rule order applies (rules sit on top of the preset; [App tab](https://antigravity.google/docs/permissions)). Not on a CLI reader's path.
- GitHub #565 detail: Windows 11, allow-listed commands still prompting under `always-proceed`, closed by its reporter without a documented fix.
- Run setup detail (§2): each run explored about 20 files and changed 6-8.
- The author's personal rule file: about ten `allow` lines, five `ask` and four `deny`.
- Version context for scenes: the blocked `git push origin` happened around 2026-11-10 on a build near 1.5.0; auto became the default in 1.5.7 (2026-11-12); the "always allow" suggestion change shipped in 1.5.14 (2026-11-21).

## 7. Details moved out of the post (reader check r2, 2026-11-22)

- Where the 6 minutes went: by the author's estimate about 3 of the 6 minutes per run were time spent answering approval prompts; the rest came from the agent replanning after a declined change and from run-to-run spread (one always-proceed run spent about 20 minutes heading the wrong way). Estimate, not a measurement (interview answer, constructed).
- Narrow always-proceed jobs (clearing lint warnings, moving tests) in a throwaway worktree take the author about 12 minutes.
- Misdiagnosis detail: before finding the `ask` line, the author also toggled the sandbox off and on; the prompt stayed.
- Docs wording behind the rule order (Permissions, CLI tab, read 2026-11-22): "Your fine-grained `allow`, `ask`, and `deny` rules always take precedence"; order Deny > Ask > Allow.
- `regex:` syntax (Permissions, CLI tab, read 2026-11-22): examples `command(regex:npm run (build|lint|test))` and `command(regex:git .*)`; the App docs say each whitespace-separated token is evaluated as an anchored regular expression.
- Auto availability (Permissions, CLI tab, read 2026-11-22): v1.3.5+ on macOS and Linux, v1.4.4+ on Windows, terminal sandbox available, not business or enterprise accounts. Mode values: Agent Mode `auto`, `accept-edits`, `""` (default); Tool Permission `request-review` (default, asks before commands run), `proceed-in-sandbox`, `strict`, `always-proceed` (= `--dangerously-skip-permissions`); `strict` and `always-proceed` override auto.
- The "Run command?" card (author's interview answer, 2026-11-22): it shows the full command with every argument; choices are allow once, allow for this session, always allow and deny (y approves, n declines), plus a run-outside-the-sandbox-once option when the sandbox is on; it does not show which `ask` rule or mode raised it. The docs say only that "an interactive prompt card appears in your TUI" and that scope editing isn't supported for terminal commands.
- Version check: the author reads his version with `agy --version` (1.5.7 after the mid-November update). The Permissions page itself names no version command.

## 8. Details moved out of the post (reader check r3, 2026-11-22)

- Run setup in full (§2): the same refactor 10 times, 5 in each mode, in a separate Git worktree of a personal repository with a Docker container for tests; production credentials, the home directory and SSH keys were out of reach; every run ended with tests and lint.
- One of the 4 stopped actions (author's interview answer, 2026-11-22): a proposed change that also edited test fixtures and config files; the author declined it and told the agent to fix it inside the service code only, and that run took longer because the agent replanned. The other three are counted, not named.
- Mode axes (Permissions, CLI tab, and the Codelabs `/config` screen, read 2026-11-22): Agent Mode (`auto`, `accept-edits`, default) and Tool Permission (`request-review` default, `proceed-in-sandbox`, `strict`, `always-proceed`) are separate items in `/config`, each with the current value marked. From 1.5.7 the default Agent Mode is `auto` where auto is available; auto reviews commands that would run outside the terminal sandbox. Saving Tool Permission as `strict` or `always-proceed` overrides auto.
- "Always allow" scope change: shipped in 1.5.14 (2026-11-21); the post says "newer releases" and links the release notes.
- The author's rule file is short; each line is one he can explain in a sentence.

## Limits

- The run comparison is one environment, one task, 5 runs per mode, rounded averages; the CLI version was not logged, and it predates auto mode, so it compares `request-review` with `always-proceed` only.
- Of the 4 stopped actions, one is described from the author's interview (§8); the other three are counted, not matched to specific commands.
- Nothing was re-run for this round: `agy` is not installed on the machine that compiled this note.
- GitHub #565 is a single Windows 11 report; the 1.5.10 note describes the Remote Control screen.
- The release page carries no year; the codelab and GitHub #36 were last read on 2026-11-10; the Naver counts are from 2026-11-10.

Article: [Antigravity CLI Always Proceed Still Asks? 5-Run Test](https://loopnotes.dev/antigravity-cli-always-proceed-permissions/)
