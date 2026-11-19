#!/usr/bin/env python3
"""E-C2 add-on (T-only): a fact that lives only in tool output, never written in any chat message.

In the main E-C2 seed Claude copied the failing test names into its own reply, so the "tool output only" channel was
not isolated. Here the reply is limited to the failure count (the author's scene: the reply said "a few failing"),
then more files are read so the test run is not the last thing in the session. Same project, same cost cap
(the shared calls.jsonl in raw-r3/ counts every call of round 3).

Usage: python3 harness_r3t.py
"""
import re, shutil, subprocess, sys, uuid
from pathlib import Path
import harness_r3 as h

TURNS = [
    "Read src/ledger/refunds.py and docs/01-overview.md and give me a two-line summary.",
    "Run `python3 tests/run.py`. Reply with only the number of failing tests, nothing else.",
    "Now read docs/02-payout-writer.md and docs/03-reconciliation.md and summarize each in one line.",
]
PROBE = ("Without opening any files or running anything: which tests failed, by exact name, and what error code did "
         "they print? If you don't know, say so.")
TESTS = h.TESTS


def main():
    h.RAW.mkdir(exist_ok=True); h.SUM.mkdir(exist_ok=True)
    work = h.WORK.parent / 'cmp-exp-r3t'
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    proj = work / 'ledger-svc'
    subprocess.run([sys.executable, str(h.HERE / 'make_project_r3.py'), str(proj)], check=True)
    sid = str(uuid.uuid4())
    for i, t in enumerate(TURNS, 1):
        r = h.run_claude(proj, t, f'T-seed-t{i}', 0.30, session_id=sid if i == 1 else None,
                         resume=None if i == 1 else sid, tools=h.SEED_TOOLS)
        print(f'  reply t{i}: {r["reply"][:200]!r}')
    for b in ['TA1', 'TA2']:
        rc = h.run_claude(proj, '/compact', f'{b}-compact', 0.30, resume=sid, fork=True)
        fsid = rc['session']
        summary, after = h.after_compact(proj, fsid)
        (h.SUM / f'{b}.txt').write_text(h.redact(summary or '(summary not found)'))
        (h.RAW / f'{b}.after-compact.jsonl').write_text(after or '')
        p = h.run_claude(proj, PROBE, f'{b}-P1', 0.30, resume=fsid, block=h.PROBE_BLOCK)
        s = summary or ''
        print(f'  {b}: names in summary {sum(t in s for t in TESTS)}/3, code in summary {"RECON-E-6604" in s}, '
              f'names in probe {sum(t in p["reply"] for t in TESTS)}/3, code in probe {"RECON-E-6604" in p["reply"]}')
        print(f'  probe: {p["reply"][:400]!r}')


if __name__ == '__main__':
    main()
