# Is the Galaxy Z Fold 8 cheaper in Korea than in the US right now?

Research note for the loopnotes.dev post "Galaxy Z Fold 8 Korea Price vs US". All prices and rates checked on 2026-11-11 (KST) unless a row says otherwise.

## Conclusions
- In a US list-price week, such as 2026-11-11 at ₩1,343.3 per dollar, all six Fold 8 and Fold 8 Ultra SKUs cost less in Korea, by 4.8% to 10.7% of the US price, so a buyer should first check whether Samsung US is running a sale before deciding where to buy.
- In a week when Samsung US takes $300 off, all six SKUs are cheaper in the US before sales tax, by $84.3 to $169.7, so a US resident gains more by waiting for a sale than by buying in Korea.
- That US advantage is thin: on the Fold 8 256GB it is $95.9, or 6.0% of the sale price, so a buyer whose state and local sales tax is above about 6% pays roughly the same or more than the Korean price.
- In a $200-off week the answer splits by model: the Fold 8 256GB and 512GB stay slightly cheaper in Korea, while the Fold 8 1TB and all three Ultra SKUs become cheaper in the US.
- A visitor gets the VAT refund on a Fold 8 only at the airport with the box unopened, because the price is over ₩1,000,000; the refund brings the 256GB to at most ₩2,071,000 (about $1,541.7, before operator fees), and a visitor who uses the phone during the trip should compare at the full Korean price, about $1,695.9.
- Samsung US limits phone service to the country of first sale but gives a limited 12-month international warranty from the Galaxy S23 and Z Fold5 onward, with possible charges and delays, and returns only in the country of sale, so a Korean unit can be repaired in the US but not returned there.

## Question
Someone who could buy a Galaxy Z Fold 8 in Korea (a visitor, or a US resident thinking about ordering one) wants to know whether it is actually cheaper than buying in the US today, under which US sale conditions the answer flips, and what changes for a visitor (tax refund, warranty).

## Evidence

### 1. Exchange rate
- Bank of Korea ECOS, table 731Y001, KRW per USD (매매기준율, base rate), 2026-11-11: **₩1,343.3**. Raw response: `bok-ecos-731Y001-usdkrw-20261101-20261111.json` (Nov 2 to Nov 11; range ₩1,337.2 to ₩1,357.9).
- Cross-check: ECB reference rate via [Frankfurter](https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW) for 2026-11-10 was ₩1,339.0, a 0.3% difference. The post and every calculation below use the BOK value only.

