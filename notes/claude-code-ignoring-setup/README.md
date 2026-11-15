# When Claude Code seems to ignore CLAUDE.md, skills or hooks, which layer actually missed?

Research note for the loopnotes.dev hub post on Claude Code ignoring your setup. Compiled 2026-11-15 from four earlier measurements on one Linux machine plus one small new check run that day. Every count below was re-read from the raw result files of each measurement, not copied from the posts that used them.

## Conclusions

1. In every run where a CLAUDE.md rule was actually in context, Claude Code followed it (45 of 45 runs, including a rule buried on line 228 of a 309-line file and a rule that contradicted the user's own request), so a reader whose rule "gets ignored" should first check that the file loaded (`/context`, `/memory`) before shortening or rewording it.
2. The skill misses we recorded came only from requests that never named the job: 9 of 15 called the skill as the first tool, 4 called it late and 2 never called it, while 30 of 30 requests that named the job called it with all three descriptions, so a reader should look for the `Skill(...)` call and invoke the skill by `/name` when the output format matters, rather than rewriting the description first.
3. A subfolder `CLAUDE.md` arrived only after Claude Code had touched that folder: on 2.1.322, files written before anything in the folder was read lacked the rule at first (0 of 4), and files written after reading a file there had it from the start (4 of 4), so a rule needed on the very first file belongs in the root `CLAUDE.md` or needs a read in that folder first.
4. After `/compact`, the root CLAUDE.md rule and a rule given only in chat were both still followed in 10 of 10 compacted runs, and a SessionStart hook with matcher `compact` printed its output in 10 of 10, so a reader who "lost rules after compact" should check whether the lost instruction ever lived in a file before adding a re-injection hook.
5. None of our runs showed the two causes readers usually suspect first, a loaded rule dropped because the file was long or the rule sat deep in it, and the user's request overriding a CLAUDE.md prohibition; the scope that limits this is short single-task sessions on tiny repos, so long multi-turn sessions remain unmeasured.

## Layer table

| Layer | What we asked | Loaded / called? | Followed (N) | Date, version, model |
|---|---|---|---|---|
| CLAUDE.md, one rule per file (JSDoc, snake_case, no `git commit`, run tests, reply in Korean, don't edit `legacy/`) | short coding tasks that tempt the opposite | loaded (project CLAUDE.md) | 30/30 (6 rules x 5) | 2026-10-19, 2.1.296, claude-sonnet-5-5 |
| Same, rule near the top vs buried | `// reviewed: claude` rule on line 6 of a 308-line file vs line 228 of a 309-line file | loaded | 5/5 and 5/5 | same |
| Same, rule vs the user's own request | "commit the fix" vs "never run `git commit`" | loaded | 5/5 (0 commits) | same |
| Control: same tasks, no rule | | n/a | rule behaviour absent in 11 of 12 control checks | same |
| CLAUDE.md, general principles file (Karpathy-style, 65 lines) | 5 tasks x 6 runs vs control | loaded | behaviour changed only where the request was ambiguous (asked first 0/6 -> 3/6); surgical bug fix 6/6 with and without the file | 2026-10-20, 2.1.296, claude-sonnet-5-5 |
| Skill, request names the job (3 different descriptions) | "release notes", "what changed", "summarise CHANGES.txt" | called | 30/30 (29 as the first tool, 1 after Bash and Read) | 2026-11-12, 2.1.317, claude-sonnet-5-5 |
| Skill, request never names the job | "what should we tell customers about 1.5?" x 3 descriptions | first tool 9/15, late 4/15, never 2/15 | output format followed 13/15 | same |
| Skill + one CLAUDE.md line / + 40 dummy skills installed | keyword and no-keyword requests | called | 10/10 and 10/10 | same |
| After `/compact`, root CLAUDE.md rule | probe questions after manual (9) or auto (1) compaction | re-read from disk (official behaviour) | 10/10 | 2026-10-21, 2.1.296, claude-sonnet-5-5 |
| After `/compact`, rule given only in chat | same | carried by the compaction summary | 10/10 | same |
| After `/compact`, subfolder `billing/CLAUDE.md` rule | same | re-injected 0/10; survived because the summary copied it 10/10 | 10/10 | same |
| After `/compact`, SessionStart hook with matcher `compact` | same | hook output present | 10/10 | same |
| Subfolder `CLAUDE.md`, new check (below) | create two files in `src/test/` without reading anything there first | loaded only after the first writes | first writes 0/4 had the rule; both runs then edited the files to comply (4/4 final) | 2026-11-15, 2.1.322, claude-haiku-5-5 |
| Subfolder `CLAUDE.md`, read a file there first | same, after reading `src/test/helpers.js` | loaded before writing | 4/4 from the first write | same |

Sources of the rows: the CLAUDE.md rule rows come from the results table behind [our CLAUDE.md rule test](https://loopnotes.dev/claude-code-claude-md-rules-test/) (57 scored `claude -p` runs); the principles-file row from the results behind [our Karpathy CLAUDE.md test](https://loopnotes.dev/karpathy-claude-md-tested/); the skill rows from the per-run file in the [skill-triggering research note](https://github.com/CertainAmount/loopnotes-lab/tree/main/notes/claude-code-skill-not-triggering) (`runs.csv`, columns `axis` and `tool_sequence`); the `/compact` rows from a 2026-10-21 run on a synthetic project of about 80K to 90K tokens (compacted runs: 5 plain `/compact`, 4 `/compact` with a preserve instruction, 1 auto-compaction; 4 uncompacted controls), whose post is not published yet; the subfolder rows from the new check in this note.

Correction: an earlier summary row for the indirect-request skill runs said "Skill as first tool = 8/15". Recounting `tool_sequence` per run gives 9 first, 4 late, 2 never. A correcting row was added to the `claude-code-skill-trigger` dataset on 2026-11-15; no new runs were made for it.

## Official "Debug your configuration" causes vs what we actually saw

Official page read 2026-11-15: <https://code.claude.com/docs/en/debug-your-config>. Of the causes it lists for Claude ignoring an instruction, these showed up in our runs:

- Subdirectory `CLAUDE.md` files load on demand, not at session start: seen in the new check (rule missing on the first writes) and after `/compact` (not re-injected, carried only by the summary).
- A skill listed in `/skills` that Claude never invokes because its description doesn't match how the request is phrased: seen only for requests that named neither the job nor its words (6 of 15 late or missed); changing the description changed nothing on requests that named the job (30/30 with all three).
- Not seen in any run: a loaded rule ignored because of file length or position (rule on line 228 of 309: 5/5), or the user's request winning over a CLAUDE.md prohibition (5/5 kept the prohibition).
- Not measured: Explore and Plan subagents skipping CLAUDE.md, `omitClaudeMd`, `settings.local.json` overrides, AGENTS.md precedence, hook matcher mistakes, `permissions.deny` bypasses, long multi-turn sessions.

## New check: when does a subfolder CLAUDE.md arrive? (2026-11-15)

Why: the official memory page now says a subdirectory `CLAUDE.md` loads once Claude "reads, writes, or edits another file in that subdirectory". Earlier wording of the page (not re-fetched for this note) said subtree files were included only when Claude reads files in those subtrees. The check asks which one the current version does, and when.

Setup (`subdir-claude-md-load/run.sh` in this folder): a fresh git repo per run; a root `CLAUDE.md` with a one-line project description; `src/test/CLAUDE.md` = "the first line of every file created in src/test must be exactly: // TESTRULE-OK"; `src/test/helpers.js` and `src/main/add.js` as neutral files. Command: `claude -p --model haiku --max-turns 6 --setting-sources project --permission-mode acceptEdits --no-session-persistence`, Claude Code 2.1.322, model reported as `claude-haiku-5-5`. Full stream logs: `W1`, `W2`, `R1`, `R2` `.stream.jsonl` in the same folder.

| Run | Prompt | Tool order | First line at first Write | Final first line |
|---|---|---|---|---|
| W1 | create `src/test/add.test.js` and `add2.test.js`, don't read other files in `src/test` | Read add.js > Write x2 > Bash > Read x2 > Edit x2 | `import assert ...` (both) | `// TESTRULE-OK` (both) |
| W2 | same | Read add.js > Write x2 > Bash (sed inserts the line) > Read x2 > Edit x2 | `import assert ...` (both) | `// TESTRULE-OK` (both) |
| R1 | read `src/test/helpers.js` first, then same | Read helpers.js > Read add.js > Write x2 > Bash | `// TESTRULE-OK` (both) | same |
| R2 | same | Read helpers.js > Read add.js > Glob > Write x2 > Bash | `// TESTRULE-OK` (both) | same |

W1's reply after the writes: "The new `src/test/CLAUDE.md` rule requires every file created in `src/test` to start with `// TESTRULE-OK`, so I'm adding that line to both test files." The rule arrived as a context attachment after the write; it is not in any tool result in the stream.

Reading: on 2.1.322 a write does pull the subfolder file in, but only after that write. Files written before anything in the folder was read missed the rule at first and were fixed afterwards in both runs. Cost: about $0.02 for the 4 runs (CLI `total_cost_usd`).

## Other people's reports (links only)

- [anthropics/claude-code #18454](https://github.com/anthropics/claude-code/issues/18454): "Claude Code ignores CLAUDE.md and Skills files during multi-step tasks"; closed without a fix or measurement.
- [#4017](https://github.com/anthropics/claude-code/issues/4017), [#6354](https://github.com/anthropics/claude-code/issues/6354), [#19471](https://github.com/anthropics/claude-code/issues/19471): reports of instructions being ignored after compaction; our compacted runs above did not reproduce the loss for file-based or chat-given rules in short sessions.
- [#32184](https://github.com/anthropics/claude-code/issues/32184), [#36570](https://github.com/anthropics/claude-code/issues/36570): reports of skills never triggering in headless mode; our headless runs on 2.1.317 called the skill whenever the request named the job.

## Official pages read 2026-11-15

- Memory: <https://code.claude.com/docs/en/memory> ("Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook"; under 200 lines recommended, longer files "reduce adherence"; subdirectory files load once Claude reads, writes or edits another file there; AGENTS.md is read only when no CLAUDE.md is present, v2.1.277+; after `/compact` the project-root CLAUDE.md is re-read from disk, nested files load again on demand, conversation-only instructions are lost).
- Debug your configuration: <https://code.claude.com/docs/en/debug-your-config> (`/context` first; Explore and Plan skip CLAUDE.md, custom subagents load it unless `omitClaudeMd`; hook matching is case-sensitive; Bash deny rules match the literal command string, so a PreToolUse hook or the sandbox is the hard guarantee).
- Hooks: <https://code.claude.com/docs/en/hooks> (exit code 2 blocks a PreToolUse call and stderr is shown; `/hooks` lists configured hooks with their source; SessionStart matchers `startup`, `resume`, `clear`, `compact`, `fork`).
- Skills: <https://code.claude.com/docs/en/skills> (invoke with `/skill-name`; "Custom commands have been merged into skills", `.claude/commands/` files keep working; `disable-model-invocation: true` stops automatic use; no `/project:` prefix appears on the page).

## Limits

- Every measurement was a short session: one `claude -p` task per run (the compaction runs used one seeded session of about 80K to 90K tokens). Long multi-turn sessions, where most "it forgot my rules" reports come from, were not measured.
- Small N: 5 runs per CLAUDE.md condition (5/5 still allows a true rate well below 100%), 6 per principles-file condition, 15 indirect skill requests, 2 runs per subfolder condition.
- Tiny synthetic repos, one rule per file in most conditions; many vague or conflicting rules were not tested.
- Models and versions differ by layer (Sonnet 5.5 on 2.1.296 and 2.1.317; Haiku 5.5 on 2.1.322 for the new check), so the rows are compared by outcome, not as one controlled experiment. Haiku corrected its own files once the rule arrived; a larger task or another model may not go back.
- `permissions.deny` bypasses and hook matcher failures appear in the post as the author's own experience and official documentation, not as measurements in this note.

## Added for the post's "must never happen" steps (2026-11-15)

The post now gives the `.env` PreToolUse hook as a settings block and a script, and names the sandbox settings for a folder Claude must not edit. What these rest on:

- Hook shape: the `PreToolUse` / `matcher` / `hooks` / `type: command` structure, the `"$CLAUDE_PROJECT_DIR"/.claude/hooks/...` script path, reading stdin with `jq`, and `exit 2` with a stderr message follow the "Block edits to protected files" example in the official hooks guide (<https://code.claude.com/docs/en/hooks-guide>, read 2026-11-15); the post's version matches `Bash` and reads `.tool_input.command` instead of `.tool_input.file_path`.
- The author ran this kind of hook (Bash matcher, `.env` in `tool_input.command`, stderr then exit 2) in a scratch folder on Claude Code 2.1.322 on 2026-11-15, headless, once per matcher: lowercase `"bash"` never fired and `cat .env` printed the fake key; `"Bash"` blocked the command and Claude quoted the hook message without trying another route.
- The script as printed in the post was fed sample hook input on 2026-11-15 (shell only, no Claude session): the `node -e "...readFileSync('.env'...)"` command exited 2 with the message; `python3 read_env.py` and `ls` exited 0. That is why the post keeps the narrow key ahead of the hook: a command line that never contains `.env` passes.
- Sandbox: `/sandbox` turns it on, sandboxed shell commands can write to the working directory, the per-user temp directory and added directories by default, `sandbox.filesystem.denyWrite` blocks paths inside a writable directory, and the sandbox covers shell commands only, so Read/Edit/Write follow permission rules (<https://code.claude.com/docs/en/sandboxing>, read 2026-11-15). In project settings a `./legacy` or bare `legacy` path resolves to the project root, while Read/Edit permission rules use `/path` for project-relative (<https://code.claude.com/docs/en/settings-reference#sandbox-path-prefixes>, read 2026-11-15). The folder recipe is the author's plan for a new repository built from these pages, not a measured run.

Moved out of the post body in the same edit (reader feedback: conditions the reader skims): the version and model per table row (in the layer table above), the principles-file counts (asked first 0/6 -> 3/6; bug fix 6/6 with and without; row above), the deny-list test date and version (2026-10-13, 2.1.296), and the length of the off-track detour after an auto-compaction (five to ten minutes, author's recollection).

Article: [Claude Code Ignores CLAUDE.md or Skills? Where to Look First](https://loopnotes.dev/claude-code-ignoring-setup/)
