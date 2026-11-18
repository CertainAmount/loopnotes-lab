"""시간선: 한 사건의 단계와 걸린 시간, 어디서 막혔나(실패 지점 강조). 장애·대기·설치 과정."""
import style as S

NAME = "timeline"
QUESTION = "Where did the time go, and at which step did it go wrong? (mode steps: order only, label above, small line below)"
EXAMPLE = {
    "frame": "timeline",
    "unit": "min",
    "events": [
        {"t": 0, "label": "cat .env runs"},
        {"t": 5, "label": "Script tested by hand"},
        {"t": 18, "label": "/hooks looks fine", "bad": True},
        {"t": 25, "label": "Log line: matcher"},
    ],
    "note": "Author's first .env guard",
}


def steps(spec):
    """순서만 있는 단계(시각 없음): 위에 단계 이름, 아래에 작은 줄. ai-code-review-false-positives 그림 3에서 일반화."""
    ev = spec["events"]
    fig = S.figure(3.0)
    ax = fig.add_axes([0.02, 0.12, 0.96, 0.84])
    xs = list(range(len(ev)))
    ax.plot([xs[0], xs[-1]], [0, 0], color=S.LIGHT, lw=7, solid_capstyle="round", zorder=1)
    for x, e in zip(xs, ev):
        hot, first = e.get("bad") or e.get("focus"), x == 0
        col = S.ACCENT if hot else (S.GRAY if first else S.NAVY)
        ax.scatter([x], [0], s=420 if hot else 240, zorder=3, color="white" if first else col, edgecolors=col, linewidths=2.5)
        ax.text(x, 0.28, e["label"], ha="center", va="bottom", fontsize=S.FONT + 1, color=col,
                fontweight="bold" if hot else None, linespacing=1.15)
        if e.get("sub"):
            ax.text(x, -0.28, e["sub"], ha="center", va="top", fontsize=S.FONT_SMALL + 1, color=S.GRAY)
    ax.set_xlim(-0.55, len(ev) - 0.45); ax.set_ylim(-0.95, 1.25); ax.axis("off")
    S.note(fig, spec.get("note"))
    return fig


def draw(spec):
    if spec.get("mode") == "steps" or "t" not in spec["events"][0]:
        return steps(spec)
    ev = spec["events"]
    unit = spec.get("unit", "")
    fig = S.figure(2.3)
    ax = fig.add_axes([0.05, 0.18, 0.90, 0.70])
    t0, t1 = ev[0]["t"], ev[-1]["t"]
    span = (t1 - t0) or 1
    ax.plot([t0, t1], [0, 0], color=S.LIGHT, lw=6, solid_capstyle="round", zorder=1)
    for i, e in enumerate(ev):
        c = S.RED if e.get("bad") else (S.ACCENT if i == len(ev) - 1 else S.NAVY)
        ax.scatter([e["t"]], [0], s=160, color=c, zorder=3)
        up = i % 2 == 0
        ax.text(e["t"], 0.45 if up else -0.45, e["label"], ha="center", va="bottom" if up else "top",
                fontsize=S.FONT_SMALL, color=c, fontweight="bold" if e.get("bad") else None)
        ax.text(e["t"], 0.16 if up else -0.16, f"{e['t']:g} {unit}".strip(), ha="center", va="bottom" if up else "top",
                fontsize=S.FONT_SMALL - 1, color=S.GRAY)
    ax.set_xlim(t0 - span * 0.12, t1 + span * 0.12); ax.set_ylim(-1.1, 1.1); ax.axis("off")
    S.note(fig, spec.get("note"))
    return fig
