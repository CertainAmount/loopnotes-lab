# Ollama default context length: docs vs code

What context window does Ollama allocate when OLLAMA_CONTEXT_LENGTH and num_ctx are unset, and do its docs and code agree?

## Latest per item

| Item | Value | Measured | Source |
|---|---|---|---|
| code-lower-tier-boundary | 23 GiB | 2026-11-14 | https://github.com/ollama/ollama/commit/0334ffa6 |
| code-upper-tier-boundary | 47 GiB | 2026-11-14 | https://github.com/ollama/ollama/commit/0334ffa6 |
| doc-agent-coding-minimum | 64000 tokens | 2026-11-14 | https://docs.ollama.com/context-length |
| doc-tier-24-48GiB | 32768 tokens | 2026-11-14 | https://docs.ollama.com/context-length |
| doc-tier-48GiB-plus | 262144 tokens | 2026-11-14 | https://docs.ollama.com/context-length |
| doc-tier-under-24GiB | 4096 tokens | 2026-11-14 | https://docs.ollama.com/context-length |
| faq-default-context | 4096 tokens | 2026-11-14 | https://docs.ollama.com/faq |

## Method

Read the Ollama FAQ, the context-length doc page and the source commit that sets the VRAM tiers on the given day; record each stated value with its URL. Re-read on each Ollama release.

## Files

- `observations.csv`: 7 rows, one per measurement (date, item, value, unit, source)

## Articles that use it

- https://loopnotes.dev/local-llm-hardware-runtime-guide/
