"""재현 매트릭스: 경우(행) × 조건(열) → 결과 칸. E1·E2 같은 '어느 설정에서 무엇이 일어났나' 실험."""
from matplotlib.patches import FancyBboxPatch
import style as S

NAME = "matrix"
QUESTION = "Under which setting does each case block, run, or fail silently?"
EXAMPLE = {
    "frame": "matrix",
    "rows": ["Path typo", "No execute bit", "Lowercase matcher"],
    "cols": ["Interactive", "claude -p"],
    "cells": [["ran", "ran"], ["ran", "ran"], ["silent", "silent"]],
    "cell_text": [["hook failed", "no warning"], ["hook failed", "no warning"], ["no log", "no log"]],
    "note": "Claude Code 2.1.327, 2026-11-18, this machine",
}


def draw(spec):
    rows, cols, cells = spec["rows"], spec["cols"], spec["cells"]
    texts = spec.get("cell_text")
    outcomes = {**S.OUTCOMES, **{k: tuple(v) for k, v in spec.get("outcomes", {}).items()}}
    nr, nc = len(rows), len(cols)
    label_w = spec.get("label_width", 0.34)
    h_in = 1.0 + 0.62 * nr + 0.35 * max(0, len(set(c for r in cells for c in r)) - 2) + 0.4
    fig = S.figure(h_in)
    aspect = ((nr + 1) / (h_in * 0.84)) / (1 / S.WIDTH_IN)  # 모서리를 x·y 같은 반지름으로(타원 끝 방지)
    ax = fig.add_axes([0, 0.08, 1, 0.84])
    ax.set_xlim(0, 1); ax.set_ylim(0, nr + 1); ax.axis("off")
    cw = (1 - label_w - 0.02) / nc
    sub = spec.get("col_sub")  # 열 머리 아래 작은 줄(열마다 합계 등)
    for j, c in enumerate(cols):
        ax.text(label_w + cw * (j + 0.5), nr + (0.62 if sub else 0.45), c, ha="center", va="center", fontweight="bold", fontsize=S.FONT)
        if sub:
            ax.text(label_w + cw * (j + 0.5), nr + 0.22, sub[j], ha="center", va="center", fontsize=S.FONT_SMALL, color=S.GRAY)
    used = []
    for i, r in enumerate(rows):
        y = nr - i - 0.5
        ax.text(label_w - 0.02, y, r, ha="right", va="center", fontsize=S.FONT,
                family=S.MONO if spec.get("mono_rows") else None)
        for j in range(nc):
            key = cells[i][j]
            lab, col = outcomes.get(key, (key, S.GRAY))
            if key not in used:
                used.append(key)
            x = label_w + cw * j + 0.008
            ax.add_patch(FancyBboxPatch((x, y - 0.36), cw - 0.016, 0.72, boxstyle="round,pad=0,rounding_size=0.008", mutation_aspect=aspect,
                                        fc=col, ec="none", alpha=0.9 if col != S.LIGHT else 1))
            t = texts[i][j] if texts else lab
            ax.text(x + (cw - 0.016) / 2, y, t, ha="center", va="center", fontsize=S.FONT_SMALL,
                    color="white" if col not in (S.LIGHT, S.AMBER) else S.NAVY, fontweight="bold")
    if texts and spec.get("legend", True):  # 칸에 자세한 글이 있으면 결과 색의 뜻을 머리 줄 왼쪽에
        y = nr + 0.45
        for k in used:
            lab, col = outcomes.get(k, (k, S.GRAY))
            ax.text(0.01, y, "■", color=col, fontsize=S.FONT, va="center")
            ax.text(0.035, y, lab, fontsize=S.FONT_SMALL, va="center")
            y -= 0.32
    S.note(fig, spec.get("note"))
    return fig