### 2. US prices (Samsung US, official)
- Pages: [Galaxy Z Fold8 buy](https://www.samsung.com/us/smartphones/galaxy-z-fold8/buy/) and [Galaxy Z Fold8 Ultra buy](https://www.samsung.com/us/smartphones/galaxy-z-fold8-ultra/buy/), fetched with curl on 2026-11-11; the JSON-LD `Offer` blocks and price-string counts are saved in `samsung-us-jsonld-2026-11-11.md`.
- Fold8 256GB unlocked (SM-F971UZGAXAA): `price` 1899.99. Fold8 Ultra 512GB unlocked (SM-F976UDGEXAA): `price` 2299.99. Both `priceValidUntil` 2026-12-11.
- Other SKUs from price strings on the same pages: Fold8 $2,099.99 (512GB) and $2,499.99 (1TB); Ultra $2,099.99 (256GB) and $2,699.99 (1TB).
- Neither page contained the sale strings 1599.99 or 1699.99, so 2026-11-11 was a list-price week.
- Earlier sales seen on the same pages: $200 off every model with `priceValidUntil` 2026-10-30 (checked 2026-10-29); Fold8 256GB at $1,599.99 ($300 off) with `priceValidUntil` 2026-11-08 (checked 2026-11-07; the Ultra 512GB was at list price that day). The [Gadgeteer report of 2026-11-07, updated 2026-11-10](https://the-gadgeteer.com/?p=542473) gives the same $300 sale ($1,599.99 / 512GB $1,799.99, through 11-08).
- US prices are before state and local sales tax, which ranges from 0 to about 10% combined by locality (Tax Foundation, 2026 midyear).

### 3. Korean list prices (official, 10% VAT included)
- Fold8 ₩2,278,100 (256GB) / ₩2,531,100 (512GB) / ₩3,152,600 (1TB); Ultra ₩2,577,300 / ₩2,830,300 / ₩3,451,800. Source: Samsung Newsroom Korea, 2026-07-27.
- Unchanged as of [IT Chosun, 2026-11-01](https://it.chosun.com/news/articleView.html?idxno=2023092173188) ("256GB from ₩2,278,100").

### 4. Break-even exchange rates (calculation)
Break-even rate = Korean price (₩) ÷ US price ($). When the day's rate is above an SKU's break-even, Korea is cheaper in dollars; below it, the US is cheaper. The $200 and $300 columns apply that cut to every SKU; a $300 cut was seen on the Fold 8 only, so the Ultra $300 values mean "if the same cut applied". Script `breakeven.py`, output `breakeven-2026-11-11.csv`, chart script `draw_chart.py` (the chart image is in the post).

| SKU | Break-even: list | $200 off | $300 off | Korea in USD @₩1,343.3 | US list − Korea | US $300 off − Korea |
|---|---|---|---|---|---|---|
| Fold 8 256GB | 1,199.0 | 1,340.1 | 1,423.8 | $1,695.9 | +$204.1 (10.7%) | −$95.9 (6.0%) |
| Fold 8 512GB | 1,205.3 | 1,332.2 | 1,406.2 | $1,884.2 | +$215.7 (10.3%) | −$84.3 (4.7%) |
| Fold 8 1TB | 1,261.0 | 1,370.7 | 1,433.0 | $2,346.9 | +$153.1 (6.1%) | −$146.9 (6.7%) |
| Ultra 256GB | 1,227.3 | 1,356.5 | 1,431.8 | $1,918.6 | +$181.4 (8.6%) | −$118.6 (6.6%) |
| Ultra 512GB | 1,230.6 | 1,347.8 | 1,415.2 | $2,107.0 | +$193.0 (8.4%) | −$107.0 (5.3%) |
| Ultra 1TB | 1,278.4 | 1,380.7 | 1,438.3 | $2,569.6 | +$130.3 (4.8%) | −$169.7 (7.1%) |

Percentages are the dollar gap divided by the US price in that column.

### 5. Visitor effective price (Fold 8 256GB, calculation)
- Bought and used in Korea: ₩2,278,100 ≈ $1,695.9.
- Bought sealed, VAT refunded at the airport at the upper bound (1/11 of the price = ₩207,100, before refund-operator fees): ₩2,071,000 ≈ $1,541.7.
- A single purchase over ₩1,000,000 cannot be refunded instantly at the store; the refund is at the airport and requires the item unused and unopened at departure (covered on our posts [Buying a phone in Korea](https://loopnotes.dev/buy-phone-in-korea/) and the VisitKorea rules cited there).
- US comparison: $1,899.99 list or $1,599.99 in the $300 sale, both before sales tax.

### 6. Warranty wording (official)
- [Samsung US warranty page](https://www.samsung.com/us/support/warranty/), read 2026-11-11: Samsung limits service for smartphones to the country where the product was first sold; from the Galaxy S23 and Z Fold5 onward there is a limited international warranty of 12 months, under which repairs may be charged or delayed; returns and refunds happen only in the country of sale.
- The opposite direction (a US phone repaired in Korea) is covered by a Samsung Service Korea notice of 2023-11-20 (one-year international warranty, delays if parts are not in stock). That notice does not answer a Korean unit taken to the US.

### 7. Korean web search (Naver Search API, 2026-11-11)
Other people's reports, used to see what Korean buyers and sellers are talking about, not as prices for the post.

| Search term (Korean) | Meaning | Type: total results | What the sample showed |
|---|---|---|---|
| 폴드8 출고가 인하 | Fold 8 list price cut | news 585, blog 2,298 | No news report of an official list-price cut after launch (only July's "₩101,200 below the previous model"). Of 25 blog posts sampled, 6 from 10-30 to 11-05 describe a "sale", and each one says itself that the drop comes from carrier subsidies, cards or store financing, not the list price. |
| 폴드8 바겐세일 삼성닷컴 혜택가 | Fold 8 sale, Samsung.com Korea price | news 0 | Nothing found. |
| 갤럭시 폴드8 할인 11월 삼성전자 | Galaxy Fold 8 discount, November, Samsung | news 648 | Many 11-03 reports of Korean Fold 8 sales up 20%+; two November Samsung Korea promotions (Korea Grand Festival, Galaxy AI subscription club extended to 11-30). |
| 폴드8 공시지원금 인상 | Fold 8 carrier subsidy increase | news 325 | Carrier subsidies raised by about ₩100,000 on 10-21 (KT) and 10-22 (SKT, LG U+), up to ₩600,000 by carrier, for Korean carrier plans. |
| 외국인 폴드8 구매 택스리펀 | Foreigner buying Fold 8, tax refund | blog 4, cafe 0, Q&A 0 | One relevant post (a store's promotional blog). Visitor questions are almost absent from the Korean web too. |
| 폴드8 국내판 해외에서 사용 | Using a Korean Fold 8 abroad | blog 101, cafe 418, Q&A 3 | Few Fold 8 cases; cafe questions are mostly about the opposite direction (overseas phones in Korea: Samsung Pay, repairs). |

Posts referred to above (one-line summaries; not used as prices in the post):
- [todaypick00, 2026-10-31](https://blog.naver.com/todaypick00/224460141124): LG U+ number-port financed price of ₩1,418,100 for the 256GB, from subsidies, not a list-price cut.
- [queen0326, 2026-11-04](https://blog.naver.com/queen0326/224464120984): "₩1.03M range" store deals; says the official list price is still ₩2,278,100.
- [yamoojwi, 2026-10-07](https://blog.naver.com/yamoojwi/224433769664): compares an Amazon US price converted to about ₩2.08M with the Korean ₩2,278,100.
- [Lotte Hi-Mart Songdo, 2026-06-19](https://blog.naver.com/himart416/224320594729): store blog on tax refunds for foreign visitors.
- News: [Money Today, 10-30](https://n.news.naver.com/mnews/article/008/0005434298?sid=105) (subsidy increase), [Maeil Business, 11-10](https://n.news.naver.com/mnews/article/009/0005761604?sid=101) (up to ₩600,000 by carrier), [Yonhap, 11-03](https://n.news.naver.com/mnews/article/001/0016417501?sid=105) (sales up, subscription club extended).

### 8. Korean buyer reactions (earlier round, 2026-10-29)
Naver blog, cafe and Q&A results for 8 resident-side queries (about 700 results), with ads and duplicates removed: N=32 posts, several tags each. Price 9, iPhone Duo comparison or switch 8, switching from iPhone 5, battery and charging 5 (no measured screen-on times), weight 4 (all positive), "ended up using it folded" 4, crease 3, model choice 3, inner-screen scratches 2. Naver monthly search volume on the same date: crease 170, price 2,770, unlocked (자급제) 10,340. Example posts: [cafe, price](https://cafe.naver.com/appleiphone/9178188), [cafe, used folded](https://cafe.naver.com/appleiphone/9177496), [cafe, Duo crease vs Fold 8 Ultra](https://cafe.naver.com/appleiphone/9176108).

## Limits
- US sale status changes week to week; the 2026-11-11 reading shows a list-price week only. The conclusions are written per sale condition for that reason.
- The break-even table compares the US price before sales tax with the Korean price including VAT; sales tax depends on the buyer's state and locality.
- The visitor refund figure is an upper bound; refund operators deduct fees that are not published as one number.
- Korean carrier subsidies apply only to Korean carrier plans with a contract and are taken from news reports, not from the carriers' own notices.
- A PhoneArena report of $400 off the Ultra could not be read (Cloudflare challenge and HTTP 403 on 2026-11-11), so its date is unknown and it is not used.
- Network band compatibility of the Korean model on US carriers was not confirmed from an official band list.

## Added 2026-11-11 (reader check round 1): card costs, refund steps, model number

### 9. Card costs on the Korean side (calculation)
- A card fee applies to the Korean charge, so it raises the Korean price in dollars: Korea USD × (1 + fee). At a 3% fee the Fold 8 256GB becomes $1,746.8 at ₩1,343.3, and its $300-sale cutoff rises from 6.0% to 9.2% ((1,746.8 − 1,599.99) ÷ 1,599.99). The 3% is an example rate, not a quoted card's fee.
- Cutoff for any discount = (Korea price in USD − US sale price) ÷ US sale price. Example: $250 off the 256GB ($1,649.99) gives (1,695.9 − 1,649.99) ÷ 1,649.99 = 2.8%.
- Dynamic currency conversion: [GSA SmartPay Smart Bulletin 007](https://smartpay.gsa.gov/guidance-and-audits/smart-bulletins/007/) (revised 2024-03-22, read 2026-11-11): "Typically, the most cost effective purchase option is to make the purchase in a foreign currency"; merchant DCC fees "are often higher than if the cardholder simply made the purchase in the foreign currency".

### 10. Sealed-refund margin (calculation)
- Sealed, full VAT back: ₩2,071,000 = $1,541.73. Edge over the $300 sale: $58.26 = about ₩78,300 at ₩1,343.3.
- A 3% card fee on ₩2,278,100 = ₩68,343, which leaves about ₩9,900 of that edge before the refund operator's fee. Operator fees are not published as a table (Global Tax Free and Easy Tax Refund tourist pages, checked 2026-10-30 for our post buy-phone-in-korea); the author has never seen a net refund on a phone of this price (author interview).

### 11. Airport refund steps (official)
- [Incheon Airport, Tax refund](https://www.airport.kr/ap_en/1425/subview.do), read 2026-11-11: ask for the purchase receipt and tax refund documents at the store with your passport; check in; do not check refund items or documents as baggage; process at the departure-hall kiosk; if the kiosk requires customs inspection, show passport, the unopened and unused items and the purchase confirmation at the customs desk; checked-bag route: tell airline staff, bag gets a customs inspection tag, reclaim it and go to the customs desk; large refunds can be credited to a credit card.

### 12. Model number and US sales tax lookup
- Korean Fold 8 unlocked model: SM-F971N ([Compuzone listing](https://www.compuzone.co.kr/product/product_detail.htm?ProductNo=1393119) and [11st listing](https://www.11st.co.kr/products/9492622997), read 2026-11-11). Samsung Korea's own buy page returned a queue page. US unlocked: SM-F971U (Samsung US JSON-LD, section 2). The Ultra's Korean code was not confirmed from a fetched page.
- LTE/5G band list for SM-F971N: not found from an official source; the post tells the reader to run the unit's IMEI through the US carrier's bring-your-own-phone check.
- [Tax Foundation 2026 midyear](https://taxfoundation.org/data/all/state/2026-sales-tax-rates-midyear/), read 2026-11-11: columns include Average Local Tax Rate and Combined Tax Rate; highest combined Louisiana 10.13%, lowest Delaware, Montana, New Hampshire and Oregon at 0.00%; local averages are ZIP-code weighted.
- First discount: [9to5Google, 2026-09-07](https://9to5google.com/2026/09/07/samsung-galaxy-z-fold-8-first-ever-discount/): "$250 discounts across all Fold 8 variants" at Amazon and Best Buy (256GB $1,650, 512GB $1,850).

### 13. Moved out of the post (reader check, 2026-11-11)
- Per-model $200-week cutoffs: Fold 8 1TB 2.0%, Ultra 256GB 1.0%, Ultra 512GB 0.3%, Ultra 1TB 2.8% (Fold 8 256GB and 512GB stay cheaper in Korea before tax). Break-even ranges: list ₩1,199 to ₩1,278, $200 off ₩1,332 to ₩1,381, $300 off ₩1,406 to ₩1,438 (section 4).
- Korean prices are Samsung's launch list prices, the same unlocked or through a carrier; carrier subsidies (section 7) apply only with a Korean carrier plan.

## Added 2026-11-11 (reader check round 2): moved out of the post, where to buy, Samsung Pay

### 14. Moved out of the post (reader check round 2)
- Break-even exchange rate per model = Korean price (₩) ÷ US price ($), section 4. The post now keeps only the chart and its conclusion (at ₩1,343.3 every model is cheaper in Korea at US list and cheaper in the US at $300 off, before tax); the formula and the 256GB list break-even (₩1,199.0) stay here.
- July's "23% cheaper" headline: [Android Authority, 2026-07-23](https://www.androidauthority.com/galaxy-z-fold-8-korean-price-explanation-3690710/) converted at about ₩1,478; the Korean price has not changed since launch ([IT Chosun, 2026-11-01](https://it.chosun.com/news/articleView.html?idxno=2023092173188)), so the stronger won closed most of that gap.
- US sale timeline (rows that were a table in the post): early September, $250 off every Fold 8 at Amazon and Best Buy (9to5Google, 2026-09-07); through 2026-10-30, $200 off every model at Samsung US; through 2026-11-08, $300 off the Fold 8 at Samsung US (The Gadgeteer); 2026-11-11, back at list price.
- List-price gap by model: Samsung US charges $130 (Ultra 1TB) to $216 (Fold 8 512GB) more than Korea (section 4, table column).
- Tax range: combined state and local rates run from 0% (Oregon, Delaware, Montana, New Hampshire) to 10.13% (Louisiana), section 12.
- Example cutoff for a $250 discount on the 256GB: 2.8% (section 9).
- Samsung US international warranty applies from the Galaxy S23 and Z Fold5 onward ([Samsung US Warranty](https://www.samsung.com/us/support/warranty/), read 2026-11-11).
- The author's reverse case: in November the author priced a US Fold 8 at $1,599.99 for use in Seoul; [Samsung Electronics Service Korea](https://www.samsungsvc.co.kr/notice/3029667) repairs US units under a one-year international warranty, but at the roughly 8% US sales tax the author assumed (an estimate), the saving disappeared, and returns would still happen only in the US.

### 15. Sealed-refund margin in dollars (calculation)
- Edge of a sealed, full-VAT-back 256GB over the $300 sale: $58.26 (section 10). A 3% card fee on ₩2,278,100 is ₩68,343 = $50.88 at ₩1,343.3, leaving about $7.38 before the refund operator's fee. With a card that charges no foreign transaction fee, the full $58.26 remains before that fee.
- ₩207,100 = ₩2,278,100 ÷ 11, the 10% VAT contained in a VAT-inclusive price.

### 16. Where to buy, and payments on a Korean unit
- Where to buy: the author would send a visitor to a Samsung Store (Samsung's own retail shops in Korea) and tell them to show the passport and ask about tax refund documents before paying. Web searches on 2026-11-11 (Korean and English) found no page from Samsung Store, Lotte Hi-Mart or Electroland confirming post-departure tax refund documents for phones, and no confirmation of in-store discounts below the launch price; refund documents come only from shops enrolled in the tourist tax refund scheme ([VisitKorea](https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=140736)). The post tells the reader to ask both questions at the counter.
- Samsung Pay on a Korean unit: a Samsung Members (Gulf) community manager replied on 2025-10-20 that "Samsung Pay is region-specific and only works on devices that were originally intended for the region" ([thread](https://community.samsung.com/ae/conversations/Galaxy-S/Samsung-wallet-is-not-supporting-on-s25-international-version/r2_20839429), read 2026-11-11). No Samsung US support page on this was found. Other Samsung community threads (Canada, UAE) report the same tie to the phone's country code (CSC); these are user reports.
- eSIM support of the SM-F971N on US carriers: no official page found; the post tells the reader to ask the carrier during the IMEI check.

## Added 2026-11-11 (reader check round 1, rerun with author scenes kept)

### 17. Moved out of the post (rerun)
- The author's October reasoning on the reverse purchase (a US unit used in Seoul): he first dropped it believing Korean service centers would not repair a US unit for free; [Samsung Electronics Service Korea's 2023-11-20 notice](https://www.samsungsvc.co.kr/notice/3029667) says they repair it under a one-year international warranty, with delays when parts are short. The post keeps only the November step that applies to the reader: the $1,599.99 sale stopped saving him money once an estimated ~8% US sales tax was added (author interview, the 8% is an estimate).
- List-price gap by model ($130 to $216) and break-even ranges (sections 4, 13, 14): the post keeps the table column and the chart.
- Developer-specific purchase conditions (terminal app on the demo units, tmux in the emulator, 80-column test, replacing a Galaxy S23 test phone, a ₩3.1 million ceiling for the 512GB with 24 months of Samsung Care+) were taken out of this post as another reader's question (candidate article). The store visits themselves stay in the post as what a visitor should check on the floor unit.
- Sales tax examples used in the post: Louisiana combined average 10.13% (rounded to about 10.1%), Oregon 0.00% (section 12).

## Added 2026-11-11 (reader check round 2, rerun): airport payout and locations, moved out of the post

### 18. Incheon refund kiosks, desks and payout (official)
- [Incheon Airport, Tax refund](https://www.airport.kr/ap_en/1425/subview.do), read 2026-11-11: automated kiosks run 24 hours, on the 3rd floor of the duty-free zone near Gate 28 (Terminal 1, next to the central pharmacy on the Concourse 3rd floor listing), in the Concourse, and near Gate 253 across from Gate 250 (Terminal 2). Staffed desks: Terminal 1 (Korea Information & Communications) near Gate 28, 07:00 to 22:00; Terminal 2 (NICE Information & Telecommunication) near Gate 253, 07:00 to 21:30. Payout: "If the refund amount is large or if you prefer not to receive cash, you can choose to have the refund credited to your own credit card." The page does not state the cash currency, how long a card credit takes, or where the customs desk for carry-on inspection sits.
- Checked-bag route on the same page: tell airline staff at check-in, the bag gets a customs inspection tag and is reclaimed, kiosk, customs if required, then the bag goes on the large conveyor next to the customs desk.
- [Incheon Airport, Customs Declaration](https://www.airport.kr/ap_en/1424/subview.do), read 2026-11-11: covers currency and valuables declarations; no customs desk location for tax refund inspection.
- Author (author interview): has never claimed an airport refund at Incheon nor watched a visitor do it; no first-hand currency, card-credit timing or desk location.

### 19. Moved out of the post (reader check round 2, rerun)
- Sale history (section 14): $250 off at Amazon and Best Buy in early September, $200 off at Samsung US through October 30, $300 off the Fold 8 through November 8. The post keeps the link to the first cut and the $300 end date.
- Tax examples Louisiana about 10.1% and Oregon 0% (section 17): the post keeps only where to look up a rate.
- July conversion at about ₩1,478 (Android Authority, section 14): the post says the headlines used a much weaker won.
- The ₩1,000,000 store-refund ceiling (section 5): the post says a phone at this price isn't refunded at the store.
- $200-week cutoffs (section 13): 1TB 2.0%, Ultra 256GB 1.0%, Ultra 512GB 0.3%, Ultra 1TB 2.8%, below which Samsung US was cheaper; the post now gives the range and the direction (at 3% or more sales tax, Korea won all six at $200 off). An earlier draft had the direction reversed.
- Break-even exchange rates used in the post for the 256GB (section 4): ₩1,199.0 at list price and ₩1,423.8 at $300 off; all six models' $300-off break-evens (₩1,406.2 to ₩1,438.3) sit above, and all list break-evens (₩1,199.0 to ₩1,278.4) below, the ₩1,343.3 rate of 2026-11-11.

Article: [Galaxy Z Fold 8 Korea Price vs US (Nov 2026): Still Cheaper?](https://loopnotes.dev/galaxy-z-fold-8-korea-price/)
