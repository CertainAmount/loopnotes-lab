# How many AI code review comments are worth acting on, and what removes the wrong ones?

Research note for the loopnotes article on AI code review false positives. It holds the evidence behind the article: one measurement made for it (E3, six planted-bug diffs reviewed under five prompts) and a side-by-side reading of the public "resolved" and "useful" figures the article compares against.

## Conclusions
- Every wrong comment in our run flagged input that the caller had already validated. When the reviewer also saw the caller file and three team rules, wrong comments went from 6 to 0 and the pile went from 53 to 29 comments. If your reviewer keeps flagging handled cases, give it the callers and your team's rules before you change anything else.
- The biggest slice was never the wrong comments. Under the first three prompts, 61–62% of comments were true about the code but not worth a change. Judge your bot by the share of comments that led to a code change, not by its false-positive rate.
- A one-line scope instruction ("only security, concurrency, error handling, data integrity, performance") cut the count from 53 to 38 but left the mix where it was (61% low value) and kept 5 wrong comments; some nitpicks came back under the allowed category names ("no authorization check", "CSV formula injection" on numeric columns). Adding one sentence to that same prompt, "If you are not confident an issue is real, do not mention it", cut the low-value share to 40% and the pile to 20, with no relabelled nitpicks and 5/5 planted bugs. It did not touch the two wrong comments about input validated elsewhere, and it dropped the "add a test" comments.
- So the two slices answer to different fixes: wrong comments come from code the reviewer cannot see and go away only with context; right-but-low-value comments come from a reviewer that says everything it notices and shrink when it is told to stay quiet unless sure.
- No prompt missed a planted bug: all three caught 5 of 5, including an off-by-one that sat outside the scope list. In this small run, adding context or a scope line cost nothing in bugs caught. The diff with no planted bug still drew 6–11 comments under every prompt, so a long list is not a sign that something is wrong.
- Public figures count different things. Uber's 65% "addressed" means the comment did not come back when the reviewer was rerun on the final commit, its 75% "useful" comes from engineers who chose to rate comments, and Beko's 73.8% "resolved" is a label the PR author set. Before comparing your team's number with theirs, recount 20–30 of your own PRs by one rule: did a person change the code because of the comment?

## Measurement E3: six diffs, five prompts

Measured 2026-11-18 on the author's machine. Tool: Claude Code 2.1.327, headless (`claude -p`), default model (`claude-opus-5-5`, recorded per run in `outputs/*.json` under `modelUsage`), no tools (`--tools ""`), no settings files (`--setting-sources ""`), run from an empty directory so no project instructions were loaded. One run per prompt, 18 runs, total cost $0.42. Runner: `run_e3.sh`; prompts built by `build_prompts.py`.

### Material
Six small Python diffs (20–30 lines each, `diffs/`), written for this test. Five carry one planted bug each; the sixth is a control with no planted bug. Each diff also carries "non-problems": things a reviewer might flag that are already handled outside the diff or allowed by the team.

