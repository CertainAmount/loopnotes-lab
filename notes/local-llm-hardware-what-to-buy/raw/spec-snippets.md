# Spec lines quoted in the research note (fetched 2026-11-14)

- https://support.apple.com/en-us/122211 (Mac Studio 2025 tech specs): "Apple M3 Ultra chip 28-core CPU ... 60-core GPU ... 32-core Neural Engine 819GB/s memory bandwidth"
- https://www.apple.com/newsroom/2025/03/apple-unveils-new-mac-studio-the-most-powerful-mac-ever/: "over 800GB/s of unified memory bandwidth. Mac Studio with M3 Ultra starts with 96GB of unified memory"
- https://www.apple.com/mac-studio/specs/ now lists M5 Max / M5 Ultra configurations (M3 Ultra no longer on the current specs page).
- https://www.nvidia.com/en-us/products/workstations/dgx-spark/: "128 GB LPDDR5x, coherent unified system memory  Memory Interface 256-bit  Memory Bandwidth 273 GB/s"
- https://developer.apple.com/documentation/metal/mtldevice/recommendedmaxworkingsetsize: "An approximation of how much memory, in bytes, this GPU device can allocate without affecting its runtime performance."
- https://github.com/ggml-org/llama.cpp/blob/61dbf49228c8a96b72e40c89d93cb7c003411f8c/ggml/src/ggml-metal/ggml-metal-device.m line 1364: `GGML_LOG_INFO("%s: recommendedMaxWorkingSetSize  = %8.2f MB\n", __func__, dev->props.max_working_set_size / 1e6);`
- https://github.com/ggml-org/llama.cpp/blob/61dbf49228c8a96b72e40c89d93cb7c003411f8c/ggml/src/ggml-common.h line 251: `#define QK8_0 32` / `block_q8_0 { ggml_half d; int8_t qs[QK8_0]; }`
- https://github.com/ollama/ollama/blob/main/docs/faq.mdx: "Ollama uses Flash Attention automatically when the selected backend and devices support it. To force Flash Attention on, set `OLLAMA_FLASH_ATTENTION=1`"; "`OLLAMA_KV_CACHE_TYPE` - The quantization type for the K/V cache. Default is `f16`."; "`q8_0` - 8-bit quantization, uses approximately 1/2 the memory of `f16`"
