import json,re,sys
from gen import norm
qs=[json.loads(l) for l in open('questions.jsonl')]
for k in sys.argv[1:]:
    ch={c['id']:c for c in map(json.loads,open(f'chunks-{k}.jsonl'))}
    top=json.load(open(f'top50-{k}.json'))
    row=[]
    for q in qs:
        g=norm(q['gold_span'])
        r=next((t['rank'] for t in top[q['id']] if g in norm(ch[t['id']]['text'])),None)
        row.append(f"{q['id']}:{r}")
    print(k,' '.join(row))
