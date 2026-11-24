# What does one Codex /compact keep, and when should you move to /new instead?

Research note for the loopnotes.dev article on the Codex CLI message "Codex ran out of room in the model's context window" (live URL `/codex-context-window-error/`). The question it answers: once a long Codex CLI chat is full, should you `/compact` or start a new chat with `/new`, and what do you have to put back by hand either way? It collects one measured Codex session (what a `/compact` kept and dropped, and the `/status` readings around two compactions and a `/new`), the official OpenAI pages read on 2026-11-24, a count of Korean blog and cafe posts on the same topic, what the top English results cover, and the background the article leaves out (window-size numbers, issue history, auto-compaction settings). GitHub issues, forum threads and blog posts are other people's reports, not our experience.

## Conclusions

1. In one measured 90-minute Codex CLI session, a single `/compact` kept the goal, all 7 files touched, both off-limits modules and the conclusions of all 7 accepted decisions, but dropped 2 of the 3 approaches the author had already rejected and most exact values, so after a compact the reader re-pastes the rejected approaches with their reasons rather than the whole history.
2. About four turns after that compact, Codex proposed one of the dropped approaches (`@DirtiesContext` on the base test class) as if it were new, so a reader should check a confident post-compact suggestion against their own list of ruled-out approaches before accepting it.
3. The second compact gave back less room than the first (high 60s to low 70s percent left, against 70s to 80s) and lost the failing test names completely, so when the chat fills a second time the reader moves to `/new` instead of compacting again.
4. In the roughly 10 turns between the two compacts, the turns that used the most room were the two where whole failure logs were pasted, so the reader pastes only the failing test name and the line with the cause.
5. `/new` with six carried lines started at about 90 percent left, yet the reason for one rejected approach had to be explained again on the third turn because a `git diff` carries results, not reasons, so every rejected approach and decision the reader carries gets a one-line "why".
6. The official slash-command page documents no argument for `/compact` (the documented way to steer the summary is the `compact_prompt` config key), and none of the top three English results or the 35 Korean posts we read checked what a compact keeps, so the reader should not count on typing instructions after `/compact` or on the page's "keeping critical details" wording.

## 1. The measured session

Codex is not installed on the machine we run our own tests on, so this measurement was made by the author in his own Codex CLI on a real work session, and reported to us step by step on 2026-11-24. It is one session, recorded as ranges and counts rather than tokens.

**Setup**

| Item | Value |
|---|---|
| Codex CLI | 0.167.0 line (latest on npm the same day: 0.172.0) |
| Model | gpt-5.5 |
| Work | Java/Spring multi-module repository, tracing integration tests that broke separately per module |
| Length | about 90 minutes before the first compact; about 2.5 to 3 hours in total |
| Compaction | manual `/compact`, twice; it took tens of seconds and showed no warning text worth quoting |

**Method.** Just before the first `/compact`, everything settled in the session was written down by type. Right after the compact, Codex was told not to read files or run commands and to recite that list from memory. Each item was marked kept, blurred (present but changed or vaguer) or dropped. The same recall was repeated after the second compact. `/status` remaining context was read at five points. The compacted summary itself could not be read in any human-readable form, so the recall question was the only way to see what it held.

**Figure 1 data: after one `/compact`**

| Fact type | Count before | After one /compact | Detail |
|---|---|---|---|
| Goal | 1 | kept | |
| Files touched | 7 | kept | |
| Off-limits modules | 2 | kept | |
| Decisions accepted (4 the author made, 3 Codex proposed) | 7 | kept | conclusions all present; the reason behind 5 of them squashed to one vague line (all 4 of the author's, 1 of Codex's) |
| Failing tests | 2 | blurred | one kept only its class name; the method name was gone |
| Approaches rejected | 3 | dropped | 2 of 3 gone: `@DirtiesContext` on the base test class, and forcing a module order; "put everything in the shared config" survived |
| Exact values (config keys, line numbers, error codes) | about 5 | dropped | most gone; these were values Codex had mentioned while reading logs |

The author expected only values like line numbers to go. The surprise was that the approaches he had turned down went first. The accepted decisions survived whoever proposed them, so the split in this session was accepted versus rejected, not who said it.

**What the dropped approach did.** Around the fourth turn after the first compact, Codex suggested adding `@DirtiesContext` to the base test class to clean up state leaking between tests, presented as a fresh idea. The author turned it down in one line (the context reloads every time, integration tests slow down, and it does not find the source of the leak) and pasted his notepad list of rejected approaches back in. Forcing a module order did not come back. Without the list he might have accepted it.

