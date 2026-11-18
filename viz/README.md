# loopnotes viz engine

The small chart and diagram engine behind the figures on [loopnotes.dev](https://loopnotes.dev). Every figure is drawn from one JSON spec, and each article's research note keeps that spec, the data (`data.csv`) and the drawing (`figure.svg`) next to it, so anyone can redraw it and check the numbers.

```
python viz.py list                    # frames and the question each one answers
python viz.py example matrix          # a spec to start from
python viz.py redraw <figure folder>  # redraw a published figure from its spec.json
```

Requires Python 3 with matplotlib and Pillow.

| Frame | Question it answers |
|---|---|
| `matrix` | Under which setting does each case block, run, or fail silently? |
| `bars` | How many of each kind, and which one dominates? |
| `compare` | What changed for each item between two conditions? |
| `dots` | How spread out are repeated measurements? |
| `timeline` | Where did the time go, and at which step did it go wrong? |
| `stack` | When the condition changes, which part of the total shrinks? |
| `flow` | What happens step by step, and where does the path split? |

`examples/` shows each frame drawn from its example spec (sample values, not measurements). New frames are added as articles need them.

Code: MIT. Figures and data: free to reuse with credit to loopnotes and a link to the article.
