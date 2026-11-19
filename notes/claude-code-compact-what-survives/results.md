# Results: what survives /compact (Claude Code 2.1.296, claude-sonnet-5-5, 1M context window), run 2026-10-21

Harness: harness.py + make_project.py (synthetic ledger-svc). 6 seed sessions (rep0 pilot + rep1–4 main + rep5 auto), all valid (7/7 files edited in order, legacy/ untouched, seed replies followed KIWI and ROOTOK). Probes ran with every tool blocked. Scoring is regex over replies, the compaction summary (isCompactSummary message in the session JSONL) and the post-compact JSONL. Costs are per-call deltas of total_cost_usd (which is cumulative per session).

| Clue | A: /compact (N=5) | B: /compact + preserve instruction (N=4) | C: no compaction (N=4) | D: auto-compact at 5% override (N=1) |
|---|---|---|---|---|
| Chat-only rule KIWI in probe replies (P1, P2) | 5/5, 5/5 | 4/4, 4/4 | 4/4, 4/4 | 1/1, 1/1 |
| Root CLAUDE.md rule ROOTOK in probe replies | 5/5, 5/5 | 4/4, 4/4 | 4/4, 4/4 | 1/1, 1/1 |
| Subfolder billing/CLAUDE.md rule HERON (P2) | 5/5 | 4/4 | 4/4 | 1/1 |
| Edited file names recalled (P1, of 7) | 7,7,7,7,7 | 7,7,7,7 | 7,7,7,7 | 7 |
| Decision HALF_EVEN + reason SPEC-7731 | 5/5 | 4/4 | 4/4 | 1/1 |
| Failed approach + exact error E_LOCK_9472 | 5/5 | 4/4 | 4/4 | 1/1 |
| Frozen dir legacy/ + date 2026-11-30 | 5/5 | 4/4 | 4/4 | 1/1 |
| Next step tests/test_rounding.py | 5/5 | 4/4 | 4/4 | 1/1 |
| legacy/ wrongly listed as modified | 0/5 (regex hit 1, manual check: reply said "untouched") | 0/4 | 0/4 | 0/1 |
| Same clues present in the summary text itself | KIWI 5/5, HERON 5/5, 7 paths 5/5, SPEC 5/5, error 5/5, next step 5/5 | 4/4 on all | n/a | 1/1 on all |

Numbers:
- pre_tokens → post_tokens: A 82,890→5,832; 84,892→5,933; 81,270→5,642; 90,548→6,011; 88,105→5,813. B 84,892→5,840; 81,270→5,867; 90,548→3,747; 88,105→3,627. D (trigger auto) 80,639→5,949.
- Compaction duration: 21.3–27.0 s (A), 23.0–28.9 s (B), 22.9 s (D).
- Summary length: 866–1,041 words (A), 928–995 (B), 934 (D).
- Cost of the compaction call: $0.110–0.117. First probe turn after compaction: $0.058–0.071 (A/B), $0.088 (D) vs $0.280–0.315 with no compaction (C).
- File references after compaction (compact_file_reference): in every compacted run (10/10), 5 references to the docs/*.md files read last (turn 2, ~5K tokens each), each with the note "too large to include. Use Read tool if you need to access it" — path only, no content. None of the 7 edited files was re-attached in any form; report_templates.py (~7K tokens) never appeared. (Corrected 2026-10-21 after audit: earlier wording said the files were re-attached.)
- billing/CLAUDE.md: no re-injection outside the summary in any run (checked all 10 post-compact JSONLs, excluding the isCompactSummary message). The HERON rule survived because the summary text copied it (10/10). The SessionStart "compact" hook output (OWL-HOOK) appeared after compaction in 10/10. (Corrected 2026-10-21: the earlier line counted summary text as re-injection.)
- Auto memory: in 11 of 14 probe-1 replies the model said it had also written the next step to a memory note (MEMORY.md) outside the repo. It's a default Claude Code behavior and a second path for "next step" to survive; the summary carried it on its own in every run.
- Total experiment cost: $5.73 (pilot + 4 main repetitions + 1 auto). Smoke test separate ($0.28).

Limits: one synthetic project, ~80–90K tokens (8–9% of a 1M window), every clue stated explicitly in one early message, Sonnet 5.5 only, headless -p. Long multi-turn sessions where reasons are spread over many messages (the author's own failure case) were not reproduced. N is small; no percentages.