| diff | planted bug | planted non-problems |
|---|---|---|
| d1 `profiles/service.py` | None not handled: `find_by_id` / `find_team` can return None, then `.team_id` / `.short_label` is read | `uid` already validated by the route (`parse_uid`); short names `u`, `uid`, `out` |
| d2 `orders/checkout.py` | exception swallowed and success returned: `except Exception: log; return True` after charge/insert | the second broad `except` in `_emit_placed` is marked `# intentional:`; `order` already validated by `Order.from_json` |
| d3 `reports/export.py` | connection not closed: `return 0` on empty result (and any exception) skips `conn.close()`; the job runs hourly in one long-lived worker | `out_path` is built by the caller from a fixed directory; `month` is regex-checked by the caller |
| d4 `search/paging.py` | off-by-one: `end = start + size - 1` drops the last item of every page (this bug type is **outside** condition C's scope list) | `page` already range-checked by the route; short name `n` |
| d5 `pricing/cache.py` | race: `_hits[cur] = n + 1` read-modify-write from a 16-thread pool; the counts are billed | `cur` already checked against `CURRENCIES` by the caller; pre-existing check-then-set in `get_rate` only causes a duplicate fetch |
| d6 `accounts/names.py` | none (control) | `name` stripped and non-empty by the route; short names `n`, `s` |

`src/dN/caller.py` holds the unchanged caller shown only in condition B. `prompts/team-rules.txt` holds the three team rules shown only in condition B.

### Conditions (same base prompt)
Base: `Review this diff. List each issue as one comment.` plus a one-line output format (one `- ` line per comment), identical across conditions.
- **A** diff only.
- **B** diff + the caller file + three team rules.
- **C** diff only + `Only comment on security, concurrency, error handling, data integrity, or performance/resource usage. Skip style and naming.`

6 diffs × 3 conditions = 18 runs (`prompts/dN-X.txt` → `outputs/dN-X.json`, `.txt`).

### Classification rules (written before the runs, applied as written)
Each `- ` line is one comment. Each comment gets exactly one class:
- **Acted on**: points at the planted bug or at another defect that really exists in this code and that a reviewer on a real team would ask to fix in this PR (wrong result, crash path, leak, lost error, data corruption, missing test for the new branch that the planted bug sits in).
- **Wrong**: flags a planted non-problem as a problem (input the caller already validates, a team-allowed name, the `# intentional:` except), or claims something the code does not do.
- **Right, low value**: true about the code but not worth a change here (naming, docstrings, type hints, hypothetical inputs no caller can produce, defensive checks, i18n/Unicode/width concerns for an internal helper, micro-performance, pre-existing code outside the diff that works).
- Unclear between two classes → the lower one (Right, low value over Acted on; Wrong over Right, low value only when the comment's premise is false). Marked `ambiguous=1` in the CSV.
- **Planted hit** (per run): 1 if any comment names the planted bug's mechanism (for d4: the dropped item / `- 1`; for d5: the non-atomic increment). Recall per condition = hits / 5.
- `reason_tag` for Wrong comments: `already-handled-elsewhere`, `team-allowed`, `misread`.

Classifier: the agent that wrote the diffs, reading each comment against the rules above and the known planted list. One judge, no second rater. Labels are in `classify.py`.

### Results
`e3-summary.csv` (per condition), `e3-classified.csv` (one row per comment, 158 rows: 120 for A–C, 38 for D–E, with a short note).

| prompt | comments | acted on | wrong | right, low value | planted bugs caught |
|---|---|---|---|---|---|
| A diff only | 53 | 14 (26%) | 6 (11%) | 33 (62%) | 5/5 |
| B diff + callers + team rules | 29 | 11 (38%) | 0 (0%) | 18 (62%) | 5/5 |
| C diff + risk-area scope line | 38 | 10 (26%) | 5 (13%) | 23 (61%) | 5/5 |

What moved:
- **Context removed every wrong comment** (6 → 0) and cut the pile from 53 to 29. All six wrong comments in A were `already-handled-elsewhere`: input the caller already validated (d3 month, d4 page ×2, d5 currency, d6 whitespace/strip ×2).
- **The scope line did not change the mix.** Low-value share stayed 61–62% under all three prompts. C cut 15 comments but kept 5 wrong ones (d4: page and size bounds the route already enforces; d6: whitespace and None names) and reframed nits into the allowed categories (d1 "no authorization check", d1 "uids has no size limit", d3 "CSV formula injection" on numeric columns, d6 "impersonation risk" from name collisions).
- **Nothing was lost by narrowing in this run.** C still caught all 5 planted bugs, including the off-by-one that sits outside its scope list (it called it data integrity).
- **The control diff (d6, no planted bug) drew 6–11 comments under every prompt and none worth a change.**
- Per diff, A / B / C comment counts: d1 9/4/7, d2 7/5/5, d3 9/6/7, d4 7/1/6, d5 10/6/7, d6 11/7/6.
- 20 of 120 labels are marked `ambiguous=1` (placed in the lower class per the rule).

### E3-D: the team's own scope paragraph (pre-registered 2026-11-18, before the runs)
Why: a scope paragraph cut nitpicks on the author's real team but the one-line scope in C did not change the mix here. The visible difference is one line, "If you are not confident an issue is real, do not mention it", plus a fuller do-not list.
- Condition D: diff only + "Only review for security, concurrency, error handling, and data integrity. Do not comment on naming, style, formatting, or minor refactors. If you are not confident an issue is real, do not mention it." Same base prompt, same settings as A–C (`claude -p`, Claude Code 2.1.327, `--tools "" --setting-sources ""`, empty directory), 6 diffs × 1 run.
- Four areas, no performance, as on the team; so d3 (resource cleanup) and d4 (off-by-one) both sit outside the list.
- Classification: the rules above, unchanged.
- Threshold, set before running: if the right-but-low-value share is 10+ points below A (62%), D "cut the low-value share"; otherwise "same". One run, six diffs: a small gap counts as same. Also marked: whether nits come back under the allowed area names (as in C).

### E3-E: which part of D did it (pre-registered 2026-11-18, after D, before E's runs)
D differs from C in three ways at once (the confidence line, a fuller do-not list, no performance area). E isolates the line a reader can paste: C's prompt word for word + "If you are not confident an issue is real, do not mention it." Same settings, 6 diffs × 1 run. Same threshold: low-value share 10+ points below A (62%) → the confidence line alone cut it; otherwise the fuller do-not list / four-area list did.

### Results D and E (run 2026-11-18, same settings, model `claude-opus-5-5`, 12 runs, about $0.22)
| prompt | comments | acted on | wrong | right, low value | planted bugs caught |
|---|---|---|---|---|---|
| D team scope paragraph (4 areas + do-not list + stay-quiet line) | 18 | 9 (50%) | 2 (11%) | 7 (39%) | 5/5 |
| E = C + "If you are not confident an issue is real, do not mention it." | 20 | 10 (50%) | 2 (10%) | 8 (40%) | 5/5 |

- By the pre-registered threshold both D and E **cut the low-value share** (62% → 39% / 40%, 22+ points). E differs from C by that one sentence only, so the stay-quiet line did the work, not the area list (C alone: 61%).
- No nitpick came back under a security or data-integrity name in D or E (C had four).
- The stay-quiet line did **not** remove the wrong comments: 2 remain in both, and both are `already-handled-elsewhere` (d4 page, d6 whitespace-only name). The reviewer was sure about input it could not see being validated. Only context (B) removed that kind.
- What the line cost: acted-on comments fell from 14 to 9–10. Every lost one was a "missing test for this path" comment (d1–d5 in A); planted bugs stayed 5/5 and the bug-level comments all stayed.
- Per diff, D / E comment counts: d1 3/4, d2 5/4, d3 1/3, d4 3/3, d5 4/5, d6 2/1. Ambiguous labels: 4 and 4.

### Figures
- Counts per prompt, stacked by class (used in the article): drawn by `fig_f1_counts.py` from `e3-summary.csv`.
- 100% bars per prompt (`fig_f1.py`): not used in the article. Its leftmost bar is the author's own team count described in the article (about 120 comments over about 50 PRs, 2026-09: about 40% acted on, about 20% wrong, 30–40% right but low value; the three do not sum to 100, so the bar draws 40 / 20 / 40 with the last slice as the remainder and is labelled "approx.").
- Terminal capture of `outputs/d4-A.txt`: comment 1 is the planted bug; comments 2 and 4 are the wrong "page not validated" kind.

Stripped from `outputs/*.json` after the run: session_id, uuid, credential_expires_at.

## What the public figures count

Read 2026-11-18. These are other teams' numbers; the article uses them only to show that "resolved" means different things.

| source | figure | what it counts |
|---|---|---|
| [Uber Engineering: uReview](https://www.uber.com/blog/ureview/) (posted 2025-08-12; read from the search result summary) | 65% of comments addressed | a comment counts as addressed when rerunning the reviewer (5 times) on the final commit no longer produces it |
| same | 75% useful | share rated useful by the engineers who chose to rate a comment |
| same | 51% of human reviewer comments addressed | share of comments from human reviewers that were addressed, as reported in the same post: human review is not a 100% baseline either |
| [Automated Code Review In Practice, arXiv 2412.18531 (ICSE 2025 SEIP)](https://arxiv.org/html/2412.18531v2) (read in full) | 73.8% resolved | Beko, a tool built on Qodo PR-Agent with GPT-4 Turbo; "Resolved" is a label the PR author set, not a per-comment check that code changed (the paper names label reliability as a limit); 21.3% "Won't Fix"; average PR closure time rose from 5h52m to 8h20m, with some projects going down |
| [cubic: learnings from building AI agents](https://www.cubic.dev/blog/learnings-from-building-ai-agents) (read from the search result summary) | 51% fewer false positives, recall kept | vendor's own report after splitting into narrow micro-agents; baseline method not published |
| [graphite.com: Is AI code review worth it](https://graphite.com/guides/is-ai-code-review-worth-it) | "<3% false positives" | vendor claim, no method given |
| [codeant.ai: AI code review noise problem](https://codeant.ai/blogs/ai-code-review-noise-problem) | Cursor BugBot resolution 52% → 70%+ | vendor article, no source link for the figure |

The article's own measure is narrower than all of these: did a person change the code because of the comment.

No Naver or other Korean web data was used; this is an English-language engineering question with no Korean angle.

## Limits
- E3 is 6 diffs, 1 run per prompt, Python only, one model, with small single-file diffs written for the test. It shows how the three slices of a review pile move when context or scope changes; it is not an accuracy figure for Claude or for any review product.
- One person classified all 158 comments, with no second rater; 28 labels were close calls, placed in the lower class.
- Planted bugs are simple and well known. 5/5 in every condition means these bugs did not separate the prompts; it does not show that narrowing never costs real bugs in a large codebase.
- The scope-line and stay-quiet results (C, D, E) are from this run only; context plus the stay-quiet line together was not run. A team that narrows scope over weeks on real code (with its own vocabulary and allowed styles) may see the low-value share move differently.
- Uber and cubic figures were read from search result summaries, not the full pages.

## Where to put context and the test check (added 2026-11-18, reader fix 1)
Moved here from the article body, which now keeps only the conclusions:
- The five planted bugs (None not handled, swallowed exception, unclosed connection, off-by-one, race on a shared dict) and the planted non-problems (validated input, team-allowed short names, a commented broad `except`) are in the Material table above; the base prompt is under Conditions.
- Uber's 75% "useful" (comments rated by engineers who chose to rate them) was dropped from the article's comparison table; it stays in the public-figures table here.
- Team-level details the article now says in words: on one PR, five or six bot threads were resolved seconds apart; the N+1 shipped about six weeks after the scope paragraph, its tests used three or four rows, and staging response went from a few hundred milliseconds to over a second; counting took three to five minutes per PR, over ten when a wrong comment needed checking; roughly one in ten comments after the scope paragraph were security-named comments on checks done upstream. The control diff drew 6–11 comments under prompts A–C.

Official pages checked 2026-11-18 for the "how" the article gives:
- [About GitHub Copilot code review](https://docs.github.com/en/copilot/concepts/agents/code-review), GitHub Docs: the review "analyzes your entire repository to better understand the context of code changes"; repository-wide rules go in `.github/copilot-instructions.md`, path-specific rules in `.github/instructions/**/*.instructions.md` (applied when changed files match), and `AGENTS.md` at the root is also read; instructions are read from the PR's head branch, so a change to them can be tried in the same PR.
- [Using GitHub Copilot code review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review), GitHub Docs: same instruction files; no length limit stated.
- [diff-cover README](https://github.com/Bachmann1234/diff_cover): `diff-cover coverage.xml` compares the current branch with `origin/main` by default (`--compare-branch` to change it); `--fail-under=80` returns non-zero below 80%; input is Cobertura, Clover or JaCoCo XML, or LCov; coverage.py writes Cobertura-style XML via `pytest --cov --cov-report=xml`.
- The author's team's own changed-line coverage tool is not recorded; the article gives diff-cover as one way to do it, not as what the team used. Vendor bots other than Copilot were not checked one by one; the article tells the reader to look for the bot's repository instructions file.

## Reader fix 2 (2026-11-18): moved out of the body, and pages checked
- Uber's 51% (human reviewer comments addressed in the same changeset) left the article's table; the article says it in words ("about half the time"), the figure stays in the public-figures table above.
- The arXiv ID 2412.18531 left the table's link text; the link and Sources entry stay. The paper's own description, checked 2026-11-18 on [the HTML version](https://arxiv.org/html/2412.18531v2): "Beko, a multinational home appliances company"; the study ran in Beko's software development division.
- The GitHub Changelog link for "outdated when its line changes" (2018-09-24) left the counting step; it stays in Sources.
- [diff-cover README](https://github.com/Bachmann1234/diff_cover), checked 2026-11-18: `--fail-under=80` is the README's own example ("will return a non zero status if the coverage or quality score was below 80%"); no default threshold is given. Accepted inputs: Cobertura, Clover or JaCoCo XML, or LCov.
- Not measured: whether rules alone (without pasting the callers) clear the wrong comments for a reviewer that reads only the diff. E3-B gave callers and rules together.

## Reader fix 3 (2026-11-18)
- The article now shows condition C's scope line word for word and tells readers to add it together with the stay-quiet line, the pair tested as E. Expected size given in the body: A 53 comments → E 20 on the same six diffs. The stay-quiet line without a scope line was not run.
- "The 80 is the README's example" left the body; the source stays in Reader fix 2 above.
- Uber's human-reviewer figure (51%, in words "about half") now appears only as a reason not to compare against 100%.

Article: [AI Code Review False Positives: What 120 Comments Showed](https://loopnotes.dev/ai-code-review-false-positives/)
