"""E1 step 2: embed chunks of each setting and questions with nomic-embed-text v1.5
served by llama.cpp (llama-server --embedding), then store the top-50 per question."""
import json, os, sys, time, urllib.request
import numpy as np

W = os.path.expanduser("<workdir>/work")
URL = "http://127.0.0.1:8091/v1/embeddings"

def embed(texts):
    req = urllib.request.Request(URL, data=json.dumps({"input": texts, "model": "nomic"}).encode(),
                                 headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=600))
    v = np.array([d["embedding"] for d in sorted(r["data"], key=lambda d: d["index"])], dtype=np.float32)
    return v / np.linalg.norm(v, axis=1, keepdims=True)

def main(settings):
    qs = [json.loads(l) for l in open(f"{W}/questions.jsonl")]
    qv = embed(["search_query: " + q["question"] for q in qs])
    np.save(f"{W}/q.npy", qv)
    for k in settings:
        ch = [json.loads(l) for l in open(f"{W}/chunks-{k}.jsonl")]
        path = f"{W}/emb-{k}.npy"
        if not os.path.exists(path):
            t0, vs = time.time(), []
            for i in range(0, len(ch), 8):
                vs.append(embed(["search_document: " + c["text"] for c in ch[i:i + 8]]))
                if i % 400 == 0:
                    print(k, i, len(ch), round(time.time() - t0), flush=True)
            np.save(path, np.vstack(vs))
        E = np.load(path)
        sims = qv @ E.T
        out = {}
        for qi, q in enumerate(qs):
            order = np.argsort(-sims[qi])[:50]
            out[q["id"]] = [{"rank": r + 1, "id": ch[j]["id"], "score": float(sims[qi, j])} for r, j in enumerate(order)]
        json.dump(out, open(f"{W}/top50-{k}.json", "w"))
        print(k, "done", flush=True)

if __name__ == "__main__":
    main(sys.argv[1:] or list("ABCD"))
