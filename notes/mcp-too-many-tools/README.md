# How many MCP tools is too many in Claude Code, and what actually goes wrong?

Research note for the loopnotes.dev article on MCP tool overload. One experiment (we call it E4) on one Linux machine: headless Claude Code 2.1.328 talking to seven dummy stdio MCP servers, 200 runs between 2026-11-19 19:17 and 19:51 UTC, total cost $0.91. Every number below comes from `runs.csv` and `results.md` in this folder.

## Conclusions

- With tool search on (the Claude Code default), going from 10 to 100 MCP tools added about 1,130 tokens to the first turn, roughly 13 per tool; with `ENABLE_TOOL_SEARCH=false` the same step added about 7,800 (roughly 87 per tool, on short dummy definitions). Before cutting servers to save context, check whether your client loads tool definitions up front.
- Tool count alone did not break the first choice: a clean catalog of 100 tools got the right first call 15/15, the same as 10, 25 and 50. A "40 tools" rule of thumb is not a reason to remove servers on its own.
- A same-verb tool on another server never took the first call (0 of 200 runs, both models). The only misses were one request where `docs.search` was called before `docs.get_page` on the same server (Haiku at 50 and 100 tools 6/6, Sonnet at 100 tools 3/3), and every one of them reached the right tool on the next call. Look for competing names inside one server's list, not only across servers.
- With tool search on, the model chose by name: 176 of 189 ToolSearch calls were `select:<exact tool names>` from the deferred list, before any description was loaded. Under tool search, tool names carry more of the choice than descriptions.
- The fix depends on where the competing name lives: switching off the other servers left the miss in place (0/3 on that request), a 10-tool task set fixed it (3/3, 14/15 overall), and turning tool search off at 100 tools also fixed it (3/3) at the cost of about 7,800 extra tokens.

## The question

Someone with several MCP servers attached sees the agent call the wrong tool first, or the context shrink before the first prompt, and wants to know whether to remove servers and how many tools are too many. The top results (checked 2026-11-20) give a number near 40 that they cite from each other, measured before Claude Code deferred MCP tools by default. We wanted to know, in today's default setup, what tool count changes (tokens, first choice) and what it doesn't.

## Setup

- **Client**: Claude Code 2.1.328, `claude -p` with `--strict-mcp-config` (only our servers), `--setting-sources ""`, `--output-format stream-json --verbose`, `--permission-mode bypassPermissions`, built-in tools disallowed (`Bash, Read, Edit, Write, Glob, Grep, WebFetch, WebSearch, Task, Agent, NotebookEdit, TodoWrite, Skill`), an empty temporary working directory, `--max-budget-usd 0.40` per run (this version has no `--max-turns`). Each run under `systemd-run --user --scope -p MemoryMax=2G`, one Claude process at a time, on a 7.5 GB machine.
- **Tool search**: on = no environment variable (default); off = `ENABLE_TOOL_SEARCH=false`.
- **Models**: every point on `claude-haiku-5-5`. A Sonnet pilot projected about $4.2 for the full grid, over the $3 budget, so the grid moved to Haiku as planned. `claude-sonnet-5-5` was run as a cross-check at 100 lookalike tools (15 runs) and 10 lookalike tools (5 runs).
- **Servers** (`servers/server.py`, `catalog.py`): seven dummy stdio servers (`github`, `slack`, `docs`, `db`, `ci`, `flags`, `observability`). Each tool has a one-line English description and 1 to 3 arguments, logs its call to `logs/calls.jsonl` and returns a fixed "ok". Real servers usually ship longer schemas, so the per-tool token cost with tool search off is a floor.
- **Requests** (one right tool each, the request never names it):

| id | request | right tool |
|---|---|---|
| R1 | Find the recent code changes to the payments service that could explain today's outage. | `github.list_commits` |
| R2 | What did the team say about the deploy freeze? | `slack.search_messages` |
| R3 | Show me the runbook page for cache eviction. | `docs.get_page` |
| R4 | Which feature flags are on for checkout in production? | `flags.list_flags` |
| R5 | Did last night's CI run for the main branch fail? | `ci.get_run` |

