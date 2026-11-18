"""E1 steps 3-5: assemble the final context under a 3,000-token budget, generate with a
local model (llama.cpp llama-server, temperature 0, fixed seed), classify each answer.

usage: gen.py run A B B-control C D | gen.py knowngood | gen.py classify
"""
import json, os, re, sys, urllib.request
import tiktoken

W = os.path.expanduser("<workdir>/work")
URL = "http://127.0.0.1:8092/v1/chat/completions"
BUDGET, K = 3000, 5
enc = tiktoken.get_encoding("cl100k_base")
SYSTEM = ("You answer questions about Kubernetes using only the context below. "
          "Reply in exactly two lines:\nAnswer: <the answer>\nQuote: <the sentence from the context you used>\n"
          "If the answer is not in the context, reply 'Answer: not in context'.")

def norm(s):
    s = s.lower().replace("`", "").replace("*", "").replace("\\", "")
    return re.sub(r"\s+", " ", s).strip()

def chat(context, question):
    body = {"messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}],
            "temperature": 0, "seed": 42, "max_tokens": 200, "cache_prompt": False}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=1800))
    return r["choices"][0]["message"]["content"], r.get("usage", {})

def load(k):
    return {c["id"]: c for c in map(json.loads, open(f"{W}/chunks-{k}.jsonl"))}

def run(setting):
    k = setting.split("-")[0]
    budget = None if setting == "B-control" else BUDGET
    chunks, top = load(k), json.load(open(f"{W}/top50-{k}.json"))
    qs = [json.loads(l) for l in open(f"{W}/questions.jsonl")]
    os.makedirs(f"{W}/runs", exist_ok=True)
    with open(f"{W}/runs/{setting}.jsonl", "w") as f:
        for q in qs:
            topk = [t["id"] for t in top[q["id"]][:K]]
            final, used = [], 0
            for cid in topk:
                n = chunks[cid]["tokens"]
                if budget is not None and used + n > budget:
                    break  # lower-ranked chunks are cut, as a fixed context window does
                final.append(cid); used += n
            context = "\n\n---\n\n".join(chunks[c]["text"] for c in final)
            g = norm(q["gold_span"])
            in_final = any(g in norm(chunks[c]["text"]) for c in final)
            # CPU-time rule (fixed before any generation): generate only when the gold sentence
            # reached the prompt; B-control only for the questions B lost at assembly.
            only = os.environ.get("ONLY")
            if (not in_final) or (only and q["id"] not in only.split(",")):
                ans, usage = None, {}
            else:
                ans, usage = chat(context, q["question"])
            gold_rank = next((t["rank"] for t in top[q["id"]] if g in norm(chunks[t["id"]]["text"])), None)
            rec = {"qid": q["id"], "setting": setting, "top50": top[q["id"]], "topk": topk, "final_ids": final,
                   "final_tokens": used, "final_context": context, "answer": ans, "usage": usage,
                   "gold_rank_top50": gold_rank,
                   "gold_in_topk": any(g in norm(chunks[c]["text"]) for c in topk),
                   "gold_in_final": any(g in norm(chunks[c]["text"]) for c in final),
                   "top1_file": chunks[topk[0]]["file"]}
            f.write(json.dumps(rec) + "\n"); f.flush()
            print(setting, q["id"], rec["gold_in_topk"], rec["gold_in_final"], (ans or "-").replace("\n", " | ")[:120], flush=True)

def auto_correct(q, ans):
    a = norm(ans)
    m = re.search(r"answer:(.*?)(quote:|$)", a, re.S)
    line = m.group(1) if m else a
    if "not in context" in line:
        return False
    for group in q["expected"]:
        if not any(x in line for x in group):
            return False
    for x in q.get("forbidden", []):
        if x in line:
            return False
    return True

def knowngood():
    C = load("C")
    qs = {q["id"]: q for q in map(json.loads, open(f"{W}/questions.jsonl"))}
    cls = list(map(json.loads, open(f"{W}/classified-auto.jsonl")))
    gen_q = sorted({r["qid"] for r in cls if r["stage"] == "generation"})
    with open(f"{W}/known-good.jsonl", "w") as f:
        for qid in gen_q:
            q = qs[qid]; g = norm(q["gold_span"])
            cid = next(c for c, v in C.items() if g in norm(v["text"]) and v["file"] == q["gold_file"])
            ans, _ = chat(C[cid]["text"], q["question"])
            rec = {"qid": qid, "chunk": cid, "answer": ans, "auto_correct": auto_correct(q, ans)}
            f.write(json.dumps(rec) + "\n"); print(rec, flush=True)

def classify():
    qs = {q["id"]: q for q in map(json.loads, open(f"{W}/questions.jsonl"))}
    over = {}
    if os.path.exists(f"{W}/overrides.json"):
        over = json.load(open(f"{W}/overrides.json"))
    out = []
    for s in ["A", "B", "B-control", "C", "D"]:
        p = f"{W}/runs/{s}.jsonl"
        if not os.path.exists(p):
            continue
        for r in map(json.loads, open(p)):
            q = qs[r["qid"]]
            if r["answer"] is None and s == "B-control" and r["gold_in_final"]:
                continue
            ok = r["answer"] is not None and auto_correct(q, r["answer"])
            key = f"{s}:{r['qid']}"
            if key in over:
                ok = over[key]["correct"]
            stage = "correct" if ok else ("retrieval" if not r["gold_in_topk"] else
                                          "assembly" if not r["gold_in_final"] else "generation")
            out.append({"qid": r["qid"], "setting": s, "stage": stage, "auto": ok if r["answer"] is None else auto_correct(q, r["answer"]),
                        "gold_rank_top50": r["gold_rank_top50"], "answer": r["answer"]})
    with open(f"{W}/classified-auto.jsonl", "w") as f:
        for r in out:
            f.write(json.dumps(r) + "\n")
    from collections import Counter
    for s in ["A", "B", "B-control", "C", "D"]:
        print(s, dict(Counter(r["stage"] for r in out if r["setting"] == s)))

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "run":
        for s in sys.argv[2:]:
            run(s)
    elif cmd == "knowngood":
        knowngood()
    else:
        classify()
