# A reranker couldn't lift a chunk that wasn't a candidate; the heading path did.

Frame `ladder`: Which attempt finally pushed the value past the cutoff, and how far did each one get?

A reranker couldn't lift a chunk that wasn't a candidate; the heading path did.

Data: One question from the author's internal RAG POC; logs kept the top 30 candidates; reranker saw 20

Files: `data.csv` (the values drawn), `spec.json` (the exact settings), `figure.svg`.

Redraw with the loopnotes viz engine: `python tools/viz/viz.py redraw <this folder>`.
