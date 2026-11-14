# How much memory does a local LLM need for the model and context you'll actually run?

Research note for the loopnotes.dev hub article on choosing local LLM hardware. Built 2026-11-14 from
official model files, public spec pages, public llama.cpp issue logs and two published measurements.
No model was run for this note; every new number below is a calculation that you can redo with the
scripts in this folder.

## Conclusions

1. The memory a model needs is its Q4 weight file plus the KV cache for the context you feed it every day, so pick your context (8K chat, 32K agent work, 128K whole-repo) before you pick a card: Qwen3-Coder-30B-A3B at 32K comes to 20.3 GB calculated and 21.1 GB measured, which fits a 24GB card, while its 17.3 GB weight file alone already rules out a 16GB card.
2. On the same 24GB card a dense Qwen3-32B needs 26.4 GB at 32K, because it has twice the KV heads and a third more layers than the 30B MoE, so a 24GB buyer who wants long context should run the MoE or plan on 8-bit KV, which brings the 32B to 23.7 GB with the runtime included and no room left.
3. A 14B dense model at Q4 fits a 16GB card up to about 32K (13.4 GB), so a buyer who will stay at 14B does not need the 24GB step.
4. In public llama.cpp logs, Macs with 36GB or more give the GPU about three quarters of their memory by default (64GB to 48 GB, 96GB to 72 GB) and smaller Macs about two thirds, so count a Mac at that share and check your own machine before you size a model to it.
5. Llama 3.3 70B at Q4 needs 49.6 GB at 32K, which is over the 48 GB default of a 64GB Mac and inside the 72 GB of a 96GB Mac up to 64K, and its generation speed is capped at about 19 tokens per second on an M3 Ultra and about 6 on a DGX Spark, so a 70B buyer who wants real context starts at the 96GB Mac and plans for jobs that run unattended rather than chat.
6. The runtime adds up to about 1 GB on top of weights plus KV, so treat any setup that lands within 1 GB of a memory line as borderline, not as a fit.

## Evidence 1: weights plus KV cache, by model class and context

`fit_table.py` reads the files in `raw/` and writes `fit-table.csv`; `draw_chart.py fit-table.csv <png>`
draws the article chart from it.

Architecture, from each model's Hugging Face `config.json` (fetched 2026-11-14):

