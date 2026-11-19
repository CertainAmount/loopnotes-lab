# What survives Claude Code /compact, and what gets lost?

Research note for the loopnotes.dev article on what Claude Code keeps after `/compact`. The question: after a manual, auto or idle compaction, which parts of a session come back from disk, which depend on the written summary, and what should you say again before or after compacting?

Evidence: one measurement on this machine (2026-10-21, Claude Code 2.1.296, Sonnet 5.5, 1M context window, headless), a check of the summaries that run produced, and a comparison with the official Claude Code docs and the top search results (read 2026-11-20).

## Conclusions

- Everything typed into the chat survived: in 10 of 10 compactions (5 plain `/compact`, 4 with a preservation instruction, 1 auto-compact) the chat-only rule, the decision with its reason, the failed approach with its exact error code, the frozen directory with its date and the next step all came back in replies made with every tool blocked. A reader whose rules "vanished" after compaction should look past the rules they typed before moving them anywhere.
- The reason is visible in the summary itself: all 10 summaries had the same nine numbered sections, and section 6, "All user messages", quoted the first user message word for word. What the user typed is copied; anything else is there only if the summarizer chose to write it down.
- A subfolder rule (`billing/CLAUDE.md`) was never reloaded from disk after compaction (0 of 10 post-compact transcripts); it survived only because the summary copied it. The SessionStart `compact` hook output came back in 10 of 10. A rule that must survive belongs in the root CLAUDE.md or a SessionStart `compact` hook, not in a nested CLAUDE.md.
- The five files attached after compaction were the docs read last (path only, "too large to include"), and none of the 7 edited files came back in any form, although the official page says files are re-read "most recently modified first". After a compaction, give Claude the edited paths yourself (for example `git diff --stat`).
- A preservation instruction made no measurable difference here (B matched A on every clue), because this was the easy case: every clue sat in one early message. Whether it helps when facts are spread over many turns or only appear in tool output is not measured yet.

## Evidence 1: survival measurement, round 1 (2026-10-21)

**Setup.** `make_project.py` builds a synthetic Python ledger service (`ledger-svc`) with a root `CLAUDE.md` rule (marker ROOTOK), a subfolder `billing/CLAUDE.md` rule (marker HERON), a SessionStart hook with matcher `compact` that prints a marker (OWL-HOOK), large `docs/*.md` files (about 5K tokens each) and a frozen `legacy/` folder. `harness.py` runs one seed session per repetition with real reads and edits:

- Turn 1 (one user message) plants every clue: a chat-only rule ("start every reply with `KIWI:`"), the decision ROUND_HALF_EVEN with reason SPEC-7731, the constraint "do not modify legacy/, frozen until 2026-11-30", a migration script that fails with E_LOCK_9472 ("do not retry"), edits to 7 files in a fixed order, a test run, and a next step (update `tests/test_rounding.py`) to remember but not do.
- Turn 2: read every file in `docs/` and summarize the architecture.

Branches fork from the seed: A `/compact`; B `/compact` with a preservation instruction ("Preserve verbatim: every file path you modified, each decision with its reason, approaches that failed with their exact error codes, directories we must not touch, the next step, and any formatting rules I gave in chat."); C no compaction (control); D auto-compact forced with `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`. Each branch then gets two probe turns with every tool blocked (Read, Grep, Glob, Bash, Edit, Write, Task, Agent, WebFetch, WebSearch): P1 asks from memory for the modified files, the abandoned approach and its error, the rounding decision and why, the frozen directory and date, and the next step; P2 asks what convention applies to `billing/`.

Calls: `claude -p --output-format stream-json --verbose --resume <session>`, model `sonnet`. Scoring is regex over the probe replies, the compaction summary (the `isCompactSummary` message in the session JSONL) and the post-compact JSONL, with one manual check noted below. Repetitions: rep0 pilot + rep1–4 main + rep5 auto; all seeds valid (7/7 files edited in order, `legacy/` untouched, seed replies followed KIWI and ROOTOK).

**Results.**

