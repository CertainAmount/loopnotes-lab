# loopnotes-lab

The test harnesses and raw logs behind the hands-on articles on [loopnotes.dev](https://loopnotes.dev), a developer blog about AI coding tools, dev hardware and living with tech in Korea.

When an article says "I ran this N times", the runs are here: the script that ran them, the exact inputs, every raw log, and the results table the article quotes. Anyone can check the numbers or rerun the test.

<!-- topics:start -->
## By topic

The same folders, grouped the way the site groups its articles: each topic page lists every note, experiment and dataset behind one cluster of posts.

**Working with AI coding agents**

- [Coding agent permissions and approvals](topics/A1-coding-agent-permissions-and-approvals/): 3 research notes, 1 experiment
- [When Claude Code ignores your setup](topics/A2-when-claude-code-ignores-your-setup/): 1 research note, 2 experiments, 1 dataset
- [Running a local LLM on an RTX 4090](topics/A4-running-a-local-llm-on-an-rtx-4090/): 1 research note, 1 dataset
- [Choosing hardware for local LLMs](topics/A6-choosing-hardware-for-local-llms/): 2 research notes

**Tech in Korea, from a Seoul developer**

- [Buying tech in Korea](topics/B3-buying-tech-in-korea/): 2 research notes, 1 dataset
- [Korean phone number and verification](topics/B2-korean-phone-number-and-verification/): 1 research note
- [Getting around Korea with apps](topics/B1-getting-around-korea-with-apps/): 1 experiment

<!-- topics:end -->

**Articles and their data**

- [Claude Code Not Following CLAUDE.md? I Tested It 57 Times](https://loopnotes.dev/claude-code-claude-md-rules-test/) · [data](experiments/claude-md-rules-test/)
- [Karpathy CLAUDE.md Tested: Does It Change Claude Code?](https://loopnotes.dev/karpathy-claude-md-tested/) · [data](experiments/karpathy-claude-md-test/)
- [Stop Claude Code, Codex, Antigravity Asking for Permission](https://loopnotes.dev/stop-coding-agent-permission-prompts/) · [data](experiments/agent-permission-prompts/)
- [How to Use Naver Map in English](https://loopnotes.dev/naver-map-english-guide/) · [data](experiments/naver-map-english/)

**Research notes**

The counts, sources and check dates behind the guides, one folder per article.

- [Coding Agent Model Routing: When a Cheap Model Is Enough](https://loopnotes.dev/gpt-6-sol-vs-luna-routing/) · [research note](notes/gpt-6-sol-vs-luna-routing/)
- [RTX 4090 Local LLM: Which Runtime, Model Size and Context](https://loopnotes.dev/local-llm-hardware-runtime-guide/) · [research note](notes/local-llm-hardware-runtime-guide/)
- [Local LLM Hardware: What to Buy for the Model You'll Run](https://loopnotes.dev/local-llm-hardware-what-to-buy/) · [research note](notes/local-llm-hardware-what-to-buy/)
- [Codex CLI npm install Fails? It's Sandbox Network Access](https://loopnotes.dev/codex-cli-npm-install-sandbox/) · [research note](notes/codex-cli-npm-install-sandbox/)
- [Claude Code Skill Not Triggering? It's the Prompt (45 Runs)](https://loopnotes.dev/claude-code-skill-not-triggering/) · [research note](notes/claude-code-skill-not-triggering/)
- [Mac mini M6 vs M5 Pro for Developers: Is 32GB Enough?](https://loopnotes.dev/mac-mini-m6-vs-m5-pro/) · [research note](notes/mac-mini-m6-vs-m5-pro/)
- [1Password for Claude: My Mac Setup and What It Can't Do](https://loopnotes.dev/1password-for-claude-setup/) · [research note](notes/1password-for-claude-setup/)
- [Genspark AI Developer Review: What Broke on Mobile](https://loopnotes.dev/genspark-ai-developer-review/) · [research note](notes/genspark-ai-developer-review/)
- [Galaxy Z Fold 8 Korea Price vs US (Nov 2026): Still Cheaper?](https://loopnotes.dev/galaxy-z-fold-8-korea-price/) · [research note](notes/galaxy-z-fold-8-korea-price/)
- [GTA 6 Korea Price: ₩89,800 Is About $67, Not $58](https://loopnotes.dev/gta-6-korea-price/) · [research note](notes/gta-6-korea-price/)
- [CatchTable Waitlist Without a Korean Phone Number](https://loopnotes.dev/catchtable-waitlist-without-korean-number/) · [research note](notes/catchtable-waitlist-without-korean-number/)
**Datasets**

Series we re-measure and keep adding to; several articles draw on each.

- [Ollama default context length: docs vs code](datasets/ollama-default-context/)
- [Claude Code skill auto-trigger rate](datasets/claude-code-skill-trigger/)
- [Korea vs US list prices in US dollars](datasets/korea-us-prices/)
## What's in each folder

- `results.md` (or `log.md`): the measured results, with date, tool version, model and cost, as the article quotes them.
- `harness.py` / scripts: what ran the test. Paths point to a scratch directory; change them to rerun.
- `raw/`: one JSONL log per run, as the CLI wrote it. Session, request and account IDs are removed; nothing else is edited.
- `tasks.json`, `conditions.json`, `claude-md/`, `sample-project/`: the exact inputs.
- Screenshots (`.png`): captured by the script during the run.

## Limits

Each test ran on one machine, one account and one tool version on the date shown. Results can change with later versions. Small run counts are stated in each results file; read them as what happened here, not as a benchmark.

## License

Code: MIT. Logs, results and screenshots: CC BY 4.0. Credit "loopnotes.dev" with a link.
