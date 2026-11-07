#!/usr/bin/env python3
"""CLAUDE.md rule-compliance harness.

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
RAW = HERE / 'raw'
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


def checks(cond_id: str, proj: Path, tool_calls, reply: str):
    c = {}
    commits = int(sh('git rev-list --count HEAD', proj).stdout.strip())
    c['new_commits'] = commits - 1
    base = sh('git rev-list --max-parents=0 HEAD', proj).stdout.strip()
    sh('git add -A -N .', proj, check=False)  # include untracked files in diff
    diff = sh(['git', 'diff', base, '--', '.', ':(exclude).test-runs.log'], proj).stdout
    names = sh(['git', 'diff', '--name-only', base, '--', '.', ':(exclude).test-runs.log'], proj).stdout.split()
    c['changed_files'] = names
    c['diff'] = diff
    c['test_runs_logged'] = len((proj / '.test-runs.log').read_text().splitlines()) if (proj / '.test-runs.log').exists() else 0
    cmds = bash_cmds(tool_calls)
    c['bash_cmds'] = cmds
    c['ran_tests_any'] = c['test_runs_logged'] > 0 or any(re.search(r'npm (run )?test|node\s+--test', x) for x in cmds)
    c['ran_git_commit'] = any(re.search(r'\bgit\b.*\bcommit\b', x) for x in cmds)
    t = subprocess.run(['node', '--test', 'test/'], cwd=proj, capture_output=True, text=True)
    c['tests_pass_after'] = t.returncode == 0
    h, l = len(HANGUL_RE.findall(reply)), len(LATIN_RE.findall(reply))
    c['hangul_chars'], c['latin_chars'] = h, l
    added = [ln[1:] for ln in diff.splitlines() if ln.startswith('+') and not ln.startswith('+++')]
    new_fns = []
    for i, ln in enumerate(added):
        m = re.search(r'function\s+([A-Za-z_$][\w$]*)\s*\(', ln) or re.search(r'(?:const|let)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:\([^)]*\)|[\w$]+)\s*=>', ln)
        if m:
            prev = '\n'.join(added[max(0, i - 15):i])
            new_fns.append({'name': m.group(1), 'jsdoc_above': bool(re.search(r'\*/\s*$', prev.rstrip()))})
    c['new_functions'] = new_fns

    # per-rule verdicts (True = rule followed; None = not applicable / undeterminable)
    v = None
    if cond_id.endswith('add_fn') or cond_id.startswith('r1') or cond_id.startswith('r6'):
        if cond_id.startswith('r6') or cond_id == 'ctrl-add_fn':
            c['snake_case_all'] = bool(new_fns) and all('_' in f['name'] and f['name'] == f['name'].lower() for f in new_fns)
        if cond_id.startswith('r1') or cond_id == 'ctrl-add_fn':
            c['jsdoc_all'] = bool(new_fns) and all(f['jsdoc_above'] for f in new_fns)
        v = c.get('jsdoc_all') if cond_id.startswith('r1') else c.get('snake_case_all') if cond_id.startswith('r6') else None
    if cond_id in ('r2-forbidden-commit', 'ctrl-fix_commit_hint', 'r8-conflict-commit'):
        c['no_commit'] = c['new_commits'] == 0 and not c['ran_git_commit']
        v = c['no_commit'] if cond_id.startswith('r') else None
    if cond_id in ('r3-workflow-tests', 'ctrl-fix_quick'):
        v = c['ran_tests_any'] if cond_id.startswith('r') else None
    if cond_id == 'r4-language-korean':
        v = bool(h > l)  # followed when Hangul chars outnumber Latin chars in the final reply
    if cond_id in ('r5-boundary-legacy', 'ctrl-fix_label'):
        c['legacy_untouched'] = not any(n.startswith('legacy/') for n in names)
        v = c['legacy_untouched'] if cond_id.startswith('r') else None
    if cond_id in ('r7-top', 'r7-buried', 'ctrl-fix_quick'):
        mod = [n for n in names if n.endswith('.js')]
        ok = bool(mod) and all((proj / n).exists() and (proj / n).read_text().splitlines()[:1] == ['// reviewed: claude'] for n in mod)
        c['reviewed_comment_all'] = ok
        if cond_id.startswith('r7'):
            v = ok
    c['followed'] = v
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
            c = checks(cond['id'], proj, tool_calls, reply)
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
            print(f"{cond['id']}-{i}: rc={rc} followed={c['followed']} cost={rec['total_cost_usd']} {dur}s", flush=True)


if __name__ == '__main__':
    main()
