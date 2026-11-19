import json, sys, re, os, glob
DROP = {"session_id","uuid","parent_uuid","parentUuid","credential_expires_at","request_id","requestId","apiKeySource","account","email","organization","memory_paths","output_style","plugins","slash_commands","skills","agents"}
def s(x):
    x = re.sub(r"<scratch>/e1", "/tmp/e1", x)
    x = x.replace(os.path.expanduser("~"), "~")
    return x
def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items() if k not in DROP}
    if isinstance(o, list): return [clean(v) for v in o]
    if isinstance(o, str): return s(o)
    return o
out = sys.argv[1]
for p in sorted(glob.glob("logs/*")):
    name = os.path.basename(p)
    if p.endswith(".jsonl"):
        with open(os.path.join(out, name), "w") as f:
            for line in open(p):
                try: f.write(json.dumps(clean(json.loads(line)), ensure_ascii=False) + "\n")
                except Exception: pass
    elif p.endswith(".state"):
        open(os.path.join(out, name), "w").write(s(open(p).read()))
