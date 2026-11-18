"""누적 막대: 조건(행)마다 전체를 몇 갈래로 나눈 개수. 조건을 바꾸면 어느 갈래가 줄었나(2026-11-18, ai-code-review-false-positives 그림 1에서 일반화)."""
import style as S

NAME = "stack"
QUESTION = "When the condition changes, which part of the total shrinks?"
EXAMPLE = {
    "frame": "stack",
    "rows": ["Diff only", "Diff + callers", "Risk areas + stay quiet"],
    "classes": [{"name": "Acted on", "color": "accent"}, {"name": "Wrong", "color": "navy"}, {"name": "Right, low value", "color": "light"}],
    "values": [[14, 6, 33], [11, 0, 18], [10, 2, 8]],
    "total_label": "comments",
    "note": "6 diffs, 1 run per prompt, 2026-11-18",
}
COLORS = {"accent": S.ACCENT, "navy": S.NAVY, "light": S.LIGHT, "gray": S.GRAY, "red": S.RED, "green": S.GREEN, "amber": S.AMBER}


def draw(spec):
    rows, classes, vals = spec["rows"], spec["classes"], spec["values"]
    cols = [COLORS.get(c.get("color"), c.get("color", S.GRAY)) for c in classes]
    n = len(rows)
    fig = S.figure(1.2 + 0.78 * n)
    ax = fig.add_axes([0.27, 0.13, 0.70, 0.74])
    xmax = max(sum(v) for v in vals) * 1.27
    for i, (name, row) in enumerate(zip(rows, vals)):
        y = n - 1 - i
        left = 0
        for v, col in zip(row, cols):
            if v:
                ax.barh(y, v - xmax * 0.0045, left=left + xmax * 0.0022, height=0.64, color=col)
                if v >= xmax * 0.025:
                    ax.text(left + v / 2, y, f"{v:g}", ha="center", va="center", fontsize=S.FONT + 1,
                            color=S.NAVY if col in (S.LIGHT, S.AMBER) else "white", fontweight="bold" if col == S.ACCENT else None)
            left += v
        ax.text(-xmax * 0.012, y, name, ha="right", va="center", fontsize=S.FONT + 1)
        tl = spec.get("total_label")
        ax.text(left + xmax * 0.012, y, f"{left:g} {tl}" if (i == 0 and tl) else f"{left:g}", ha="left", va="center",
                fontsize=S.FONT, color=S.GRAY)
    left = 0  # 갈래 이름은 맨 위 막대의 칸 위에 한 번(범례 상자 없이)
    for v, c, col in zip(vals[0], classes, cols):
        ax.text(left + max(v, xmax * 0.06) / 2, n - 1 + 0.44, c["name"], ha="center", va="bottom", fontsize=S.FONT + 1,
                color=S.GRAY if col == S.LIGHT else col, fontweight="bold")
        left += v
    ax.set_xlim(0, xmax); ax.set_ylim(-0.5, n - 0.2); ax.axis("off")
    S.note(fig, spec.get("note"))
    return fig
