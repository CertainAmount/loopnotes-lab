"""loopnotes 그림 스타일: 모든 프레임이 이 한 곳의 값만 쓴다(2026-11-18).
가독성 기준: 출력 1600px 폭, 본문에서 약 1024px로 보이므로 글자 13pt(출력 약 29px, 화면 약 18px) 이상.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NAVY = "#1E3A5F"
GRAY = "#8A96A3"
LIGHT = "#E6EAEE"
ACCENT = "#3B82F6"
RED = "#D9483B"      # 실패·위험 한 곳에만
GREEN = "#2E9E6A"    # 통과·정상 한 곳에만
AMBER = "#E0A526"    # 조용한 실패·애매
BG = "#FFFFFF"

# 결과 키 → (표시 라벨, 색). 프레임들이 같은 뜻에 같은 색을 쓴다.
OUTCOMES = {
    "blocked": ("Blocked", GREEN),
    "ran": ("Ran anyway", RED),
    "silent": ("Silent fail", AMBER),
    "ok": ("Works", GREEN),
    "fail": ("Fails", RED),
    "partial": ("Partly", AMBER),
    "na": ("n/a", LIGHT),
    "yes": ("Yes", GREEN),
    "no": ("No", RED),
}

WIDTH_IN = 10.0
DPI = 160
FONT = 13
FONT_SMALL = 11.5
MONO = "DejaVu Sans Mono"


def setup():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": FONT,
        "axes.edgecolor": GRAY,
        "axes.labelcolor": NAVY,
        "xtick.color": NAVY,
        "ytick.color": NAVY,
        "text.color": NAVY,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "svg.fonttype": "none",
    })


def figure(height_in):
    setup()
    return plt.figure(figsize=(WIDTH_IN, height_in), dpi=DPI)


def note(fig, text):
    """그림 아래 작은 회색 줄: N, 기준일, 출처(캡션과 겹치지 않는 사실만)."""
    if text:
        fig.text(0.01, 0.01, text, fontsize=FONT_SMALL - 1, color=GRAY, ha="left", va="bottom")
