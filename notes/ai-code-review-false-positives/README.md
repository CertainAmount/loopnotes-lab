# How many AI code review comments are worth acting on, and what removes the wrong ones?

Research note for the loopnotes article on AI code review false positives. It holds the evidence behind the article: one measurement made for it (E3, six planted-bug diffs reviewed under five prompts; the four prompts the article uses were run three times each) and a side-by-side reading of the public "resolved" and "useful" figures the article compares against.

## Conclusions
Updated 2026-11-19 to the three-run picture (prompts A, B, C, E, three runs each; see 「Repeats」 below). Ranges are min–max across the three runs.
- Every wrong comment flagged input that the caller had already validated (one in C's third run framed it as path traversal). When the reviewer also saw the caller file and three team rules, wrong comments went from 4–6 per run to 0 in every run, and the pile went from 52–57 to 25–29 comments. If your reviewer keeps flagging handled cases, give it the callers and your team's rules before you change anything else.
- The biggest slice was never the wrong comments. Under the first three prompts, 54–67% of comments were true about the code but not worth a change, more than half in every run. Judge your bot by the share of comments that led to a code change, not by its false-positive rate.
- A one-line scope instruction ("only security, concurrency, error handling, data integrity, performance") cut the count from a mean of 54 to 37 but barely moved the mix (54–61% low value against A's 62–67%) and kept 5–6 wrong comments per run, as many as the diff alone; in every run some nitpicks came back under the allowed category names ("no authorization check", "CSV formula injection" on numeric columns, "resource exhaustion" from an uncapped uid list, path traversal on a path the caller builds). Adding one sentence to that same prompt, "If you are not confident an issue is real, do not mention it", cut the low-value pile from 19–23 to 7–8 comments (37–40%) and the whole pile to 19–20 in every run, with no relabelled nitpicks and 5/5 planted bugs. It did not touch the two wrong comments about input validated elsewhere (the same two in all three runs), and it dropped every "add a test" comment.
- So the two slices answer to different fixes: wrong comments come from code the reviewer cannot see and go away only with context; right-but-low-value comments come from a reviewer that says everything it notices and shrink when it is told to stay quiet unless sure.
- No prompt missed a planted bug in any run: 5 of 5 every time, including an off-by-one that sat outside the scope list. In this small test, adding context or a scope line cost nothing in bugs caught. The diff with no planted bug drew 3–11 comments in every run without the stay-quiet line, and with the diff alone it drew as many as the buggy diffs (10–11 against 7–12), so a long list is not a sign that something is wrong.
- Public figures count different things. Uber's 65% "addressed" means the comment did not come back when the reviewer was rerun on the final commit, its 75% "useful" comes from engineers who chose to rate comments, and Beko's 73.8% "resolved" is a label the PR author set. Before comparing your team's number with theirs, recount 20–30 of your own PRs by one rule: did a person change the code because of the comment?

## Measurement E3: six diffs, five prompts

Measured 2026-11-18 on the author's machine. Tool: Claude Code 2.1.327, headless (`claude -p`), default model (`claude-opus-5-5`, recorded per run in `outputs/*.json` under `modelUsage`), no tools (`--tools ""`), no settings files (`--setting-sources ""`), run from an empty directory so no project instructions were loaded. Run 1: one run per prompt, 18 runs, total cost $0.42 (repeats of A, B, C and E: 「Repeats」 below). Runner: `run_e3.sh`; prompts built by `build_prompts.py`.

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
`e3-summary.csv` (run 1, per condition), `e3-classified.csv` (one row per comment with a `run` column; run 1 is 158 rows: 120 for A–C, 38 for D–E, with a short note; the repeats add 273 rows).

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
- Counts per prompt, stacked by class (used in the article): first drawn by `fig_f1_counts.py` from run 1 (`e3-summary.csv`); redrawn 2026-11-19 from the three-run means in `e3-summary-runs.csv` with the loopnotes viz engine (`stack` frame), spec and data in `figures/fig-1/`.
- 100% bars per prompt (`fig_f1.py`): not used in the article. Its leftmost bar is the author's own team count described in the article (about 120 comments over about 50 PRs, 2026-09: about 40% acted on, about 20% wrong, 30–40% right but low value; the three do not sum to 100, so the bar draws 40 / 20 / 40 with the last slice as the remainder and is labelled "approx.").
- Terminal capture of `outputs/d4-A.txt`: comment 1 is the planted bug; comments 2 and 4 are the wrong "page not validated" kind.

Stripped from `outputs/*.json` after the run: session_id, uuid, credential_expires_at.

## Repeats (2026-11-19): three runs per prompt
Why: run 1 was one run per prompt, so a gap between prompts could be run-to-run noise. Prompts A, B, C and E (the four in the article) were run twice more on the same six diffs; D (the team paragraph, not in the article) was not repeated.

Method
- Same prompts (`prompts/dN-X.txt`, unchanged), same command and flags as `run_e3.sh` (`claude -p ... --tools "" --setting-sources "" --output-format json`), Claude Code 2.1.327, model `claude-opus-5-5` in every run (`modelUsage`), from an empty temp directory, sequential, each run under a 2 GB memory cap. Runner: `run_e3_repeats.sh`. Outputs: `outputs/r2/`, `outputs/r3/`; run 1 stays in `outputs/` as r1. 48 runs, total cost $0.83 (about $0.017 each); no run errored. session_id, uuid and credential_expires_at stripped from the JSON as in run 1.
- Classification: the rules under 「Classification rules」, unchanged, applied by the same judge the same way as run 1 (labels in `classify.py`, keys `r2/dN-X`, `r3/dN-X`). `e3-classified.csv` now has a `run` column; `e3-summary-runs.csv` has per-run counts and, per condition, the mean and min–max across the three runs (plus `control_d6_comments`, comments on the bug-free diff).

Per run (comments: acted on / wrong / right, low value; planted bugs caught)

| prompt | run 1 | run 2 | run 3 | mean (range) |
|---|---|---|---|---|
| A diff only | 53: 14 / 6 / 33; 5/5 | 57: 14 / 5 / 38; 5/5 | 52: 14 / 4 / 34; 5/5 | 54 (52–57): 14 / 5.0 (4–6) / 35 (33–38) |
| B diff + callers + team rules | 29: 11 / 0 / 18; 5/5 | 25: 11 / 0 / 14; 5/5 | 29: 12 / 0 / 17; 5/5 | 27.7 (25–29): 11.3 (11–12) / 0 (0–0) / 16.3 (14–18) |
| C diff + risk-area scope line | 38: 10 / 5 / 23; 5/5 | 35: 10 / 6 / 19; 5/5 | 37: 10 / 6 / 21; 5/5 | 36.7 (35–38): 10 / 5.7 (5–6) / 21 (19–23) |
| E = C + stay-quiet line | 20: 10 / 2 / 8; 5/5 | 19: 10 / 2 / 7; 5/5 | 19: 10 / 2 / 7; 5/5 | 19.3 (19–20): 10 / 2 (2–2) / 7.3 (7–8) |

Right-but-low-value share per run: A 62 / 67 / 65%, B 62 / 56 / 59%, C 61 / 54 / 57%, E 40 / 37 / 37%. Per diff counts (d1–d6), run 2 / run 3: A 8,8,12,7,12,10 / 8,8,9,7,9,11; B 4,5,4,1,6,5 / 4,6,7,1,6,5; C 6,6,6,6,7,4 / 7,6,6,6,9,3; E 4,4,3,3,4,1 / 4,4,3,3,4,1.

What held across runs
- **B had 0 wrong comments in every run.** A had 4–6, all `already-handled-elsewhere` (d4 page ×2 in every run, d6 whitespace in every run; d3 month and d5 currency in two of three).
- **The stay-quiet line cut right-but-low-value comments in every run**: C 23 / 19 / 21 → E 8 / 7 / 7. By the pre-registered E3-E threshold (10+ points below A's 62%), E's 37–40% passes in every run.
- **Every run caught all 5 planted bugs** under every prompt, including C's off-by-one outside its scope list.
- **E's two wrong comments are the same two in all three runs** (d4 `page` not validated, d6 whitespace-only name): the stay-quiet line did not remove the kind that needs context.
- **E dropped every "add a test" comment in every run** (A had 4–5 per run, all acted on); A's acted-on count was 14 in all three runs, E's 10.
- **C relabelled nitpicks under allowed names in every run** (run 2: "resource exhaustion" from an uncapped `uids` list, "may leak payment data" in a log line, "stale rates" as data integrity; run 3: the same `uids` one, non-transactional reads as concurrency, path traversal on `out_path`, stale rates). E had none in any run. The two examples the article names ("CSV formula injection" on a numeric column, "impersonation risk" from a name collision) are from run 1 only.
- E is the steadiest prompt: 19–20 comments, the same per-diff counts in runs 2 and 3.

What didn't hold, or moved
- **The scope line's effect on the mix is small but not zero.** In run 1 C's low-value share equalled A's (61 vs 62%); in runs 2 and 3 it was 13 and 8 points below A in the same run. Against the pre-registered 62% anchor C never reaches the 10-point line (lowest 54%, 8 below), so "the scope line did not change the mix" becomes "barely changed it": C's mean 57% against A's 65% and E's 38%.
- **The scope line did not reduce wrong comments**: C had 5–6 per run, A 4–6. Run 3's C added one new kind (path traversal on a path the caller builds from a fixed directory).
- **The control diff no longer drew comments under every prompt "as many as the buggy ones".** d6 drew A 11 / 10 / 11 and B 7 / 5 / 5, in the range of the buggy diffs, but C fell to 4 and 3 in runs 2 and 3 (buggy diffs 6–9). Without the stay-quiet line it still drew 3–11 comments in every run, none worth a change; under E it drew one (wrong) comment in every run.

Labelling notes (run-1 labels were not changed)
- The repeats were labelled with the run-1 notes as the reference, so the same comment kind gets the same class (for example "N+1 batch", "in-memory billing", "idempotency key", "stale file when empty", "size<=0" stay `right_low_value` with `ambiguous=1`; "page not validated", "page beyond total", "cur unvalidated", "whitespace-only name" stay `wrong`).
- Mixed comments: when a comment's main point is true but an aside assumes unvalidated input, it is `right_low_value` with `ambiguous=1` (r3 d3-A month column; r2 d6-A normalization). This matches run 1's d5-C comment 7 (no TTL plus unbounded `cur` keys), labelled the same way. When the comment's whole premise is that handled input is unhandled, it is `wrong` (r3 d6-A leading/trailing whitespace, like run 1's d6-A "name not stripped"; r3 d3-C path traversal).
- r3 d2-B comment 6 restates the planted bug from the caller's side (the 502 branch is dead); the rules give it `acted_on` as a comment that points at the planted bug, which adds one acted-on comment to that run that is not a separate defect.
- Run-1 labels re-read against these: none looked inconsistent enough to change. One note: run 1's d1-C "authorization check" and d3-C "CSV formula injection" carry no "(security framing)" tag in their note text although they are the same kind as the repeats' tagged notes; the class is the same.

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
- E3 is 6 diffs, 3 runs per prompt for A, B, C and E (1 run for D), Python only, one model, with small single-file diffs written for the test. Three runs show which differences hold from run to run on these diffs; they are not enough for a confidence interval, and a different set of diffs could move the numbers more than the runs did. It shows how the three slices of a review pile move when context or scope changes; it is not an accuracy figure for Claude or for any review product.
- One person classified all 431 comments, with no second rater; 80 labels were close calls, placed in the lower class (run 1: 28; repeats: 52). The same judge wrote the diffs, knew the planted list and, for the repeats, knew the run-1 result.
- Planted bugs are simple and well known. 5/5 in every condition and every run means these bugs did not separate the prompts; it does not show that narrowing never costs real bugs in a large codebase.
- The scope-line and stay-quiet results (C, D, E) are from this test only; context plus the stay-quiet line together was not run, and D was not repeated. A team that narrows scope over weeks on real code (with its own vocabulary and allowed styles) may see the low-value share move differently.
- Runs are not independent draws from a fixed reviewer in any strict sense: same prompts, same model, same day, default sampling settings of `claude -p`.
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
- The article now shows condition C's scope line word for word and tells readers to add it together with the stay-quiet line, the pair tested as E. Expected size given in the body: A 53 comments → E 20 on the same six diffs (since 2026-11-19 the body gives the three-run figures, about 54 → 19 or 20; see 「Repeats」). The stay-quiet line without a scope line was not run.
- "The 80 is the README's example" left the body; the source stays in Reader fix 2 above.
- Uber's human-reviewer figure (51%, in words "about half") now appears only as a reason not to compare against 100%.

Article: [AI Code Review False Positives: What 120 Comments Showed](https://loopnotes.dev/ai-code-review-false-positives/)
