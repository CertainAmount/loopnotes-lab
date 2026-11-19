#!/usr/bin/env python3
"""/compact survival experiment for Claude Code 2.1.296 (headless).

One seed session per repetition fills the context with real reads and edits in a
synthetic project (make_project.py). Branches fork from the seed:
  A  /compact
  B  /compact with a preservation instruction
  C  no compaction (control)
  D  auto-compact via CLAUDE_AUTOCOMPACT_PCT_OVERRIDE (optional)
Each branch then gets two probes with all tools blocked. Scoring is regex-only.

Usage:
  python3 harness.py run REP [--branches A,B,C]
  python3 harness.py auto REP --pct N
  python3 harness.py score
"""
import json, os, re, uuid, shutil, subprocess, sys, argparse, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = Path('/tmp/exp/
RAW = HERE / 'raw'
SUM = HERE / 'summaries'
RESULTS = RAW / 'results.jsonl'
HOME = str(Path.home())
MODEL = 'sonnet'
CAP_USD = 11.0
SEED_TOOLS = ['Read', 'Edit', 'Write', 'Glob', 'Grep', 'Bash(python scripts/migrate.py*)',
              'Bash(python3 scripts/migrate.py*)', 'Bash(python tests/run.py*)',
              'Bash(python3 tests/run.py*)', 'Bash(ls *)']
PROBE_BLOCK = ['Read', 'Grep', 'Glob', 'Bash', 'Edit', 'Write', 'Task', 'Agent', 'WebFetch', 'WebSearch']
EDIT_ORDER = ['rounding', 'settlement', 'fees', 'payouts', 'refunds', 'report_templates', 'fx']
MODIFIED = [f'src/ledger/{n}.py' for n in EDIT_ORDER]

TURN1 = ("For the rest of this session, start every reply with `KIWI:`.\n\n"
         "Decision: we are switching ROUNDING_MODE to ROUND_HALF_EVEN because partner spec SPEC-7731 requires banker's rounding.\n"
         "Constraint: do not modify anything under legacy/ — it is frozen until 2026-11-30.\n\n"
         "Do these in order:\n"
         "1. Read billing/invoice.py and billing/tax.py and give a one-line summary of each.\n"
         "2. Run `python3 scripts/migrate.py` to migrate the rounding setting. If it fails, do not retry; switch to editing files by hand.\n"
         "3. In src/ledger/, change ROUNDING_MODE to ROUND_HALF_EVEN (import it from decimal) in exactly this order: "
         + ", ".join(f"{n}.py" for n in EDIT_ORDER) + ".\n"
         "4. Run `python3 tests/run.py`.\n"
         "5. Remember the next step for later, but do not do it now: update tests/test_rounding.py.")
TURN2 = "Now read every file in docs/ and give me a 5-bullet summary of the architecture."
COMPACT_B = ("/compact Preserve verbatim: every file path you modified, each decision with its reason, approaches that "
             "failed with their exact error codes, directories we must not touch, the next step, and any formatting "
             "rules I gave in chat.")
P1 = ("Without opening any files, answer from memory: (1) list every file you modified this session, (2) which "
      "approach did we try and abandon, and what was the exact error, (3) what rounding decision did we make and why, "
      "(4) which directory must we not touch and until when, (5) what is the next step?")
P2 = "In one line, from memory: what convention applies when we talk about the billing/ code?"


def redact(s):
    return s.replace(HOME, '~')


def _recs():
    return [json.loads(l) for l in RESULTS.read_text().splitlines() if l.strip()] if RESULTS.exists() else []


def spent():
    # total_cost_usd is cumulative per session (forks inherit the parent's total), so sum per-call deltas
    return sum(r.get('delta', 0) or 0 for r in _recs())


def last_cum(sid):
    c = [r.get('cost', 0) for r in _recs() if r.get('session') == sid and 'delta' in r]
    return c[-1] if c else 0.0


def child_env(extra=None):
    env = {k: v for k, v in os.environ.items() if not (k.startswith('CLAUDE') or k == 'CLAUDECODE')}
    env.update(extra or {})
    return env


def run_claude(proj, prompt, tag, budget, resume=None, session_id=None, fork=False, tools=None, block=None, env=None):
    if spent() > CAP_USD:
        sys.exit(f'cost cap reached: ${spent():.2f}')
    cmd = ['claude', '-p', prompt, '--model', MODEL, '--output-format', 'stream-json', '--verbose',
           '--permission-mode', 'acceptEdits', '--setting-sources', 'project', '--max-budget-usd', str(budget)]
    if resume: cmd += ['--resume', resume]
    if session_id: cmd += ['--session-id', session_id]
    if fork: cmd += ['--fork-session']
    if tools: cmd += ['--allowedTools', *tools]
    if block: cmd += ['--disallowedTools', *block]
    p = subprocess.run(cmd, cwd=proj, capture_output=True, text=True, timeout=900, env=child_env(env))
    (RAW / f'{tag}.stream.jsonl').write_text(redact(p.stdout))
    sid, cost, text, compact = None, 0.0, '', None
    for line in p.stdout.splitlines():
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get('type') == 'system' and d.get('subtype') == 'init':
            sid = d.get('session_id')
        if d.get('type') == 'system' and d.get('subtype') == 'compact_boundary':
            compact = d.get('compact_metadata')
        if d.get('type') == 'result':
            cost = d.get('total_cost_usd') or 0.0
            text = d.get('result') or ''
    parent = last_cum(resume) if resume else 0.0
    rec = {'tag': tag, 'cost': cost, 'delta': round(cost - parent, 6), 'session': sid, 'compact': compact, 'reply': redact(text),
           'rc': p.returncode, 'stderr': redact(p.stderr[-500:])}
    with RESULTS.open('a') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    print(f'{tag}: +${cost - parent:.3f} (session total ${cost:.3f}) session={sid} compact={compact} total=${spent():.2f}')
    return rec


def jsonl_path(proj, sid):
    return Path(HOME) / '.claude' / 'projects' / re.sub(r'[^A-Za-z0-9]', '-', str(proj)) / f'{sid}.jsonl'


def extract_after_compact(proj, sid):
    """Return (summary_text, post_compact_raw) from the session JSONL after the last compact boundary."""
    p = jsonl_path(proj, sid)
    if not p.exists():
        return None, None
    lines = p.read_text().splitlines()
    idx = max((i for i, l in enumerate(lines) if '"compact_boundary"' in l), default=None)
    if idx is None:
        return None, None
    after = lines[idx + 1:]
    summary = None
    for l in after:
        try:
            d = json.loads(l)
        except Exception:
            continue
        if d.get('isCompactSummary') or 'This session is being continued' in l:
            c = d.get('message', {}).get('content')
            summary = c if isinstance(c, str) else ''.join(x.get('text', '') for x in c if isinstance(x, dict))
            break
    return summary, redact('\n'.join(after))


def setup(rep):
    d = WORK / f'rep{rep}'
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    subprocess.run([sys.executable, str(HERE / 'make_project.py'), str(d / 'ledger-svc')], check=True)
    return d / 'ledger-svc'


def seed(rep):
    proj = setup(rep)
    sid = str(uuid.uuid4())
    r1 = run_claude(proj, TURN1, f'rep{rep}-seed1', 1.50, session_id=sid, tools=SEED_TOOLS)
    r2 = run_claude(proj, TURN2, f'rep{rep}-seed2', 1.50, resume=sid, tools=SEED_TOOLS)
    diff = subprocess.run('git diff --name-only', shell=True, cwd=proj, capture_output=True, text=True).stdout.split()
    mt = sorted(((proj / f).stat().st_mtime_ns, f) for f in diff)
    info = {'tag': f'rep{rep}-seedinfo', 'cost': 0, 'session': sid, 'diff': diff,
            'mtime_order': [f for _, f in mt], 'legacy_touched': any(f.startswith('legacy/') for f in diff),
            'seed1_kiwi': r1['reply'].lstrip().startswith('KIWI:'), 'seed2_kiwi': r2['reply'].lstrip().startswith('KIWI:'),
            'seed1_rootok': r1['reply'].rstrip().endswith('-- ROOTOK'), 'seed2_rootok': r2['reply'].rstrip().endswith('-- ROOTOK')}
    with RESULTS.open('a') as f:
        f.write(json.dumps(info) + '\n')
    print(info)
    return proj, sid, info


def branch(rep, proj, sid, b, env=None, fill=None):
    tag = f'rep{rep}-{b}'
    if b == 'C':
        r = run_claude(proj, P1, f'{tag}-P1', 0.40, resume=sid, fork=True, block=PROBE_BLOCK)
        fsid = r['session']
    else:
        if b == 'D':
            rc = run_claude(proj, fill, f'{tag}-fill', 1.50, resume=sid, fork=True, tools=SEED_TOOLS, env=env)
        else:
            rc = run_claude(proj, '/compact' if b == 'A' else COMPACT_B, f'{tag}-compact', 0.60, resume=sid, fork=True)
        fsid = rc['session']
        summary, after = extract_after_compact(proj, fsid)
        (SUM / f'{tag}.txt').write_text(redact(summary or '(summary not found)'))
        (RAW / f'{tag}.after-compact.jsonl').write_text(after or '')
        r = run_claude(proj, P1, f'{tag}-P1', 0.40, resume=fsid, block=PROBE_BLOCK)
    run_claude(proj, P2, f'{tag}-P2', 0.40, resume=fsid, block=PROBE_BLOCK)


def score():
    recs = [json.loads(l) for l in RESULTS.read_text().splitlines() if l.strip()]
    by = {r['tag']: r for r in recs}
    rows = []
    for tag, r in by.items():
        m = re.match(r'(rep\d+)-([ABCD])-P1$', tag)
        if not m:
            continue
        rep, b = m.groups()
        p1, p2 = r['reply'], by.get(f'{rep}-{b}-P2', {}).get('reply', '')
        sfile = SUM / f'{rep}-{b}.txt'
        summ = sfile.read_text() if sfile.exists() else ''
        after = (RAW / f'{rep}-{b}.after-compact.jsonl')
        after = after.read_text() if after.exists() else ''
        def has(s, pat): return bool(re.search(pat, s))
        row = {'rep': rep, 'branch': b,
               'P1_kiwi': p1.lstrip().startswith('KIWI:'), 'P2_kiwi': p2.lstrip().startswith('KIWI:'),
               'P1_rootok': p1.rstrip().endswith('-- ROOTOK'), 'P2_rootok': p2.rstrip().endswith('-- ROOTOK'),
               'P2_heron': has(p2, 'HERON'), 'sum_heron': has(summ, 'HERON'), 'sum_kiwi': has(summ, 'KIWI'),
               'after_billing_claudemd': 'billing/CLAUDE.md' in after, 'after_owl': 'OWL-HOOK' in after,
               'P1_paths': sum(bool(re.search(rf'\b{n}\.py', p1)) for n in EDIT_ORDER),
               'sum_paths': sum(bool(re.search(rf'\b{n}\.py', summ)) for n in EDIT_ORDER),
               'P1_memory_file': has(p1, r'MEMORY\.md|memory file'),
               'P1_legacy_as_modified': has(re.split(r'\n\s*\**\(?2[.)]', p1)[0], r'legacy/'),
               'P1_half_even': has(p1, 'HALF_EVEN'), 'P1_spec': has(p1, 'SPEC-7731'),
               'sum_spec': has(summ, 'SPEC-7731'),
               'P1_err': has(p1, 'E_LOCK_9472'), 'sum_err': has(summ, 'E_LOCK_9472'), 'P1_migrate': has(p1, 'migrat'),
               'P1_legacy_date': has(p1, 'legacy') and has(p1, '2026-11-30'),
               'P1_next': has(p1, 'tests/test_rounding.py'), 'sum_next': has(summ, 'test_rounding'),
               'reattached': re.findall(r'"displayPath":\s*"([^"]+)"', after),
               'report_templates_ref_only': ('Referenced file' in after and 'report_templates' in after),
               'compact': by.get(f'{rep}-{b}-compact', by.get(f'{rep}-{b}-fill', {})).get('compact'),
               'P1_cost': r.get('delta'), 'sum_words': len(summ.split())}
        rows.append(row)
    out = HERE / 'results-rows.json'
    out.write_text(json.dumps(rows, indent=1))
    print(json.dumps(rows, indent=1)[:6000])
    print(f'total spent ${spent():.2f}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['run', 'auto', 'score'])
    ap.add_argument('rep', nargs='?', type=int)
    ap.add_argument('--branches', default='A,B,C')
    ap.add_argument('--pct', type=int, default=40)
    a = ap.parse_args()
    RAW.mkdir(exist_ok=True); SUM.mkdir(exist_ok=True)
    if a.cmd == 'score':
        return score()
    proj, sid, info = seed(a.rep)
    if len(info['diff']) < 7 or info['legacy_touched']:
        print('seed invalid'); return
    if a.cmd == 'run':
        bs = a.branches.split(',')
        random.Random(a.rep).shuffle(bs)
        for b in bs:
            branch(a.rep, proj, sid, b)
    else:
        branch(a.rep, proj, sid, 'D', env={'CLAUDE_AUTOCOMPACT_PCT_OVERRIDE': str(a.pct)},
               fill='Read docs/ again and list every section heading.')


if __name__ == '__main__':
    main()
