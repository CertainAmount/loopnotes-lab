# Claude Code skill auto-trigger rate

How often does Claude Code call a matching skill on its own, by description wording and request wording?

## Latest per item

| Item | Value | Measured | Source |
|---|---|---|---|
| headless D1 + CLAUDE.md line, all requests | 10/10 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |
| headless D1 far-wording requests | 4/5 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |
| headless D1 keyword requests | 5/5 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |
| headless D1 no-keyword requests | 5/5 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |
| headless D2 far-wording requests | 5/5 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |
| headless D2 keyword requests | 5/5 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |
| headless D2 no-keyword requests | 5/5 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |
| headless D3 + 40 dummy skills, all requests | 10/10 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |
| headless D3 far-wording requests | 4/5 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |
| headless D3 keyword requests | 5/5 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |
| headless D3 no-keyword requests | 5/5 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |
| headless far-wording, Skill as first tool | 8/15 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |
| interactive D3 no-keyword requests | 5/5 calls/runs | 2026-11-12 | content/en/03-reviewed/claude-code-skill-not-triggering-evidence/runs.csv (Claude Code 2.1.317, claude-sonnet-5-5) |

## Method

claude -p stream-json + interactive transcript, count Skill tool_use per prompt

## Files

- `observations.csv`: 13 rows, one per measurement (date, item, value, unit, source)

## Articles that use it

- https://loopnotes.dev/claude-code-skill-not-triggering/
