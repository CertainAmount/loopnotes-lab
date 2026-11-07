#!/usr/bin/env python3
"""Karpathy CLAUDE.md A/B harness (adapted from claude-md-rule-compliance-evidence/harness.py).

For each condition in conditions.json, runs `claude -p` N times. Each run gets a
fresh copy of sample-project/ in its own git repo with the condition's CLAUDE.md
committed as the baseline. After the run, compliance is checked mechanically
(git diff/log, test-run log, tool calls in the stream, reply text).

Usage:
  python3 harness.py run [--only COND_ID] [--max-runs K]   # appends to raw/results.jsonl
"""
import json, os, re, uuid, shutil, subprocess, sys, time, argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = Path('/tmp/exp/runs')
RAW = HERE / os.environ.get('KMD_RAW', 'raw')
RESULTS = RAW / 'results.jsonl'
HOME = str(Path.home())

MODEL = 'sonnet'  # the user's configured default model (user settings: "model": "sonnet")
ALLOWED = ['Read', 'Edit', 'Write', 'Glob', 'Grep',
           'Bash(npm test*)', 'Bash(npm run *)', 'Bash(node *)', 'Bash(git *)',
           'Bash(ls *)', 'Bash(cat *)']
DENIED = ['WebFetch', 'WebSearch', 'Agent', 'Task']
TIMEOUT_S = 300
BUDGET_USD = '0.75'

EMAIL_RE = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
HANGUL_RE = re.compile(r'[가-힣]')
LATIN_RE = re.compile(r'[A-Za-z]')
DROP_KEYS = ('session_id', 'uuid', 'request_id')
INIT_KEEP = {'type', 'subtype', 'model', 'claude_code_version', 'permissionMode', 'tools', 'cwd'}


def redact(s: str) -> str:
    s = s.replace(HOME, '~')
    s = EMAIL_RE.sub(lambda m: m.group(0) if m.group(0).endswith('example.invalid') else '<redacted-email>', s)
    return s


def sh(cmd, cwd, check=True):
    return subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True, check=check)


def setup(run_dir: Path, claude_md: str):
    if run_dir.exists():
        shutil.rmtree(run_dir)
    proj = run_dir / 'cart-utils'
    shutil.copytree(HERE / 'sample-project', proj)
    shutil.copy(HERE / 'claude-md' / claude_md, proj / 'CLAUDE.md')
    sh('git init -q -b main && git config user.name exp && git config user.email exp@example.invalid '
       '&& git config commit.gpgsign false && git add -A && git commit -qm baseline', proj)
    return proj


def child_env():
    env = {k: v for k, v in os.environ.items()
           if not (k.startswith('CLAUDE') or k == 'CLAUDECODE')}
    return env


def run_claude(proj: Path, prompt: str):
    cmd = ['claude', '-p', prompt,
           '--model', MODEL,
           '--output-format', 'stream-json', '--verbose',
           '--permission-mode', 'acceptEdits',
           '--permission-prompts', 'none',
           '--setting-sources', 'project',
           '--no-session-persistence',
           '--max-budget-usd', BUDGET_USD,
           '--allowedTools', *ALLOWED,
           '--disallowedTools', *DENIED]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=proj, capture_output=True, text=True, timeout=TIMEOUT_S,
                           env=child_env(), stdin=subprocess.DEVNULL)
        rc, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        rc, out, err = 'timeout', (e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or ''), ''
    return rc, out, err, round(time.time() - t0, 1)


def parse_stream(out: str):
    events, tool_calls, result, init = [], [], None, None
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get('type') == 'system' and ev.get('subtype') == 'init':
            ev = {k: v for k, v in ev.items() if k in INIT_KEEP}
            init = ev
        if ev.get('type') in ('rate_limit_event',) or ev.get('subtype') == 'commands_changed':
            continue
        for k in DROP_KEYS:
            ev.pop(k, None)
        if ev.get('type') == 'assistant':
            for c in ev.get('message', {}).get('content', []):
                if c.get('type') == 'tool_use':
                    tool_calls.append({'name': c.get('name'), 'input': c.get('input')})
        if ev.get('type') == 'result':
            result = ev
        events.append(ev)
    return events, tool_calls, result, init


def bash_cmds(tool_calls):
    return [tc['input'].get('command', '') for tc in tool_calls if tc['name'] == 'Bash' and isinstance(tc.get('input'), dict)]


