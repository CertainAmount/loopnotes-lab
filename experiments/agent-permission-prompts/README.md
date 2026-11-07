# Which Claude Code permission mode asks for what?

Headless runs of each permission mode (default, acceptEdits, auto, bypassPermissions, dontAsk) and of allow/deny rules against the same tasks: editing a file, running tests, pushing, writing outside the project, deleting a folder, reading `.env`. 85 runs on 2026-10-23, Claude Code 2.1.296, on a fresh synthetic project with a local bare remote and a fake `.env`.

Article: [Stop Claude Code, Codex, Antigravity Asking for Permission](https://loopnotes.dev/stop-coding-agent-permission-prompts/)

## Files

- `results.md`: mode x task table and rule results
- `raw/`: one JSONL stream per run

## Rerun

```
python3 harness.py probe | run C1,C2 T1,T2 [N] | summary
```

Paths in the script point to a scratch directory; change them first. Results can differ with later CLI or model versions.