- **Tool sets** (exact split per server in `config/*.json`, `config/summary.json`):
  - *clean*: the 5 right tools plus filler tools with write/admin verbs no request needs.
  - *lookalike*: the right tools plus same-verb tools on other servers (1 per request at 10 tools, 2 per request from 25 tools; e.g. for R2 `github.search_issues` and `docs.search`), the rest filler. Note that `docs.search`, a lookalike for R2, sits on the same server as R3's right tool, and is present from 25 tools up.
  - *fixa*: the 100-tool lookalike catalog with the two servers holding that request's lookalikes switched off (68 to 73 tools left).
  - *fixb*: a task set of 10 tools: the right tool plus 9 filler, no lookalikes.
- **Points**: 10/25/50/100 tools × clean/lookalike with tool search on; lookalike at 10 and 100 with tool search off; fixa and fixb with tool search on. Each point = 5 requests × 3 repeats (`batch.sh`). One run = one row in `runs.csv`.
- **Scored**: the first MCP tool called (ToolSearch excluded) against the right tool; whether the right tool was reached at all; first-turn context tokens (input plus cache read plus cache creation on the first turn); ToolSearch calls and what they returned; cost.
- **Files**: `runs.csv` (200 rows), `results.md` (generated by `results.py`), `logs/raw/<run_id>.jsonl` (stream-json per run, paths and session ids removed by `sanitize.py`), `logs/calls.jsonl`, `pilot/` (three pilot runs: two Sonnet, one Haiku, not counted in the table).

## Results

### First call and tokens per point

| model | set | tool search | tools | runs | right first call | first-turn context tokens, mean (min-max) | reached right tool |
|---|---|---|---|---|---|---|---|
| haiku | clean | on | 10 | 15 | 15/15 | 16,480 (16,476-16,488) | 15/15 |
| haiku | clean | on | 25 | 15 | 15/15 | 16,665 (16,659-16,672) | 15/15 |
| haiku | clean | on | 50 | 15 | 15/15 | 16,981 (16,978-16,987) | 15/15 |
| haiku | clean | on | 100 | 15 | 15/15 | 17,609 (17,605-17,616) | 15/15 |
| haiku | lookalike | on | 10 | 15 | 15/15 | 16,475 (16,471-16,483) | 15/15 |
| haiku | lookalike | on | 25 | 15 | 15/15 | 16,658 (16,648-16,693) | 15/15 |
| haiku | lookalike | on | 50 | 15 | 12/15 | 16,971 (16,967-16,979) | 15/15 |
| haiku | lookalike | on | 100 | 15 | 12/15 | 17,602 (17,597-17,609) | 15/15 |
| haiku | lookalike | off | 10 | 15 | 15/15 | 29,398 (29,393-29,405) | 15/15 |
| haiku | lookalike | off | 100 | 15 | 15/15 | 37,195 (37,190-37,203) | 15/15 |
| haiku | fixa | on | 68-73 | 15 | 11/15 | 17,235 (17,217-17,258) | 14/15 |
| haiku | fixb | on | 10 | 15 | 14/15 | 16,487 (16,475-16,498) | 14/15 |
| sonnet | lookalike | on | 10 | 5 | 5/5 | 15,651 (15,648-15,659) | 5/5 |
| sonnet | lookalike | on | 100 | 15 | 12/15 | 16,778 (16,774-16,783) | 15/15 |

### Tokens per added tool (10 to 100, Haiku)

- clean, tool search on: 16,480 → 17,609 (+1,130, about 13 per tool)
- lookalike, tool search on: 16,475 → 17,602 (+1,127, about 13 per tool)
- lookalike, tool search off: 29,398 → 37,195 (+7,797, about 87 per tool)
- Sonnet, lookalike, on: 15,651 → 16,778 (+1,127, same slope)

The spread between repeats was tens of tokens, far below the gap between points. The roughly 13,000-token gap between "off, 10 tools" and "on, 10 tools" is not MCP: with tool search off, Claude Code's own deferred built-in tools (about 15, such as Cron and Worktree) are also loaded, as the init tool list shows.

