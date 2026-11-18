"""집계 막대: 항목별 값(가로 막대, 직접 라벨). 그룹이 있으면 그룹 막대. 네이버 집계, PR 리뷰 건수, 분류 결과."""
import style as S

NAME = "bars"
QUESTION = "How many of each kind, and which one dominates?"
EXAMPLE = {
    "frame": "bars",
    "items": ["Led to a fix", "Style or taste", "False positive"],
    "series": [{"name": "AI review comments", "values": [40, 40, 20]}],
    "unit": "%",
    "highlight": ["False positive"],
    "note": "About 50 PRs, 2025-2026, author's team",
}


def draw(spec):
    items, series = spec["items"], spec["series"]
    unit = spec.get("unit", "")
    hl = set(spec.get("highlight", []))
    n, k = len(items), len(series)
    fig = S.figure(0.9 + 0.55 * n * max(1, k * 0.75))
    ax = fig.add_axes([0.30, 0.12, 0.62, 0.80])
    h = 0.8 / k
    mx = max(max(s["values"]) for s in series) or 1
    colors = [S.ACCENT, S.NAVY, S.GRAY]
    for si, s in enumerate(series):
        for i, (it, v) in enumerate(zip(items, s["values"])):
            y = n - 1 - i + (k - 1) / 2 * h - si * h
            c = (S.ACCENT if it in hl else S.GRAY) if k == 1 else colors[si % 3]
            ax.barh(y, v, height=h * 0.85, color=c)
            ax.text(v + mx * 0.015, y, f"{v:g}{unit}", va="center", fontsize=S.FONT, color=S.NAVY,
                    fontweight="bold" if it in hl else None)
            if k > 1 and i == 0:
                ax.text(v + mx * 0.12, y, s["name"], va="center", fontsize=S.FONT_SMALL, color=colors[si % 3])
    ax.set_yticks([n - 1 - i for i in range(n)]); ax.set_yticklabels(items)
    ax.set_xlim(0, mx * 1.25); ax.set_xticks([])
    ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)
    S.note(fig, spec.get("note"))
    return fig