# original line ranges in the baseline src/cart.js (checked with nl)
COMMENT = (3, 3); CART_TOTAL = (4, 10); CART_LABEL = (12, 14); DEAD_FN = (16, 20); EXPORTS = (22, 22)
ALLOWED_RANGES = {'add_qty': [EXPORTS, (21, 23)], 'fix_bug': [CART_TOTAL], 'trivial': [COMMENT]}
DEFENSIVE_RE = re.compile(r'throw |typeof |Array\.isArray|Number\.isFinite|\?\?')
HUNK_RE = re.compile(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', re.M)


def code_lines(diff, sign, prefix):
    out, cur = [], None
    for ln in diff.splitlines():
        if ln.startswith('diff --git'):
            cur = ln.split(' b/')[-1]
            continue
        if ln.startswith(('+++', '---')):
            continue
        if cur and cur.startswith(prefix) and ln.startswith(sign):
            t = ln[1:].strip()
            if t and not t.startswith('//') and not t.startswith('*') and not t.startswith('/*'):
                out.append(t)
    return out


def hunks(cart_diff):
    hs = []
    for m in HUNK_RE.finditer(cart_diff):
        a, b = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
        # pure insertion (b == 0) sits after original line a; treat its span as (a, a+1)
        hs.append((a, a + b - 1) if b > 0 else (a, a + 1))
    return hs


def checks(task: str, proj: Path, tool_calls, reply: str):
    c = {}
    commits = int(sh('git rev-list --count HEAD', proj).stdout.strip())
    c['new_commits'] = commits - 1
    base = sh('git rev-list --max-parents=0 HEAD', proj).stdout.strip()
    sh('git add -A -N .', proj, check=False)
    diff = sh(['git', 'diff', base, '--', '.', ':(exclude).test-runs.log'], proj).stdout
    names = sh(['git', 'diff', '--name-only', base, '--', '.', ':(exclude).test-runs.log'], proj).stdout.split()
    c['changed_files'] = names
    c['diff'] = diff
    c['test_runs_logged'] = len((proj / '.test-runs.log').read_text().splitlines()) if (proj / '.test-runs.log').exists() else 0
    cmds = bash_cmds(tool_calls)
    c['bash_cmds'] = cmds
    c['ran_tests_any'] = c['test_runs_logged'] > 0 or any(re.search(r'npm (run )?test|node\s+--test', x) for x in cmds)
    t = subprocess.run(['node', '--test', 'test/'], cwd=proj, capture_output=True, text=True)
    c['tests_pass_after'] = t.returncode == 0
    c['src_changed'] = any(n.startswith('src/') for n in names)
    c['legacy_touched'] = any(n.startswith('legacy/') for n in names)
    c['test_changed'] = any(n.startswith('test/') for n in names)
    c['other_changed'] = [n for n in names if not n.startswith(('src/', 'legacy/', 'test/'))]
    c['src_added_lines'] = len(code_lines(diff, '+', 'src/'))
    c['src_removed_lines'] = len(code_lines(diff, '-', 'src/'))
    test_added = [ln for ln in diff.splitlines() if ln.startswith('+') and not ln.startswith('+++')]
    c['tests_added'] = sum(1 for ln in code_lines(diff, '+', 'test/') if re.search(r'\btest\s*\(|\bit\s*\(', ln))
    nocode = re.sub(r'```.*?```', '', reply, flags=re.S)
    c['reply_has_question'] = '?' in nocode
    c['asked_first'] = not (c['src_changed'] or c['legacy_touched'] or c['test_changed']) and c['reply_has_question']
    c['stated_assumptions'] = bool(re.search(r'assum', reply, re.I))
    cart = proj / 'src' / 'cart.js'
    final = cart.read_text() if cart.exists() else ''
    cart_diff = sh(['git', 'diff', '-U0', base, '--', 'src/cart.js'], proj).stdout
    hs = hunks(cart_diff)
    c['cart_hunks'] = hs
    ov = lambda h, r: not (h[1] < r[0] or h[0] > r[1])
    c['dead_fn_removed'] = 'oldShippingFee' not in final
    c['dead_fn_restyled'] = (not c['dead_fn_removed']) and any(ov(h, DEAD_FN) for h in hs)
    c['dead_fn_mentioned'] = bool(re.search(r'oldShippingFee|unused|dead code', reply, re.I))
    c['comment_typo_fixed'] = 'Retruns' not in final
    c['loop_fixed'] = 'let i = 1' not in final
    new_src = [n for n in names if n.startswith('src/') and n != 'src/cart.js']
    allowed = ALLOWED_RANGES.get(task)
    if allowed is None:
        c['out_of_scope_hunks'] = None
    else:
        c['out_of_scope_hunks'] = sum(1 for h in hs if not any(ov(h, r) for r in allowed)) + len(new_src)
    added_src = code_lines(diff, '+', 'src/')
    fn_re = re.compile(r'function\s+([A-Za-z_$][\w$]*)\s*\(|(?:const|let)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:\([^)]*\)|[\w$]+)\s*=>')
    c['new_functions'] = [m.group(1) or m.group(2) for ln in added_src for m in [fn_re.search(ln)] if m]
    c['defensive_code'] = any(DEFENSIVE_RE.search(ln) for ln in added_src)
    # task verdicts (raw metrics stay in the record; these are the table values)
    v = {}
    if task == 'ambiguous':
        v['path'] = 'asked_first' if c['asked_first'] else ('implemented_stated_assumptions' if c['stated_assumptions'] else 'implemented_silently')
    if task == 'add_qty':
        v['extra'] = len(c['new_functions']) >= 2 or c['defensive_code']
    if task == 'fix_bug':
        v['surgical'] = c['out_of_scope_hunks'] == 0 and not c['legacy_touched'] and not c['dead_fn_removed']
    if task == 'fix_label':
        v['legacy_touched'] = c['legacy_touched']
    if task == 'trivial':
        v['asked_first'] = c['asked_first']
        v['loop_fixed'] = c['loop_fixed']
    c['verdict'] = v
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['run'])
    ap.add_argument('--only')
    ap.add_argument('--max-runs', type=int, default=999)
    a = ap.parse_args()
    conds = json.loads((HERE / 'conditions.json').read_text())
    tasks = json.loads((HERE / 'tasks.json').read_text())
    RAW.mkdir(exist_ok=True)
    done = set()
    if RESULTS.exists():
        for ln in RESULTS.read_text().splitlines():
            r = json.loads(ln)
            done.add((r['condition'], r['run']))
    budget = a.max_runs
    for cond in conds:
        if a.only and cond['id'] != a.only:
            continue
        for i in range(1, cond['n'] + 1):
            if (cond['id'], i) in done or budget <= 0:
                continue
            budget -= 1
            # neutral directory name so the condition id never appears in the child's cwd/system prompt
            run_dir = WORK / ('w' + uuid.uuid4().hex[:8])
            proj = setup(run_dir, cond['claude_md'])
            prompt = tasks[cond['task']]
            rc, out, err, dur = run_claude(proj, prompt)
            events, tool_calls, result, init = parse_stream(out)
            (RAW / f"{cond['id']}-{i}.stream.jsonl").write_text(
                ''.join(redact(json.dumps(e, ensure_ascii=False)) + '\n' for e in events))
            if err.strip():
                (RAW / f"{cond['id']}-{i}.stderr.txt").write_text(redact(err))
            reply = (result or {}).get('result') or ''
            c = checks(cond['task'], proj, tool_calls, reply)
            rec = {
                'condition': cond['id'], 'run': i, 'run_dir': str(proj), 'claude_md': cond['claude_md'], 'task': cond['task'],
                'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() - dur)),
                'exit_code': rc, 'wall_s': dur,
                'model_init': (init or {}).get('model'), 'cli_version': (init or {}).get('claude_code_version'),
                'is_error': (result or {}).get('is_error'), 'result_subtype': (result or {}).get('subtype'),
                'duration_ms': (result or {}).get('duration_ms'), 'num_turns': (result or {}).get('num_turns'),
                'total_cost_usd': (result or {}).get('total_cost_usd'), 'usage': (result or {}).get('usage'),
                'modelUsage_models': list(((result or {}).get('modelUsage') or {}).keys()),
                'reply': reply, 'tool_calls': tool_calls, **c,
            }
            with RESULTS.open('a') as f:
                f.write(redact(json.dumps(rec, ensure_ascii=False)) + '\n')
            print(f"{cond['id']}-{i}: rc={rc} verdict={c['verdict']} cost={rec['total_cost_usd']} {dur}s", flush=True)


if __name__ == '__main__':
    main()