### Where wrong first calls went

All 14 wrong first calls:

| model | set | tools | request | right tool | first tool | runs |
|---|---|---|---|---|---|---|
| haiku | lookalike, on | 50 | R3 | `docs.get_page` | `docs.search` | 3 |
| haiku | lookalike, on | 100 | R3 | `docs.get_page` | `docs.search` | 3 |
| sonnet | lookalike, on | 100 | R3 | `docs.get_page` | `docs.search` | 3 |
| haiku | fixa, on | 69 | R3 | `docs.get_page` | `docs.search` | 3 |
| haiku | fixa, on | 71 | R1 | `github.list_commits` | no tool call (asked for the repo name) | 1 |
| haiku | fixb, on | 10 | R1 | `github.list_commits` | no tool call (asked for the repo name) | 1 |

- Other tool on the same server: 12. No tool call: 2. Same-verb tool on another server: 0.
- R3 with `docs.search` present but answered right: 25 lookalike tools on (3/3), 100 lookalike tools with tool search off (3/3).
- Per request, Haiku, tool search on, all sizes: every request 12/12 in both sets except R3 in the lookalike set, 6/12.
- The two "no tool call" runs happened only in the fix sets; the other 30 Haiku R1 runs all called `list_commits`.
- Some runs first tried a disallowed built-in tool (refused); this does not change the first-MCP-call score.

### How ToolSearch picked tools

Of 189 ToolSearch calls with tool search on, 176 were `select:<names>` (exact names taken from the deferred tool list) and 13 were keyword searches. All 9 R3 misses outside the fix sets fetched `select:mcp__docs__search,mcp__docs__get_page` together and then called `search` first. The model picked from the name list; descriptions arrived only after the pick.

## Official pages compared (read 2026-11-20)

