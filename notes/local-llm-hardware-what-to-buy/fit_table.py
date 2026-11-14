"""Weights + KV cache per model and context, from official config.json and GGUF file sizes.

Inputs: raw/config_*.json (Hugging Face config.json, fetched 2026-11-14) and
raw/tree_*.json (Hugging Face file listing API, fetched 2026-11-14).
Output: fit-table.csv (one row per model x context).

KV (FP16) bytes = 2 (K and V) x layers x KV heads x head_dim x 2 bytes x tokens.
q8_0 KV is 8.5 bits per value (32 values + one fp16 scale), so 8.5/16 of FP16.
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
GiB = 2 ** 30
OVERHEAD_GIB = 1.0  # runtime buffers + CUDA context; see README "measured vs computed"

MODELS = [
    # label, config file, GGUF listing, GGUF path(s), quant
    ("14B dense (Qwen3-14B)", "config_Qwen_Qwen3-14B.json", "tree_Qwen_Qwen3-14B-GGUF.json",
     ["Qwen3-14B-Q4_K_M.gguf"], "Q4_K_M"),
    ("30B MoE (Qwen3-Coder-30B-A3B)", "config_Qwen_Qwen3-Coder-30B-A3B-Instruct.json",
     "tree_unsloth_Qwen3-Coder-30B-A3B-Instruct-GGUF.json",
     ["Qwen3-Coder-30B-A3B-Instruct-Q4_K_M.gguf"], "Q4_K_M"),
    ("32B dense (Qwen3-32B)", "config_Qwen_Qwen3-32B.json", "tree_Qwen_Qwen3-32B-GGUF.json",
     ["Qwen3-32B-Q4_K_M.gguf"], "Q4_K_M"),
    ("70B dense (Llama 3.3 70B)", "config_unsloth_Llama-3.3-70B-Instruct.json",
     "tree_bartowski_Llama-3.3-70B-Instruct-GGUF.json",
     ["Llama-3.3-70B-Instruct-Q4_K_M.gguf"], "Q4_K_M"),
    ("235B MoE (Qwen3-235B-A22B)", "config_Qwen_Qwen3-235B-A22B.json",
     "tree_unsloth_Qwen3-235B-A22B-GGUF.json",
     ["Q2_K/Qwen3-235B-A22B-Q2_K-00001-of-00002.gguf",
      "Q2_K/Qwen3-235B-A22B-Q2_K-00002-of-00002.gguf"], "Q2_K"),
    ("235B MoE (Qwen3-235B-A22B)", "config_Qwen_Qwen3-235B-A22B.json",
     "tree_unsloth_Qwen3-235B-A22B-GGUF.json",
     ["Q4_K_M/Qwen3-235B-A22B-Q4_K_M-00001-of-00003.gguf",
      "Q4_K_M/Qwen3-235B-A22B-Q4_K_M-00002-of-00003.gguf",
      "Q4_K_M/Qwen3-235B-A22B-Q4_K_M-00003-of-00003.gguf"], "Q4_K_M"),
]
CONTEXTS = [8192, 16384, 32768, 65536, 131072]


def load(name):
    with open(os.path.join(RAW, name)) as f:
        return json.load(f)


def main():
    rows = []
    for label, cfg_f, tree_f, paths, quant in MODELS:
        cfg = load(cfg_f)
        layers = cfg["num_hidden_layers"]
        kvh = cfg["num_key_value_heads"]
        hd = cfg.get("head_dim") or cfg["hidden_size"] // cfg["num_attention_heads"]
        sizes = {e["path"]: e["size"] for e in load(tree_f) if e.get("type") == "file"}
        wbytes = sum(sizes[p] for p in paths)
        per_tok = 2 * layers * kvh * hd * 2
        for ctx in CONTEXTS:
            kv = per_tok * ctx
            rows.append({
                "model": label, "quant": quant, "layers": layers, "kv_heads": kvh, "head_dim": hd,
                "max_position_embeddings": cfg.get("max_position_embeddings"),
                "weights_bytes": wbytes, "weights_gib": round(wbytes / GiB, 2),
                "weights_gb": round(wbytes / 1e9, 2),
                "kv_bytes_per_token_fp16": per_tok, "context": ctx,
                "kv_fp16_gib": round(kv / GiB, 2), "kv_fp16_gb": round(kv / 1e9, 2),
                "kv_q8_0_gib": round(kv * 8.5 / 16 / GiB, 2),
                "total_fp16_gib": round((wbytes + kv) / GiB, 2),
                "total_fp16_gb": round((wbytes + kv) / 1e9, 2),
                "total_fp16_plus_overhead_gib": round((wbytes + kv) / GiB + OVERHEAD_GIB, 2),
                "total_q8_0_plus_overhead_gib": round((wbytes + kv * 8.5 / 16) / GiB + OVERHEAD_GIB, 2),
            })
    out = os.path.join(HERE, "fit-table.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f'{r["model"][:30]:30} {r["quant"]:7} {r["context"]:>6}  W {r["weights_gib"]:6.2f}  '
              f'KV {r["kv_fp16_gib"]:6.2f}  sum {r["total_fp16_gib"]:6.2f}  +1 {r["total_fp16_plus_overhead_gib"]:6.2f}  '
              f'q8 {r["total_q8_0_plus_overhead_gib"]:6.2f} GiB')


if __name__ == "__main__":
    main()
