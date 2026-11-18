"""시간선: 한 사건의 단계와 걸린 시간, 어디서 막혔나(실패 지점 강조). 장애·대기·설치 과정."""
import style as S

NAME = "timeline"
QUESTION = "Where did the time go, and at which step did it go wrong?"
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


def draw(spec):
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
