"""흐름·갈림 도식: 상자와 화살표. 열(col)·행(row) 좌표로 놓는다. AI 도식 대신 정확한 라벨로(2026-11-18)."""
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import style as S

NAME = "flow"
QUESTION = "What happens step by step, and where does the path split?"
EXAMPLE = {
    "frame": "flow",
    "nodes": [
        {"id": "a", "label": "Tool call", "col": 0, "row": 1},
        {"id": "b", "label": "Matcher fits?", "col": 1, "row": 1, "kind": "question"},
        {"id": "c", "label": "Script runs", "col": 2, "row": 0},
        {"id": "d", "label": "Hook skipped", "col": 2, "row": 2, "kind": "bad"},
        {"id": "e", "label": "exit 2: blocked", "col": 3, "row": 0, "kind": "good"},
    ],
    "edges": [["a", "b"], ["b", "c", "yes"], ["b", "d", "no"], ["c", "e"]],
    "note": "",
}


def draw(spec):
    nodes = {n["id"]: n for n in spec["nodes"]}
    ncol = max(n["col"] for n in nodes.values()) + 1
    nrow = max(n.get("row", 0) for n in nodes.values()) + 1
    fig = S.figure(0.8 + 1.15 * nrow)
    ax = fig.add_axes([0.02, 0.06, 0.96, 0.9])
    ax.set_xlim(0, ncol); ax.set_ylim(0, nrow); ax.axis("off")
    bw, bh = 0.78, 0.62
    fills = {"bad": S.RED, "good": S.GREEN, "question": S.NAVY, "focus": S.ACCENT}
    pos = {}
    for n in nodes.values():
        x, y = n["col"] + 0.5, nrow - n.get("row", 0) - 0.5
        pos[n["id"]] = (x, y)
        kind = n.get("kind")
        fc = fills.get(kind, "white")
        ax.add_patch(FancyBboxPatch((x - bw / 2, y - bh / 2), bw, bh, boxstyle="round,pad=0,rounding_size=0.08",
                                    fc=fc, ec=S.NAVY if kind is None else fc, lw=1.6))
        ax.text(x, y, n["label"], ha="center", va="center", wrap=True, fontsize=S.FONT_SMALL,
                color="white" if kind else S.NAVY, fontweight="bold",
                family=S.MONO if n.get("mono") else None)
    for e in spec["edges"]:
        (x0, y0), (x1, y1) = pos[e[0]], pos[e[1]]
        if abs(y0 - y1) < 1e-6:
            p0, p1 = (x0 + bw / 2, y0), (x1 - bw / 2, y1)
        elif abs(x0 - x1) < 1e-6:
            p0 = (x0, y0 - bh / 2 if y1 < y0 else y0 + bh / 2); p1 = (x1, y1 + bh / 2 if y1 < y0 else y1 - bh / 2)
        else:
            p0, p1 = (x0 + bw / 2, y0), (x1 - bw / 2, y1)
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=18, color=S.GRAY, lw=1.8))
        if len(e) > 2:
            mx, my = p0[0] + (p1[0] - p0[0]) * 0.45, p0[1] + (p1[1] - p0[1]) * 0.45
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            ln = (dx * dx + dy * dy) ** 0.5 or 1
            nx, ny = -dy / ln, dx / ln  # 선의 왼쪽 법선
            if ny < 0 or (abs(ny) < 1e-6 and nx > 0):
                nx, ny = -nx, -ny
            ax.text(mx + nx * 0.16, my + ny * 0.16, e[2], ha="center", va="center", fontsize=S.FONT_SMALL, color=S.NAVY,
                    bbox=dict(fc="white", ec="none", pad=1.5))
    S.note(fig, spec.get("note"))
    return fig