| Model | Source repo | Layers | KV heads | head_dim | KV per token (FP16) |
|---|---|---|---|---|---|
| Qwen3-14B | [Qwen/Qwen3-14B](https://huggingface.co/Qwen/Qwen3-14B) | 40 | 8 | 128 | 160 KiB |
| Qwen3-Coder-30B-A3B-Instruct | [Qwen/Qwen3-Coder-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct) | 48 | 4 | 128 | 96 KiB |
| Qwen3-32B | [Qwen/Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B) | 64 | 8 | 128 | 256 KiB |
| Llama 3.3 70B Instruct | [unsloth/Llama-3.3-70B-Instruct](https://huggingface.co/unsloth/Llama-3.3-70B-Instruct) (public mirror; the meta-llama repo is gated and returned 401) | 80 | 8 | 128 | 320 KiB |
| Qwen3-235B-A22B | [Qwen/Qwen3-235B-A22B](https://huggingface.co/Qwen/Qwen3-235B-A22B) | 94 | 4 | 128 | 188 KiB |

KV (FP16) bytes = 2 (K and V) x layers x KV heads x head_dim x 2 bytes x tokens.

Weight sizes, from the Hugging Face file-listing API (fetched 2026-11-14):

| Model | GGUF repo | Bytes | GiB |
|---|---|---|---|
| Qwen3-14B Q4_K_M | [Qwen/Qwen3-14B-GGUF](https://huggingface.co/Qwen/Qwen3-14B-GGUF) | 9,001,752,960 | 8.38 |
| Qwen3-Coder-30B-A3B Q4_K_M | [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF](https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF) | 18,556,689,568 | 17.28 |
| Qwen3-32B Q4_K_M | [Qwen/Qwen3-32B-GGUF](https://huggingface.co/Qwen/Qwen3-32B-GGUF) | 19,762,149,024 | 18.40 |
| Llama 3.3 70B Q4_K_M | [bartowski/Llama-3.3-70B-Instruct-GGUF](https://huggingface.co/bartowski/Llama-3.3-70B-Instruct-GGUF) | 42,520,398,816 | 39.60 |
| Qwen3-235B-A22B Q2_K (2 parts) | [unsloth/Qwen3-235B-A22B-GGUF](https://huggingface.co/unsloth/Qwen3-235B-A22B-GGUF) | 85,691,002,112 | 79.81 |
| Qwen3-235B-A22B Q4_K_M (3 parts) | [unsloth/Qwen3-235B-A22B-GGUF](https://huggingface.co/unsloth/Qwen3-235B-A22B-GGUF) | 142,154,075,488 | 132.39 |

Totals, weights + FP16 KV, in GiB (the article labels these GB):

| Model | 8K | 16K | 32K | 64K | 128K |
|---|---|---|---|---|---|
| 14B dense Q4_K_M | 9.6 | 10.9 | 13.4 | 18.4 | 28.4 |
| 30B MoE (Coder) Q4_K_M | 18.0 | 18.8 | 20.3 | 23.3 | 29.3 |
| 32B dense Q4_K_M | 20.4 | 22.4 | 26.4 | 34.4 | 50.4 |
| 70B dense Q4_K_M | 42.1 | 44.6 | 49.6 | 59.6 | 79.6 |
| 235B MoE Q2_K | 81.3 | 82.7 | 85.7 | 91.6 | 103.3 |
| 235B MoE Q4_K_M | 133.9 | 135.3 | 138.3 | 144.1 | 155.9 |

- Native context: Qwen3-14B, Qwen3-32B and Qwen3-235B-A22B list 40,960 max positions (128K needs YaRN
  scaling); Qwen3-Coder-30B-A3B lists 262,144; Llama 3.3 70B lists 131,072.
- Units: GiB throughout, because card capacities and `nvidia-smi` are binary (an RTX 4090 reports
  24,564 MiB). `fit-table.csv` also carries decimal GB columns.
- 8-bit KV: llama.cpp's `q8_0` stores 32 int8 values plus one FP16 scale per block (34 bytes per 32
  values, `block_q8_0` in `ggml-common.h`), so 8.5 bits per value, 53% of FP16. `fit-table.csv` has a
  `total_q8_0_plus_overhead_gib` column (weights + 8-bit KV + 1 GiB runtime); Qwen3-32B at 32K comes to 23.7 there. Ollama's FAQ describes
  `q8_0` as "approximately 1/2 the memory of f16" and names `OLLAMA_KV_CACHE_TYPE` (default `f16`) as
  the setting.

## Evidence 2: calculation against two published measurements

The two readings were published in our
[RTX 5060 Ti 16GB vs used RTX 3090 post](https://loopnotes.dev/rtx-5060-ti-vs-used-3090-local-llm/):
Qwen3-Coder-30B-A3B Q4 in LM Studio on an RTX 4090 24GB, September 2026, KV at the default precision,
VRAM read in `nvidia-smi`.

| Context | Calculated weights + KV (GiB) | Measured | Difference |
|---|---|---|---|
| 32K | 20.28 | 21.1 | +0.8 |
| 64K | 23.28 | 23.4 | +0.1 |

The measured values only make sense as GiB (read as decimal GB, the 32K weights + KV alone come to
21.8, above the measurement). The runtime adds up to about 1 GB on top of weights + KV, less when the
card is nearly full. The chart draws weights + KV only, its caption says the runtime adds about 1 GB,
and `fit-table.csv` has a `+1 GiB` column. A row within 1 GB of a memory line is borderline.

## Evidence 3: the default GPU memory limit on Macs, from public llama.cpp logs

Apple documents `MTLDevice.recommendedMaxWorkingSetSize` as "an approximation of how much memory, in
bytes, this GPU device can allocate without affecting its runtime performance" and publishes no ratio.
llama.cpp prints that value as `recommendedMaxWorkingSetSize = N MB` (N in units of 10^6 bytes) when it
starts on Metal (`ggml/src/ggml-metal/ggml-metal-device.m`, commit 61dbf49).

`mac_limit_survey.py` searched GitHub on 2026-11-14 for every public issue in ggml-org/llama.cpp that
contains that string: 264 issues, 161 distinct issue/value lines. It matched each value to a standard
Apple memory size when the value equals 3/4 or 2/3 of that size within 0.4%. Output, one row per line
with the issue number and date: `mac-limit-survey.csv`.

| Inferred memory | Ratio | Lines |
|---|---|---|
| 8, 16, 18, 24, 32 GB | 2/3 | 50 |
| 36 GB | 2/3: 1, 3/4: 10 | 11 |
| 48 GB | 3/4 | 1 |
| 64 GB | 3/4 (48 GiB) | 19 |
| 96 GB | 3/4 (72 GiB) | 3 |
| 128, 192, 512 GB | 3/4 | 10 |
| no match | raised limits, other values | 67 |

Every value that matches a formula follows 2/3 below 36GB and 3/4 from 36GB up. To check your own Mac:
the `recommendedMaxWorkingSetSize` line in the llama.cpp startup log, or `sysctl iogpu.wired_limit_mb`
(0 means the default is in effect).

## Evidence 4: generation speed ceiling for 70B (calculation)

Generating each token reads the whole dense weight file once, so memory bandwidth divided by weight
size is an upper bound on tokens per second:

- Mac Studio M3 Ultra: 819 GB/s ([Apple tech specs](https://support.apple.com/en-us/122211)) / 42.52 GB = 19.3 tokens/s.
- DGX Spark: 273 GB/s ([NVIDIA product page](https://www.nvidia.com/en-us/products/workstations/dgx-spark/)) / 42.52 GB = 6.4 tokens/s.

Real runs land below these ceilings; the ratio between the two machines is the useful part.

## Evidence 5: details moved out of the article (reader fix, 2026-11-14)

The article keeps the conclusions; the working behind them sits here.

- Units: every size is binary GB (GiB), as `nvidia-smi` counts it; the cache is FP16 unless stated.
- 8-bit KV cache: `block_q8_0` stores 32 values in 34 bytes, 8.5 bits per value, 53% of FP16
  ([ggml-common.h at 61dbf49](https://github.com/ggml-org/llama.cpp/blob/61dbf49228c8a96b72e40c89d93cb7c003411f8c/ggml/src/ggml-common.h)).
- 14B on 16GB: Qwen3-14B Q4_K_M at 32K is 13.38 GiB plus about 1 GiB of runtime, 14.4 GiB (`fit-table.csv`).
- 70B on a 64GB Mac (48 GiB GPU share): 8K is 43.1 GiB and 16K is 45.6 GiB with runtime, both under 48;
  32K is 50.6 GiB, over it. Hence "up to about 16K".
- Second way to read the Mac GPU share: llama.cpp prints it at startup on the
  [`recommendedMaxWorkingSetSize` line](https://github.com/ggml-org/llama.cpp/blob/61dbf49228c8a96b72e40c89d93cb7c003411f8c/ggml/src/ggml-metal/ggml-metal-device.m)
  in millions of bytes; a 96GB Mac at the default shows about 77,300 MB (72 GiB).
- The `iogpu.wired_limit_mb=88000` on the 96GB Mac Studio: 85.7GB Q2_K weights of Qwen3-235B-A22B plus about
  1.5 GiB of FP16 cache for 8K and a little buffer; 98,304 MB minus 88,000 leaves about 10GB for macOS.
- Second RTX 4090: the author's box already caps the card at 350W; a second card meant a new case and a
  1500W-class power supply (ask.sh, see gate).
- DGX Spark vs M3 Ultra for dense 70B: 273GB/s vs 819GB/s, about 6 vs 19 tokens per second as a bandwidth
  ceiling (Evidence 4).
- Dev Mac load: the author's 32GB Mac mini M6 with three coding agents, IntelliJ, about 20 Chrome tabs and
  five OrbStack containers sits in the low 30s GB with 2-3GB of swap.
- 24GB check: the author confirmed a 30B at Q4 loads on an RTX 3090 rented in the cloud for three hours.

## Evidence 6: where Ollama reads server settings

From the [Ollama FAQ](https://github.com/ollama/ollama/blob/main/docs/faq.mdx) (read 2026-11-14,
"How do I configure Ollama server?", "How can I tell if my model was loaded onto the GPU?"):

- Linux (systemd): `systemctl edit ollama.service`, one `Environment="KEY=value"` line per variable under
  `[Service]`, then `systemctl daemon-reload` and `systemctl restart ollama`.
- macOS app: `launchctl setenv KEY value` for each variable, then restart the Ollama application.
- Windows: quit Ollama from the taskbar, add user environment variables, start Ollama again.
- `ollama ps` PROCESSOR column: `100% GPU` means fully on the GPU; a CPU/GPU split means part of the model
  is in system memory.
- `OLLAMA_KV_CACHE_TYPE` defaults to `f16`; Flash Attention is used automatically where supported and
  forced on with `OLLAMA_FLASH_ATTENTION=1`.

## Limits

- Every total except the two 30B MoE points is a calculation, not a measurement. Runtimes that
  allocate extra buffers, or a GPU that also drives a display, leave less room than the table shows.
- KV totals assume FP16 KV, the default in Ollama and llama.cpp. 8-bit KV roughly halves the KV part;
  4-bit KV was not calculated.
- The runtime overhead of about 1 GB comes from one model in one runtime on one card.
- In the Mac survey, the memory size is inferred from the logged value, not stated by each reporter,
  and 67 of 161 lines match neither ratio (many from builds where the reporter had raised
  `iogpu.wired_limit_mb`, or from newer macOS). The 48 and 72 GB lines are the usual default, not a
  guarantee.
- The Llama 3.3 70B architecture comes from a public mirror of the gated official repo.
- The speed figures are upper bounds from bandwidth; they ignore prompt processing, which decides time
  to first token on long inputs.

## Files

- `fit_table.py` -> `fit-table.csv`; `draw_chart.py fit-table.csv <png>` draws the article chart.
- `mac_limit_survey.py` -> `mac-limit-survey.csv`.
- `raw/config_*.json`: Hugging Face config.json files. `raw/tree_*.json`: Hugging Face file listings.
- `raw/spec-snippets.md`: the spec lines quoted above, with URLs and fetch date.

## Sources

- Hugging Face model and GGUF repos linked in the tables above (fetched 2026-11-14).
- Apple Developer: [MTLDevice.recommendedMaxWorkingSetSize](https://developer.apple.com/documentation/metal/mtldevice/recommendedmaxworkingsetsize) (read 2026-11-14).
- Apple Support: [Mac Studio (2025) technical specifications](https://support.apple.com/en-us/122211) (read 2026-11-14).
- NVIDIA: [DGX Spark product page](https://www.nvidia.com/en-us/products/workstations/dgx-spark/) (read 2026-11-14).
- llama.cpp: [ggml-metal-device.m](https://github.com/ggml-org/llama.cpp/blob/61dbf49228c8a96b72e40c89d93cb7c003411f8c/ggml/src/ggml-metal/ggml-metal-device.m) and [ggml-common.h](https://github.com/ggml-org/llama.cpp/blob/61dbf49228c8a96b72e40c89d93cb7c003411f8c/ggml/src/ggml-common.h) at commit 61dbf49 (read 2026-11-14).
- Ollama: [FAQ](https://github.com/ollama/ollama/blob/main/docs/faq.mdx), Flash Attention and `OLLAMA_KV_CACHE_TYPE` (read 2026-11-14).
- loopnotes.dev: [RTX 5060 Ti 16GB vs used RTX 3090](https://loopnotes.dev/rtx-5060-ti-vs-used-3090-local-llm/) (the two RTX 4090 measurements).

Article: [Local LLM Hardware: What to Buy for the Model You'll Run](https://loopnotes.dev/local-llm-hardware-what-to-buy/)