**After the second compact.** The failing test name that had blurred was now gone entirely, and the author's decisions remained as conclusions with no reason at all.

**Figure 2 data: `/status` remaining context**

| Point | Reported | Label used in the figure |
|---|---|---|
| Just before compact 1 | low 20s % | low 20s |
| Just after compact 1 | 70s to 80s % | 70s–80s |
| About 10 turns later | mid-teens % | mid-teens |
| Just after compact 2 | high 60s to low 70s % | high 60s–low 70s |
| Start of `/new` with six carried lines | about 90 % | ~90% |

The 10 turns between the compacts held two pasted full failure logs, reads of two or three test classes and one service, and three or four reruns of one fix; the log turns used the most room. Token counts were not noted, so the figure shows ranges, not points joined by a line.

**The `/new` handover.** Six lines were carried: the goal in one line, the `git diff` at that point, the confirmed cause, the failing test names, the rejected approaches, and the modules not to touch. No chat history was carried. The first thing that needed explaining again came on the third turn: why putting everything in the shared config had been rejected. After that, a one-line reason went next to every rejected approach and decision. The cause turned out to be two modules pulling the same test configuration class, with the transaction boundary sitting outside the service; splitting the config per module and moving the boundary into the service made the tests pass both per module and as a whole, 40 minutes to an hour after `/new`.

**An earlier session, same pattern.** In an earlier Java/Spring multi-module refactor, the author first took this message for his usage limit, resent the same prompt twice, compacted once, kept re-explaining why an approach had been dropped, and moved to `/new` with the same six items; the remaining modules were done in under two hours and pushed that day. The same error came back twice later, once in a session of pasted Gradle failure logs and once when an investigation spread across configuration classes in several modules. This session was not measured, and the article walks only the measured one.

## 2. Official pages compared (read 2026-11-24)

