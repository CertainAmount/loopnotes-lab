# Does the Karpathy CLAUDE.md change Claude Code?

A/B test: a 3-line project CLAUDE.md versus the same lines plus the Karpathy-style CLAUDE.md, 5 tasks x 2 conditions x 6 runs (60 scored runs, 2026-10-20, Claude Code 2.1.296, Sonnet 5.5). The reading rule (3+ of 6 = changed) was fixed before the runs.

Article: [Karpathy CLAUDE.md Tested: Does It Change Claude Code?](https://loopnotes.dev/karpathy-claude-md-tested/)

## Files

- `results.md`: results by task and the reading rule
- `claude-md/control.md`, `claude-md/karpathy-fetch.txt`: the control file, and the URL, commit and sha256 of the Karpathy file (the file itself has no license, so it is not copied here; fetch it from that commit and append it to `control.md` after one blank line to rebuild `k4.md`)
- `tasks.json`, `conditions.json`, `sample-project/`: inputs
- `raw/`: one JSONL stream per run

## Rerun

```
python3 harness.py run [--only COND_ID] [--max-runs K]
```

Paths in the script point to a scratch directory; change them first. Results can differ with later CLI or model versions.