| page | what it says that bears on this question |
|---|---|
| [Claude Code docs: Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) | Tool search is on by default; it is absent with `ENABLE_TOOL_SEARCH=false` and, on Google Cloud Agent Platform, with models older than Opus 4.5 / Sonnet 4.5 / Haiku 4.5; servers can be switched off in `/mcp` or with `disabledMcpServers`; a full tool name over 128 characters can't be used. We read the first 100,000 characters of the page; the `auto` threshold and `alwaysLoad` definitions further down were not confirmed from it. |
| [Claude Agent SDK: Tool search](https://code.claude.com/docs/en/agent-sdk/tool-search) | In `auto` mode the deferrable definitions are summed and compared to a threshold; tools marked `alwaysLoad` are excluded (search snippet). |
| [Anthropic Engineering: Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) | Anthropic's own MCP evaluation with the Tool Search Tool: Opus 4 49% → 74%, Opus 4.5 79.5% → 88.1%; about 85% fewer definition tokens; recommended from 10+ tools or 10K+ definition tokens (search snippet). |
| [Anthropic Engineering: Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Too many or overlapping tools distract agents; namespace by service or resource prefix (search snippet). |
| [OpenAI: Function calling guide](https://developers.openai.com/api/docs/guides/function-calling) | A soft suggestion of fewer than 20 functions at the start of a turn (read 2026-11-01). |

Tool search settings beyond on/off (`auto`, `auto:N`, `alwaysLoad`, reports of a raised `auto` threshold on 1M-context models) were left out of the article: we did not confirm them from the official page and did not test them.

## Other people's posts (as found 2026-11-20)

- [archestra: How many MCP tools is too many?](https://archestra.ai/blog/how-many-mcp-tools-too-many): from the search snippet, frontier models degrade around 40 tools; the page returned 404 when fetched.
- [getunblocked: MCP Tool Overload](https://getunblocked.com/blog/mcp-tool-overload/): a 30 to 40 always-loaded tool ceiling, and states that no clean before/after measurement of tool search exists.
- [alphasignal: Why your MCP server picks the wrong tool](https://alphasignalai.substack.com/p/why-your-mcp-server-picks-the-wrong): five design patterns (snippet only).
- [Speakeasy: Best practices for using MCP tools](https://www.speakeasy.com/mcp/using-mcp/using-tools.md): notes some models ignore tools beyond about 40.
- [Cursor forum: CLI MCP tool limits](https://forum.cursor.com/t/cli-mcp-tool-limits/165642): the CLI message "Too many MCP tools are enabled for this model" and a reply that the cap is per model (forum, not an official doc; we did not test Cursor).
- [Cursor forum: MCP tools name collision](https://forum.cursor.com/t/mcp-tools-name-collision-causing-cross-service-tool-call-failures/70946): user reports of cross-service tool call failures from colliding names.

No Naver data was collected: this is an English-language developer question with no Korean angle that would change the reader's decision.

## Limits

- One machine, one Claude Code version (2.1.328), one day. Tool search defaults change between versions; rerun before relying on the numbers for a later version.
- Haiku 5.5 for every point; Sonnet 5.5 only at two points (20 runs). Other clients (Cursor, VS Code, others) were not tested.
- Dummy tools with one-line descriptions and fixed "ok" replies. Real servers have longer schemas (higher token cost with tool search off) and real results that can steer later calls.
- Five requests, 3 repeats per point. The only first-call miss came from one request (R3), consistent across 2 sizes, 2 models and the fixa set, but it is one request: it shows that a same-server search tool can be picked before the lookup tool, not how often that happens in general.
- "Lookalike" here means a same-verb tool on another server. The experiment does not show that cross-server name collisions are harmless in general, only that these ones did not take the first call.
- First-turn tokens are the sum of input, cache read and cache creation on the first turn; they measure context loaded, not money spent.

## Moved from the article (reader fix r1, 2026-11-20)

The article keeps only the conclusions; these details now live here.

- Test setup in full: Claude Code 2.1.328, run headless on a Linux machine on November 19, 2026; Claude Haiku 5.5 at every point, Sonnet 5.5 rechecking two points (lookalike set, 10 and 100 tools); seven dummy MCP servers with one-line descriptions and at most three arguments; five requests, three repeats at each Haiku point.
- Per-tool slope: about 13 tokens per added tool with tool search on (roughly one long name), about 87 per tool with it off (one-line dummy definitions; real schemas cost more).
- Exact-name picking: 176 of 189 ToolSearch calls were `select:<names>`, so naming tools before any description arrived was the normal path, not a quirk of the runbook request.
- Author's own `/context` reading (author interview): with the Claude Docs, Gmail and Notion connectors plus two small servers, a hundred-plus tools, the MCP tools line sat around 10% to 15% of the context when everything loaded up front; with tool search it reads about 1k to 3k tokens.
- Gateway scene detail (author interview): with close to 50 tools visible, deploy history came fourth or fifth in the call order.

### How to read the first MCP tool call from a headless run

Tested on the raw logs in `logs/raw/` (2026-11-20): `100-lookalike-R3-on-1.jsonl` prints `mcp__docs__search`, `100-clean-R3-on-1.jsonl` prints `mcp__docs__get_page`, matching `runs.csv`. Filtering on the `mcp__` prefix skips ToolSearch and any refused built-in tool, the same rule `run.py` scores by.

```
claude -p "<request>" --output-format stream-json --verbose \
  | jq -r 'select(.type=="assistant") | .message.content[]?
      | select(.type=="tool_use" and (.name|startswith("mcp__"))) | .name' \
  | head -n 1
```

### Where `ENABLE_TOOL_SEARCH` can be set (read 2026-11-20)

- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp): unset means all MCP tools are deferred and loaded on demand; `false` loads all up front; example `ENABLE_TOOL_SEARCH=false claude`.
- [Settings files and precedence](https://code.claude.com/docs/en/settings): an `env` block inside a settings file is an ordinary key and follows the settings levels, so the variable can also come from `~/.claude/settings.json` or the project's `.claude/settings.json`.

## Moved from the article (reader fix r2, 2026-11-20)

- Models: Claude Haiku 5.5 ran every point; Sonnet 5.5 rechecked the lookalike set at 10 and 100 tools, and at 100 tools it opened the runbook request with the same `select:mcp__docs__search,mcp__docs__get_page` query and called `search` first on every repeat (3/3), like Haiku at 50 and 100.
- Repeats behind "every time" in the article: clean 100-tool set 15/15 first calls right; tool search off at 100 tools, runbook request 3/3; Haiku lookalike set at 50 and 100 tools, runbook request 0/3 each.
- Author's `/context` reading with tool search on (author interview): the MCP tools line reads about 1k to 3k tokens with the Claude Docs, Gmail and Notion connectors plus two small servers. The article now keeps this reading in words only, so the one percentage it gives (the Gradle scene, above 10% to about 2% to 3%) is not compared against a token count.
- Notion deny scene (author interview): about ten write tools on the Notion connector are denied, for example `mcp__claude_ai_Notion__notion-create-pages`.

### Where to see MCP calls in an interactive session (read 2026-11-20)

- [Interactive mode](https://code.claude.com/docs/en/interactive-mode): `Ctrl+O` toggles the transcript viewer, which "shows detailed tool usage and execution" and "expands lines that collapse by default, such as MCP calls, shown as a single `Called slack 3 times` line". The collapsed line names the server; the page does not say whether the full `mcp__<server>__<tool>` name is printed, so the article points to the print-mode jq check for the exact name.

### Threshold for clients that load every definition up front (read 2026-11-20)

- [Connect Claude Code to tools via MCP, Configure tool search](https://code.claude.com/docs/en/mcp#configure-tool-search): `ENABLE_TOOL_SEARCH=auto` is "Threshold mode. Tools that would otherwise be deferred load upfront while their definitions total under 10% of the context window. At 10% or more, tool search turns on"; `auto:N` sets a custom percentage. The article uses Anthropic's 10% as the point to act for a reader whose client loads every definition.

### Where a deny rule can live (read 2026-11-20)

- [Configure permissions, Settings precedence](https://code.claude.com/docs/en/permissions#settings-precedence): "a user-level deny blocks a project-level allow, because deny rules from any scope are evaluated before allow rules"; "To apply permission rules across all your projects, add them to your user settings instead: `~/.claude/settings.json`".

### Moved from the article in reader fix 3 (2026-11-20)

- Test setup line removed from the body: Claude Code 2.1.328, seven dummy MCP servers (full setup above under "Test setup in full"). The body keeps only "each tool described in one line", the condition that limits the token figures.
- Team gateway scene: the session showed close to 50 tools before it was cut to about ten (author interview). The body now says "with every tool in view".

### What the `/context` MCP lines look like (run on this machine, 2026-11-20)

`claude -p "/context"` with Claude Code 2.1.328 (model claude-sonnet-5-5, 1M window) and the Claude Docs, Gmail and Notion connectors connected printed, among its category rows:

| Category | Tokens | Percentage |
|---|---|---|
| MCP tools | 677 | 0.1% |
| MCP server instructions | 1.1k | 0.1% |
| MCP tools (deferred) | 122.8k | 12.3% |

The session total was 15.4k tokens (2%), so the deferred row is not counted in what each request carries. Two later runs the same evening started before the connectors connected and printed no MCP rows; the article quotes the first run. This agrees with the author's reading (author interview): around 10% to 15% of the context when everything loaded up front, about 1k to 3k tokens with tool search on (677 + 1.1k here).

### Which models run without tool search (read 2026-11-20)

- [Connect Claude Code to tools via MCP, Configure tool search](https://code.claude.com/docs/en/mcp#configure-tool-search): "Claude Code uses tool search on Claude Opus 4, Claude Sonnet 4, Claude Haiku 4.5, and later models, or Opus 4.5, Sonnet 4.5, Haiku 4.5, and later models on Google Cloud's Agent Platform. On earlier models, Claude Code loads all MCP tools upfront, and `ENABLE_TOOL_SEARCH=true` doesn't override this." The same page also lists Microsoft Foundry deployments hosted on Azure, `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` and HIPAA-configured sessions as running without tool search; the article names only the model condition (an edge case off the target reader's path otherwise).

Article: [Too Many MCP Tools? How Many Is Too Many in Claude Code](https://loopnotes.dev/mcp-too-many-tools/)
