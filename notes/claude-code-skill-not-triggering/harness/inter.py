import os,pty,sys,time,select,json,glob,subprocess,re
S=os.path.dirname(os.path.abspath(__file__))
proj,desc,pid,text=sys.argv[1:5]
cwd=f"{S}/{proj}"
subprocess.run("git checkout -q -- . && git clean -fdq -e .claude -e CLAUDE.md",shell=True,cwd=cwd)
enc=re.sub(r'[^A-Za-z0-9]','-',cwd)
tdir=os.path.expanduser(f"~/.claude/projects/{enc}")
before=set(glob.glob(f"{tdir}/*.jsonl"))
pid_,fd=pty.fork()
if pid_==0:
    [os.environ.pop(k) for k in list(os.environ) if k.startswith("CLAUDE")]; os.chdir(cwd); os.environ["TERM"]="xterm-256color"; os.environ["COLUMNS"]="120"; os.environ["LINES"]="40"
    os.execvp("claude",["claude"])
buf=b""
def pump(sec):
    global buf
    end=time.time()+sec
    while time.time()<end:
        r,_,_=select.select([fd],[],[],0.3)
        if r:
            try: buf+=os.read(fd,65536)
            except OSError: return
def send(s):
    os.write(fd,s.encode())
pump(8)
low=buf.decode('utf-8','ignore').lower()
if "trust" in low: send("\x1b[B"); pump(1); send("\r"); pump(8)
for ch in text: send(ch); time.sleep(0.01)
time.sleep(0.5); send("\r")
# wait for transcript to settle
t0=time.time(); last=None; stable=0
while time.time()-t0<240:
    pump(5)
    new=set(glob.glob(f"{tdir}/*.jsonl"))-before
    if new:
        f=max(new,key=os.path.getmtime); sz=os.path.getsize(f)
        if sz==last: stable+=1
        else: stable=0
        last=sz
        if stable>=3: break
send("\x03"); pump(1); send("\x03"); pump(2)
try: os.kill(pid_,9)
except: pass
new=set(glob.glob(f"{tdir}/*.jsonl"))-before
skills=[];tools=[];final=""
for f in new:
    for l in open(f):
        try:e=json.loads(l)
        except:continue
        if e.get("type")=="assistant":
            for c in e.get("message",{}).get("content",[]) or []:
                if isinstance(c,dict) and c.get("type")=="tool_use":
                    tools.append(c["name"])
                    if c["name"]=="Skill": skills.append(json.dumps(c.get("input")))
                if isinstance(c,dict) and c.get("type")=="text": final=c.get("text","")
    os.makedirs(f"{S}/logs",exist_ok=True)
    subprocess.run(["cp",f,f"{S}/logs/interactive-{desc}-{pid}.jsonl"])
called=int(any("release-notes" in s for s in skills)); hdr=int("=== Acme Tracker release notes ===" in final)
open(f"{S}/results-interactive-{desc}.csv","a").write(f"interactive,{desc},{pid},0,interactive,{called},{hdr},{'|'.join(tools)},,\n")
print(pid,called,hdr,tools,len(new))
if not new: print(buf.decode('utf-8','ignore')[-1500:])
