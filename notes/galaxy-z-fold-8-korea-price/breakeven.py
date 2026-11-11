"""Break-even KRW/USD rate per SKU: Korean list price (VAT in) / US price (before tax).
Usage: python breakeven.py <out.csv> <today_rate>"""
import csv,sys
KR={'Fold 8 256GB':2278100,'Fold 8 512GB':2531100,'Fold 8 1TB':3152600,
    'Ultra 256GB':2577300,'Ultra 512GB':2830300,'Ultra 1TB':3451800}
US={'Fold 8 256GB':1899.99,'Fold 8 512GB':2099.99,'Fold 8 1TB':2499.99,
    'Ultra 256GB':2099.99,'Ultra 512GB':2299.99,'Ultra 1TB':2699.99}
out,rate=sys.argv[1],float(sys.argv[2])
with open(out,'w',newline='') as f:
    w=csv.writer(f); w.writerow(['sku','kr_krw','us_list_usd','be_list','be_200off','be_300off','kr_usd_at_rate','us_list_minus_kr_usd','us_list_vs_kr_pct','us300_minus_kr_usd','us300_vs_kr_pct'])
    for k in KR:
        kr,us=KR[k],US[k]; kru=kr/rate
        w.writerow([k,kr,us,round(kr/us,1),round(kr/(us-200),1),round(kr/(us-300),1),round(kru,1),
                    round(us-kru,1),round((us-kru)/us*100,1),round(us-300-kru,1),round((us-300-kru)/(us-300)*100,1)])
