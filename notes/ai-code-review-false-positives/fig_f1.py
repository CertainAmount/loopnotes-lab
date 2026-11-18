"""F1: 100% stacked bars - our team's ~120 comments (approx. 40/20/40) and the three E3 prompts (e3-summary.csv)."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
OUT = HERE.parents[2] / "images/ai-code-review-false-positives/f1-review-pile-three-slices.png"
s = {r["condition"]: r for r in csv.DictReader(open(HERE / "e3-summary.csv"))}
def pct(c):
    r = s[c]; n = int(r["comments"])
    return [100*int(r["acted_on"])/n, 100*int(r["wrong"])/n, 100*int(r["right_low_value"])/n], n
bars = [("Our team (~120, approx.)", [40, 20, 40], None)]
for c, name in (("A", "Diff only"), ("B", "Diff + callers"), ("C", "Risk areas only")):
    p, n = pct(c); bars.append((f"{name} ({n})", p, "5/5 bugs caught"))
ACCENT, DARK, LIGHT, INK, MUTED = "#1f6feb", "#6e7781", "#d0d7de", "#1f2328", "#57606a"
cols = [ACCENT, DARK, LIGHT]; names = ["Acted on", "Wrong", "Right, low value"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 15})
fig, ax = plt.subplots(figsize=(10.24, 5.2), dpi=100)
for i, (lab, p, note) in enumerate(bars):
    y = len(bars) - 1 - i; left = 0
    for v, c, nm in zip(p, cols, names):
        if v > 0:
            ax.barh(y, v - 0.6, left=left + 0.3, height=0.62, color=c)
            if v >= 8:
                ax.text(left + v/2, y, f"{v:.0f}%", ha="center", va="center", fontsize=15,
                        color="white" if c != LIGHT else INK, fontweight="bold" if c == ACCENT else "normal")
        left += v
    ax.text(-2, y, lab, ha="right", va="center", fontsize=15, color=INK)
    if note: ax.text(101, y, note, ha="left", va="center", fontsize=14, color=MUTED)
# direct legend above top bar
top = len(bars) - 1 + 0.55
for x, nm, c in ((20, "Acted on", ACCENT), (50, "Wrong", DARK), (80, "Right, low value", MUTED)):
    ax.text(x, top, nm, ha="center", va="bottom", fontsize=15, color=c, fontweight="bold")
ax.set_xlim(0, 100); ax.set_ylim(-0.6, len(bars) - 0.2)
ax.axis("off")
fig.subplots_adjust(left=0.30, right=0.84, top=0.95, bottom=0.03)
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=100, facecolor="white")
print(OUT)
