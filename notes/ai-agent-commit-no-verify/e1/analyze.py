import json, sys, glob, os, re
def runs(path):
    out = {"calls": [], "cost": 0, "result": "", "turns": 0}
    ids = {}
    for line in open(path):
        try: d = json.loads(line)
        except: continue
        if d.get("type") == "assistant":
            for c in d["message"].get("content", []):
                if c.get("type") == "tool_use":
                    inp = c["input"]
                    s = inp.get("command") or inp.get("file_path") or json.dumps(inp)[:120]
                    ent = {"tool": c["name"], "arg": s, "res": ""}
                    ids[c["id"]] = ent; out["calls"].append(ent)
        if d.get("type") == "user":
            for c in d["message"].get("content", []) if isinstance(d["message"].get("content"), list) else []:
                if c.get("type") == "tool_result" and c.get("tool_use_id") in ids:
                    t = c.get("content"); t = t if isinstance(t, str) else json.dumps(t)
                    ids[c["tool_use_id"]]["res"] = t[:200].replace("\n", " | ")
                    ids[c["tool_use_id"]]["err"] = c.get("is_error", False)
        if d.get("type") == "result":
            out["cost"] = d.get("total_cost_usd", 0); out["result"] = d.get("result", ""); out["turns"] = d.get("num_turns")
    return out
for p in sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else "logs/*.jsonl")):
    r = runs(p); name = os.path.basename(p)[:-6]
    print(f"===== {name} cost={r['cost']:.3f} turns={r['turns']}")
    for c in r["calls"]:
        print(f"  [{c['tool']}{' ERR' if c.get('err') else ''}] {c['arg'][:160]}\n      -> {c['res'][:160]}")
    print("  RESULT:", r["result"][:600].replace("\n", " "))
    print("  STATE:", open(p[:-6] + ".state").read().replace("\n", " ; ")[:400] if os.path.exists(p[:-6] + ".state") else "")
