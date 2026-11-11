import csv,sys,datetime as dt
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as md
src,out=sys.argv[1],sys.argv[2]
rows=list(csv.DictReader(open(src)))
d=[dt.date.fromisoformat(r['date']) for r in rows]; s=[float(r['standard_89800_usd']) for r in rows]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13})
fig,ax=plt.subplots(figsize=(12,6.75),dpi=120); fig.patch.set_facecolor('#fcfcfb'); ax.set_facecolor('#fcfcfb')
ax.axhline(79.99,color='#eb6834',lw=2); ax.plot(d,s,color='#2a78d6',lw=2)
ax.text(d[2],80.6,'US price $79.99',color='#0b0b0b',fontsize=13)
ax.text(d[-1],s[-1]-2.6,'Korea price in USD',color='#0b0b0b',fontsize=13,ha='right')
for key,lab,dy in [('2026-07-01','$57.63 (Jul 1)',-2.2),('2026-11-10','$67.06 (Nov 10)',1.1)]:
    i=[r['date'] for r in rows].index(key); ax.plot(d[i],s[i],'o',ms=8,color='#2a78d6',mec='#fcfcfb',mew=2)
    ax.text(d[i],s[i]+dy,lab,color='#52514e',fontsize=12,ha='center' if key<'2026-11' else 'right')
ax.set_ylim(50,85); ax.set_ylabel('USD',color='#52514e')
ax.xaxis.set_major_formatter(md.DateFormatter('%b')); ax.xaxis.set_major_locator(md.MonthLocator())
for sp in ['top','right']: ax.spines[sp].set_visible(False)
for sp in ['left','bottom']: ax.spines[sp].set_color('#c3c2b7')
ax.tick_params(colors='#52514e'); ax.grid(axis='y',color='#ecebe7',lw=1)
ax.set_title('GTA 6 Standard: ₩89,800 in USD',loc='left',color='#0b0b0b',fontsize=16,pad=14)
fig.text(0.01,0.01,'ECB reference rates via Frankfurter, Jun 22 – Nov 10, 2026',color='#52514e',fontsize=10)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(out,facecolor=fig.get_facecolor())
