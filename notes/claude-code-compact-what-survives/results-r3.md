# E-C2 (round 3, 2026-11-20): does who said a fact decide whether it survives /compact?

Claude Code 2.1.328, model `sonnet` (Sonnet 5.5), headless `claude -p --resume`, one claude process at a time under a 2 GB memory scope. Cost cap $2.00; spent $2.01 (the cap stopped the second tool-output-only run).

## Setup

`make_project_r3.py` builds a small ledger service where some answers can only be found by reading files or running a command. `harness_r3.py` runs one 7-turn seed session that plants 12 facts through different channels:

| Fact | Channel | How it entered |
|---|---|---|
| U1 start replies with `KIWI:` | you typed | turn 1 |
| D end replies with `-- ROOTOK` | root CLAUDE.md | disk |
| U2 drop the cache layer: invalidation can't be timed with the nightly import | you typed (drop reason) | turn 5 |
| U3 nightly import starts at 02:10 UTC | you typed (value) | turn 4 |
| A1 root cause: `legacy/money.py` line 42 rounds ROUND_HALF_UP | Claude worked out from files (you only asked "why?") | turn 2 |
| A2 payout writer `retry = 7` | Claude found in config (you only asked) | turn 3 |
| T1 three failing test names | test output (Claude also listed them in a one-line reply) | turn 4 |
| T2 error code RECON-E-6604 | test output | turn 4 |
| RU refunds HALF_UP → HALF_EVEN because SPEC-8802 | your reversal, reason typed | turns 3 → 7 |
| RC payouts: end-of-day batch → write inside the settlement transaction | Claude proposed the switch from a doc, you said "fine, go with that." | turns 1 → 5–6 |
| A3 why the batch was dropped (reconciliation reads in the same transaction) | Claude's reason | turn 5 |
| E five edited files | edits | turn 7 |

Seed: 78,118 tokens at compaction; all five edits made; `git diff` shows exactly the five files.

Branches forked from the same seed: A plain `/compact` ×3, B `/compact Keep abandoned directions with their reasons, every file path you edited, and the names of failing tests.` ×2, C no compaction ×1. Two probe turns each, every tool blocked. First pass by regex, then every cell read by hand.

Add-on (`harness_r3t.py`): a 3-turn session (49,833 tokens) where the test run's reply was limited to the count ("3"), so the test names lived only in tool output, followed by more file reads. One `/compact` and one probe.

## Results

| Fact | A1 | A2 | A3 | B1 | B2 | C (no compaction) |
|---|---|---|---|---|---|---|
| U1 chat rule | kept | kept | kept | kept | kept | kept |
| D root CLAUDE.md rule | kept | kept | kept | kept | kept | kept |
| U2 your drop reason | kept | kept | kept | kept | kept | kept |
| U3 your value 02:10 UTC | kept | kept | kept | kept | kept | kept |
| A1 root cause Claude found | kept | altered | kept | altered | altered | kept |
| A2 config value Claude found | kept | kept | kept | kept | kept | kept |
| T1 failing test names | kept | kept | kept | kept | kept | kept |
| T2 error code | kept | kept | kept | kept | kept | kept |
| RU your reversal + reason | kept | kept | kept | kept | kept | kept |
| RC Claude-proposed switch | kept | kept | kept | kept | kept | kept |
| A3 Claude's drop reason | kept | kept | kept | kept | kept | kept |
| E edited paths (5 of 5) | kept | kept | kept | kept | kept | kept |

The only "altered" cells: the root cause kept its file, function and mechanism in every run, but the line number blurred in 3 of 5 compactions (B1 gave no line; A2 and B2 said they no longer trusted "42"). The control and A1/A3 gave lines 40-42.

Tool-output-only add-on (TA1): the reply had said only "3", yet the summary listed all 3 test names and RECON-E-6604, and the probe answered them correctly. The summarizer reads tool output, not only chat messages.

## Also recorded

- Summary shape: all 6 summaries had the same nine numbered sections as round 1 (Primary Request and Intent, Key Technical Concepts, Files and Code Sections, Errors and fixes, Problem Solving, All user messages, Pending Tasks, Current Work, Optional Next Step). Length 1,023–1,234 words (A/B), about 1,000 in TA1.
- Tokens: 78,118 → 15,347–15,693 after compaction (round 1 on 2.1.296: about 85K → 5.8K). `compact_metadata` now also carries `preserved_segment` / `preserved_messages`: one message kept verbatim across the boundary.
- Re-attached files: in 5 of 5 compactions the five edited files came back with full content. In this seed the edits were also the last files Claude touched, so this run does not separate "last read" from "last modified"; round 1 (edits first, then large docs read) re-attached the docs read last and none of the edits.
- Preservation instruction (B): no fact moved from lost to kept, because nothing was lost in A; the two B runs were the two that dropped or hedged the line number.
- Cost per call: compaction $0.057–0.063; first probe after compaction $0.108–0.117 vs $0.265 without compaction.

## Conclusions

1. On 2.1.328, in sessions of 50–78K tokens, compaction kept every fact we planted, at the same level as no compaction: rules and values you typed, the root cause and config value Claude worked out, Claude's own reasons and its proposed switch, both reversals, and test names that appeared only in tool output. Who said a fact did not decide whether it survived.
2. The one thing that blurred was precision inside a Claude finding: the exact line of the root cause (3 of 5 compactions), while the file and the cause stayed.
3. With round 1 (2.1.296, 10 of 10), that is 16 compactions across two versions with no planted fact lost. Losses like the author's (failing test names turned into "a few", a dropped approach coming back) happened in sessions of an hour and a half or more; this experiment did not reach that size.

## Limits

One synthetic project, one seed forked 5 times (variance of the summarizer, not of sessions), Sonnet 5.5, headless, 50–78K tokens of a 1M window. Counts only; no percentages.

Files: `make_project_r3.py`, `harness_r3.py`, `harness_r3t.py`, `results-r3-rows.json` (fact × run, with manual notes), `raw-r3/` (stream logs, post-compact JSONL), `summaries-r3/` (6 summaries).