| Clue | A: /compact (N=5) | B: + preserve instruction (N=4) | C: no compaction (N=4) | D: auto-compact (N=1) |
|---|---|---|---|---|
| Chat-only rule KIWI in probe replies (P1, P2) | 5/5, 5/5 | 4/4, 4/4 | 4/4, 4/4 | 1/1, 1/1 |
| Root CLAUDE.md rule ROOTOK in probe replies | 5/5, 5/5 | 4/4, 4/4 | 4/4, 4/4 | 1/1, 1/1 |
| Subfolder billing/CLAUDE.md rule HERON (P2) | 5/5 | 4/4 | 4/4 | 1/1 |
| Edited file names recalled (P1, of 7) | 7,7,7,7,7 | 7,7,7,7 | 7,7,7,7 | 7 |
| Decision HALF_EVEN + reason SPEC-7731 | 5/5 | 4/4 | 4/4 | 1/1 |
| Failed approach + exact error E_LOCK_9472 | 5/5 | 4/4 | 4/4 | 1/1 |
| Frozen dir legacy/ + date 2026-11-30 | 5/5 | 4/4 | 4/4 | 1/1 |
| Next step tests/test_rounding.py | 5/5 | 4/4 | 4/4 | 1/1 |
| legacy/ wrongly listed as modified | 0/5 (one regex hit; the reply said "untouched") | 0/4 | 0/4 | 0/1 |
| Same clues present in the summary text | 5/5 on all | 4/4 on all | n/a | 1/1 on all |

**What came back from disk, and what did not** (checked in all 10 post-compact JSONLs, excluding the summary message):

- Re-attached files (`compact_file_reference`): in 10 of 10 compacted runs, 5 references to the `docs/*.md` files read last in turn 2, each with the note "too large to include. Use Read tool if you need to access it". Path only, no content. None of the 7 edited files was re-attached; `report_templates.py` (about 7K tokens) never appeared.
- `billing/CLAUDE.md`: no reload outside the summary in any run. HERON survived because the summary text copied it (10/10).
- SessionStart `compact` hook output (OWL-HOOK): present after compaction in 10/10.
- Auto memory: in 11 of 14 first-probe replies the model said it had also written the next step to a memory note (MEMORY.md). The summary carried the next step on its own in every run.

**Side numbers** (not used in the article, which answers a different question):

- `pre_tokens → post_tokens`: A 82,890→5,832; 84,892→5,933; 81,270→5,642; 90,548→6,011; 88,105→5,813. B 84,892→5,840; 81,270→5,867; 90,548→3,747; 88,105→3,627. D (trigger auto) 80,639→5,949.
- Compaction duration: 21.3–27.0 s (A), 23.0–28.9 s (B), 22.9 s (D).
- Summary length: 866–1,041 words (A), 928–995 (B), 934 (D).
- Cost of the compaction call: $0.110–0.117. First probe turn after compaction: $0.058–0.071 (A/B), $0.088 (D), against $0.280–0.315 with no compaction (C). Costs are per-call differences of `total_cost_usd`, which is cumulative per session.
- Total cost: $5.73 (pilot + 4 main repetitions + 1 auto), plus a $0.28 smoke test.

**Smoke test (2026-10-21).** In a throwaway folder with the CLAUDE.md rule "Always end replies with the word BANANA", a chat-only KIWI rule, then `claude -p "/compact" --resume <session>`: the stream showed a `system/compact_boundary` event with `trigger: manual`, `pre_tokens 23078`, `post_tokens 4009`, `duration_ms 7165`, and the next reply still started with "KIWI:" and ended with "BANANA". This confirmed headless `/compact` via `--resume` works and can be observed. Details in `smoke-2026-10-21.md`.

Files: `harness.py`, `make_project.py`, `results.md`, `results-rows.json` (one row per run), `raw/` (stream logs per call), `summaries/` (the 10 compaction summaries).

## Evidence 2: what the summary looks like

All 10 summaries in `summaries/` have the same nine numbered sections: 1. Primary Request and Intent, 2. Key Technical Concepts, 3. Files and Code Sections, 4. Errors and fixes, 5. Problem Solving, 6. All user messages, 7. Pending Tasks, 8. Current Work, 9. Optional Next Step. In all 10, section 6 quotes the first user message in full (the KIWI rule, the SPEC-7731 reason, the legacy/ date, the edit order and the next step). Third-party reconstructions of the compaction prompt describe the same nine sections; they are unofficial and the wording changes between versions, so this note relies only on the section titles seen in our own summaries.

