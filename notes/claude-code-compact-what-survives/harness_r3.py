#!/usr/bin/env python3
"""E-C2 (round 3): does who said a fact decide whether it survives /compact?

One multi-turn seed session (make_project_r3.py) plants facts through four channels:
  you typed (U*), Claude worked out from files (A*), tool output only (T*), reversals (RU by you, RC by Claude).
Branches fork from the same seed: A plain /compact (x3), B /compact with a keep instruction (x2), C no compaction (x1).
Each branch gets two probe turns with every tool blocked. Scoring: regex on probe replies and on the summary text,
then a manual read of every cell (notes in results-r3.md).

Usage: python3 harness_r3.py seed | branch A1 | score
"""
import json, os, re, shutil, subprocess, sys, uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = Path(os.environ.get('R3_WORK', '/tmp/exp/
RAW = HERE / 'raw-r3'
SUM = HERE / 'summaries-r3'
LOG = RAW / 'calls.jsonl'
HOME = str(Path.home())
MODEL = 'sonnet'
CAP_USD = 2.0
SEED_TOOLS = ['Read', 'Edit', 'Write', 'Glob', 'Grep', 'Bash(python3 tests/run.py*)', 'Bash(python tests/run.py*)',
              'Bash(ls *)']
PROBE_BLOCK = ['Read', 'Grep', 'Glob', 'Bash', 'Edit', 'Write', 'Task', 'Agent', 'WebFetch', 'WebSearch']
EDITED = ['refunds', 'fees', 'payouts', 'fx', 'settlement']

TURNS = [
    # 1: U1 chat rule, RC original plan (typed by user)
    "For the rest of this session, start every reply with `KIWI:`.\n\nWe're fixing refund rounding in ledger-svc. "
    "Plan for payouts: we'll write payout records with a batch job at end of day.\n\n"
    "First read src/ledger/refunds.py, legacy/money.py and docs/01-overview.md, then give me a two-line summary.",
    # 2: A1 root cause, user only asks
    "A customer refund came out one cent off. Why? Find the root cause.",
    # 3: RU decision X (typed), A2 config value (user only asks)
    "Decision for now: refunds keep ROUND_HALF_UP to match the partner statement, so don't change it yet.\n\n"
    "How many times does the payout writer retry on failure? Check the config.",
    # 4: U3 typed value, T1/T2 tool output only
    "FYI the nightly import starts at 02:10 UTC.\n\nRun the test suite with `python3 tests/run.py` and reply in one short line.",
    # 5: U2 typed drop reason, RC/A3 Claude reads docs and proposes
    "Let's drop the cache layer idea: invalidation can't be timed with the nightly import.\n\n"
    "Now read docs/02-payout-writer.md and docs/03-reconciliation.md. Does anything there change the end-of-day batch plan for payouts?",
    # 6: user only agrees
    "fine, go with that.",
    # 7: RU reversal typed with reason, E edits
    "Change of plan on rounding: refunds use ROUND_HALF_EVEN instead, because partner spec SPEC-8802 requires banker's rounding. "
    "Set ROUNDING_MODE to ROUND_HALF_EVEN (import it from decimal) in src/ledger/refunds.py, fees.py, payouts.py, fx.py "
    "and settlement.py. Don't run the tests yet.",
]
COMPACT_B = "/compact Keep abandoned directions with their reasons, every file path you edited, and the names of failing tests."
P1 = ("Without opening any files, answer from memory: (1) which tests are failing, by exact name, and what error code did "
      "they print? (2) what is the root cause of the refund being off by a cent, and where exactly is it (file and line)? "
      "(3) what retry value did you find in the config? (4) when does the nightly import start?")
P2 = ("From memory, no files: (1) which approaches or ideas did we drop, and why was each dropped? (2) what is the current "
      "rounding decision for refunds, and why? (3) how are we writing payout records now? (4) list every file you edited.")


def redact(s):
    return (s or '').replace(HOME, '~').replace(str(WORK), '<work>')


def calls():
    return [json.loads(l) for l in LOG.read_text().splitlines() if l.strip()] if LOG.exists() else []


def spent():
    return sum(r.get('delta', 0) or 0 for r in calls())


def last_cum(sid):
    c = [r['cost'] for r in calls() if r.get('session') == sid]
    return c[-1] if c else 0.0


def child_env():
    return {k: v for k, v in os.environ.items() if not (k.startswith('CLAUDE') or k == 'CLAUDECODE')}


def run_claude(proj, prompt, tag, budget, resume=None, session_id=None, fork=False, tools=None, block=None):
    if spent() > CAP_USD:
        sys.exit(f'cost cap reached: ${spent():.2f}')
    cmd = ['systemd-run', '--user', '--scope', '--quiet', '-p', 'MemoryMax=2G',
           'claude', '-p', prompt, '--model', MODEL, '--output-format', 'stream-json', '--verbose',
           '--permission-mode', 'acceptEdits', '--setting-sources', 'project', '--max-budget-usd', str(budget)]
    if resume: cmd += ['--resume', resume]
    if session_id: cmd += ['--session-id', session_id]
    if fork: cmd += ['--fork-session']
    if tools: cmd += ['--allowedTools', *tools]
    if block: cmd += ['--disallowedTools', *block]
    p = subprocess.run(cmd, cwd=proj, capture_output=True, text=True, timeout=900, env=child_env())
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
    rec = {'tag': tag, 'cost': cost, 'delta': round(cost - parent, 6), 'session': sid, 'compact': compact,
           'reply': redact(text), 'rc': p.returncode, 'stderr': redact(p.stderr[-400:])}
    with LOG.open('a') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    print(f'{tag}: +${rec["delta"]:.3f} total=${spent():.2f} compact={compact} rc={p.returncode}')
    return rec


def jsonl_path(proj, sid):
    return Path(HOME) / '.claude' / 'projects' / re.sub(r'[^A-Za-z0-9]', '-', str(proj)) / f'{sid}.jsonl'


def after_compact(proj, sid):
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


def state():
    f = RAW / 'seed.json'
    return json.loads(f.read_text()) if f.exists() else None


def seed():
    d = WORK
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    proj = d / 'ledger-svc'
    subprocess.run([sys.executable, str(HERE / 'make_project_r3.py'), str(proj)], check=True)
    sid = str(uuid.uuid4())
    replies = []
    for i, t in enumerate(TURNS, 1):
        r = run_claude(proj, t, f'seed-t{i}', 0.40, session_id=sid if i == 1 else None,
                       resume=None if i == 1 else sid, tools=SEED_TOOLS)
        replies.append(r['reply'])
    diff = subprocess.run('git diff --name-only', shell=True, cwd=proj, capture_output=True, text=True).stdout.split()
    info = {'session': sid, 'proj': str(proj), 'diff': diff, 'version': subprocess.run(
        ['claude', '--version'], capture_output=True, text=True).stdout.strip()}
    (RAW / 'seed.json').write_text(json.dumps(info, indent=1))
    print(json.dumps(info, indent=1))


def branch(tag):
    st = state()
    proj, sid = Path(st['proj']), st['session']
    kind = tag[0]
    if kind == 'C':
        r = run_claude(proj, P1, f'{tag}-P1', 0.40, resume=sid, fork=True, block=PROBE_BLOCK)
        fsid = r['session']
    else:
        rc = run_claude(proj, '/compact' if kind == 'A' else COMPACT_B, f'{tag}-compact', 0.40, resume=sid, fork=True)
        fsid = rc['session']
        summary, after = after_compact(proj, fsid)
        (SUM / f'{tag}.txt').write_text(redact(summary or '(summary not found)'))
        (RAW / f'{tag}.after-compact.jsonl').write_text(after or '')
        run_claude(proj, P1, f'{tag}-P1', 0.40, resume=fsid, block=PROBE_BLOCK)
    run_claude(proj, P2, f'{tag}-P2', 0.40, resume=fsid, block=PROBE_BLOCK)


TESTS = ['test_refund_partial_cents', 'test_fx_refund_total', 'test_settlement_close_balance']


def judge(p1, p2):
    """Regex first pass: kept / altered / lost per fact. Every cell is re-read by hand afterwards."""
    h = lambda s, pat: bool(re.search(pat, s, re.I | re.S))
    out = {}
    out['U1 chat rule (KIWI)'] = 'kept' if p1.lstrip().startswith('KIWI') and p2.lstrip().startswith('KIWI') else (
        'altered' if p1.lstrip().startswith('KIWI') or p2.lstrip().startswith('KIWI') else 'lost')
    out['D root CLAUDE.md rule'] = 'kept' if 'ROOTOK' in p1 and 'ROOTOK' in p2 else ('altered' if 'ROOTOK' in p1 + p2 else 'lost')
    out['U2 your drop reason (cache)'] = ('kept' if h(p2, r'cache') and h(p2, r'invalidat|nightly import') else
                                         'altered' if h(p2, r'cache') else 'lost')
    out['U3 your value (02:10 UTC)'] = 'kept' if h(p1, r'02:10') else ('altered' if h(p1, r'nightly') and h(p1, r'\d{1,2}:\d{2}') else 'lost')
    out['A1 root cause found'] = ('kept' if h(p1, r'legacy/money\.py') and h(p1, r'\b42\b') and h(p1, r'HALF_UP') else
                                  'altered' if h(p1, r'money\.py|to_cents|HALF_UP') else 'lost')
    out['A2 config value found (retry 7)'] = ('kept' if h(p1, r'retry[^\n]{0,40}\b7\b|\b7\b[^\n]{0,20}retr|seven') else
                                              'altered' if h(p1, r'retry') else 'lost')
    n = sum(t in p1 for t in TESTS)
    out['T1 failing test names (output only)'] = 'kept' if n == 3 else ('altered' if n or h(p1, r'\b3\b|three') else 'lost')
    out['T2 error code (output only)'] = 'kept' if 'RECON-E-6604' in p1 else ('altered' if h(p1, r'RECON|balance mismatch') else 'lost')
    out['RU your reversal (HALF_EVEN, SPEC-8802)'] = ('kept' if h(p2, r'HALF_EVEN') and 'SPEC-8802' in p2 else
                                                      'altered' if h(p2, r'HALF_EVEN|HALF_UP') else 'lost')
    out['RC Claude-proposed switch (inline write)'] = ('kept' if h(p2, r'inside the settlement transaction|within the settlement transaction|same transaction|in the settlement transaction|synchronous|inline') else
                                                       'altered' if h(p2, r'batch') else 'lost')
    out["A3 Claude's drop reason (reconciliation)"] = ('kept' if h(p2, r'batch') and h(p2, r'reconcil') else
                                                       'altered' if h(p2, r'batch') else 'lost')
    m = sum(bool(re.search(rf'\b{e}\.py', p2)) for e in EDITED)
    out['E edited paths (5)'] = 'kept' if m == 5 else ('altered' if m else 'lost')
    return out


def score():
    by = {r['tag']: r for r in calls()}
    rows = []
    for tag in sorted({t.rsplit('-', 1)[0] for t in by if re.match(r'[ABC]\d-P1$', t)}):
        p1, p2 = by[f'{tag}-P1']['reply'], by.get(f'{tag}-P2', {}).get('reply', '')
        sf = SUM / f'{tag}.txt'
        summ = sf.read_text() if sf.exists() else ''
        af = RAW / f'{tag}.after-compact.jsonl'
        after = af.read_text() if af.exists() else ''
        j = judge(p1, p2)
        for fact, v in j.items():
            rows.append({'run': tag, 'fact': fact, 'verdict': v})
        rows.append({'run': tag, 'meta': {
            'reattached': re.findall(r'"displayPath":\s*"([^"]+)"', after) or re.findall(r'"filename":\s*"([^"]+)"', after),
            'summary_tests_named': sum(t in summ for t in TESTS), 'summary_has_6604': 'RECON-E-6604' in summ,
            'summary_has_42': bool(re.search(r'\b42\b', summ)), 'summary_has_retry7': bool(re.search(r'retry\D{0,15}7', summ)),
            'summary_has_0210': '02:10' in summ, 'summary_reconcil': bool(re.search('reconcil', summ, re.I)),
            'summary_sections': re.findall(r'^\s*(\d+\.\s+[A-Z][^\n:]{2,40}):', summ, re.M),
            'compact': by.get(f'{tag}-compact', {}).get('compact'), 'summary_words': len(summ.split())}})
    (HERE / 'results-r3-rows.json').write_text(json.dumps(rows, indent=1))
    for r in rows:
        if 'fact' in r:
            print(f"{r['run']:4} {r['verdict']:8} {r['fact']}")
        else:
            print(r['run'], json.dumps(r['meta'])[:600])
    print(f'total spent ${spent():.2f}')


if __name__ == '__main__':
    RAW.mkdir(exist_ok=True); SUM.mkdir(exist_ok=True)
    cmd = sys.argv[1]
    if cmd == 'seed':
        seed()
    elif cmd == 'branch':
        branch(sys.argv[2])
    elif cmd == 'score':
        score()
