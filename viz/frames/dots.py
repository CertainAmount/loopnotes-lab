"""점그림: 항목마다 여러 번 잰 값(반복 측정 분포, 벤치). 평균만 보이면 숨는 흔들림을 보인다."""
import style as S

NAME = "dots"
QUESTION = "How spread out are repeated measurements, and where does each item sit?"
EXAMPLE = {
    "frame": "dots",
    "items": ["llama.cpp", "vLLM"],
    "runs": [[101, 99, 103, 98, 102], [140, 151, 138, 149, 145]],
    "unit": " tok/s",
    "highlight": ["vLLM"],
    "note": "RTX 4090, 5 runs each, 2026-11",
}


def draw(spec):
    items, runs = spec["items"], spec["runs"]
    unit = spec.get("unit", "")
    hl = set(spec.get("highlight", []))
    n = len(items)
    fig = S.figure(1.1 + 0.6 * n)
    ax = fig.add_axes([0.24, 0.16, 0.66, 0.74])
    allv = [v for r in runs for v in r]
    lo, hi = min(allv), max(allv)
    pad = (hi - lo) * 0.15 or 1
    for i, (it, r) in enumerate(zip(items, runs)):
        y = n - 1 - i
        c = S.ACCENT if it in hl else S.GRAY
        ax.scatter(r, [y] * len(r), s=90, color=c, alpha=0.75, zorder=2)
        m = sorted(r)[len(r) // 2]
        ax.plot([m, m], [y - 0.25, y + 0.25], color=S.NAVY, lw=2.5, zorder=3)
        ax.text(max(r) + pad * 0.4, y, f"median {m:g}{unit}", va="center", fontsize=S.FONT_SMALL, color=S.NAVY)
    ax.set_yticks(range(n)); ax.set_yticklabels(list(reversed(items)))
    ax.set_xlim(lo - pad, hi + pad * 2.6)
    ax.spines["left"].set_visible(False); ax.tick_params(left=False)
    if spec.get("xlabel"):
        ax.set_xlabel(spec["xlabel"], fontsize=S.FONT_SMALL)
    S.note(fig, spec.get("note"))
    return fig
