"""사다리: 한 대상을 고칠 때마다(시도 행) 순위·값이 어디까지 왔나, 컷오프 선 하나를 언제 넘었나.
축 밖 값은 축 끝에 "> N" 표지로, 값이 없는 시도는 짧은 글 라벨만 둔다(rag-retrieval-generation-debug 그림 2에서).
"""
import style as S

NAME = "ladder"
QUESTION = "Which attempt finally pushed the value past the cutoff, and how far did each one get?"
EXAMPLE = {
    "frame": "ladder",
    "steps": [
        {"label": "Default config", "beyond": "> 40"},
        {"label": "Cache warmed", "value": 22},
        {"label": "Pool resized", "text": "not tried"},
        {"label": "Index added", "value": 3},
    ],
    "max": 40,
    "cutoff": 10,
    "cutoff_label": "Target",
    "lower_is_better": True,
    "highlight": ["Index added"],
    "xlabel": "Rank",
    "note": "one query, 2026-11",
}


def draw(spec):
    steps = spec["steps"]
    vmax = spec["max"]
    vmin = spec.get("min", 1 if spec.get("lower_is_better", True) else 0)
    hl = set(spec.get("highlight", []))
    n = len(steps)
    fig = S.figure(1.3 + 0.62 * n)
    ax = fig.add_axes([0.30, 0.17, 0.60, 0.70])
    span = vmax - vmin
    over = vmax + span * 0.09          # 축 밖 값을 놓는 자리
    cut = spec.get("cutoff")
    low = spec.get("lower_is_better", True)
    if cut is not None:  # 컷오프 안쪽을 옅은 띠로: 선 하나보다 "안/밖"이 바로 읽힌다
        edge = cut + 0.5 if low else cut
        x0, x1 = (vmin - span * 0.04, edge) if low else (edge, over + span * 0.04)
        ax.axvspan(x0, x1, color=S.ACCENT, alpha=0.10, lw=0, zorder=0)
        ax.axvline(edge, color=S.ACCENT, lw=1.5, zorder=1)
        ax.text(edge + (span * 0.012 if low else -span * 0.012), n - 0.35, spec.get("cutoff_label", ""),
                color=S.ACCENT, fontsize=S.FONT_SMALL, fontweight="bold", va="bottom", ha="left" if low else "right")
    for i, s in enumerate(steps):
        y = n - 1 - i
        on = s["label"] in hl
        col = S.ACCENT if on else S.GRAY
        ax.plot([vmin, over], [y, y], color=S.LIGHT, lw=1.5, zorder=0)
        if "value" in s:
            v = s["value"]
            ax.scatter([v], [y], s=150 if on else 90, color=col, zorder=3)
            ax.text(v + span * 0.025, y + 0.08, f"{v:g}", va="bottom", ha="left", fontsize=S.FONT,
                    color=S.NAVY if on else S.GRAY, fontweight="bold")
        elif "beyond" in s:
            ax.scatter([over], [y], s=120, facecolor="white", edgecolor=S.GRAY, lw=2, zorder=3)
            ax.text(over - span * 0.03, y + 0.08, s["beyond"], va="bottom", ha="right", fontsize=S.FONT,
                    color=S.GRAY, fontweight="bold")
        if s.get("text"):
            x = vmin + span * 0.5 if "value" not in s and "beyond" not in s else None
            if x is not None:
                ax.text(x, y, s["text"], va="center", ha="center", fontsize=S.FONT_SMALL, color=S.GRAY,
                        style="italic", bbox=dict(fc="white", ec="none", pad=2))
            else:
                ax.text(over - span * 0.03, y - 0.12, s["text"], va="top", ha="right", fontsize=S.FONT_SMALL,
                        color=S.GRAY, style="italic")
    ax.set_yticks(range(n))
    ax.set_yticklabels([s["label"] for s in reversed(steps)], fontsize=S.FONT)
    for t, s in zip(ax.get_yticklabels(), reversed(steps)):
        if s["label"] in hl:
            t.set_color(S.ACCENT); t.set_fontweight("bold")
    ax.set_ylim(-0.6, n - 0.2)
    ax.set_xlim(vmin - span * 0.04, over + span * 0.04)
    ticks = spec.get("ticks") or [vmin, cut, vmax]
    ax.set_xticks([t for t in ticks if t is not None])
    ax.spines["left"].set_visible(False); ax.tick_params(left=False)
    if spec.get("xlabel"):
        ax.set_xlabel(spec["xlabel"], fontsize=S.FONT_SMALL)
    S.note(fig, spec.get("note"))
    return fig
