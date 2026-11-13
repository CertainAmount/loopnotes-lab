# Does Claude Code call a matching skill when the request skips the description's words?

Research note for the loopnotes.dev post `claude-code-skill-not-triggering`. Measured on 2026-11-12 on one Linux machine with Claude Code 2.1.317.

## Conclusions

- Rewriting the description changed nothing in this test: with three different descriptions, every request that named the task in any words ("release notes", "what changed", "summarise CHANGES.txt") called the skill, 30 of 30, so a reader whose skill is visible in `/skills` should not start by rewriting the description.
- Misses came only from requests that never named the task ("what should we tell customers about 1.5?"): 2 of 15 never called the skill and 4 more called it only after reading the repo first, so when you phrase a job indirectly, or the format matters, call the skill as `/skill-name` instead of hoping it fires.
- The final answer's format is not a reliable sign that the skill ran: one run followed the format by reading `SKILL.md` as a plain file without calling the skill, and one called the skill but ran out of turns before writing the header, so check for the `Skill` tool call itself.
- Headless `claude -p` called the skill as often as an interactive session on the same requests (5 of 5 each), so the 0% headless reports in older GitHub issues did not reproduce on this version; a script still cannot tell you it missed, which is why a pipeline prompt should name the skill.
- A one-line CLAUDE.md rule and 40 extra skills (skill listing at its 1% cap) made no measurable difference here, because the baseline was already 10 of 10; neither is a fix to reach for first.

## Setup

- Claude Code `2.1.317 (Claude Code)`, model `claude-sonnet-5-5` (the user-level `model: sonnet` default), 1M-token context window, default permission mode `bypassPermissions`.
- Fresh git repo in a scratch directory (no CLAUDE.md, no other project skills). User-level skills already installed on the machine were left in place, as a reader's would be: 30 other skills in the list (built-in and synced, e.g. `docs`, `pdf`, `pptx`, `deep-research`) plus one plugin with hooks. `/context` in the base project: `Skills: 5.7k tokens (0.6%)`, 31 skills.
- Test skill `.claude/skills/release-notes/SKILL.md`: the body is a house format with a fixed 3-line header (`=== Acme Tracker release notes ===`, `Version: ...`, `Audience: ...`) and `[Added]/[Fixed]/[Changed]` labels. The task is one Claude can do passably without the skill, which is what makes a miss possible. `CHANGES.txt` sits in the repo root. Files: `harness/body.md`, `harness/CHANGES.txt`.
- Descriptions (only the `description:` line changes, `harness/descs.json`):

| ID | description |
|---|---|
| D1 | Formats release notes in the house style with fixed header and category labels. |
| D2 | Release notes, changelog, 'what changed' write-ups for an announcement: formats them in the house style with fixed header and category labels. |
| D3 | D2 + Use when the user asks to summarise changes since a version, even if the request doesn't say 'release notes'. |

- Requests (English, same set for every description; the skill name never appears): `harness/prompts.json` (K1-K5 contain "release notes", N1-N5 name the task in other words) and `harness/prompts-far.json` (F1-F5 name neither release notes nor changes).
- Headless command per run: `claude -p "<request>" --output-format stream-json --verbose --max-turns 4 --no-session-persistence`, one run per request, with the project reset (`git checkout -- . && git clean -fd`, keeping `.claude/` and CLAUDE.md) before every run. Harness: `harness/run.py`, `harness/setup.py`.
- Interactive mode: `claude` started in a pseudo-terminal (`harness/inter.py`), request typed and sent with Enter, then the session transcript JSONL was read for `Skill` tool calls. Inherited `CLAUDE*` environment variables from the parent session were removed so the child session wrote its own transcript.
- Called = a `tool_use` block with `name == "Skill"` and `release-notes` in its input, anywhere in the run (a call after other tools also counts). `header_ok` = the final answer contains the fixed first header line.

## Results

| Axis | Description | Requests | Skill called | Header in answer |
|---|---|---|---|---|
| description, headless | D1 | K (has "release notes") | 5/5 | 5/5 |
| description, headless | D1 | N (other words for the task) | 5/5 | 5/5 |
| description, headless | D2 | K | 5/5 | 5/5 |
| description, headless | D2 | N | 5/5 | 5/5 |
| description, headless | D3 | K | 5/5 | 5/5 |
| description, headless | D3 | N | 5/5 | 5/5 |
| far wording, headless | D1 | F (names neither) | 4/5 | 4/5 |
| far wording, headless | D2 | F | 5/5 | 4/5 (1 run hit max turns) |
| far wording, headless | D3 | F | 4/5 | 5/5 (1 run read SKILL.md as a file) |
| interactive | D3 | N | 5/5 | 5/5 |
| CLAUDE.md line | D1 + "Release notes and change summaries go through the release-notes skill." | K + N | 10/10 | 10/10 |
| 40 dummy skills | D3 + 40 skills (`harness/dummies.json`) | K + N | 10/10 | 10/10 |

