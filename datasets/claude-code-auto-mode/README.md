# Claude Code auto mode: where it takes effect

Which way of asking for auto mode actually starts a Claude Code session in auto, per version, and what the session shows when it doesn't?

## Latest per item

| Item | Value | Measured | Source |
|---|---|---|---|
| 2.1.326 headless | --permission-mode auto + project disableAutoMode disable | default mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 headless | --permission-mode auto | Haiku 4.5 | default mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 headless | --permission-mode auto | Haiku 5.5 | auto mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 headless | none (user default bypassPermissions) | bypassPermissions mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 headless | project .claude/settings.json defaultMode auto | default mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 headless | project .claude/settings.local.json defaultMode auto | default mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 headless | user defaultMode auto + project defaultMode auto | auto mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 headless | user ~/.claude/settings.json defaultMode auto | auto mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 interactive | --permission-mode auto + project disableAutoMode disable | manual mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 interactive | --permission-mode auto | Haiku 4.5 | manual mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 interactive | --permission-mode auto | Haiku 5.5 | auto mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 interactive | auto session, /model switched to Haiku 4.5 | manual mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 interactive | none (user default bypassPermissions) | bypassPermissions mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 interactive | project .claude/settings.json defaultMode auto | auto mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 interactive | project .claude/settings.local.json defaultMode auto | auto mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |
| 2.1.326 interactive | user ~/.claude/settings.json defaultMode auto | auto mode | 2026-11-17 | loopnotes-lab research note claude-code-auto-mode-not-working (Run 1/2/2b) |

## Method

Fresh empty git repo per case on Linux; headless: claude -p with stream-json, permissionMode read from the system/init event; interactive: pty-driven session, status line and Shift+Tab cycle read from the rendered screen. User-level defaultMode is bypassPermissions unless the case says otherwise. One run per case.

## Files

- `observations.csv`: 16 rows, one per measurement (date, item, value, unit, source)

## Articles that use it

- https://loopnotes.dev/claude-code-auto-mode-not-working/
