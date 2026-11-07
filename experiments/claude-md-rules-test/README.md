# Does Claude Code follow CLAUDE.md rules?

Eight rule types (style, naming, a forbidden command, a test-before-done workflow, reply language, a file boundary, rule position in a long file, and a rule that conflicts with the prompt), each run 5 times with `claude -p` on a tiny Node project, plus no-rule controls. 57 scored runs on 2026-10-19, Claude Code 2.1.296, Sonnet 5.5. Compliance is checked mechanically from git, test logs and tool calls, not from the reply.

Article: [Claude Code Not Following CLAUDE.md? I Tested It 57 Times](https://loopnotes.dev/claude-code-claude-md-rules-test/)

## Files

- `results.md`: summary table and limits
- `conditions.json`, `tasks.json`, `claude-md/`, `sample-project/`: exact inputs
- `raw/`: one JSONL stream per run
- `smoke/`: one excluded run, kept for transparency

## Rerun

```
python3 harness.py run [--only COND_ID] [--max-runs K]
```

Paths in the script point to a scratch directory; change them first. Results can differ with later CLI or model versions.