When the skill was called first (counted from `tool_sequence` in `runs.csv`):

| Axis | Skill as first tool | Skill after other tools | Never called |
|---|---|---|---|
| description (K + N, 30 runs) | 29 | 1 (D1-N4: `Bash>Read>Skill`) | 0 |
| far wording (F, 15 runs) | 9 | 4 | 2 |
| interactive (5 runs) | 5 | 0 | 0 |
| CLAUDE.md line + 40 dummy skills (20 runs) | 20 | 0 | 0 |

The two runs that never called the tool: D1-F5 answered in its own format; D3-F1 listed `.claude`, read `SKILL.md` directly and followed the format. D2-F1 called the skill late (after `Bash>Bash>Read(SKILL.md)`) and stopped at max turns before writing the header.

`/context` with the 40 dummy skills added: `Skills: 10k tokens (1.0%)`, 70 skills. The listing budget is 1% of the context window (see the official comparison below), so the listing was at its cap. `release-notes` was still called 10 of 10.

Row-level data: `runs.csv` (columns `axis,description,prompt_id,has_keyword,mode,skill_called,header_ok,tool_sequence,result,prompt`; 70 rows).

## Official documentation compared with older numbers in top results

Read on 2026-11-12: [Claude Code docs: Extend Claude with skills](https://code.claude.com/docs/en/skills).

| Point | What top-ranking posts still say | What the official page says now |
|---|---|---|
| Skill listing budget | 15,000 characters, raised with `SLASH_COMMAND_TOOL_CHAR_BUDGET` (written against 2.0.70) | 1% of the model's context window; when it overflows, descriptions of the least-used skills are dropped first; adjustable with `skillListingBudgetFraction` (`SLASH_COMMAND_TOOL_CHAR_BUDGET` and `skillOverrides` `"name-only"` also listed) |
| Description length | 1,024 characters | `description` + `when_to_use` are cut at 1,536 characters per entry (`skillListingMaxDescChars`); put the key use case first |
| How to check truncation | not covered | `/context` Skills row (accurate from v2.1.196), `/doctor`, `/skill-doctor` (v2.1.252+) |
| Broken frontmatter | not covered | if the YAML fails to parse, the skill loads with empty metadata: `/skill-name` works, automatic matching does not; check with `--debug` or `claude plugin validate` (v2.1.233+) |
| Forcing or blocking auto-use | "ALWAYS invoke" wording, hooks | "Skill not triggering": use words users would naturally say, ask "What skills are available?", rephrase, call `/skill-name`; `disable-model-invocation: true` stops automatic loading while `/skill-name` still works; rules that must hold every time belong in hooks |

## Other people's reports (not our data)

GitHub issues in `anthropics/claude-code`, titles and states read on 2026-11-12:

- [#32184](https://github.com/anthropics/claude-code/issues/32184): recall 0% in headless `claude -p` regardless of description (closed 2026-05-26). Not reproduced on 2.1.317 in this test.
- [#36570](https://github.com/anthropics/claude-code/issues/36570): `claude -p` does not trigger skills, skill-creator eval at 0% (closed 2026-06-08). Not reproduced here.
- [#34648](https://github.com/anthropics/claude-code/issues/34648): skills never trigger in `-p` with 40+ skills and MCP servers (closed 2026-04-18). Our 40-dummy run (no MCP servers) called the skill 10 of 10.
- [#46952](https://github.com/anthropics/claude-code/issues/46952): auto-activation seems to use keyword overlap (closed 2026-05-24). Our N requests shared no "release notes" wording and still called the skill; misses appeared only when the task itself went unnamed.
- [#21947](https://github.com/anthropics/claude-code/issues/21947): personal skill not auto-triggering despite a matching description (closed 2026-02-28).

Top blog results compared for the article (links only): [dev.to/lizechengnet](https://dev.to/lizechengnet) (list of causes, an unsourced "about 50%" rate), [scottspence.com](https://scottspence.com) (20 sessions with a hook, 9 of 20, version not stated), [blog.fsck.com](https://blog.fsck.com) (15,000-character budget on 2.0.70).

## Limits

- One run per request and description. With all 30 description-axis runs calling the skill, the test cannot show a description effect on these requests, and the 2 far-wording misses out of 15 are too few to rank the descriptions.
- One model (Sonnet 5.5 via the user default) and one version. Requests are in English.
- The test project held only `CHANGES.txt`, so the request and the repo pointed the same way. A large repo with competing skills can behave differently.
- The CLAUDE.md and 40-dummy runs started from a 10-of-10 baseline, so they show no harm, not a benefit.

## Runs discarded

- First D3 and 40-dummy runs: the project was not reset between runs, and an earlier run had written `RELEASE_NOTES_v1.5.txt` into the repo that later runs read. Re-run with a reset before every run. One far-wording D3 batch ran concurrently in the same directory as another batch; re-run in its own copy. Only the re-runs are in `runs.csv`.
- Cost of all headless runs including the discarded ones: about $6.5 by the CLI's `total_cost_usd` (planned cap about $5; the overrun is the re-runs).

## Not measured

- `/skill-doctor` output (the weekly usage limit was nearly reached during the session).
- A `UserPromptSubmit` hook condition.

## Checks added for the reader fix (2026-11-12)

How a reader confirms the two look-alikes, run on the same machine with Claude Code `2.1.322` (the CLI had auto-updated since the main runs) in a scratch repo with two project skills: `good-skill` (valid frontmatter) and `broken-yaml` (a `description` line followed by a mis-indented `with: bad indent: here` line).

- `claude plugin validate .claude/skills` (and `claude plugin validate .claude`, same result), exit code 1:
  ```
  Validating components in: <repo>/.claude/skills
  Validating skill: <repo>/.claude/skills/broken-yaml/SKILL.md
  ✘ Found 1 error:
    ❯ frontmatter: YAML frontmatter failed to parse: YAML Parse error: Unexpected token. At runtime this skill loads with empty metadata (all frontmatter fields silently dropped).
  ✘ Validation failed
  ```
  With `broken-yaml` moved out: `✔ Validation passed`, exit code 0. A description containing an unquoted `Release notes: house style` (colon) alone passed, so that is not shown as a cause.
- `claude --debug -p "Reply with the single word ok." --max-turns 1`: nothing on stderr; the log was written to `~/.claude/debug/<session-id>.txt` with a `~/.claude/debug/latest` symlink. Lines for the broken skill:
  ```
  [WARN] Failed to parse YAML frontmatter in <repo>/.claude/skills/broken-yaml/SKILL.md: YAML Parse error: Unexpected token
  [ERROR] [skills] YAML frontmatter in <repo>/.claude/skills/broken-yaml/SKILL.md failed to parse and was ignored: YAML Parse error: Unexpected token
  ```
- Listing over budget: not triggered in this check (the 40-dummy run above reached `Skills: 10k tokens (1.0%)`, the default cap, but its debug log was not kept). The warning string in the 2.1.322 binary is `Skill listing over budget: `; the official page says the warning goes to the debug log.
- `/context` Skills row readings from the main runs: 0.6% with 31 skills, 1.0% with 70 skills (cap). 1M-token context window.

Official pages read on 2026-11-12:

- [Extend Claude with skills, "Skill not triggering"](https://code.claude.com/docs/en/skills#skill-not-triggering): "run `claude plugin validate` on the skills directory, for example `claude plugin validate .claude/skills` for project skills or `claude plugin validate ~/.claude/skills` for personal skills. Requires Claude Code v2.1.233 or later." Malformed YAML: "Run with `--debug` to see the parse error."
- [Extend Claude with skills, "Skill descriptions are cut short"](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short): the listing always keeps every skill name and drops descriptions of the least-invoked skills first; "When the listing exceeds its budget, Claude Code also writes a warning to the debug log"; the `/context` Skills row reports the size after the budget (accurate from v2.1.196); `skillListingBudgetFraction` "for example, `0.02` = 2%".
- [Settings reference, `skillListingBudgetFraction`](https://code.claude.com/docs/en/settings-reference#skilllistingbudgetfraction): number greater than 0 and at most 1, default `0.01` (1% of the context window), example `0.02`.
- [Plugins CLI reference, "Validate a directory"](https://code.claude.com/docs/en/plugins/cli-reference): without a manifest, a directory named `skills` validates the files inside it, a directory named `.claude` validates its `skills`, `agents` and `commands`; this needs v2.1.233 or later.
- `claude update --help` (2.1.322): "Check for updates and install if available".

Moved out of the article body in the reader fix (already recorded above): the 15,000-character / 1,024-character figures in older posts versus the official 1% budget and 1,536-character cap; GitHub issues #32184 and #36570; the 9 / 4 / 2 split of the far-wording runs; model and the 30 installed skills in the setup.

Article: [Claude Code Skill Not Triggering? It's the Prompt (45 Runs)](https://loopnotes.dev/claude-code-skill-not-triggering/)
