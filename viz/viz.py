"""loopnotes 시각화 엔진(2026-11-18, mkviz-engine을 본뜸): 그림은 명세(JSON) 하나로 그리고, 명세·데이터·그림을 함께 남겨 누구나 다시 그릴 수 있게 한다.
    .venv/bin/python tools/viz/viz.py list                      # 프레임과 각 프레임이 답하는 질문
    .venv/bin/python tools/viz/viz.py example <frame>           # 명세 예시(JSON)
    .venv/bin/python tools/viz/viz.py draw <spec.json> <slug> <n>   # 그림 n을 그린다
    .venv/bin/python tools/viz/viz.py redraw <bundle dir>       # 남긴 명세로 다시 그린다
draw는 두 곳에 쓴다:
  content/images/<slug>/img-<n>.jpg                     WordPress 업로드용(1600px)
  content/en/03-reviewed/<slug>-evidence/figures/fig-<n>/   spec.json, data.csv, figure.svg, README.md(다시 그리는 명령)
evidence 폴더는 labnote.py가 loopnotes-lab notes/<WP slug>/로 그대로 올리므로 그림 데이터도 공개된다.
맞는 프레임이 없으면 일회용 스크립트 대신 frames/에 프레임을 더한다(README 「프레임 더하기」): 엔진이 글마다 자란다.
"""
import csv
import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parent.parent
from frames import FRAMES  # noqa: E402


def rows_of(spec):
    """명세에서 표 형태 데이터를 뽑는다(공개용 data.csv)."""
    f = spec["frame"]
    if f == "matrix":
        return [["case"] + spec["cols"]] + [[r] + c for r, c in zip(spec["rows"], spec["cells"])]
    if f == "bars":
        return [["item"] + [s["name"] for s in spec["series"]]] + [[it] + [s["values"][i] for s in spec["series"]] for i, it in enumerate(spec["items"])]
    if f == "compare":
        return [["item", spec["before"]["name"], spec["after"]["name"]]] + [[it, spec["before"]["values"][i], spec["after"]["values"][i]] for i, it in enumerate(spec["items"])]
    if f == "dots":
        return [["item", "run", "value"]] + [[it, j + 1, v] for it, r in zip(spec["items"], spec["runs"]) for j, v in enumerate(r)]
    if f == "timeline":
        return [["t", "label", "sub", "bad"]] + [[e.get("t", i), e["label"].replace("\n", " "), e.get("sub", ""), bool(e.get("bad") or e.get("focus"))] for i, e in enumerate(spec["events"])]
    if f == "stack":
        return [["condition"] + [c["name"] for c in spec["classes"]]] + [[r] + v for r, v in zip(spec["rows"], spec["values"])]
    if f == "ladder":
        return [["step", "value", "beyond", "text"]] + [[st["label"], st.get("value", ""), st.get("beyond", ""), st.get("text", "")] for st in spec["steps"]]
    if f == "flow":
        return [["from", "to", "label"]] + [[e[0], e[1], e[2] if len(e) > 2 else ""] for e in spec["edges"]]
    return [["spec"], [json.dumps(spec)]]


def render(spec, jpg=None, bundle=None):
    from PIL import Image
    fr = FRAMES[spec["frame"]]
    fig = fr.draw(spec)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=160, facecolor="white")
    if jpg:
        Path(jpg).parent.mkdir(parents=True, exist_ok=True)
        Image.open(io.BytesIO(buf.getvalue())).convert("RGB").save(jpg, quality=88)
    if bundle:
        b = Path(bundle); b.mkdir(parents=True, exist_ok=True)
        (b / "spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
        with open(b / "data.csv", "w", newline="") as fh:
            csv.writer(fh).writerows(rows_of(spec))
        fig.savefig(b / "figure.svg", format="svg", facecolor="white")
        (b / "README.md").write_text(
            f"# {spec.get('title') or spec.get('caption') or b.name}\n\n"
            f"Frame `{spec['frame']}`: {fr.QUESTION}\n\n"
            + (f"{spec['caption']}\n\n" if spec.get("caption") else "")
            + (f"Data: {spec['note']}\n\n" if spec.get("note") else "")
            + "Files: `data.csv` (the values drawn), `spec.json` (the exact settings), `figure.svg`.\n\n"
            "Redraw with the loopnotes viz engine: `python tools/viz/viz.py redraw <this folder>`.\n")
    import matplotlib.pyplot as plt
    plt.close(fig)


def main(a):
    if not a or a[0] == "list":
        for k, m in sorted(FRAMES.items()):
            print(f"{k:10} {m.QUESTION}")
        return
    if a[0] == "example":
        print(json.dumps(FRAMES[a[1]].EXAMPLE, indent=1)); return
    if a[0] == "draw":
        spec = json.loads(Path(a[1]).read_text()); slug, n = a[2], a[3]
        jpg = ROOT / f"content/images/{slug}/img-{n}.jpg"
        bundle = ROOT / f"content/en/03-reviewed/{slug}-evidence/figures/fig-{n}"
        render(spec, jpg, bundle)
        print(f"{jpg}\n{bundle}/"); return
    if a[0] == "redraw":
        b = Path(a[1]); render(json.loads((b / "spec.json").read_text()), b / "figure.jpg", b)
        print(b / "figure.jpg"); return
    if a[0] == "sample":  # 모든 프레임의 예시를 한 폴더에(점검용)
        out = Path(a[1]); out.mkdir(parents=True, exist_ok=True)
        for k, m in FRAMES.items():
            render(m.EXAMPLE, out / f"{k}.jpg")
            print(out / f"{k}.jpg")
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
