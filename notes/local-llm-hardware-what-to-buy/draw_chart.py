"""Draw the fit chart from fit-table.csv: Q4 weights + FP16 KV cache per model at 8K / 32K / 128K,
against memory lines. Usage: draw_chart.py fit-table.csv out.png"""
import csv, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

src, out = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(src)))
GROUPS = [  # (csv model, quant, short label)
    ("14B dense (Qwen3-14B)", "Q4_K_M", "14B dense"),
    ("30B MoE (Qwen3-Coder-30B-A3B)", "Q4_K_M", "30B MoE"),
    ("32B dense (Qwen3-32B)", "Q4_K_M", "32B dense"),
    ("70B dense (Llama 3.3 70B)", "Q4_K_M", "70B dense"),
    ("235B MoE (Qwen3-235B-A22B)", "Q2_K", "235B MoE, Q2_K"),
]
CTX = [(8192, "8K"), (32768, "32K"), (131072, "128K")]
LINES = [(16, "16GB card", "right"), (24, "24GB card", "left"), (48, "64GB Mac\ndefault", "center"),
         (72, "96GB Mac\ndefault", "center"), (128, "128GB", "center")]
INK, MUTED, SURF, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#ecebe7"
W_COL, KV_COL = "#2a78d6", "#eb6834"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13})
fig, ax = plt.subplots(figsize=(12, 8), dpi=120)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)

y, ticks, ticklabels, bar_y = 0.0, [], [], {}
for model, quant, short in GROUPS:
    for ctx, cl in CTX:
        r = next(r for r in rows if r["model"] == model and r["quant"] == quant and int(r["context"]) == ctx)
        w, kv = float(r["weights_gib"]), float(r["kv_fp16_gib"])
        ax.barh(y, w, height=0.72, color=W_COL, edgecolor=SURF, linewidth=2)
        ax.barh(y, kv, left=w, height=0.72, color=KV_COL, edgecolor=SURF, linewidth=2)
        lab = f"{w + kv:.0f}"
        if short == "30B MoE" and cl == "32K":
            lab = f"{w + kv:.0f} calculated, 21.1 measured"
        ax.text(max(w + kv, 21.1 if lab != f"{w + kv:.0f}" else 0) + 1.4, y, lab, va="center", color=MUTED, fontsize=11)
        ticks.append(y); ticklabels.append(f"{short}  {cl}" if cl == "8K" else cl)
        bar_y[(short, cl)] = y
        y += 1
    y += 0.7

for x, lab, ha in LINES:
    ax.axvline(x, color="#9a9890", lw=1.2, ls=(0, (4, 3)), zorder=0)
    ax.text(x + (-0.6 if ha == "right" else 0.6 if ha == "left" else 0), -1.6, lab, ha=ha, va="bottom", color=MUTED, fontsize=10.5)

# measured on the author's RTX 4090 (Qwen3-Coder-30B-A3B Q4, nvidia-smi): 32K 21.1, 64K 23.4
my = bar_y[("30B MoE", "32K")]
ax.plot([21.1], [my], "D", ms=9, color=INK, mec=SURF, mew=2, zorder=5)

ax.set_yticks(ticks); ax.set_yticklabels(ticklabels, color=MUTED)
ax.invert_yaxis(); ax.set_ylim(y - 0.5, -2.2)
ax.set_xlim(0, 135); ax.set_xlabel("Memory needed (GB)", color=MUTED)
for sp in ["top", "right", "left"]: ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color("#c3c2b7")
ax.tick_params(colors=MUTED, length=0); ax.grid(axis="x", color=GRID, lw=1); ax.set_axisbelow(True)
ax.set_title("Does it fit? Model weights + context memory", loc="left", color=INK, fontsize=16, pad=34)
h1 = plt.Rectangle((0, 0), 1, 1, color=W_COL); h2 = plt.Rectangle((0, 0), 1, 1, color=KV_COL)
ax.legend([h1, h2], ["Model weights (Q4_K_M)", "Context memory (KV, FP16)"], loc="upper right", bbox_to_anchor=(1.0, 0.86),
          frameon=True, facecolor=SURF, edgecolor=SURF, framealpha=1, fontsize=11.5, labelcolor=INK)
fig.text(0.01, 0.01, "Hugging Face config.json and GGUF sizes, Nov 14, 2026. GB = GiB. Runtime adds ~1 GB.",
         color=MUTED, fontsize=10)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(out, facecolor=fig.get_facecolor())
