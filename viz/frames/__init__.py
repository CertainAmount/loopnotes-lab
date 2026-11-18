"""프레임 등록부: 이 폴더의 모듈 하나가 프레임 하나다. 모듈마다 NAME, QUESTION, EXAMPLE, draw(spec)->figure.
새 프레임은 파일 하나를 더하면 목록에 잡힌다(tools/viz/README.md 「프레임 더하기」)."""
import importlib
import pkgutil
from pathlib import Path

FRAMES = {}
for m in pkgutil.iter_modules([str(Path(__file__).parent)]):
    mod = importlib.import_module(f"frames.{m.name}")
    if hasattr(mod, "NAME") and hasattr(mod, "draw"):
        FRAMES[mod.NAME] = mod