| # | Source | What it says that matters here |
|---|---|---|
| 1 | [Codex CLI slash commands](https://learn.chatgpt.com/docs/cli/slash-commands) | `/compact` "replaces earlier turns with a concise summary, freeing context while keeping critical details"; no argument documented. `/new` starts a new chat in the same CLI session. `/resume` keeps the original history. `/status` shows "remaining context capacity". Also `/clear`, `/fork`, and `/recap` (a summary without compacting). |
| 2 | [Codex config reference](https://learn.chatgpt.com/docs/config-file/config-reference) | `model_context_window`; `model_auto_compact_token_limit` (unset uses model defaults); `model_auto_compact_token_limit_scope` (`total` by default, or `body_after_prefix`); `model_post_turn_compact_threshold_percent` (0 or omitted = off); `compact_prompt`; `experimental_compact_prompt_file`; provider capability `remote_compaction` (`unsupported` = local, `v2` = through Responses); `PreCompact` and `PostCompact` hook events. |
| 3 | [Developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli) | `codex resume` by ID or the most recent chat; `codex exec resume --last` (current directory) and `--all`; `codex fork` keeps the original transcript. This page no longer describes the slash commands; they moved to row 1. |
| 4 | [openai/codex releases](https://github.com/openai/codex/releases) | Latest stable 0.172.0 (2026-11-24), which omits unknown server versions from `/status` (#62202). 0.171.0 (2026-11-20): "Preserve active additional context across compaction" (#61390) and "Expose context usage in statusline state" (#61409). Codex moved from 0.167.0 to 0.172.0 in 18 days. |

What the comparison concludes: the official wording promises "keeping critical details" without saying which details. In the measured session, the details it did not keep were rejected approaches, exact values and, after a second compact, failing test names. The only documented control over the summary is a config key, not text typed after `/compact`. The measured session ran on the 0.167.0 line, before the 0.171.0 compaction change; that change concerns "active additional context", and whether it affects rejected approaches was not tested.

## 3. Korean posts on the same topic (other people's reports)

Search on Naver, 2026-11-24, relevance order, query "codex compact 컨텍스트": 166 blog results (top 25 read), 10 cafe posts (all read), 0 Q&A results.

| What the 35 posts did | Posts |
|---|---|
| Introduced config keys (`model_context_window`, auto-compact limit) | 6 |
| General "when to use /compact vs /clear or /new" advice | 5 |
| Beginner intros combining Claude Code and Codex | 4 |
| Compared what was left after a compact against what was decided | 0 |

- One measured value: `/compact` took context use from about 70% to 4% ([survdev, 2026-07-20](https://blog.naver.com/survdev/224352110162)).
- One claim that conflicts with the official page: instructions can be attached to `/compact` ([victorious_s, 2026-09-08](https://blog.naver.com/victorious_s/224404534369)); the official slash-command page documents no argument.
- One cafe note: `/compact` shows no completion notice and some detailed conversation can be lost ([gilbutitbook 22633](https://cafe.naver.com/gilbutitbook/22633)).

The full snapshot of titles and links is kept with the article's working files; only the counts above are used.

## 4. What the top English results cover

Query "codex ran out of room in the model's context window", 2026-11-24.

| # | Result | One-line summary |
|---|---|---|
| 1 | [OpenAI Developer Community thread 1384241](https://community.openai.com/t/codex-reports-codex-ran-out-of-room-in-the-models-context-window-start-a-new-thread-or-clear-earlier-history-before-retrying/1384241) | User reports of the message; support asks for version and logs. |
| 2 | [smartscope.blog: Codex context window error](https://smartscope.blog/en/generative-ai/chatgpt/codex-context-window-error/) | Defines the error and lists general fixes. |
| 3 | [getunblocked.com: Codex context window](https://getunblocked.com/blog/codex-context-window/) | Explains the window and window sizes; "compact for the same task, new chat for a new task". |

Also read: [smartscope: Claude Code vs Codex compaction](https://smartscope.blog/en/blog/claude-code-codex-compact-comparison/) (267 words, four H2s, states that no compression or retention rate was measured) and the forum thread [How are people managing context in Codex?](https://community.openai.com/t/how-are-people-managing-context-in-codex/1393098) (one user's 18 readings on 2026-09-13: a new CLI chat starts at 19.3K to 25.5K tokens and a Desktop chat at 28.8K to 30.9K, of 258K; the same user reports that "% left" did not match the token counts). A developersdigest.tech page on this error that ranked in the top three on 2026-11-09 returned 404 on 2026-11-24. None of these checked what a compact keeps against a list of decisions.

## 5. Background the article leaves out

**Window size.** The numbers change by model and version, and the reader can read `/status` instead. [InfoWorld, 2026-07-20](https://www.infoworld.com/article/4198811/openais-codex-context-reduction-for-gpt-5-6-sparks-dissatisfaction-among-developers.html): GPT-5.6 default window cut from 372,000 to 272,000 tokens. A user report ([openai/codex #32806](https://github.com/openai/codex/issues/32806), unconfirmed): gpt-5.6-sol from 353,400 to 258,400. The forum thread above uses 258K.

**Issue history** (status as last read; not re-checked on 2026-11-24 unless noted).
- [#19269](https://github.com/openai/codex/issues/19269): public report carrying the full error message.
- [#29041](https://github.com/openai/codex/issues/29041), [#28937](https://github.com/openai/codex/issues/28937), [#43963](https://github.com/openai/codex/issues/43963): remote compaction failures, including "Error running remote compact task"; #43963 was open on 2026-11-09. The article's step for that error is to update Codex and move to `/new`.
- [#11805](https://github.com/openai/codex/issues/11805): a 90% auto-compaction threshold cap from v0.100.0; the newer `model_auto_compact_token_limit_scope` key changes what the threshold counts.
- [#4363](https://github.com/openai/codex/issues/4363): auto-compaction not running on v0.42.0 (historical).

**Auto-compaction settings.** The keys are listed in section 2, row 2. The author compacts by hand because an automatic compaction at the very end does not let him choose when the summary is made; his switch rule is to keep going at about half left unless the direction has already changed twice, and to move work that pastes logs to a new chat below 20 to 30 percent.

**Research on repeated compaction.** [arXiv 2610.31778, "Benchmarks Are Surprisingly Compaction-Friendly"](https://arxiv.org/pdf/2610.31778) reports that GPT-5.3-Codex accuracy dropped after many compactions while GPT-5.4 did not, so the effect depends on the model.

**Contrast with our Claude Code measurement.** Our [Claude Code `/compact` test](https://loopnotes.dev/claude-code-compact-what-survives/) ([research note](https://github.com/CertainAmount/loopnotes-lab/tree/main/notes/claude-code-compact-what-survives)), on 2026-11-20 with Claude Code 2.1.328 and Sonnet 5.5, planted 12 facts in a synthetic session of about 50K to 78K tokens and compacted it 5 times: drop reasons the user typed survived 5 of 5, and only a line number Claude had found blurred (3 of 5). Here, in a 90-minute real Codex session, 2 of 3 rejected approaches were dropped after one compact. Session size, task and how facts entered differ, so this is not a tool comparison and the article does not make one.

## Limits

- One session, one repository, one model (gpt-5.5) on the Codex CLI 0.167.0 line, with local manual compaction. Later versions (0.171.0 changed what compaction preserves) or remote compaction may behave differently.
- Recall was checked by asking Codex to recite from memory; the summary text itself was not readable, so an item Codex failed to recite might still be in the summary in some form.
- `/status` values are ranges as read and reported, without token counts; the figure shows them as ranges.
- No `/new` recall check was run; for `/new` there is only the starting `/status` reading and the first re-explanation.
- The exact on-screen error text was not saved by the author; the message is quoted from public reports (forum 1384241, #19269).
- Codex app and IDE behaviour, `/fork` and `/clear`, and changed auto-compaction settings were not tested.
- The Korean post count is one search on one day, 35 posts read, used only as a tally.

## Moved from the article (reader fix r1, 2026-11-24)

These details were in the article body and moved here because they prove the measurement but do not change the reader's step.

- Setup: Codex CLI 0.167.0 line, gpt-5.5 (see Limits). The first compact came about 90 minutes into the session.
- Where the summary is: it never appeared on screen, and no readable copy turned up in `~/.codex/sessions`. The official pages document no argument for `/compact`; the one control they describe is the `compact_prompt` config key (section 2, row 2), which was not used.
- Timing: Codex re-proposed `@DirtiesContext` about four turns after the first compact; the first compact carried the session about ten more turns; the tests passed 40 minutes to an hour after the switch to `/new`.
- Between the two compacts: two full integration-test failure logs pasted, two or three test classes and one service read, one fix rerun three or four times. The log turns used the most room.
- The `/new` handover carried the `git diff` itself (pasted in), and `/status` read about 90 percent left with it in (author interview, 2026-11-24). `/status` shows remaining context as a percentage (author interview, 2026-11-09).
- The error message text is quoted from the [OpenAI Developer Community thread](https://community.openai.com/t/codex-reports-codex-ran-out-of-room-in-the-models-context-window-start-a-new-thread-or-clear-earlier-history-before-retrying/1384241) (2026-06-21); the article cites it in Sources only.

## Added in reader fix r2 (2026-11-24)

- Updating Codex CLI (for the "Error running remote compact task" path): the official CLI page ([learn.chatgpt.com/docs/cli](https://learn.chatgpt.com/docs/cli), checked 2026-11-24) gives the same command for install and update, `curl -fsSL https://chatgpt.com/codex/install.sh | sh`. The [openai/codex README](https://github.com/openai/codex) (checked 2026-11-24) gives `npm install -g @openai/codex` for npm installs; the article uses the npm `@latest` form of that line for updating.
- Account usage: the official slash-command page ([learn.chatgpt.com/docs/cli/slash-commands](https://learn.chatgpt.com/docs/cli/slash-commands), checked 2026-11-24) lists `/usage` ("Inspect daily, weekly, or cumulative ChatGPT token activity from inside the TUI"); `/status` shows "remaining context capacity". The article names `/usage` only as the slower check that the second-terminal test replaces.
- The `/new` handover pasted the whole `git diff` (author interview, 2026-11-24); its size was not part of the answers, so the article gives no diff size.

## Added in reader fix r3 (2026-11-24)

- Where `/status` shows the remaining context: in the Codex TUI source ([codex-rs/tui/src/status/card.rs](https://github.com/openai/codex/blob/main/codex-rs/tui/src/status/card.rs), main branch, read 2026-11-24) the `/status` card has a "Context window" line that renders "NN% left"; the input box footer ([codex-rs/tui/src/bottom_pane/footer.rs](https://github.com/openai/codex/blob/main/codex-rs/tui/src/bottom_pane/footer.rs)) shows "NN% context left". The article names the "Context window" line only.
- The `/status` ranges around the two compacts (low 20s → 70s–80s after compact 1, high 60s–low 70s after compact 2) are now said in the article prose as well as in Figure 2; they come from the Figure 2 data table above.

Article: [Codex \"Ran Out of Room in the Model's Context Window\" Fix](https://loopnotes.dev/codex-context-window-error/)
