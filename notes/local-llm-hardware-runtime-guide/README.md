# When a local LLM on an RTX 4090 stalls, what is the cause, and does switching runtimes fix it?

Research note for the loopnotes.dev hub article on running a local LLM on one RTX 4090
(https://loopnotes.dev/local-llm-hardware-runtime-guide/). Built on 2026-11-14 by grouping every
stall on the author's RTX 4090 that is written up in our long-tail posts or in the author's own
notes, then checking each public fact in those rows against the official docs on the same day.
No model was run for this note: the machine that built it has no GPU.

## Conclusions

- Of ten stalls on file, five were context or memory spilling past the card's 24 GB, one was a
  quantization below Q4, one was the GPU driver, and three were runtime or runtime-feature changes;
  none of the ten was fixed by switching runtime, so when a model gets slow or odd, check
  `ollama ps` and the context length before moving to llama.cpp, vLLM or Docker Model Runner.
- Every spill showed in the PROCESSOR column of `ollama ps` before anything else (a CPU share such
  as `14%/86% CPU/GPU`, or `100% CPU` when the driver broke) and Ollama raised no error, so the
  first check for "why is Ollama slow" is whether that column reads `100% GPU`.
- Ollama's docs and code disagree about the default context on a 4090: the FAQ says 4096, the
  context-length page puts cards under 24 GiB at 4k, and the code's boundary is 23 GiB, which
  puts a 4090 (23.99 GiB) at 32768; since the same page recommends at least 64000 for coding
  agents, set `OLLAMA_CONTEXT_LENGTH` yourself instead of trusting any of the three.
- Cline sends its own context-window value to Ollama as `num_ctx`, and Ollama reloads the model at
  that length, so a 64K server setting alone does not protect you; set the same value in Cline.
- The values in circulation are split: of four Korean blog posts on Ollama context truncation,
  one from 2026-11-09 still gives 2048 and one from 2026-11-07 sets 32768 by hand, so read the
  CONTEXT column of `ollama ps` rather than a number from a blog post.

## 1. Stalls on the author's RTX 4090

Each row is one stall the author hit on his own card. Rows 1, 6, 8, 9 and 10 are written up in our
long-tail posts (linked); rows 2-5 and 7 come from the author's own account of what he saw and
did. Times and speeds are what he observed, not controlled benchmarks.

| # | Symptom | What `ollama ps` (or the screen) showed | Cause | What fixed it | Write-up |
|---|---|---|---|---|---|
| 1 | 30B-class model forced on quick questions: first reply 20-30 s, long answers over a minute | n/a | Model too big for interactive use | A smaller model for quick asks | [local-llm-8b-vs-30b](https://loopnotes.dev/local-llm-8b-vs-30b/) |
| 2 | Qwen3-Coder 30B at 128K context: first reply 10 s or more | Spill to system RAM | Context past 24 GB | Back to 32K: first reply about 2.8 s | author's account |
| 3 | Qwen3 32B dense, a 30k-token log plus source at 32K: first character after 20 s or more | CPU share in the teens of percent | KV cache at f16 pushed past 24 GB, although the 18.4 GiB weights looked roomy | `OLLAMA_FLASH_ATTENTION=1` and `OLLAMA_KV_CACHE_TYPE=q8_0`; CPU share back to 0 | author's account |
| 4 | Cline ignored `.clinerules` (edited test files, did not re-read) after reading six or seven files; once ended without a tool call | CONTEXT 4096 | Older Ollama default context shorter than Cline's system prompt and files | `OLLAMA_CONTEXT_LENGTH` fixed on the server (32768, now 65536) | author's account |
| 5 | Monorepo task: tokens came one at a time while Cline read 10+ files | `14%/86% CPU/GPU` | Cline's own context window set larger; Cline sends it as `num_ctx`, Ollama reloaded at that length and the KV cache went past 24 GB | Cancel, set Cline's window back to 64K, `.clineignore` for build output, generated code and fixtures, `ollama stop` and reload: `100% GPU` | author's account |
| 6 | TypeScript refactor broke (types redefined, signatures changed) | n/a | Quantization below Q4 | Stay at Q4_K_M or above | [local-llm-8b-vs-30b](https://loopnotes.dev/local-llm-8b-vs-30b/) |
| 7 | Morning replies came out letter by letter, fans quiet, all CPU cores busy | `100% CPU`; `nvidia-smi`: `Failed to initialize NVML: Driver/library version mismatch` | Overnight automatic driver package update with the old kernel module still loaded; Ollama fell back to CPU without an error | Reboot; driver taken off automatic updates | author's account |
| 8 | Endpoint moved to Docker Model Runner: JSON parsing failed; about 1.5 h to find the cause | n/a | The runtime switch introduced a new failure | Not a speed fix; Docker Model Runner not kept for daily use | [docker-model-runner-vs-ollama](https://loopnotes.dev/docker-model-runner-vs-ollama/) |
| 9 | vLLM in Docker next to Ollama brought no gain | n/a | No concurrent requests (one user) | Back to Ollama | [rtx-4090-vllm-vs-llama-cpp](https://loopnotes.dev/rtx-4090-vllm-vs-llama-cpp/) |
| 10 | Speculative decoding on Coder 30B: 18 to 27 tok/s, but the whole task was not faster | n/a | The draft speed-up did not shorten the work | Turned off | [rtx-4090-vllm-vs-llama-cpp](https://loopnotes.dev/rtx-4090-vllm-vs-llama-cpp/) |

Tally by cause:

| Cause | Rows | Count | Fixed by switching runtime |
|---|---|---|---|
| Context or memory past 24 GB | 1-5 | 5 | 0 |
| Quantization below Q4 | 6 | 1 | 0 |
| GPU driver | 7 | 1 | 0 |
| Runtime or runtime-feature change | 8-10 | 3 | 0 (one created a new failure) |
| Total | | 10 | 0 |

## 2. How often each kind comes back

The author's own estimate for the last two to three months (an estimate, not a log count):

| Kind | Times per month |
|---|---|
| Context overflow (CPU share in `ollama ps`) | 2-6 |
| Model size (a new model plus its KV cache over 24 GB) | 1-2 |
| Runtime problem | 0-1 |

## 3. Ollama's default context: docs vs code (read 2026-11-14)

The same values are kept as a re-readable dataset, `datasets/ollama-default-context/` in this
repository, to be read again on each Ollama release.

| Where | What it says | URL |
|---|---|---|
| Ollama FAQ | Default context window 4096 tokens | https://docs.ollama.com/faq |
| Context-length page | Under 24 GiB VRAM: 4096; 24-48 GiB: 32768; 48 GiB and up: 262144 | https://docs.ollama.com/context-length |
| Context-length page | Agents and coding tools: at least 64000 | https://docs.ollama.com/context-length |
| Source commit 0334ffa6 | Tiers by total VRAM, boundaries at 23 GiB and 47 GiB ("small differences in the exact value"); `OLLAMA_CONTEXT_LENGTH` default changed from 4096 to 0 (pick by tier) | https://github.com/ollama/ollama/commit/0334ffa6 |

Calculation for a 4090: `nvidia-smi` reports 24564 MiB, and 24564 / 1024 = 23.99 GiB. That is
under the docs' 24 GiB line (which would mean 4096) but over the code's 23 GiB boundary, so with
`OLLAMA_CONTEXT_LENGTH` and `num_ctx` unset the code gives a 4090 32768 tokens. Either way it is
below the 64000 the docs recommend for coding agents. The commit page does not show which release
first shipped the change.

## 4. Korean blog posts on Ollama context truncation (Naver, 2026-11-14)

Search term: "올라마 num_ctx 컨텍스트 잘림" (Ollama num_ctx context truncation), blog, cafe and
Q&A results. Blog 4, cafe 0, Q&A 0. These are other people's reports, summarized in one line each.

| Date | Post | One-line summary |
|---|---|---|
| 2026-11-09 | [lesniel](https://blog.naver.com/lesniel/224470118206) | Says the default context is 2048; check `ollama ps` again after raising `num_ctx` |
| 2026-09-04 | [celeb_s_](https://blog.naver.com/celeb_s_/224401034785) | LM Studio shows a context slider on load, so the short default is easier to notice than in Ollama |
| 2026-11-07 | [pearlkt](https://blog.naver.com/pearlkt/224468169714) | A coding agent's context grew to tens of thousands of tokens; sets `num_ctx` to 32768 by hand |
| 2026-09-13 | [lesniel](https://blog.naver.com/lesniel/224409968549) | Calls the short default context the biggest Ollama trap; earlier conversation gets dropped |

Three of the four warn that the default context is too short and truncates conversations or
files; the defaults they quote are split between 2048, 4096 and 32768.

## 5. Public facts in the rows, checked against official sources (2026-11-14)

| Claim | Official source | Result |
|---|---|---|
| `ollama ps` PROCESSOR shows `100% GPU`, `100% CPU` or a split such as `48%/52% CPU/GPU` | https://docs.ollama.com/faq ("How can I tell if my model was loaded onto the GPU?") | Matches |
| `OLLAMA_KV_CACHE_TYPE` is one setting for all models; `q8_0` uses about half the memory of `f16` and needs Flash Attention | https://docs.ollama.com/faq (K/V cache section: "Currently this is a global option") | Matches |
| Flash Attention turns on by itself where supported; `OLLAMA_FLASH_ATTENTION=1` forces it | https://docs.ollama.com/faq | Matches |
| Server environment variables go in a systemd override (`systemctl edit ollama.service`) | https://docs.ollama.com/faq | Matches |
| GPU discovery can fail and Ollama then runs on CPU; reboot is a listed fix | https://docs.ollama.com/troubleshooting (NVIDIA GPU Discovery) | Matches (the docs list a reboot and the latest driver; the NVML message in row 7 is from the author's screen and is not in the docs) |
| Cline passes its context window to Ollama as `num_ctx` | https://github.com/cline/cline/blob/main/sdk/packages/llms/src/providers/vendors/ollama.ts (`contextWindow` sent as `options.num_ctx`) | Matches |
| Ollama cannot do speculative decoding (the reason given for row 10 at the time) | https://docs.ollama.com/modelfile (`draft_num_predict` parameter) | Outdated: current Ollama has a draft-model parameter, so this held only at the time of row 10 |

## Limits

- No GPU measurement was made for this note. Every row is one person's report from one RTX 4090,
  and the times and speeds in them were observed in daily use, not in controlled runs.
- Ten stalls from one machine show which causes this setup hits, not how common each cause is
  for everyone. The frequency table is the author's estimate.
- We have no same-model, same-context speed comparison between Ollama, llama.cpp and LM Studio,
  so this note says nothing about which runtime is faster.
- The Korean blog sample is four posts from one search term.
- Ollama's defaults change between releases; the docs and code values above are as read on
  2026-11-14.

## 6. Details moved out of the article (reader pass, 2026-11-14)

These were in the article body and moved here because the reader needs only their conclusion.

- Default context on a 4090: the context-length page puts cards under 24 GiB at 4096, a 4090
  reports 23.99 GiB, and commit 0334ffa6 draws the line at 23 GiB, so the code gives a 4090 32768
  (section 3). The FAQ still says 4096 and a 2026-11-09 Korean blog post gives 2048 (section 4).
  The article keeps only "a 4090 with nothing set gets 32768; trust the CONTEXT column".
- Red Hat's llama.cpp vs vLLM comparison
  (https://developers.redhat.com/articles/2026/06/15/llamacpp-vs-vllm-choosing-right-local-llm-inference-engine,
  June 15, 2026): with 64 concurrent users vLLM delivered about 44 times the tokens per second of
  llama.cpp, measured on one H200 with Llama 3.1 8B at 16-bit; with one request at a time the two
  were about even. The article keeps "vLLM only pays off with concurrent requests".
- Speculative decoding on Qwen3-Coder 30B (row 10): a draft model raised generation from 18 to
  27 tok/s, but whole agent tasks did not finish sooner.
- LM Studio pre-check: "offloads every layer" means 48 of 48 layers for Qwen3-Coder 30B.
- Docker Model Runner (row 8): the author's first setup took 40-60 minutes, the next project
  about 10.

## 7. Public facts added for the reader's steps (checked 2026-11-14)

| Step | Official source | What it says |
|---|---|---|
| Model tag to pull | https://ollama.com/library/qwen3-coder/tags | `qwen3-coder:30b` (same as `latest`) is the Q4_K_M build of the 30B-A3B model, 19 GB |
| Windows environment variables | https://docs.ollama.com/faq, https://docs.ollama.com/windows | Ollama on Windows inherits user and system environment variables: quit Ollama from the taskbar, open Settings (Windows 11) or Control Panel (Windows 10), search "environment variables", choose "Edit environment variables for your account", add the variables, start Ollama from the Start menu |
| Cline's context field | https://docs.ollama.com/integrations/cline | Cline settings > API Configuration, API Provider Ollama, model, then "Context Window" |
| What `.clineignore` is | https://docs.cline.bot/customization/clineignore | Tells Cline which files and directories to skip when it loads the codebase; `.gitignore` syntax; not an access-control boundary |

The article's `.clineignore` contents (build output, generated code, test fixtures) are what the
author listed for his own monorepo (row 5).

## 8. Qwen3-Coder 30B speed at 64K (author's estimate)

The author's figure for Qwen3-Coder 30B Q4_K_M at 64K in Ollama is 70-100 tok/s, calculated from
about 3B active parameters per token and the 4090's memory bandwidth, not timed: near 100-140 with
an empty context, 70-100 with the context half full, 50-70 when full. First reply on a short
Cline request (about 10k tokens of system prompt and tools) estimated at 3-4 s at 64K, against
about 2.8 s measured at 32K. Row 10's 18 to 27 tok/s comes from the speculative-decoding test and
is not used for the daily comparison.

## 9. Added for reader check 2 (2026-11-14)

| Step | Source | What it says |
|---|---|---|
| Quick-ask and chat model tags | https://ollama.com/library/qwen3/tags (checked 2026-11-14) | `qwen3:8b` (= `latest`) 5.2GB and `qwen3:14b` 9.3GB, default tags, 40K context window |
| Thinking off | https://docs.ollama.com/capabilities/thinking (checked 2026-11-14) | `think: false` requests no thinking output; models that cannot disable it use their lowest level |
| llama-swap first step | https://github.com/mostlygeek/llama-swap README (checked 2026-11-14) | minimum `config.yaml`: `models:` → model ID → `cmd: llama-server --port ${PORT} --model ...`; optional `ttl` unloads idle models |

Author answer (interview, 2026-11-14): quick asks on `qwen3:8b`, chat on `qwen3:14b` (same family, similar
tool-call behaviour), thinking switched off for quick asks; the 8B takes side questions so Cline's
Coder 30B is not swapped out and reloaded. The LM Studio pre-check is his own habit: an
Ollama-only user can skip it and read `ollama ps` and `nvidia-smi` after loading; he repeats it
only when changing model, quantization or KV type, or going past 64K. LM Studio's estimate
differs from Ollama by about 1GB, so `ollama ps` and `nvidia-smi` decide.

Moved out of the article body in reader check 2: the 70-100 tok/s derivation (section 8), the
19GB download size (section 7), the 2.8 s first reply at 32K (section 8 and row 2), "after six or
seven files" in the 4096 Cline scene.
