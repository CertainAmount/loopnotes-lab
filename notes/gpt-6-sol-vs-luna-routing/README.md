# When does a cheap model stop being cheaper for a coding agent?

Research note for the loopnotes.dev article on model routing for coding agents (when a cheap tier is enough, and routing by risk). It holds the calculation behind the article's price-gap chart: the official list prices it uses, the date each page was read, the formula, and what the result does and does not cover. The article itself carries only the conclusions. All prices are USD per 1M tokens, standard (uncached) rates, read on 2026-11-14.

## Conclusions

1. Each cheap/strong pair below has the same price gap on input and on output, so the gap does not depend on how much of your traffic is prompt versus completion; a reader can compare tiers by one number per pair instead of modelling their token mix.
2. On a 20x pair (GPT-6 Luna vs GPT-6 Sol, Claude Haiku 5.5 vs Sonnet 5.5 on prompts up to 100,000 tokens), a router that starts on the cheap tier and escalates after one failure costs more than always using the strong tier only if the cheap tier fails its first try more than 95% of the time, so for these pairs a reader decides by review time and risk, not by retry cost.
3. On a 2x pair (GPT-6.1 Terra vs GPT-6 Sol, Sonnet 5.5 vs Opus 5.5), the same cheap-first router loses money once the cheap tier fails more than half the time, so a reader who sees the cheap tier failing that often on a task type sends that type straight to the strong tier.
4. The same Haiku 5.5 / Sonnet 5.5 pair drops from a 20x gap to 4x when the prompt passes 100,000 tokens (Haiku's long-prompt rate; Sonnet 5.5 has no long-context surcharge), so the cheap-first router loses money once Haiku fails more than three tries in four; a reader who sends whole-repository context should check prompt size before counting on the 20x gap.
5. GPT-6's long-prompt rate (over 272K input tokens) raises Luna and Sol by the same factors, so the 20x gap holds on very long prompts; prompt size changes the decision only on the Anthropic pair.

## 1. Official prices used

| Model | Input | Output | Condition | Source | Read |
|---|---|---|---|---|---|
| `gpt-6-sol` | $2.00 | $10.00 | standard, prompt up to 272K | [OpenAI API pricing](https://developers.openai.com/api/docs/pricing.md) | 2026-11-14 |
| `gpt-6-luna` | $0.10 | $0.50 | standard, prompt up to 272K | same | 2026-11-14 |
| `gpt-6.1-terra` | $1.00 | $5.00 | standard | same | 2026-11-14 |
| `gpt-6-sol`, `gpt-6-luna` over 272K | input x2, output x1.5 (Sol $4 / $15, Luna $0.20 / $0.75) | | applies to the whole request | same, and [GPT-6 Sol model page](https://developers.openai.com/api/docs/models/gpt-6-sol) | 2026-11-14 |
| Claude Haiku 5.5 | $0.10 | $0.50 | prompt up to 100,000 tokens | [Claude pricing (Anthropic)](https://platform.claude.com/docs/en/about-claude/pricing) | 2026-11-14 |
| Claude Haiku 5.5 | $0.50 | $2.50 | prompt over 100,000 tokens | same | 2026-11-14 |
| Claude Sonnet 5.5 | $2.00 | $10.00 | full 1M context at standard pricing | same | 2026-11-14 |
| Claude Opus 5.5 | $4.00 | $20.00 | full 1M context at standard pricing | same | 2026-11-14 |

The Anthropic page states that Claude 4.6 and later models, except Haiku 5.5, get the full 1M context window at standard pricing; that is why Sonnet 5.5 and Opus 5.5 have one row each. Rates not used in the calculation: Batch and Flex (50% off on OpenAI), Fast mode (2x on OpenAI), cached input (cache reads are discounted, cache writes are billed above the input rate on OpenAI), and regional processing surcharges.

## 2. Calculation

Let the strong tier cost `S` per call and the cheap tier cost `S / r` for the same call, where `r` is the price gap.

- Tries to equal one strong call: the cheap tier can be called `r` times for the price of one strong call.
- Cheap first, escalate after one failure: expected cost is `S / r + f * S`, where `f` is the share of tasks the cheap tier fails on its first try. This is cheaper than calling the strong tier alone when `f < 1 - 1/r`.

Script: [`calc.py`](calc.py) (Python 3, standard library only). It also checks that the input gap equals the output gap for every pair. Output:

| Cheap | Strong | Input gap | Output gap | Tries to equal one strong call | Cheap-first failure rate that loses money |
|---|---|---|---|---|---|
| gpt-6-luna | gpt-6-sol | 20x | 20x | 20 | above 95% |
| gpt-6-luna >272K | gpt-6-sol >272K | 20x | 20x | 20 | above 95% |
| Haiku 5.5 <=100K | Sonnet 5.5 | 20x | 20x | 20 | above 95% |
| Haiku 5.5 >100K | Sonnet 5.5 | 4x | 4x | 4 | above 75% |
| gpt-6.1-terra | gpt-6-sol | 2x | 2x | 2 | above 50% |
| Sonnet 5.5 | Opus 5.5 | 2x | 2x | 2 | above 50% |

At standard rates every model in section 1 charges five times as much for output as for input, and over 272K Luna and Sol get the same multipliers, so the cheap and strong side of each pair move together and the input:output mix of a workload cancels out of every gap.

## 3. What the top results say on this question

Read on 2026-11-14 for the query "model routing for coding agents when is a cheaper model enough". Listed for comparison only.

- [Unblocked: model routing for coding agents](https://getunblocked.com/blog/model-routing-coding-agents) — says a cheap model can cost more on complex work through rework; no price-gap numbers or threshold.
- Build Fast with AI, "Model routing for AI coding agents" (blog.buildfastwithai.com, 2026-08-18) — recommends one cheap retry then escalate and treats risk as its own dimension; example numbers are hypothetical and prices are from the GPT-5.6 generation.
- [MindStudio: frontier vs cheap models in an agent stack](https://www.mindstudio.ai/blog/ai-model-routing-frontier-vs-cheap-models-agent-stack) — general advice on mixing frontier and cheap models; no data.

None of the three gives a break-even point per tier pair or notes that prompt size changes the gap for one provider.

## Limits

- List prices only. Caching, Batch/Flex, Fast mode and negotiated rates change the dollar amounts; the gaps change only if a discount applies to one tier and not the other.
- The formula assumes a retry or escalated call is the same size as the first call. In practice a retry often carries the failed attempt as extra context, which makes the cheap-first router lose money a little sooner than the table says.
- It counts token cost only. Reviewing a wrong cheap-tier diff costs a person's time, which the article treats as the deciding cost on wide gaps.
- It assumes the strong tier succeeds on the escalated call. If the strong tier also fails sometimes, both sides add retries and the threshold moves.
- Prices were read on one day. Model names and rates change; rerun `calc.py` with the current pricing pages before reusing the numbers.
- Gemini Flash and Pro were left out: their official pricing page could not be read in full on 2026-11-14.

## 4. Context moved out of the article (2026-11-14)

- Test timing: the 30-task, two-model comparison (`gpt-6-sol` and `gpt-6-luna`, once each, 10 small edits / 10 multi-file refactors / 10 test-writing or bug-fix tasks) ran right after the GPT-6 API opened on 2026-09-22 ([OpenAI Developer Community announcement](https://community.openai.com/t/announcing-gpt-6-sol-and-gpt-6-luna-in-the-api-codex-and-chatgpt/1399925)).
- Scope as a grading criterion elsewhere: Cognition's [FrontierCode](https://cognition.com/frontiercode) benchmark (version 2.0, 2026-10-27, checked 2026-11-14) grades scope discipline next to correctness, the same split the article's four grading criteria make.
- Earlier router week (Ox Alpha, a GLM 5.3 Flash model, as the cheap side; Claude as the strong side; one week of gateway logs, not re-measured): about 65% of the week's tokens went to the cheap model; API cost about 60% lower than sending everything to Claude; simple low-risk tasks 10-15% faster, tool-heavy agentic tasks about 20% slower.
- Price dates: the break-even lines in the article use list prices read on 2026-11-14 (section 1).

Article: [Coding Agent Model Routing: When a Cheap Model Is Enough](https://loopnotes.dev/gpt-6-sol-vs-luna-routing/)
