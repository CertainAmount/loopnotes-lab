import json,os,shutil,subprocess,sys
S=os.path.dirname(os.path.abspath(__file__))
descs=json.load(open(f"{S}/descs.json")); body=open(f"{S}/body.md").read()
def make(name,desc,claude_md=None,dummies=0):
    d=f"{S}/{name}"
    if os.path.exists(d): shutil.rmtree(d)
    shutil.copytree(f"{S}/proj",d)
    sk=f"{d}/.claude/skills/release-notes"; os.makedirs(sk,exist_ok=True)
    open(f"{sk}/SKILL.md","w").write(f"---\nname: release-notes\ndescription: {json.dumps(desc)}\n---\n{body}")
    if claude_md: open(f"{d}/CLAUDE.md","w").write(claude_md+"\n")
    for i in range(dummies):
        n,dd=DUMMIES[i]
        p=f"{d}/.claude/skills/{n}"; os.makedirs(p,exist_ok=True)
        open(f"{p}/SKILL.md","w").write(f"---\nname: {n}\ndescription: {json.dumps(dd)}\n---\n\n# {n}\n\nFollow the team checklist for this task.\n")
DUMMIES=json.load(open(f"{S}/dummies.json")) if os.path.exists(f"{S}/dummies.json") else []
for k,v in descs.items(): make(f"proj-{k}",v)
make("proj-D1-claudemd",descs["D1"],claude_md="Release notes and change summaries go through the release-notes skill.")
if DUMMIES: make("proj-D3-dummies",descs["D3"],dummies=len(DUMMIES))
