import json,os,subprocess,sys,csv,time
S=os.path.dirname(os.path.abspath(__file__))
axis,proj,desc=sys.argv[1],sys.argv[2],sys.argv[3]
only=sys.argv[4].split(",") if len(sys.argv)>4 else None
prompts=json.load(open(os.environ.get("PROMPTS",f"{S}/prompts.json")))
os.makedirs(f"{S}/logs",exist_ok=True)
out=open(f"{S}/results-{axis}-{desc}.csv","a")
for pid,hk,text in prompts:
    if only and pid not in only: continue
    subprocess.run("git checkout -q -- . && git clean -fdq -e .claude -e CLAUDE.md",shell=True,cwd=f"{S}/{proj}")
    log=f"{S}/logs/{axis}-{desc}-{pid}.jsonl"
    t=time.time()
    r=subprocess.run(["claude","-p",text,"--output-format","stream-json","--verbose","--max-turns","4","--no-session-persistence"],cwd=f"{S}/{proj}",capture_output=True,text=True,timeout=600)
    open(log,"w").write(r.stdout)
    skills=[];final="";cost=None
    for line in r.stdout.splitlines():
        try:e=json.loads(line)
        except:continue
        if e.get("type")=="assistant":
            for c in e["message"].get("content",[]):
                if c.get("type")=="tool_use" and c.get("name")=="Skill":
                    skills.append(c.get("input",{}).get("skill") or c.get("input",{}).get("command") or str(c.get("input")))
        if e.get("type")=="result":
            final=e.get("result") or ""; cost=e.get("total_cost_usd")
        if e.get("type")=="system" and e.get("subtype")=="init":
            init=e
    called=int(any("release-notes" in s for s in skills))
    hdr=int("=== Acme Tracker release notes ===" in final)
    out.write(f"{axis},{desc},{pid},{hk},headless,{called},{hdr},{'|'.join(skills)},{cost},{round(time.time()-t)}\n"); out.flush()
    print(axis,desc,pid,called,hdr,skills,cost,flush=True)
