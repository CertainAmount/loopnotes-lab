"""F1-alt: comment counts per prompt over the same 6 diffs (e3-summary.csv), stacked by class."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
OUT = HERE.parents[2] / "images/ai-code-review-false-positives/f1-alt-review-pile-counts.png"
s = {r["condition"]: r for r in csv.DictReader(open(HERE / "e3-summary.csv"))}
ACCENT, DARK, LIGHT, INK, MUTED = "#1f6feb", "#6e7781", "#d0d7de", "#1f2328", "#57606a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 15})
fig, ax = plt.subplots(figsize=(10.24, 4.4), dpi=100)
rows = (("A", "Diff only"), ("B", "Diff + callers"), ("C", "Risk areas only"))
for i, (c, name) in enumerate(rows):
    y = len(rows) - 1 - i; r = s[c]; left = 0
    for key, col in (("acted_on", ACCENT), ("wrong", DARK), ("right_low_value", LIGHT)):
        v = int(r[key])
        if v:
            ax.barh(y, v - 0.25, left=left + 0.12, height=0.62, color=col)
            ax.text(left + v/2, y, str(v), ha="center", va="center", fontsize=15,
                    color=INK if col == LIGHT else "white", fontweight="bold" if col == ACCENT else "normal")
        left += v
    ax.text(-1, y, name, ha="right", va="center", fontsize=15, color=INK)
    ax.text(left + 1, y, f"{left} comments", ha="left", va="center", fontsize=14, color=MUTED)
top = len(rows) - 1 + 0.5
for x, nm, c in ((7, "Acted on", ACCENT), (22, "Wrong", DARK), (40, "Right, low value", MUTED)):
    ax.text(x, top, nm, ha="center", va="bottom", fontsize=15, color=c, fontweight="bold")
ax.set_xlim(0, 66); ax.set_ylim(-0.6, len(rows) - 0.25); ax.axis("off")
fig.subplots_adjust(left=0.20, right=0.98, top=0.93, bottom=0.03)
fig.savefig(OUT, dpi=100, facecolor="white"); print(OUT)
