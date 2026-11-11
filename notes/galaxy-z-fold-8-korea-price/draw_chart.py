"""Dot chart of break-even KRW/USD rates (non-zero axis, so dots not bars).
Usage: python draw_chart.py <breakeven.csv> <out.png> <today_rate>"""
import csv,sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
src,out,rate=sys.argv[1],sys.argv[2],float(sys.argv[3])
rows=list(csv.DictReader(open(src)))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13})
fig,ax=plt.subplots(figsize=(12,6.75),dpi=120); bg='#fcfcfb'
fig.patch.set_facecolor(bg); ax.set_facecolor(bg)
n=len(rows)
for i,r in enumerate(rows):
    ax.plot([i,i],[float(r['be_list']),float(r['be_300off'])],color='#c3c2b7',lw=2,zorder=1)
for key,lab,c,m in [('be_list','US list price','#2a78d6','o'),('be_200off','$200 off','#eb6834','s')]:
    ax.scatter(range(n),[float(r[key]) for r in rows],s=130,color=c,marker=m,label=lab,edgecolors=bg,linewidths=2,zorder=3)
# $300 off: seen on Samsung US for the Fold 8 only; Ultra dots are an assumed cut (hollow)
seen=[i for i,r in enumerate(rows) if not r['sku'].startswith('Ultra')]
assumed=[i for i,r in enumerate(rows) if r['sku'].startswith('Ultra')]
ax.scatter(seen,[float(rows[i]['be_300off']) for i in seen],s=130,color='#1baf7a',marker='D',label='$300 off',edgecolors=bg,linewidths=2,zorder=3)
ax.scatter(assumed,[float(rows[i]['be_300off']) for i in assumed],s=110,facecolors=bg,marker='D',label='Assumed $300 off',edgecolors='#1baf7a',linewidths=2.2,zorder=3)
ax.axhline(rate,color='#0b0b0b',lw=2,ls='--',zorder=2)
ax.text(-0.45,rate+5,"Today's rate",ha='left',va='bottom',color='#0b0b0b',fontsize=13)
ax.text(n-0.55,1180,'Below the line: Korea cheaper',ha='right',color='#52514e',fontsize=12)
ax.text(n-0.55,1458,'Above the line: US cheaper',ha='right',color='#52514e',fontsize=12)
ax.set_xticks(range(n)); ax.set_xticklabels([r['sku'] for r in rows],color='#52514e')
ax.set_xlim(-0.6,n-0.4); ax.set_ylim(1160,1480); ax.set_ylabel('Won per dollar',color='#52514e')
for sp in ['top','right']: ax.spines[sp].set_visible(False)
for sp in ['left','bottom']: ax.spines[sp].set_color('#c3c2b7')
ax.tick_params(colors='#52514e'); ax.grid(axis='y',color='#ecebe7',lw=1); ax.set_axisbelow(True)
ax.legend(loc='upper left',bbox_to_anchor=(0,1.02),frameon=False,ncol=4,fontsize=12)
ax.set_title('Break-even rate by model',loc='left',color='#0b0b0b',fontsize=16,pad=26)
fig.tight_layout(); fig.savefig(out,facecolor=bg)
