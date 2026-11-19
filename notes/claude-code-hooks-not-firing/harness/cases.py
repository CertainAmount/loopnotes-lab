"""Build one test folder per hook-mistake case (round 2, 2026-11-19).

Each case: fresh git repo, fake .env (FAKE_KEY=test-not-real), a guard script that
logs its first line to a file OUTSIDE the repo, then blocks commands containing
.env with exit 2 and a stderr reason. The case changes one thing.
"""
import json, os, stat, subprocess, tempfile

GUARD_BODY = r'''input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')
if [[ "$cmd" == *.env* ]]; then
  echo "blocked: .env read not allowed" >&2
  exit 2
fi
exit 0
'''

HOOK_CMD = '"$CLAUDE_PROJECT_DIR"/.claude/hooks/guard.sh'


def guard(log, shebang=True, sleep=0, tail=None):
    s = "#!/bin/bash\n" if shebang else ""
    s += f'echo "$(date +%s) fired" >> {log}\n'
    if sleep:
        s += f"sleep {sleep}\n"
    if tail is not None:          # replace the decision part
        s += "input=$(cat)\n" + tail
    else:
        s += GUARD_BODY
    return s


def settings(event="PreToolUse", matcher="Bash", cmd=HOOK_CMD, extra=None, bare=False):
    h = {"type": "command", "command": cmd}
    if extra:
        h.update(extra)
    group = h if bare else {"matcher": matcher, "hooks": [h]}
    return {"hooks": {event: [group]}}


ONF = {"onFailure": "block"}

# case -> dict(settings, where, guard kwargs, chmod, script name, raw_settings_text, prompt)
CASES = {
    "A0": {},
    "A1": {"settings": settings(matcher="bash")},
    "A1x": {"settings": settings(matcher="Bash(*)")},   # /status control: invalid regex (issue #30143)
    "A6": {"settings": settings(event="PreToolUSE")},
    "A7": {"settings": settings(event="pretooluse")},
    "A9": {"where": ".claude/hooks.json"},
    "A10": {"where": "settings.json"},
    "A11": {"raw": "trailing_comma"},
    "A12": {"settings": settings(bare=True)},
    "B1": {"settings": settings(cmd='"$CLAUDE_PROJECT_DIR"/.claude/hooks/gaurd.sh')},
    "B2": {"chmod": 0o644},
    "B3": {"guard": {"shebang": False}},
    "B4": {"settings": settings(cmd="./.claude/hooks/guard.sh"), "prompt": "cd"},
    "B5": {"settings": settings(extra={"timeout": 2}), "guard": {"sleep": 5}},
    "B6": {"settings": settings(extra={"timeout": 2, **ONF}), "guard": {"sleep": 5}},
    "B7": {"settings": settings(cmd='"$CLAUDE_PROJECT_DIR"/.claude/hooks/gaurd.sh', extra=ONF)},
    "C1": {"guard": {"tail": 'echo "blocked: .env read not allowed" >&2\nexit 1\n'}},
    "C2": {"guard": {"tail": 'echo \'{"permissionDecision":"deny","permissionDecisionReason":"no .env"}\'\nexit 0\n'}},
    "C2b": {"guard": {"tail": 'echo \'{"decision":"block","reason":"blocked: .env read not allowed"}\'\nexit 0\n'}},
    "C5": {"settings": settings(event="PostToolUse")},
    # onFailure scope (new): each silent / fail-open mistake + onFailure block
    "O1": {"settings": settings(matcher="bash", extra=ONF)},
    "O2": {"settings": settings(extra=ONF), "guard": {"shebang": False}},
    "O3": {"settings": settings(extra=ONF), "guard": {"tail": 'echo "blocked: .env read not allowed" >&2\nexit 1\n'}},
    "O4": {"settings": settings(extra=ONF), "guard": {"tail": 'echo \'{"permissionDecision":"deny","permissionDecisionReason":"no .env"}\'\nexit 0\n'}},
    "O5": {"settings": settings(extra=ONF), "chmod": 0o644},
}

PROMPTS = {
    "default": "Run this exact shell command and show its output: cat .env",
    "cd": "Run these two shell commands as two separate Bash tool calls, in order: first `cd sub`, then `cat ../.env`. Show the output.",
}


def build(case, root):
    c = CASES[case]
    repo = os.path.join(root, "repo")
    os.makedirs(os.path.join(repo, ".claude", "hooks"))
    os.makedirs(os.path.join(repo, "sub"))
    log = os.path.join(root, "hook.log")
    subprocess.run(["git", "init", "-q", repo], check=True)
    with open(os.path.join(repo, ".env"), "w") as f:
        f.write("FAKE_KEY=test-not-real\n")
    gp = os.path.join(repo, ".claude", "hooks", "guard.sh")
    with open(gp, "w") as f:
        f.write(guard(log, **c.get("guard", {})))
    os.chmod(gp, c.get("chmod", 0o755))
    s = c.get("settings", settings())
    where = c.get("where", ".claude/settings.json")
    text = json.dumps(s, indent=2)
    if c.get("raw") == "trailing_comma":
        text = text.replace('"Bash",', '"Bash",', 1)
        # add a trailing comma after the last handler field
        text = text.replace('guard.sh"\n', 'guard.sh",\n', 1)
    with open(os.path.join(repo, where), "w") as f:
        f.write(text + "\n")
    return repo, log, PROMPTS[c.get("prompt", "default")]


if __name__ == "__main__":
    import sys
    d = tempfile.mkdtemp(prefix="hk-")
    r, l, p = build(sys.argv[1], d)
    print(open(os.path.join(r, CASES[sys.argv[1]].get("where", ".claude/settings.json"))).read())
    print(open(os.path.join(r, ".claude/hooks/guard.sh")).read())
