# Korea vs US list prices in US dollars

How much cheaper (or dearer) is a product's Korean list price than its US list price, converted at each day's ECB reference rate?

## Latest

ECB rate on 2026-11-12: 1,334.10 won per dollar.

| Item | Korea list (VAT in) | In USD | US list (before tax) | Korea cheaper by (minus = dearer) |
|---|---|---|---|---|
| GTA 6 Standard (PS5/Xbox) | ₩89,800 | $67.31 | $79.99 | 15.9% |
| GTA 6 Ultimate (PS5/Xbox) | ₩112,800 | $84.55 | $99.99 | 15.4% |
| Galaxy Z Fold 8 256GB | ₩2,278,100 | $1,707.59 | $1,899.99 | 10.1% |
| Galaxy Z Fold 8 512GB | ₩2,531,100 | $1,897.23 | $2,099.99 | 9.7% |
| Galaxy Z Fold 8 1TB | ₩3,152,600 | $2,363.09 | $2,499.99 | 5.5% |
| Galaxy Z Fold 8 Ultra 256GB | ₩2,577,300 | $1,931.86 | $2,099.99 | 8.0% |
| Galaxy Z Fold 8 Ultra 512GB | ₩2,830,300 | $2,121.51 | $2,299.99 | 7.8% |
| Galaxy Z Fold 8 Ultra 1TB | ₩3,451,800 | $2,587.36 | $2,699.99 | 4.2% |
| Nintendo Switch 2 | ₩758,000 | $568.17 | $499.99 | -13.6% |

## Method

Korean list prices include 10% VAT; US list prices are before sales tax. Each ECB business day, krw / (KRW per USD) gives the Korean price in USD; korea_cheaper_pct = (usd_list - krw_in_usd) / usd_list x 100. List prices change only when a row with a later 'from' date is added, each with its source and the day it was read.

Exchange rates: ECB reference rates via the Frankfurter API (https://api.frankfurter.dev), from 2026-06-22. Rows: one per ECB business day per item.

## Files

- `items.json`: every list price with the date it starts, its source and the day it was read
- `fx-usd-krw.csv`: the daily rate
- `prices.csv`: every item on every day

## Articles that use it

- https://loopnotes.dev/gta-6-korea-price/
- https://loopnotes.dev/galaxy-z-fold-8-korea-price/

Last collected: 2026-11-13.
