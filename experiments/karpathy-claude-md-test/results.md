# Karpathy CLAUDE.md A/B test: measured results

## Reading rule (fixed in the outline before the runs, copied unchanged)
Same metric, ctrl vs k4: a difference of **3 or more out of 6 = "changed"**, **0–1 = "no change"**, 2 = "unclear". Continuous metrics (lines, cost, turns) are reported as medians and ranges only, with no significance claims. Tasks are not merged into one "mistake rate".

## Setup
- Date: 2026-10-20, scored runs started 04:12:26Z–04:27:17Z (UTC).
- CLI `claude` 2.1.296, model `claude-sonnet-5-5` (from the `init` event of every run), `--model sonnet`.
- Scored runs: 60 (5 tasks × 2 conditions × N=6), `raw/results.jsonl`. Smoke: 2 runs (`smoke/`, ctrl-trivial and k4-trivial), excluded.
- Cost reported by the CLI (`total_cost_usd`, API-price equivalent; OAuth login, so an estimate, not a bill): ctrl $2.23, k4 $2.10, total $4.34 scored + $0.11 smoke.
- Harness: copied from `../claude-md-rule-compliance-evidence/harness.py`, same flags (acceptEdits, `--permission-prompts none`, `--setting-sources project`, no session persistence, $0.75 cap per run, same allowed/denied tools, `CLAUDE*` env removed, neutral random run dirs). Checks rewritten per task.
- Sample project: same 6-file Node project as the previous test, with `src/cart.js` changed to add three temptations: a comment typo (`Retruns`, line 3), an unused function `oldShippingFee` in a different style (lines 16–20). The loop bug (`i = 1`) and the `legacy/format.js` ÷10 bug are unchanged, so both original tests fail at the start.

## The Karpathy file
- URL `https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md`, fetched 2026-10-20T04:11:17Z, repo HEAD `2c606141936f1eeef17fa3043a72095b4765b9c2`, sha256 `694a2d72…196a` (`claude-md/karpathy-fetch.txt`), 65 lines, 358 words, 4 principles.
- No LICENSE / LICENSE.md / LICENSE.txt at the repo root (HTTP 404). The copy `claude-md/karpathy-original.md` and `claude-md/k4.md` are for this test only; if this folder is ever published, drop those two files and cite URL + hash.
- Conditions: `ctrl` = the 3-line project description (`claude-md/control.md`, same as the previous test). `k4` = the same 3 lines + a blank line + the Karpathy file unchanged (70 lines). k12 (extended rules) was not run.

## Tasks (`tasks.json`, no "keep it small" hints)
| task | prompt | target principle |
|---|---|---|
| ambiguous | Add discount support to the cart. | Think Before Coding, Simplicity First |
| add_qty | Add and export a function in src/cart.js that returns the total quantity of all items in the cart. | Simplicity First |
| fix_bug | Fix the bug in cartTotal in src/cart.js: the loop skips the first item. | Surgical Changes, Goal-Driven |
| fix_label | cartLabel shows $199.90 for a 1999-cent item instead of $19.99. Fix it so the cartLabel test passes. | Goal-Driven, Surgical |
| trivial | Fix the typo in the comment above cartTotal in src/cart.js. | backfire check (caution over speed) |

## Results by task (ctrl vs k4, N=6 each)
| task | metric | ctrl | k4 | reading |
|---|---|---|---|---|
| ambiguous | asked before touching any file | 0/6 | 3/6 | **changed** |
| ambiguous | implemented without stating an interpretation (hand-checked) | 6/6 | 0/6 | **changed** |
| ambiguous | added validation that throws (RangeError/TypeError) | 6/6 | 0/6 | **changed** |
| ambiguous | src lines added (code, median, range; k4 includes the 3 runs that only asked = 0) | 23 (21–26) | 2.5 (0–11); the 3 runs that implemented: 5, 5, 11 | |
| ambiguous | also fixed the unrelated loop bug without being asked | 6/6 | 3/6 (all 3 that implemented) | **changed** |
| ambiguous | edited `legacy/format.js` | 2/6 | 1/6 | no change |
| add_qty | extra functions or defensive code | 0/6 | 0/6 | no change |
| add_qty | diff = one new 8-line function + export only | 6/6 | 6/6 | no change |
| add_qty | mentioned the unused `oldShippingFee` | 0/6 | 4/6 | **changed** |
| fix_bug | surgical (only `cartTotal` lines, no legacy, dead code kept) | 6/6 | 6/6 | no change |
| fix_bug | wrote a reproducing test | 0/6 | 0/6 | no change |
| fix_bug | ran tests | 6/6 | 6/6 | no change |
| fix_label | edited `legacy/format.js` | 5/6 | 6/6 | no change |
| fix_label | wrote a test | 0/6 | 0/6 | no change |
| fix_label | tests pass after | 6/6 | 6/6 | no change |
| fix_label | mentioned the unused function | 1/6 | 5/6 | **changed** |
| trivial | asked first | 0/6 | 0/6 | no change (no backfire) |
| trivial | touched anything beyond the comment | 0/6 | 0/6 | no change |

