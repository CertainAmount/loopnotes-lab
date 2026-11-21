"""E2/E3/E4 (2026-11-21): Qwen3.6-27B (and 3.8-27B) cache by the R1 rules, the Q4_K_M weight files, and the
two figure specs drawn with tools/viz.

Inputs: raw/config_Qwen_Qwen3.6-27B.json, raw/config_Qwen_Qwen3.8-27B.json, raw/tree_*Qwen3.6-27B-GGUF.json,
fit-table.csv (Qwen3-32B, Qwen3-Coder-30B weights), ../../../research/R1-kv-cache/kv-table.csv.
Outputs: qwen36-kv-row.csv, qwen36-q4-files.csv, figures/spec-1.json, figures/spec-2.json.
Rules (same as R1 kv.py): plain = 2 x layers x KV heads x head_dim x 2 bytes per token; aware = only
full-attention layers grow with context; Gated DeltaNet layers keep a fixed FP32 state.
Totals = Q4_K_M weights + FP16 cache (+ state) + 1 GiB runtime (README Evidence 2).
"""
import csv, json, pathlib

HERE = pathlib.Path(__file__).parent
R1 = HERE.parents[2] / "research/R1-kv-cache/kv-table.csv"
GIB, MIB = 2 ** 30, 2 ** 20
CTX = [8192, 16384, 32768, 65536, 131072]


def kv(cfgp):
    c = json.load(open(cfgp)); c = c.get("text_config", c)
    L, kvh, hd = c["num_hidden_layers"], c["num_key_value_heads"], c["head_dim"]
    full = sum(t == "full_attention" for t in c["layer_types"])
    lin = L - full
    per_layer = 2 * kvh * hd * 2
    kd, vd, nk, nv, k = c["linear_key_head_dim"], c["linear_value_head_dim"], c["linear_num_key_heads"], c["linear_num_value_heads"], c["linear_conv_kernel_dim"]
    state = lin * ((2 * nk * kd + nv * vd) * (k - 1) + nv * kd * vd) * 4
    return dict(layers=L, full=full, plain_tok=L * per_layer, aware_tok=full * per_layer, state=state,
                native_ctx=c["max_position_embeddings"])


rows = []
for name, f in [("Qwen3.6 27B", "config_Qwen_Qwen3.6-27B.json"), ("Qwen3.8 27B", "config_Qwen_Qwen3.8-27B.json")]:
    k = kv(HERE / "raw" / f)
    r = {"model": name, "repo": "Qwen/" + f[12:-5], "rule": "`layer_types` (Gated DeltaNet + full attention, 1 in 4 full)",
         "layers": k["layers"], "global_layers": k["full"], "native_ctx": k["native_ctx"],
         "plain_kib_per_token": k["plain_tok"] / 1024, "aware_kib_per_token": k["aware_tok"] / 1024,
         "state_mib": round(k["state"] / MIB, 1)}
    for c in (8192, 32768, 131072):
        t = f"{c // 1024}k"
        r[f"plain_mib_{t}"] = k["plain_tok"] * c / MIB
        r[f"aware_mib_{t}"] = k["aware_tok"] * c / MIB
        r[f"plain_over_aware_{t}"] = round(k["plain_tok"] / k["aware_tok"], 2)
    rows.append(r)
