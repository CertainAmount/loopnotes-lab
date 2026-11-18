"""전후 비교(덤벨): 같은 항목을 두 조건(버전, 설정, 기기)에서 잰 값. 업데이트마다 다시 재는 엔진(E2·E8)."""
import style as S

NAME = "compare"
QUESTION = "What changed for each item between two conditions?"
EXAMPLE = {
    "frame": "compare",
    "items": ["8B Q4", "14B Q4", "32B Q4"],
    "before": {"name": "Driver 550", "values": [92, 61, 28]},
    "after": {"name": "Driver 560", "values": [104, 66, 30]},
    "unit": " tok/s",
    "note": "RTX 4090, Ollama 0.12, 2026-11",
}


def draw(spec):
    items, b, a = spec["items"], spec["before"], spec["after"]
    unit = spec.get("unit", "")
    n = len(items)
    fig = S.figure(0.9 + 0.45 * n)
    ax = fig.add_axes([0.22, 0.16, 0.72, 0.66])
    vals = b["values"] + a["values"]
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.25 or 1
    for i, it in enumerate(items):
        y = n - 1 - i
        x0, x1 = b["values"][i], a["values"][i]
        ax.plot([x0, x1], [y, y], color=S.LIGHT, lw=6, solid_capstyle="round", zorder=1)
        ax.scatter([x0], [y], s=140, color=S.GRAY, zorder=2)
        ax.scatter([x1], [y], s=140, color=S.ACCENT, zorder=3)
        right = max(x0, x1)
        ax.text(right + pad * 0.25, y, f"{x1:g}{unit}", va="center", fontsize=S.FONT, color=S.ACCENT, fontweight="bold")
        ax.text(min(x0, x1) - pad * 0.25, y, f"{x0:g}", va="center", ha="right", fontsize=S.FONT_SMALL, color=S.GRAY)
    ax.set_yticks(range(n)); ax.set_yticklabels(list(reversed(items))); ax.set_ylim(-0.6, n - 0.4)
    ax.set_xlim(lo - pad * 0.9, hi + pad * 1.4); ax.set_xticks([])
    ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False); ax.tick_params(left=False)
    fig.text(0.24, 0.88, "●", color=S.GRAY, fontsize=S.FONT); fig.text(0.26, 0.88, b["name"], fontsize=S.FONT_SMALL)
    fig.text(0.24 + 0.03 + 0.012 * len(b["name"]), 0.88, "●", color=S.ACCENT, fontsize=S.FONT)
    fig.text(0.26 + 0.03 + 0.012 * len(b["name"]), 0.88, a["name"], fontsize=S.FONT_SMALL)
    S.note(fig, spec.get("note"))
    return fig
