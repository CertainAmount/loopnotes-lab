# How much GPU memory does a local LLM need for the model and context you'll actually run?

Research note for the loopnotes.dev hub article on choosing local LLM hardware. First built 2026-11-14,
rebuilt 2026-11-21 around one finding: models sold as the same "27 to 32B" class keep very different
amounts of cache per token, and the formula most calculators use does not see the difference. The
numbers come from official model files on Hugging Face, public spec pages, public llama.cpp issue logs,
one runtime check on this machine (Evidence 4) and two published RTX 4090 readings (Evidence 5). Every
other number is a calculation you can redo with the scripts in this folder.

## Conclusions

1. Qwen3.6 27B keeps the full context in only 16 of its 64 layers, so its cache is a quarter of Qwen3 32B's (2 GiB against 8 GiB at 32K): on a 24GB card with the default FP16 cache it reaches 64K at 20.8 GiB while Qwen3 32B is at the line by 16K, so a 24GB buyer who wants agent-length context changes the model, not the card.
2. The textbook formula (every layer keeps every token) puts Qwen3.6 27B over 24 GiB before 32K and overcounts the 32K cache of popular open models by 1x to 5.3x, exactly where a model mixes in linear, sliding-window or compressed layers, so check `layer_types` or `full_attention_interval` in the model's config.json before trusting a calculator or buying a bigger card.
3. llama.cpp allocated the cache only for the full-attention layers of two small hybrid models, to the MiB, at 8K, 32K and 128K, so the layer-aware numbers are what that runtime reserves; Qwen3.6 27B itself was not run on a GPU here.
4. Qwen3.6 27B's Q4_K_M files are 15.4 to 18.1 GiB, 17.3 GiB at 8K with the runtime, so a 27B-class model does not fit a 16GB card at any context, while Qwen3-14B at 32K comes to 14.4 GiB: a buyer who will run 27B-class models skips 16GB.
5. Macs with 36GB or more give the GPU about three quarters of their memory by default, so Llama 3.3 70B at Q4 with an FP16 cache stops at 16K on a 64GB Mac, 64K on a 96GB Mac and reaches 128K only on a 128GB Mac: a 70B buyer counts that share, not the memory on the box.
6. The runtime adds about 1 GiB on top of weights plus cache (two 4090 readings landed 0.8 and 0.1 GiB above the calculation), so treat any setup within 1 GiB of a card's capacity as borderline.

## Evidence 1: Qwen3.6 27B's layer plan and its cache per token

From the model's `config.json` (fetched 2026-11-21, copies in `raw/`):