## Evidence 3: official docs compared with the measurement

| Official statement | Page (date read) | What we saw |
|---|---|---|
| System prompt, root CLAUDE.md and unscoped rules, auto memory and the plan are reloaded after compaction; chat is kept only as far as the summary keeps it | [Explore the context window: What survives compaction](https://code.claude.com/docs/en/context-window#what-survives-compaction) (2026-11-20) | ROOTOK 10/10; chat clues survived through the summary text |
| Nested CLAUDE.md and `paths:` rules reload only when a matching file is read again, so "compaction summarizes them away"; move them to the root to keep them | same page | `billing/CLAUDE.md` reloaded 0/10; HERON survived only via the summary |
| Up to five files are re-read, "most recently modified first"; files over 5,000 tokens become a `Referenced file` (path only) | same page | The 5 files were the docs read last, path only; 0 of 7 edited files |
| Auto-compact works the same way as `/compact` | same page | The one auto run (D) matched A on every clue |
| `/compact focus on …` keeps what you choose instead of what the automatic pass guesses | same page | No difference in the easy case (B = A) |
| Root CLAUDE.md is reloaded after `/compact`; instructions given only in chat may be lost | [How Claude remembers your project: Instructions seem lost after /compact](https://code.claude.com/docs/en/memory#instructions-seem-lost-after-compact) (2026-10-30) | The chat-only rule survived 10/10 in our runs, via the summary |
| A SessionStart hook with matcher `compact` re-injects context after compaction | [Hooks guide: Re-inject context after compaction](https://code.claude.com/docs/en/hooks-guide#re-inject-context-after-compaction) (2026-10-30) | OWL-HOOK 10/10 |
| Idle compaction is on by default and turned off with `idleCompaction: false` | [Settings reference: idleCompaction](https://code.claude.com/docs/en/settings-reference#idlecompaction) (2026-11-09) | Not measured |

The survival table on the context-window page was re-read on 2026-11-20 and had the same rows as on 2026-11-09.

## Evidence 4: what the top results say (2026-11-20)

Query "what survives claude code /compact what gets lost". None of the top results runs a fact-by-fact survival test.

- faafospecialist (Substack), "Figured out why /compact loses so much useful context" (2026-01-14): blames server-side summarization with no local copy of the original; gives the author's own session token mix (68% tool results, 23% tool inputs, 6% user, 3% assistant); no survival test.
- MindStudio, Claude Code compact command and context management: says early instructions and the reasons behind mid-session decisions get lost, as a general claim. Our run kept early instructions 10/10.
- Morph, "Context left until auto-compact": about thresholds; no survival test.
- Related issue reports: [anthropics/claude-code#55531](https://github.com/anthropics/claude-code/issues/55531) (compaction loses operational knowledge, causing repeated user corrections; read via a mirror), [#17428](https://github.com/anthropics/claude-code/issues/17428) (proposal to keep a copy of the original transcript).

No Naver data was used: the topic has no Korean angle.

## Limits

- One synthetic project, about 80–90K tokens (8–9% of a 1M window), one model (Sonnet 5.5), headless `-p` only, Claude Code 2.1.296. Interactive sessions, sessions over 200K tokens and idle compaction were not reproduced.
- Every clue was stated in one early user message. That is the easiest case for the summary, and it is why everything survived. Facts that only Claude worked out, facts that only appeared in tool output (test names, error codes), and decisions reversed later in the session were not tested in this round. A second experiment that plants facts by channel (typed by the user, concluded by Claude, tool output only, reversed) was designed on 2026-11-20 and has not been run; its results will be added here when it runs.
- N is small (5, 4, 4, 1). Counts only, no percentages.
- The compaction prompt is not public and changes between versions; section titles here are what our summaries showed on 2.1.296.

## Evidence 5: round 2 on 2.1.328 (2026-11-20)

Full setup, per-fact table and files: `results-r3.md`, `results-r3-rows.json`, `raw-r3/`, `summaries-r3/`.

- Setup: Claude Code 2.1.328, Sonnet 5.5, headless `claude -p --resume`, one small synthetic ledger project. One 7-turn seed session carried 12 facts through four channels (typed, found by Claude in files, test output, two reversals), then was forked: plain `/compact` x3, `/compact` with the keep line x2, no compaction x1. Add-on: a 3-turn session where test names appeared only in tool output.
- Session size: 78,118 tokens at compaction (add-on 49,833) of a 1M window; 15,347-15,693 after. The article's own losses happened in real sessions far larger than this; this experiment did not reach that size.
- Result: every planted fact kept in all 5 compactions; the only change was the root cause's line number (no line or "can't vouch for 42") in 3 of 5, including both keep-line runs. With round 1 (2.1.296, 10 compactions) that is 16 compactions across two versions with no planted fact lost.
- Summaries: the same nine numbered sections as round 1; 1,023-1,234 words each (about 1,000 in the add-on).
- Re-attached files: the five edited files came back with full content in 5 of 5. In this seed the edits were also the last files Claude touched, so round 2 does not separate "last read" from "last modified"; round 1 did (docs read last came back, path only, none of the 7 edits).
- Example boundary line (round 2, run A1): `{"type":"system","subtype":"compact_boundary","compact_metadata":{"trigger":"manual","pre_tokens":78118,"post_tokens":15629}}`.

## How to see which files came back (checked on our raw logs, 2026-11-20)

In the session JSONL, the summary entry (`isCompactSummary: true`) is followed by one `"type":"attachment"` line per re-attached file: `"attachment":{"type":"file",...}` carries the full text (round 2), `"attachment":{"type":"compact_file_reference",...}` only the path (round 1, files over 5,000 tokens). This command printed exactly the five re-attached files on `raw-r3/A1.after-compact.jsonl` and `raw/rep0-A.after-compact.jsonl`:

```
grep -oE '"attachment":\{"type":"(file|compact_file_reference)","filename":"[^"]*"' SESSION-ID.jsonl | tail -5
```

## Official facts added for reader fix 1 (2026-11-20)

| Fact | Source (checked 2026-11-20) |
|---|---|
| Idle compaction runs by default in interactive terminal, VS Code chat panel and local desktop Code sessions when auto-compaction is on, the conversation is on the one-hour prompt cache TTL, context has reached the threshold (default 200,000 tokens, `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS`, min 100,000), and about an hour has passed since the last request | [Settings reference: idleCompaction](https://code.claude.com/docs/en/settings-reference#idlecompaction) |
| `"idleCompaction": false` or the Idle compaction row in `/config` (v2.1.302+) turns it off; key needs v2.1.290+ | same |
| `"autoCompactEnabled": false` turns off auto-compact and idle compaction; manual `/compact` keeps working; `DISABLE_AUTO_COMPACT` does the same per session | [Settings reference: autoCompactEnabled](https://code.claude.com/docs/en/settings-reference#autocompactenabled) |
| `.claude/rules/` files without `paths` frontmatter load at launch with the same priority as `.claude/CLAUDE.md`; with `paths` they load only when Claude works with matching files | [How Claude remembers your project](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/) |

## Finding the current session file (checked on this machine, 2026-11-20; reader fix 3)

- Claude Code 2.1.328 stores one `<session-id>.jsonl` per session in `~/.claude/projects/<folder>/`, where `<folder>` is the working directory with every `/` replaced by `-` (observed: `~/wp-writer` → `-home-user-wp-writer`, `/tmp/exp/ → `-tmp-exp-cmp-exp-r3-ledger-svc`).
- The session in use is the most recently written file: `ls -t *.jsonl | head -1` in the running session's folder returned the running session's own id.
- The article's combined command (`grep ... "$(ls -t *.jsonl | head -1)" | tail -5`) printed the five re-attached files on the round 2 A1 log.
- Detail moved out of the article body at reader fix 3 (still documented above): the summary's numbered section names ("All user messages", "Files and Code Sections", "Errors and fixes", Evidence 2), the add-on run's error code `RECON-E-6604` (Evidence 5 add-on), the version labels of the two file re-attach rounds (2.1.296 round 1: docs read last, path only, 0 of 7 edits; 2.1.328 round 2: 5 edits in full) and the run counts (line number lost in 3 of 5, including both keep-line runs).

Article: [What Survives Claude Code /compact? Tested on 2.1.328](https://loopnotes.dev/claude-code-compact-what-survives/)