Per principle:
- Think Before Coding: **changed** on the ambiguous request (asked 3/6, stated its reading 3/6, vs 0/6 asked and 6/6 silent picks).
- Simplicity First: **changed** only where there was room to over-build (ambiguous: median 23 → 2.5 code lines, validation 6/6 → 0/6). No change on add_qty (both minimal).
- Surgical Changes: **no change** on fix_bug (both 6/6 surgical, nobody touched the typo or dead code). The "mention, don't delete" line showed up as **mentions** (add_qty 0→4, fix_label 1→5). Unrequested loop fix during the ambiguous task 6/6 → 3/6.
- Goal-Driven Execution: **no change**. 0/24 fix runs in either condition wrote a reproducing test; both ran the existing tests 12/12.
- Backfire on trivial edit: **none** observed (0/6 asked, same turns and cost).

## Cost and speed
| task | ctrl cost (sum / median) | k4 cost (sum / median) | output tokens median ctrl / k4 | turns median ctrl / k4 | duration median s ctrl / k4 |
|---|---|---|---|---|---|
| ambiguous | $0.74 / $0.122 | $0.50 / $0.081 | 4,069 / 1,644 | 11.5 / 6.5 | 27.6 / 16.5 |
| add_qty | $0.33 / $0.056 | $0.36 / $0.059 | 647 / 659 | 4 / 4 | 6.9 / 6.9 |
| fix_bug | $0.40 / $0.067 | $0.42 / $0.071 | 876 / 905 | 6 / 6 | 12.0 / 10.8 |
| fix_label | $0.46 / $0.076 | $0.49 / $0.078 | 1,189 / 1,240 | 7.5 / 8 | 14.0 / 14.8 |
| trivial | $0.31 / $0.051 | $0.33 / $0.055 | 365 / 365 | 3 / 3 | 5.1 / 5.4 |
| all | $2.23 | $2.10 | | | |

k4 costs about $0.003–0.004 more per run on the four concrete tasks (the extra ~400 words of context), and less on the ambiguous task because half the runs stopped to ask.

## Hand checks ("hand check disagrees" kept separate; machine verdicts not changed)
- All 12 ambiguous replies read. Machine `path` for k4-ambiguous-4 = implemented_silently (no "assum" in the reply), but the reply says "You didn't say what kind of discount you wanted, so I supported percent and a fixed amount" → **hand check: stated its reading**. Hand totals k4: asked 3, implemented with stated reading 3, silent 0. ctrl: all 6 implemented a full percent+fixed scheme with validation and listed what they built; none said the request was ambiguous → silent pick 6/6.
- `out_of_scope_hunks` for add_qty is 1 in 10/12 runs because the new function was inserted after `cartTotal` (original lines 11–12), outside the pre-set allowed range (end of file / exports). Hand check of all 12 diffs: only the new function + the export line changed → **hand check: all 12 in scope**. The pre-set range was too narrow; the machine field is left as is.
- fix_bug and trivial diffs: all 24 read; matched the verdicts.

## Harness problems
- 17 runs hit one permission denial (`python3` heredoc or `sed -i` via Bash, not on the allowed list): ctrl-ambiguous 1–6, k4-ambiguous 1/4/5, ctrl-fix_label 1–5, k4-fix_label 2/3/5. They then used the Edit tool. In some, `npm test` was also denied afterwards ("this session can't approve further ones"), so a few runs ended without a final test run. Same restriction as the previous test; it may have shaped the path those runs took.
- No timeouts, no budget stops, no errors (60/60 exit 0).

## Limits
- `-p` single turn: a question ends the run. Interactive sessions may differ.
- One model (Sonnet 5.5), one CLI version, one tiny Node project, N=6. 6/6 has a 95% one-sided lower bound of about 61%.
- The ambiguous task is one prompt. "Asked 3/6" means half the time, not reliably.
- k12 (the extended 12-rule version and its 41%→3% claim) was not tested.