with open(HERE / "qwen36-kv-row.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

files = []
for repo in ["unsloth/Qwen3.6-27B-GGUF", "lmstudio-community/Qwen3.6-27B-GGUF", "bartowski/Qwen_Qwen3.6-27B-GGUF", "ggml-org/Qwen3.6-27B-GGUF"]:
    for x in json.load(open(HERE / "raw" / f"tree_{repo.replace('/', '_')}.json")):
        if x["path"].endswith("Q4_K_M.gguf"):
            s = x.get("lfs", {}).get("size", x.get("size"))
            files.append({"repo": repo, "file": x["path"], "bytes": s, "gib": round(s / GIB, 2), "checked": "2026-11-21"})
with open(HERE / "qwen36-q4-files.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(files[0])); w.writeheader(); w.writerows(files)

fit = {(r["model"], r["quant"]): r for r in csv.DictReader(open(HERE / "fit-table.csv"))}
w32 = int(fit[("32B dense (Qwen3-32B)", "Q4_K_M")]["weights_bytes"]) / GIB
wcoder = int(fit[("30B MoE (Qwen3-Coder-30B-A3B)", "Q4_K_M")]["weights_bytes"]) / GIB
w27 = files[0]["bytes"] / GIB  # unsloth, the most downloaded Qwen3.6-27B GGUF on 2026-11-21
k27 = kv(HERE / "raw/config_Qwen_Qwen3.6-27B.json")
tot = lambda w, tok, ctx, extra=0: round(w + (tok * ctx + extra) / GIB + 1, 2)
x = [8, 16, 32, 64, 128]
aware = [tot(w27, k27["aware_tok"], c, k27["state"]) for c in CTX]
plain = [tot(w27, k27["plain_tok"], c) for c in CTX[:4]]
q32 = [tot(w32, 2 * 64 * 8 * 128 * 2, c) for c in CTX[:3]]
coder = [tot(wcoder, 2 * 48 * 4 * 128 * 2, c) for c in CTX]
spec1 = {
    "frame": "curve", "x": x, "xscale": "log", "xticklabels": ["8K", "16K", "32K", "64K", "128K"],
    "xlabel": "Context length (tokens)", "height": 5.6,
    "panels": [{"title": "Memory needed: Q4 weights + cache + runtime", "ylim": [14, 34], "yticks": [16, 20, 24, 28, 32], "suffix": " GB"}],
    "series": [
        {"name": "Qwen3.6 27B", "style": "accent", "values": [aware], "dy": [-8]},
        {"name": "Qwen3.6 27B, textbook formula", "style": "muted", "dashed": True, "x": x[:4], "values": [plain], "labels": ["27B, textbook formula"]},
        {"name": "Qwen3 32B", "style": "navy", "x": x[:3], "values": [q32], "label_offset": [-10, 12]},
        {"name": "Qwen3-Coder 30B", "style": "muted", "values": [coder], "labels": ["Qwen3-Coder 30B"], "dy": [8]},
    ],
    "hlines": [{"y": 24, "label": "24GB card"}, {"y": 16, "label": "16GB card", "below": True}],
    "points": [{"x": [32, 64], "y": [21.1, 23.4], "label": "4090 measured", "style": "navy", "offset": [0, -11], "ha": "center", "va": "top"}],
    "note": f"Q4_K_M weights, FP16 cache, +1 GiB runtime; Qwen3.6 27B {w27:.2f} GiB (unsloth). Calculated from config.json, 2026-11-21.",
}
tab = {r["model"]: r for r in csv.DictReader(open(R1))}
pick = [("Qwen3.6 27B", None, "1 in 4 layers full"), ("Gemma 3 27B", "Gemma 3 27B", "1 in 6 layers global"),
        ("EXAONE 4.0 32B", "EXAONE 4.0 32B", "1 in 4 layers global"), ("gpt-oss 20B", "gpt-oss 20B", "half layers windowed"),
        ("DeepSeek V2 Lite 16B", "DeepSeek-Coder-V2-Lite 16B", "compressed latent"),
        ("Qwen3 32B", "Qwen3 32B", "all layers"), ("Qwen3-Coder 30B", "Qwen3-Coder 30B-A3B", "all layers"),
        ("Mistral Small 3.2 24B", "Mistral Small 3.2 24B", "all layers"), ("Llama 3.3 70B", "Llama 3.3 70B", "all layers")]
items, b, a, tags = [], [], [], []
for label, key, tag in pick:
    if key is None:
        p, q = rows[0]["plain_mib_32k"], rows[0]["aware_mib_32k"]
    else:
        p, q = float(tab[key]["plain_mib_32k"]), float(tab[key]["aware_mib_32k"])
    items.append(label); b.append(round(p / 1024, 1)); a.append(round(q / 1024, 1)); tags.append(tag)
spec2 = {"frame": "compare", "items": items, "tags": tags, "hi": ["Qwen3.6 27B"],
         "before": {"name": "textbook formula", "values": b}, "after": {"name": "what the model keeps", "values": a},
         "unit": " GB", "note": "KV cache at 32K tokens, FP16, from each model's config.json (R1 table + Qwen3.6 27B, 2026-11-21)"}
(HERE / "figures").mkdir(exist_ok=True)
(HERE / "figures/spec-1.json").write_text(json.dumps(spec1, indent=1) + "\n")
(HERE / "figures/spec-2.json").write_text(json.dumps(spec2, indent=1) + "\n")
print("27B weights GiB", round(w27, 2), "state MiB", round(k27["state"] / MIB, 1))
print("aware", aware); print("plain", plain); print("32B", q32); print("coder", coder)
print(list(zip(items, b, a)))