| Model | Repo | Layers | Full-attention layers | KV heads | head_dim | Native context |
|---|---|---|---|---|---|---|
| Qwen3.6 27B | [Qwen/Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B) | 64 | 16 (`layer_types`: three `linear_attention`, then one `full_attention`, repeated; `full_attention_interval` 4) | 4 | 256 | 262,144 |
| Qwen3.8 27B | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | 64 | 16 (same plan) | 4 | 256 | 262,144 |
| Qwen3.5 27B | [Qwen/Qwen3.5-27B](https://huggingface.co/Qwen/Qwen3.5-27B) | 64 | 16 (same plan) | 4 | 256 | 262,144 |

Cache per token, FP16 (`figdata.py` -> `qwen36-kv-row.csv`):

- Textbook formula, all 64 layers: 2 (K and V) x 64 x 4 x 256 x 2 bytes = 256 KiB.
- Full-attention layers only: 2 x 16 x 4 x 256 x 2 bytes = 64 KiB.
- The 48 linear (Gated DeltaNet) layers hold a fixed state that does not grow with context: 149.6 MiB
  for the whole model, from the linear-attention head counts and dimensions in the same config.

| Context | Textbook formula | Full-attention layers only |
|---|---|---|
| 8K | 2 GiB | 0.5 GiB |
| 32K | 8 GiB | 2 GiB |
| 128K | 32 GiB | 8 GiB |

Qwen3 32B, for comparison, has 64 layers, all full attention, 8 KV heads and head_dim 128: 256 KiB per
token by either count (Evidence 6). The two models land on the same textbook number for opposite reasons.

## Evidence 2: weights + cache + runtime on a 16GB and a 24GB card

Qwen3.6 27B Q4_K_M files on Hugging Face, from the file-listing API on 2026-11-21 (`qwen36-q4-files.csv`,
listings in `raw/tree_*Qwen3.6-27B-GGUF.json`):

| Repo | Bytes | GiB |
|---|---|---|
| [unsloth/Qwen3.6-27B-GGUF](https://huggingface.co/unsloth/Qwen3.6-27B-GGUF) (most downloaded, used in the figures) | 16,817,244,384 | 15.66 |
| [lmstudio-community/Qwen3.6-27B-GGUF](https://huggingface.co/lmstudio-community/Qwen3.6-27B-GGUF) | 16,547,398,784 | 15.41 |
| [bartowski/Qwen_Qwen3.6-27B-GGUF](https://huggingface.co/bartowski/Qwen_Qwen3.6-27B-GGUF) | 17,984,872,960 | 16.75 |
| [ggml-org/Qwen3.6-27B-GGUF](https://huggingface.co/ggml-org/Qwen3.6-27B-GGUF) | 19,403,683,392 | 18.07 |

The vision projector (`mmproj`) is a separate file of about 0.87 GiB and is not counted.

Totals in GiB: Q4_K_M weights + FP16 cache + 1 GiB runtime (Evidence 5). This is the data of figure 1
(`figures/fig-1/data.csv`):

| Context | Qwen3.6 27B | Qwen3.6 27B, textbook formula | Qwen3 32B | Qwen3-Coder 30B (calculated / measured on an RTX 4090) |
|---|---|---|---|---|
| 8K | 17.3 | 18.7 | 21.4 | 19.0 |
| 16K | 17.8 | 20.7 | 23.4 | 19.8 |
| 32K | 18.8 | 24.7 | 27.4 | 21.3 / 21.1 |
| 64K | 20.8 | 32.7 | 35.4 | 24.3 / 23.4 |
| 128K | 24.8 | 48.7 | 51.4 | 30.3 |

What it means:

- 24GB card (an RTX 4090 reports 24,564 MiB, 23.99 GiB): Qwen3.6 27B runs at 64K with about 3 GiB to
  spare. At 128K it is about 1 GiB over with an FP16 cache; an 8-bit (`q8_0`) cache brings 128K to
  21.1 GiB. Qwen3 32B is within 1 GiB of the line at 16K and over it at 32K.
- The textbook line for Qwen3.6 27B crosses 24 GiB just before 32K, close to Qwen3 32B's line. A buyer
  who trusts it sees the 27B as a 24GB-at-16K model and looks at the next card up.
- 16GB card: the 27B's weights alone are 15.4 to 18.1 GiB depending on the file, 17.3 GiB at 8K with the
  runtime. There is no room for context because there is no room for the weights. Qwen3-14B Q4_K_M at
  32K comes to 13.4 GiB, 14.4 GiB with the runtime (Evidence 6), which fits.

A 16GB card at 32K, file + FP16 cache + 1 GiB runtime, from the Hugging Face file-listing API and each
model's `config.json` (fetched 2026-11-21; `raw/tree_ggml-org_gpt-oss-20b-GGUF.json`,
`raw/config_openai_gpt-oss-20b.json`, `raw/tree_bartowski_Mistral-Small-3.2-24B-GGUF.json`):

| Model (4-bit file) | Bytes | File GiB | Cache at 32K | Total | 16GB card |
|---|---|---|---|---|---|
| Qwen3-14B Q4_K_M | 9,001,752,960 | 8.38 | 5.0 (all 40 layers) | 14.4 | fits |
| [gpt-oss 20B MXFP4](https://huggingface.co/ggml-org/gpt-oss-20b-GGUF) | 12,109,566,624 | 11.28 | 0.75 (12 of 24 layers full, 8 KV heads, head_dim 64; the other 12 keep a 128-token window) | 13.0 | fits |
| [Mistral Small 3.2 24B Q4_K_M](https://huggingface.co/bartowski/mistralai_Mistral-Small-3.2-24B-Instruct-2506-GGUF) | 14,333,915,264 | 13.35 | 5.0 (all layers, Evidence 3) | 19.3 | over |
| Qwen3.6 27B Q4_K_M | 16,817,244,384 | 15.66 | 2.0 | 18.7 | over |

The file alone does not set the 16GB line: gpt-oss 20B and Mistral Small 3.2 24B have files 2 GiB apart
and land 6 GiB apart at 32K, because one keeps every token in 12 layers and the other in all of them.

## Evidence 3: textbook formula against what each model keeps, nine models at 32K

Figure 2 (`figures/fig-2/data.csv`). Each row is calculated from the model's official Hugging Face
`config.json`, collected 2026-11-14 and 2026-11-15 for our KV cache study, plus the Qwen3.6 27B row from
Evidence 1. FP16 cache at 32K tokens, GiB.

| Model | Textbook formula | What the model keeps | Overcount | Why |
|---|---|---|---|---|
| Gemma 3 27B | 15.5 | 2.9 | 5.3x | 1 in 6 layers global, the rest sliding window |
| Qwen3.6 27B | 8.0 | 2.0 | 4x | 1 in 4 layers full, the rest linear |
| EXAONE 4.0 32B | 8.0 | 2.8 | 2.9x | 1 in 4 layers global |
| gpt-oss 20B | 1.5 | 0.8 | 1.9x | half the layers windowed |
| DeepSeek V2 Lite 16B | 8.4 | 0.9 | (see note) | compressed latent cache |
| Qwen3 32B | 8.0 | 8.0 | 1x | all layers |
| Qwen3-Coder 30B | 3.0 | 3.0 | 1x | all layers |
| Mistral Small 3.2 24B | 5.0 | 5.0 | 1x | all layers |
| Llama 3.3 70B | 10.0 | 10.0 | 1x | all layers |

The formula is exact for models whose every layer keeps every token and overcounts every model that
mixes in other layer types. For DeepSeek V2 Lite the "textbook" value applies the formula to its
attention heads, which no runtime would allocate; its ratio is not comparable to the others and is left
out of the 1x to 5.3x range.

Where to look in a config.json: `layer_types` (lists every layer), `full_attention_interval`,
`sliding_window` with `sliding_window_pattern`, or `kv_lora_rank` for a compressed latent cache. A model
with none of these keeps every token in every layer.

## Evidence 4: does a runtime allocate the cache by the layer plan? (llama.cpp, 2026-11-21)

Question: the textbook formula counts all layers. Does a runtime reserve cache for the full-attention
layers only?

Method (`hybrid_alloc.py`): llama.cpp build 12383 (commit c56be864f), CPU only, the process capped at
2 GB of memory. Each GGUF is started once per context with `-fa on` and the default FP16 cache, and
stopped as soon as the cache is reserved; the `llama_kv_cache: size` and `llama_memory_recurrent: size`
lines are kept in `logs/`. The Qwen3.6 27B file (15.7 GiB) does not fit this machine, so the test uses
the smallest model with the same layer plan (Qwen3.5 0.8B, architecture `qwen3_5_text`, full attention
every 4th layer), a second hybrid family (Granite 4.0-H 350M, Mamba-2 plus attention) and an all-layer
model as control.

| Model | Context | Layers / full-attention | KV layers allocated | KV MiB measured | Textbook formula | Full-attention layers only | Fixed state MiB |
|---|---|---|---|---|---|---|---|
| Qwen3.5 0.8B Q4_K_M | 8K | 24 / 6 | 6 | 96 | 384 | 96 | 19.3 |
| Qwen3.5 0.8B Q4_K_M | 32K | 24 / 6 | 6 | 384 | 1,536 | 384 | 19.3 |
| Qwen3.5 0.8B Q4_K_M | 128K | 24 / 6 | 6 | 1,536 | 6,144 | 1,536 | 19.3 |
| Granite 4.0-H 350M Q4_K_M | 8K | 32 / 4 | 4 | 32 | 256 | 32 | 21.6 |
| Granite 4.0-H 350M Q4_K_M | 32K | 32 / 4 | 4 | 128 | 1,024 | 128 | 21.6 |
| Granite 4.0-H 350M Q4_K_M | 128K | 32 / 4 | 4 | 512 | 4,096 | 512 | 21.6 |
| Qwen3 0.6B Q8_0 (control) | 8K | 28 / 28 | 28 | 896 | 896 | 896 | 0 |
| Qwen3 0.6B Q8_0 (control) | 32K | 28 / 28 | 28 | 3,584 | 3,584 | 3,584 | 0 |
| Qwen3 0.6B Q8_0 (control) | 128K | 28 / 28 | 28 | 14,336 | 14,336 | 14,336 | 0 |

All nine runs are in `hybrid-alloc.csv`. Result: llama.cpp reserved cache only for the full-attention
layers, matching the layer-aware prediction to the MiB at every context, and a quarter (Qwen3.5) or an
eighth (Granite) of the textbook value. The linear layers hold a fixed state that does not grow
(19.3 MiB for Qwen3.5 0.8B, logged as 1.27 + 18.00 MiB, matching the Gated DeltaNet state formula in
`figdata.py`). The control matched the textbook formula, as it should.

Ollama and LM Studio were not tested here.

## Evidence 5: calculation against two published RTX 4090 readings

Qwen3-Coder-30B-A3B Q4_K_M in LM Studio on an RTX 4090 24GB, September 2026, default cache precision,
VRAM read in `nvidia-smi`. The readings were published on loopnotes.dev before this note.

| Context | Calculated weights + cache (GiB) | Measured | Difference |
|---|---|---|---|
| 32K | 20.28 | 21.1 | +0.8 |
| 64K | 23.28 | 23.4 | +0.1 |

The readings only make sense as GiB (read as decimal GB, weights + cache at 32K alone come to 21.8,
above the reading). The runtime adds up to about 1 GiB, less when the card is nearly full. The tables in
this note add 1 GiB, and anything within 1 GiB of a line is borderline.

## Evidence 6: all-layer models, weights + cache by context

`fit_table.py` reads the files in `raw/` and writes `fit-table.csv`. Architecture from each model's
`config.json` (fetched 2026-11-14):

| Model | Repo | Layers | KV heads | head_dim | Cache per token (FP16) |
|---|---|---|---|---|---|
| Qwen3-14B | [Qwen/Qwen3-14B](https://huggingface.co/Qwen/Qwen3-14B) | 40 | 8 | 128 | 160 KiB |
| Qwen3-Coder-30B-A3B-Instruct | [Qwen/Qwen3-Coder-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct) | 48 | 4 | 128 | 96 KiB |
| Qwen3-32B | [Qwen/Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B) | 64 | 8 | 128 | 256 KiB |
| Llama 3.3 70B Instruct | [unsloth/Llama-3.3-70B-Instruct](https://huggingface.co/unsloth/Llama-3.3-70B-Instruct) (public mirror; the meta-llama repo is gated) | 80 | 8 | 128 | 320 KiB |
| Qwen3-235B-A22B | [Qwen/Qwen3-235B-A22B](https://huggingface.co/Qwen/Qwen3-235B-A22B) | 94 | 4 | 128 | 188 KiB |

Weight sizes from the Hugging Face file-listing API (fetched 2026-11-14):

| Model | GGUF repo | Bytes | GiB |
|---|---|---|---|
| Qwen3-14B Q4_K_M | [Qwen/Qwen3-14B-GGUF](https://huggingface.co/Qwen/Qwen3-14B-GGUF) | 9,001,752,960 | 8.38 |
| Qwen3-Coder-30B-A3B Q4_K_M | [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF](https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF) | 18,556,689,568 | 17.28 |
| Qwen3-32B Q4_K_M | [Qwen/Qwen3-32B-GGUF](https://huggingface.co/Qwen/Qwen3-32B-GGUF) | 19,762,149,024 | 18.40 |
| Llama 3.3 70B Q4_K_M | [bartowski/Llama-3.3-70B-Instruct-GGUF](https://huggingface.co/bartowski/Llama-3.3-70B-Instruct-GGUF) | 42,520,398,816 | 39.60 |
| Qwen3-235B-A22B Q2_K (2 parts) | [unsloth/Qwen3-235B-A22B-GGUF](https://huggingface.co/unsloth/Qwen3-235B-A22B-GGUF) | 85,691,002,112 | 79.81 |
| Qwen3-235B-A22B Q4_K_M (3 parts) | [unsloth/Qwen3-235B-A22B-GGUF](https://huggingface.co/unsloth/Qwen3-235B-A22B-GGUF) | 142,154,075,488 | 132.39 |

Weights + FP16 cache, GiB (add about 1 GiB for the runtime):

| Model | 8K | 16K | 32K | 64K | 128K |
|---|---|---|---|---|---|
| 14B dense Q4_K_M | 9.6 | 10.9 | 13.4 | 18.4 | 28.4 |
| 30B MoE (Coder) Q4_K_M | 18.0 | 18.8 | 20.3 | 23.3 | 29.3 |
| 32B dense Q4_K_M | 20.4 | 22.4 | 26.4 | 34.4 | 50.4 |
| 70B dense Q4_K_M | 42.1 | 44.6 | 49.6 | 59.6 | 79.6 |
| 235B MoE Q2_K | 81.3 | 82.7 | 85.7 | 91.6 | 103.3 |
| 235B MoE Q4_K_M | 133.9 | 135.3 | 138.3 | 144.1 | 155.9 |

- Native context: Qwen3-14B, Qwen3-32B and Qwen3-235B-A22B list 40,960 positions (128K needs YaRN
  scaling); Qwen3-Coder-30B-A3B lists 262,144; Llama 3.3 70B lists 131,072.
- 8-bit cache: llama.cpp's `q8_0` stores 32 int8 values plus one FP16 scale per block, 34 bytes per 32
  values (`block_q8_0` in [ggml-common.h](https://github.com/ggml-org/llama.cpp/blob/61dbf49228c8a96b72e40c89d93cb7c003411f8c/ggml/src/ggml-common.h)),
  8.5 bits per value, 53% of FP16. `fit-table.csv` has a `total_q8_0_plus_overhead_gib` column
  (weights + 8-bit cache + 1 GiB).
- Units: GiB throughout, because card capacities and `nvidia-smi` are binary. `fit-table.csv` also
  carries decimal GB columns.

## Evidence 7: the default GPU share on Macs, from public llama.cpp logs

Apple documents `MTLDevice.recommendedMaxWorkingSetSize` as "an approximation of how much memory, in
bytes, this GPU device can allocate without affecting its runtime performance" and publishes no ratio.
llama.cpp prints that value as `recommendedMaxWorkingSetSize = N MB` (N in units of 10^6 bytes) when it
starts on Metal ([ggml-metal-device.m at 61dbf49](https://github.com/ggml-org/llama.cpp/blob/61dbf49228c8a96b72e40c89d93cb7c003411f8c/ggml/src/ggml-metal/ggml-metal-device.m)).

`mac_limit_survey.py` searched GitHub on 2026-11-14 for every public issue in ggml-org/llama.cpp that
contains that string: 264 issues, 161 distinct issue/value lines. It matched each value to a standard
Apple memory size when the value equals 3/4 or 2/3 of that size within 0.4%. One row per line, with the
issue number and date: `mac-limit-survey.csv`.

| Inferred memory | Ratio | Lines |
|---|---|---|
| 8, 16, 18, 24, 32 GB | 2/3 | 50 |
| 36 GB | 2/3: 1, 3/4: 10 | 11 |
| 48 GB | 3/4 | 1 |
| 64 GB | 3/4 (48 GiB) | 19 |
| 96 GB | 3/4 (72 GiB) | 3 |
| 128, 192, 512 GB | 3/4 | 10 |
| no match | raised limits, other values | 67 |

Every value that matches a ratio follows 2/3 below 36GB and 3/4 from 36GB up. To check your own Mac:
the `recommendedMaxWorkingSetSize` line in the llama.cpp startup log, or `sysctl iogpu.wired_limit_mb`
(0 means the default is in effect).

## Evidence 8: which Mac holds Llama 3.3 70B, and at what context (calculation)

Current Mac Studio configurations ([Apple Support 128107](https://support.apple.com/128107), read
2026-11-21): M5 Max with 36GB base and 48, 64 or 128GB options, 460 or 614GB/s; M5 Ultra with 96GB base
and 256 or 512GB options, 1.2TB/s. The GPU share below applies the 3/4 rule from Evidence 7 to each
size; it is not read from those machines.

Llama 3.3 70B Q4_K_M + cache + 1 GiB runtime (`fit-table.csv`): FP16 cache 43.1 / 45.6 / 50.6 / 60.6 /
80.6 GiB at 8K / 16K / 32K / 64K / 128K; 8-bit cache 41.9 / 43.3 / 45.9 / 51.2 / 61.9 GiB.

| Mac memory | GPU share by default | Longest 70B context, FP16 cache | Longest 70B context, 8-bit cache |
|---|---|---|---|
| 48GB | 36 GiB | does not fit (43.1 at 8K) | does not fit (41.9 at 8K) |
| 64GB | 48 GiB | 16K | 32K |
| 96GB | 72 GiB | 64K | 128K |
| 128GB | 96 GiB | 128K | 128K |

## Evidence 9: generation speed ceiling for a dense 70B (calculation)

Generating each token reads the whole dense weight file once, so memory bandwidth divided by the weight
file (42.52 GB) is an upper bound on tokens per second:

| Machine | Bandwidth | Ceiling, tokens/s | Spec source (read) |
|---|---|---|---|
| DGX Spark | 273 GB/s | 6.4 | [NVIDIA](https://www.nvidia.com/en-us/products/workstations/dgx-spark/) (2026-11-14) |
| Mac Studio M5 Max (614GB/s configuration) | 614 GB/s | 14.4 | [Apple 128107](https://support.apple.com/128107) (2026-11-21) |
| Mac Studio M3 Ultra | 819 GB/s | 19.3 | [Apple 122211](https://support.apple.com/en-us/122211) (2026-11-14) |
| Mac Studio M5 Ultra | 1.2 TB/s | 28.2 | [Apple 128107](https://support.apple.com/128107) (2026-11-21) |

Real runs land below these ceilings; the ratio between machines is the useful part. This decides how
fast a model runs once it fits, not whether it fits.

## Evidence 10: how much context to count for coding agents

Ollama's [context length page](https://docs.ollama.com/context-length) (read 2026-11-21) sets the default
context by available VRAM (under 24 GiB: 4K; 24 to 48 GiB: 32K; 48 GiB and up: 256K) and recommends at
least 64,000 tokens for web search, agents and coding tools. The same tiers were recorded on 2026-11-14 in
our `ollama-default-context` dataset on loopnotes-lab. Hence 32K and 64K as the contexts this note compares
for agent work.

## Moved from the article body (reader fix r1, 2026-11-21)

- Method behind the 64K on a 24GB card: the per-token cache comes from Qwen3.6-27B's config.json (Evidence 1) and was checked against how llama.cpp allocates memory for this layer plan (Evidence 4). An earlier version of the article gave the all-layer formula, which counts all 64 layers and sized the 27B like Qwen3 32B.
- The llama.cpp allocation check (Evidence 4) was run by Claude Code on two small hybrid models on CPU, at 8K, 32K and 128K; the article keeps only its conclusion.
- The Mac GPU share (three quarters at 36GB and above, two thirds below) comes from 161 public llama.cpp log lines (Evidence 7); the article says only that public llama.cpp logs show it.
- The author chose the Mac Studio in November 2025; the article keeps the decision, not the date.
- Turning on the 8-bit cache in Ollama: the Ollama FAQ (https://docs.ollama.com/faq, read 2026-11-21) sets the K/V cache type with the `OLLAMA_KV_CACHE_TYPE` environment variable on the server (default `f16`, `q8_0` at about half the memory); quantized cache needs Flash Attention, which Ollama turns on automatically when the backend supports it (`OLLAMA_FLASH_ATTENTION=1` forces it). It is a global option for all models.
- Worked example for the per-token formula: Qwen3.6 27B, 64 KiB per token × 65,536 tokens = 4 GiB, + 15.7 GiB Q4_K_M file + about 1 GiB runtime = about 20.7 GiB (Evidence 2 gives 20.8 with the linear-layer state).

## Moved from the article body (reader fix r2, 2026-11-21)

- The textbook formula in its usual form, layers × KV heads × head dimension × 4 bytes, is the per-token formula with every layer counted; Figure 2 puts both values side by side for nine models (Evidence 3).
- The llama.cpp allocation check (Evidence 4): two small hybrid models got cache for their full-attention layers only, matching the per-token math to the MiB, while an all-layer Qwen3 model got the full textbook amount.
- The two RTX 4090 readings for Qwen3-Coder 30B, 21.1 GiB at 32K and 23.4 GiB at 64K, are in Evidence 5; the article keeps the rule they support (within 1GB of the card is the edge) and the chart's open circles.
- Spill scene details: the pasted log and source files were close to 30,000 tokens, `ollama ps` showed a CPU share in the teens, and the RTX 4090 box has 64GB of system RAM.
- The smallest 4-bit Qwen3.6 27B upload is 15.41 GiB (lmstudio-community, Evidence 2); the article keeps only that the file nearly fills a 16GB card.
- Setting the context in Ollama: the [context length page](https://docs.ollama.com/context-length) (read 2026-11-21) gives `OLLAMA_CONTEXT_LENGTH=64000 ollama serve` as the server-wide setting; the article uses 65536 (64K) on the same line as `OLLAMA_KV_CACHE_TYPE=q8_0` (Ollama FAQ).
- Two 24GB cards (two used RTX 3090s or a second 4090), 48 GiB in all: Llama 3.3 70B Q4_K_M needs 44.6 GiB with FP16 cache at 16K and 49.6 at 32K (Evidence 6), plus about 1 GiB of runtime per card, so the pair holds a 70B to about 16K, the same as a 64GB Mac's 48 GiB GPU share (Evidence 8). A calculation, not a run.
- The 70B speed ceilings are memory bandwidth divided by the 42.52 GB Q4_K_M file (Evidence 9); the article states the method in words.

## Moved from the article body (reader fix r3, 2026-11-21)

- Qwen3.8 27B uses the same layer plan as Qwen3.6 27B (one full-attention layer in every four); the article no longer names it inside the chart reading.
- The first-pull scene in full: on the RTX 4090 the Ollama loading log showed a smaller cache than expected; the author still meant to start Qwen3.6 27B at 16K, opened its config.json, loaded it at 32768 and later raised it to 65536 for Cline. The article keeps the config.json moment, the dropped 16K plan and the 65536 it runs at now.
- The two RTX 4090 Qwen3-Coder 30B readings (Evidence 5) validate the method; the article keeps the rule they give (within 1GB of the card is the edge).
- The 16GB table's layer counts: Qwen3-14B and Mistral Small 3.2 keep the cache in all layers, gpt-oss 20B in 12 of 24, Qwen3.6 27B in 16 of 64 (Evidence 2, 3). The article's table keeps the cache sizes only.
- The closing check "before trusting a calculator or a model card's memory table, check whether it counts every layer as full attention" restated the section and was cut.

### Units and file sizes (added 2026-11-21)

- All memory values in the article are binary (GiB). nvidia-smi reports MiB; an RTX 4090 shows 24,564 MiB = 23.99 GiB, so a 24GB card sits at 24 on figure 1.
- Hugging Face's file list shows decimal GB: the unsloth Qwen3.6-27B Q4_K_M file is 16,817,244,384 bytes, listed as 16.8 GB, which is 15.66 GiB (16.8 / 1.074). The article tells the reader to divide a listed size by 1.07.

### Renting a 24GB card to test first (added 2026-11-21)

- [RunPod pricing](https://www.runpod.io/pricing), read 2026-11-21: RTX 3090 (24GB) pods at $0.50/hr on Secure Cloud; the page's structured data also gives $0.22/hr for Community Cloud. The article says "about $0.50 an hour".
- Author's run (author interview, 2026-11-21): a single RTX 3090 24GB pod on RunPod for three hours, Qwen3-Coder 30B Q4 in Ollama at 8K; `ollama ps` showed PROCESSOR 100% GPU (a spill shows a CPU/GPU split such as 48%/52%, per the [Ollama FAQ](https://docs.ollama.com/faq)), and nvidia-smi showed about 20GB used of 24,576MiB. The author remembered the hourly rate as "about $0.4"; the article uses the official page.
- Prices of the Macs and DGX Spark: Apple's Mac Studio buy page and NVIDIA's DGX Spark page (both read 2026-11-21) list no price for these configurations (NVIDIA sends buyers to its marketplace), so the article gives none.

## Limits

- No Qwen3.6 27B was run on a GPU for this note. Its totals are calculations from config.json; the
  runtime check in Evidence 4 measured cache allocation for small models with the same layer plan, on
  CPU, in llama.cpp only.
- The only GPU readings are the two Qwen3-Coder 30B points in Evidence 5: one model, one runtime, one
  card. The 1 GiB runtime allowance comes from them; a GPU that also drives a display, or a runtime that
  reserves extra buffers, leaves less room.
- Totals assume an FP16 cache, the default in Ollama and llama.cpp; the 8-bit figures use the `q8_0`
  block size. 4-bit caches were not calculated.
- Q4_K_M files for the same model differ by up to 2.7 GiB between uploaders (Evidence 2). Only Qwen3.6
  27B's files were compared; other models use one file each.
- The Evidence 3 rows other than Qwen3.6 27B come from configs collected a week earlier; a model update
  that changes its layer plan would change its row.
- In the Mac survey the memory size is inferred from the logged value, not stated by each reporter, and
  67 of 161 lines match neither ratio (many from raised `iogpu.wired_limit_mb` values or newer macOS).
  The shares are the usual default, not a guarantee, and the M5 rows in Evidence 8 extend the rule to
  machines that do not appear in the logs.
- Llama 3.3 70B's architecture comes from a public mirror of the gated official repo.
- The speed figures are bandwidth ceilings; they ignore prompt processing, which decides time to first
  token on long inputs.

## Files

- `figdata.py` -> `qwen36-kv-row.csv`, `qwen36-q4-files.csv`, `figures/spec-1.json`, `figures/spec-2.json`.
- `figures/fig-1/`, `figures/fig-2/`: each figure's `spec.json`, `data.csv` and `figure.svg`, drawn with
  the loopnotes viz engine.
- `hybrid_alloc.py` -> `hybrid-alloc.csv`, `logs/` (Evidence 4).
- `fit_table.py` -> `fit-table.csv`; `draw_chart.py` draws the chart of the earlier version of the article.
- `mac_limit_survey.py` -> `mac-limit-survey.csv`.
- `raw/config_*.json`: Hugging Face config.json files. `raw/tree_*.json`: Hugging Face file listings.
- `raw/spec-snippets.md`: spec lines quoted on 2026-11-14, with URLs.

## Sources

- Hugging Face model and GGUF repos linked in the tables above (fetched 2026-11-14 and 2026-11-21).
- Apple Developer: [MTLDevice.recommendedMaxWorkingSetSize](https://developer.apple.com/documentation/metal/mtldevice/recommendedmaxworkingsetsize) (read 2026-11-14).
- Apple Support: [Mac Studio technical specifications, M5 Max and M5 Ultra](https://support.apple.com/128107) (read 2026-11-21) and [Mac Studio (2025)](https://support.apple.com/en-us/122211) (read 2026-11-14).
- NVIDIA: [DGX Spark product page](https://www.nvidia.com/en-us/products/workstations/dgx-spark/) (read 2026-11-14).
- llama.cpp: [ggml-metal-device.m](https://github.com/ggml-org/llama.cpp/blob/61dbf49228c8a96b72e40c89d93cb7c003411f8c/ggml/src/ggml-metal/ggml-metal-device.m) and [ggml-common.h](https://github.com/ggml-org/llama.cpp/blob/61dbf49228c8a96b72e40c89d93cb7c003411f8c/ggml/src/ggml-common.h) at commit 61dbf49 (read 2026-11-14); build 12383 (commit c56be864f) for Evidence 4.
- Ollama: [Context length](https://docs.ollama.com/context-length) (read 2026-11-21).

Article: [Local LLM Hardware: What to Buy for the Model You'll Run](https://loopnotes.dev/local-llm-hardware-what-to-buy/)
