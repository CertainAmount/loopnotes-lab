"""E1 (2026-11-21): does llama.cpp allocate a hybrid model's KV cache only for its full-attention layers?

Loads each small GGUF once per context with llama-completion (CPU, no warmup), stops as soon as the cache
is reserved, and reads the `llama_kv_cache: size` and `llama_memory_recurrent: size` lines. Compares with
the plain formula (every layer keeps every token) and the architecture-aware count (only full-attention
layers grow), both FP16. Run under a 2 GB memory cap:
  systemd-run --user --scope -p MemoryMax=2G -p MemorySwapMax=0 python3 hybrid_alloc.py <bin dir> <gguf dir>
Writes hybrid-alloc.csv and logs/.
"""
import csv, json, os, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).parent
BIN, GGUF = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
R1 = HERE.parents[2] / "research/R1-kv-cache/raw"
MIB = 2 ** 20
RUNS = [  # name, gguf, config path, kind
    ("Qwen3.5 0.8B (hybrid, 6 of 24 full)", "Qwen3.5-0.8B-Q4_K_M.gguf", HERE / "raw/config_Qwen_Qwen3.5-0.8B.json"),
    ("Granite 4.0-H 350M (hybrid, 4 of 32 full)", "granite-4.0-h-350m-Q4_K_M.gguf", R1 / "config_ibm-granite_granite-4.0-h-350m.json"),
    ("Qwen3 0.6B (all 28 full, control)", "Qwen3-0.6B-Q8_0.gguf", R1 / "config_Qwen_Qwen3-0.6B.json"),
]
CTX = [8192, 32768, 131072]
SIZE = re.compile(r"(llama_kv_cache|llama_memory_recurrent): size = +([\d.]+) MiB \( *(\d+) cells, +(\d+) layers")


def predict(cfgp, ctx):
    c = json.load(open(cfgp)); c = c.get("text_config", c)
    hd = c.get("head_dim") or c["hidden_size"] // c["num_attention_heads"]
    per_layer = 2 * c["num_key_value_heads"] * hd * 2
    L = c["num_hidden_layers"]
    full = sum(1 for t in c.get("layer_types", ["full_attention"] * L) if t in ("full_attention", "attention"))
    return round(L * per_layer * ctx / MIB, 1), round(full * per_layer * ctx / MIB, 1), full, L


env = {**os.environ, "LD_LIBRARY_PATH": str(BIN)}
(HERE / "logs").mkdir(exist_ok=True)
ver = subprocess.run([BIN / "llama-completion", "--version"], env=env, capture_output=True, text=True)
ver = (ver.stdout + ver.stderr).strip().splitlines()[0]
rows = []
for name, f, cfgp in RUNS:
    for ctx in CTX:
        cmd = [BIN / "llama-completion", "-m", GGUF / f, "-c", str(ctx), "-p", "hi", "-n", "1",
               "--no-warmup", "-t", "6", "-fa", "on", "-v"]
        p = subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        seen = []
        for line in p.stderr:
            seen.append(line)
            if "sched_reserve:" in line or "failed" in line.lower():
                break
        p.kill(); p.wait()
        lines = [l.split(" I ", 1)[-1] for l in "".join(seen).splitlines() if SIZE.search(l) or "failed" in l.lower()]
        (HERE / "logs" / f"{f}.{ctx}.txt").write_text("\n".join(lines) + "\n")
        parts = [m for m in (SIZE.search(l) for l in lines) if m]
        kv = sum(float(m.group(2)) for m in parts if m.group(1) == "llama_kv_cache")
        st = sum(float(m.group(2)) for m in parts if m.group(1) == "llama_memory_recurrent")
        kv_layers = sum(int(m.group(4)) for m in parts if m.group(1) == "llama_kv_cache")
        plain, aware, full, L = predict(cfgp, ctx)
        rows.append({"model": name, "gguf": f, "ctx": ctx, "layers": L, "full_attention_layers": full,
                     "kv_layers_allocated": kv_layers, "kv_mib_measured": round(kv, 1), "state_mib_measured": round(st, 1),
                     "plain_mib_predicted": plain, "aware_mib_predicted": aware,
                     "measured_over_aware": round(kv / aware, 3) if aware else "", "llama_cpp": ver})
        print(rows[-1], flush=True)
with open(HERE / "hybrid-alloc.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
