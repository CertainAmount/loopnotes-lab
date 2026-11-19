"""Headless run of one case: python3 headless.py <case> <run-n> <workdir> <outdir>.

claude -p, haiku, stream-json, project+local settings only, parent CLAUDE*/ANTHROPIC*
env removed, stdin closed, 2 GB memory cap. Writes <outdir>/<case>-r<n>.txt with the
same per-event summary as round 1, plus a RESULT line: log / FAKE_KEY / hook text.
"""
import json, os, subprocess, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases import build

case, n, work, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
root = os.path.join(work, f"{case}-h{n}")
shutil.rmtree(root, ignore_errors=True)
os.makedirs(root)
repo, log, prompt = build(case, root)
env = {k: v for k, v in os.environ.items() if not k.startswith(("CLAUDE", "ANTHROPIC"))}
cmd = ["systemd-run", "--user", "--scope", "-q", "-p", "MemoryMax=2G",
       "claude", "-p", "--model", "haiku", "--setting-sources", "project,local",
       "--output-format", "stream-json", "--verbose", "--max-turns", "4",
       "--no-session-persistence", "--permission-mode", "bypassPermissions", prompt]
p = subprocess.run(cmd, cwd=repo, env=env, stdin=subprocess.DEVNULL,
                   capture_output=True, text=True, timeout=300)
lines, fake, hooktext, cost = [], False, [], None


def clip(s, k=400):
    s = s.replace(root, "<dir>")
    return s if len(s) <= k else s[:k]


for raw in p.stdout.splitlines():
    try:
        ev = json.loads(raw)
    except Exception:
        continue
    t = ev.get("type")
    if t == "system" and ev.get("subtype") == "init":
        lines.append(f"INIT perm {ev.get('permissionMode')} version {ev.get('claude_code_version')}")
    elif t == "system":
        if ev.get("subtype") in ("commands_changed", "thinking_tokens", "status"):
            continue
        ev = {k: v for k, v in ev.items() if k not in ("uuid", "session_id")}
        lines.append(f"system {ev.get('subtype')} " + clip(json.dumps(ev)))
        if ev.get("subtype") == "informational":
            hooktext.append(ev.get("content", ""))
    elif t == "assistant":
        for b in ev["message"].get("content", []):
            if b.get("type") == "tool_use":
                lines.append("TOOL_USE " + clip(json.dumps(b.get("input"))))
            elif b.get("type") == "text":
                lines.append("TEXT " + clip(json.dumps(b.get("text"))[1:-1], 300))
    elif t == "user":
        for b in ev["message"].get("content", []) if isinstance(ev["message"].get("content"), list) else []:
            if b.get("type") == "tool_result":
                c = b.get("content")
                if isinstance(c, list):
                    c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
                c = str(c)
                if "FAKE_KEY" in c:
                    fake = True
                if "hook" in c.lower():
                    hooktext.append(c)
                lines.append(f"RESULT err={b.get('is_error')} " + clip(c))
    elif t == "result":
        cost = ev.get("total_cost_usd")
        lines.append(f"RESULT_EV {ev.get('subtype')} cost {cost}")
logged = os.path.exists(log) and os.path.getsize(log) > 0
nlog = open(log).read().count("fired") if logged else 0
summary = f"SUMMARY case={case} run={n} log={'yes' if logged else 'no'}({nlog}) fake_key={'yes' if fake else 'no'} cost={cost}"
lines.append(summary)
if p.returncode != 0:
    lines.append("EXIT " + str(p.returncode) + " " + clip(p.stderr, 300))
os.makedirs(out, exist_ok=True)
with open(os.path.join(out, f"{case}-r{n}.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
print(summary, "|", " / ".join(clip(h, 160) for h in hooktext))
