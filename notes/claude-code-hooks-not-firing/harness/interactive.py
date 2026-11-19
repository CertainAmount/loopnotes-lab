"""Interactive run of one case in a pseudo-terminal (150x50), screens rendered with pyte.

python3 interactive.py <case> <run-n> <mode: run|hooks> <workdir> <outdir>
mode run: startup screen, then the prompt, screen after the answer.
mode hooks: startup screen, then /hooks, no prompt.
mode status: startup screen, then /status and each of its tabs (Tab key), no prompt.
Paths are replaced by <dir>. Writes <outdir>/<case>-<mode>-r<n>.txt.
"""
import os, pty, re, select, shutil, signal, struct, sys, termios, fcntl, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases import build, CASES
import pyte

case, n, mode, work, out = sys.argv[1:6]
root = os.path.join(work, f"{case}-{mode}{n}")
shutil.rmtree(root, ignore_errors=True)
os.makedirs(root)
repo, log, prompt = build(case, root)
env = {k: v for k, v in os.environ.items() if not k.startswith(("CLAUDE", "ANTHROPIC"))}
env["TERM"] = "xterm-256color"
COLS, ROWS = 150, 50
screen = pyte.Screen(COLS, ROWS)
stream = pyte.ByteStream(screen)
rawbuf = bytearray()

pid, fd = pty.fork()
if pid == 0:
    os.chdir(repo)
    os.execvpe("systemd-run", ["systemd-run", "--user", "--scope", "-q", "-p", "MemoryMax=2G",
                               "claude", "--model", "haiku", "--setting-sources", "project,local"], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", ROWS, COLS, 0, 0))


def pump(sec):
    end = time.time() + sec
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.2)
        if r:
            try:
                b = os.read(fd, 65536)
            except OSError:
                return
            rawbuf.extend(b)
            stream.feed(b)


def text():
    rows = [l.rstrip() for l in screen.display]
    t = "\n".join(l for l in rows if l.strip()).replace(root, "<dir>")
    # account details shown by /status stay out of the published screens
    return re.sub(r"^(  (?:Session ID|Peer address|Organization|Email):\s+).*$", r"\1<removed>", t, flags=re.M)


def wait_for(pred, maxs):
    end = time.time() + maxs
    while time.time() < end:
        pump(0.5)
        if pred(text()):
            return True
    return False


def send(s):
    os.write(fd, s.encode())


shots = []


def shot(label):
    shots.append(f"===== {label}\n{text()}")


wait_for(lambda t: "❯" in t and ("Try" in t or "trust" in t.lower() or "Settings" in t or "Hooks" in t), 45)
pump(2)
if "Yes, I trust this folder" in text():
    send("\x1b[B")      # move from "No, exit" to "Yes, I trust this folder"
    pump(0.7)
    send("\r")
    wait_for(lambda t: "Try" in t or "Settings" in t, 30)
    pump(3)
if "Settings Warning" in text() or "Settings Error" in text():
    shot("start")
    if "Continue without these settings" in text():   # Settings Error dialog: option 3
        send("\x1b[B")
        pump(0.5)
        send("\x1b[B")
        pump(0.5)
    send("\r")
    pump(4)
    shot("after-continue")
else:
    shot("start")

ran_hook_counter = False
if mode == "hooks":
    send("/hooks")
    pump(1.5)
    send("\r")
    pump(4)
    shot("hooks")
    send("\x1b")
    pump(1)
elif mode == "status":
    send("/status")
    pump(1.5)
    send("\r")
    pump(4)
    shot("status")
    for i in range(4):
        send("\t")
        pump(2)
        shot(f"status-tab{i + 1}")
    send("\x1b")
    pump(1)
else:
    send(prompt)
    pump(1)
    send("\r")
    t0 = time.time()
    last, stable = "", 0.0
    while time.time() - t0 < 120:
        pump(1)
        t = text()
        if "Do you want to proceed" in t:
            shots.append("===== permission-prompt\n" + t)
            send("\r")
            continue
        if t == last:
            stable += 1
        else:
            stable, last = 0, t
        if time.time() - t0 > 12 and stable >= 6 and re.search(r"(Worked|Cooked|Baked|Brewed|Churned|Crunched|\w+ed) for \d+s", t):
            break
        if time.time() - t0 > 40 and stable >= 10:
            break
    shot("result")

plain = re.sub(rb"\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07", b"", bytes(rawbuf)).decode("utf-8", "replace")
ran_hook_counter = "running PreToolUse hook" in plain
fake = "FAKE_KEY" in plain.split(prompt[:30])[-1] if mode == "run" else None
send("\x03")
pump(0.5)
send("\x03")
pump(1)
try:
    os.kill(pid, signal.SIGTERM)
except Exception:
    pass
logged = os.path.exists(log) and os.path.getsize(log) > 0
summary = (f"SUMMARY case={case} mode={mode} run={n} log={'yes' if logged else 'no'} "
           f"fake_key={'n/a' if fake is None else ('yes' if fake else 'no')} running_hook_counter_seen={ran_hook_counter}")
os.makedirs(out, exist_ok=True)
with open(os.path.join(out, f"{case}-{mode}-r{n}.txt"), "w") as f:
    f.write("\n".join(shots) + "\n" + summary + "\n")
print(summary)
