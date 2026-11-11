# What does GTA 6 cost in Korea in US dollars, why is it cheaper, and can a buyer outside Korea use a Korean copy?

Research note for the loopnotes.dev article "GTA 6 Korea price" (https://loopnotes.dev/gta-6-korea-price/). Built 2026-11-11 and extended the same day with the tax basis, the Korean Xbox Store route, the Korean box price, shipping costs and code expiry (sections 5–9). Every number below comes from the files in this folder or the linked pages, read on the dates given.

## Conclusions

1. The "$58" that English price lists give for Korea is the 2026-06-24 exchange rate; on 2026-11-10 the same ₩89,800 was $67.06, so the saving against the US $79.99 is about $13 (16%), not $22 (28%), and about $11 after a 3% card fee, which is the number a buyer abroad should weigh.
2. Korea is cheaper partly on paper and partly by a low won price: ₩89,800 already includes 10% VAT (about $61 before tax on 2026-11-10) while the US $79.99 is before sales tax, and $79.99 at the June rate would have been about ₩123,700, yet the won price sits inside the ₩88,000–95,000 band Korean gamers know for $70 games; there is no hidden Korea discount left for a buyer abroad to chase.
3. A Korean PS5 copy, digital or boxed, works only on a Korea-region PSN account, whose country is fixed at creation and which may refuse a card billed abroad, so a PS5 owner outside Korea should buy at home.
4. The Korean Xbox Store charges the same ₩89,800, but buying there means switching a Microsoft account to Korea, which Microsoft blocks within three months of the last switch, may leave items unusable in another region, does not carry the balance over and advises only for a long move, so an Xbox owner abroad should not use the Korean store.
5. The Korean Xbox box lists at ₩89,800, the same as digital, and its code is not region locked, but posting the box from Korea to the US costs ₩23,500–39,000 ($17.55–29.13), more than the ~$11 left, so the route pays only when someone in Korea sends just the 25-character code or hands the box over.
6. Only Japanese PS5 box codes expire (170 days after launch); no Korean code expiry was reported, and the "2027-03-31" date going around in Korea is the GTA+ claim deadline, so a Korean code carries no known redemption deadline.

## 1. ₩89,800 in US dollars, June 22 to November 10, 2026

**How it was made.** ECB reference rates for USD→KRW for every ECB business day from 2026-06-22 to 2026-11-10 (102 days), fetched on 2026-11-11 from the Frankfurter API: https://api.frankfurter.dev/v1/2026-06-22..2026-11-10?from=USD&to=KRW. Raw response: `fx-usd-krw-raw.json`. Each day's rate converts the two Korean list prices (₩89,800 Standard, ₩112,800 Ultimate) into dollars and compares the Standard price with the US list price of $79.99. Full table: `fx-usd-krw-2026-06-22_2026-11-10.csv`. The chart in the article is drawn from that CSV by `draw_chart.py` (matplotlib).

**Selected dates from the CSV**

| Date | ₩ per $1 | ₩89,800 in $ | ₩112,800 in $ | Standard below US $79.99 |
|---|---|---|---|---|
| 2026-06-22 (first day of the series) | 1,537.08 | 58.42 | 73.39 | 27.0% |
| 2026-06-24 | 1,546.43 | 58.07 | 72.94 | 27.4% |
| 2026-07-01 (lowest dollar value) | 1,558.09 | 57.63 | 72.40 | 27.9% |
| 2026-07-15 | 1,492.17 | 60.18 | 75.59 | 24.8% |
| 2026-08-03 | 1,427.05 | 62.93 | 79.04 | 21.3% |
| 2026-08-14 | 1,411.27 | 63.63 | 79.93 | 20.5% |
| 2026-09-01 | 1,374.61 | 65.33 | 82.06 | 18.3% |
| 2026-09-15 | 1,359.15 | 66.07 | 82.99 | 17.4% |
| 2026-10-01 | 1,361.27 | 65.97 | 82.86 | 17.5% |
| 2026-10-15 | 1,345.90 | 66.72 | 83.81 | 16.6% |
| 2026-10-23 (highest dollar value) | 1,324.45 | 67.80 | 85.17 | 15.2% |
| 2026-11-02 | 1,342.90 | 66.87 | 84.00 | 16.4% |
| 2026-11-10 (last day of the series) | 1,339.00 | 67.06 | 84.24 | 16.2% |

**Calculations**
- Dollar gap, Standard: $79.99 − $57.63 = $22.36 on 2026-07-01; $79.99 − $67.06 = $12.93 on 2026-11-10.
- Dollar gap, Ultimate against the US $99.99: $27.59 on 2026-07-01; $15.75 on 2026-11-10.
- Card fee example: 3% of $67.06 ≈ $2.01, leaving about $10.92 of the $12.93 gap. 3% is an example rate for the arithmetic, not a survey of card fees.
- The $58.07 / $72.95 pair shown for Korea on gtaboom's price-by-country page (https://www.gtaboom.com/gta-6-price-by-country/) matches the 2026-06-24 rate to the cent on Standard (Ultimate $72.94 here; one cent of rounding). beebom's list (https://beebom.com/gta-6-global-prices-list/) gives "about $58". Neither page states a rate or a date.
- Single-day checks: https://api.frankfurter.dev/v1/2026-06-24?from=USD&to=KRW and https://api.frankfurter.dev/v1/2026-11-10?from=USD&to=KRW.

## 2. Official prices, read 2026-11-11

| Item | Value | Where read |
|---|---|---|
| PS Store KR, Standard / Ultimate | ₩89,800 / ₩112,800 | https://www.playstation.com/ko-kr/games/grand-theft-auto-vi/ |
| Xbox Store KR, Standard | ₩89,800 | Microsoft display catalog, market=KR, product 9P3H4968GRSM |
| Xbox Store KR, Ultimate | ₩112,800 | same, 9NNZSNHLR63L |
| Xbox Store KR, Ultimate Edition Upgrade | ₩23,000 (= ₩112,800 − ₩89,800) | same, 9PN4LLBR8RCH |
| US list, Standard / Ultimate | $79.99 / $99.99 | Rockstar Store prices as reported across November 2026 coverage; the store page itself was not fetched |
| PS5 Pro Korean list | ₩1,298,000 since 2026-05-01 (was ₩1,118,000) | Yonhap report (https://n.news.naver.com/mnews/article/001/0016045619); no later increase found in a 2026-11-11 search |
| Launch in Korea | 00:00 KST on 2026-11-19 (store header shows 2026/11/18 15:00 UTC) | PS Store KR page |

Xbox catalog query: https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds=9P3H4968GRSM,9NNZSNHLR63L,9PN4LLBR8RCH&market=KR&languages=ko-KR (02:31 UTC). Output kept in `xbox-kr-prices-2026-11-11.txt`.

The won price matches an existing price point: Mario Kart World also sells for ₩89,800 in Korea (GameMeca EN, https://www.gamemeca.com/en/view.php?gid=1776963).

## 3. Official-page checks, 2026-11-11 (about 02:30 UTC, fetched without login)

Full excerpts: `official-checks-2026-11-11.md`.

- **PS5 and PS5 Pro hardware pages** (https://www.playstation.com/ko-kr/ps5/, https://www.playstation.com/ko-kr/ps5/ps5-pro/): no KRW price on either; the FAQ sends buyers to online retailers. https://direct.playstation.com/ko-kr/buy-consoles returned HTTP 403. Result: no base PS5 Korean list price confirmed from Sony, so the article gives none.
- **PlayStation Blog, 2026-11-10** (https://blog.playstation.com/2026/11/10/pre-load-grand-theft-auto-vi-on-ps5-starting-today/): states that pre-load opened nine days early, launch rolls out at local midnight on November 19, a boxed code can be redeemed to pre-load, and PS5 Pro gets "improved clarity through PlayStation Spectral Super Resolution (PSSR) and ray-traced shadows". It contains no frame rate and no 212GB figure.
- **30fps target**: Rockstar's Rob Nelson in interviews, reported by Push Square (2026-08, https://www.pushsquare.com/news/2026/08/gta-6-targeting-30fps-on-ps5-undecided-on-performance-mode) and VGC (https://www.videogameschronicle.com/news/gta-6-is-confirmed-to-be-30-frames-per-second-at-launch-no-performance-mode-at-launch/). Both pages returned HTTP 403 on a later fetch, so the article cites Inven Global (2026-08-28, https://labs.invenglobal.com/articles/25336/gta-6-console-version-currently-runs-at-30fps-60fps-mode-unconfirmed), read in full: Rob Nelson, head of development and co-studio head at Rockstar North, says console builds run at 30fps and a 60fps mode is for the technical team to confirm. VGC's headline ("no performance mode at launch") is stronger than that and is not used. What it shows: a PS5 Pro bought for GTA 6 buys image quality, not frames.
- **Storage**: the PS Store KR product page says at least 212GB.
- **PS Store KR card rules** (https://www.playstation.com/ko-kr/support/store/ps-store-credit-debit-card-problems/): a card whose registered address does not match the store's country may not link; if no local card is available, another payment method or a PlayStation Store wallet top-up code can be used. Accepted methods: https://www.playstation.com/ko-kr/support/store/payment-methods-accepted-on-ps-store/. No official page was found saying a new Korean account needs Korean phone verification, so the article does not state that as a rule.
- **Rockstar Support, "Platforms, Editions, and Versions"** (https://support.rockstargames.com/articles/4QfG4FmZCf5W1gS8jy4UVT/grand-theft-auto-vi-platform-editions-and-versions): timed out three times (40 s each). Its content (updated 2026-11-04) is cited through Notebookcheck (https://www.notebookcheck.net/Rockstar-confirms-GTA-6-PS5-codes-are-region-locked-Xbox-players-unaffected.1353053.0.html) and PCGuide (https://www.pcguide.com/news/rockstar-confirms-gta-6-is-region-locked-on-ps5-even-if-you-buy-physical-because-you-only-get-a-download-code/): PS5 codes must match the account's region, South Korea is its own redemption group, Xbox codes are not region locked. Boxes reach Korean stores on 2026-11-12 with a code only; there is no boxed Ultimate.
- **PSN account country**: fixed at account creation, with cards and wallet tied to it (PSN Terms of Service, https://www.playstation.com/en-us/legal/psn-terms-of-service/).
- **Box vs digital**: GTA+ one month is for digital purchases, claim by 2027-03-31, auto-renews (PS Store KR page). Physical preorders get the Vintage Vice City Pack while stocks last (hothardware, https://hothardware.com/news/gta-6-preorder-guide-read-carefully-before-buying; TheSixthAxis, https://www.thesixthaxis.com/2026/06/24/gta-6-ultimate-edition-pre-order-bonus-and-vintage-vice-city-pack-revealed/). The box holds a Standard code only.

## 4. Naver searches, first round, 2026-11-11

All searches through the Naver Search API, first 25–30 results per type (blog, cafe article, Knowledge iN, news). These are other people's posts; nothing in them was verified by us. Cafe articles show no date in search results.

| Search term (Korean) | Meaning | Sort | Results (blog / cafe / kin / news) | On topic |
|---|---|---|---|---|
| GTA6 웰컴백 쿠폰 | "GTA6 welcome-back coupon" | relevance | 11 / 14 / 0 / 0 | 8 purchase reports, table below |
| GTA6 패키지 쿠팡 | "GTA6 box Coupang" | relevance | 92 / 76 / 7 / 3 | same coupon threads, box-vs-digital questions |
| GTA6 지역락 코드 | "GTA6 region-lock code" | relevance | 8 / 9 / 1 / 0 | 2 |
| 외국인 PSN 한국 계정 GTA6 | "foreigner PSN Korean account GTA6" | relevance | 6 / 2 / 2 / 0 | 0 |
| GTA6 사전 다운로드 | "GTA6 pre-download" | date | 1,477 / 347 / 39 / 246 | pre-load reports, table below |
| GTA6 다운로드 시간 | "GTA6 download time" | date | 2,544 / 649 / 507 / – | pre-load reports |
| PS5 프로 GTA6 30프레임 | "PS5 Pro GTA6 30 frames" | date | 1,922 / 6,176 / 9 / 11 | reactions to the 30fps reports |
| GTA6 패키지 가격 코드 | "GTA6 box price code" | date | 121,496 / 44,401 / 27 / 136 | broad, background only |

**Coupang coupon purchase reports (N=8, boxed PS5/Xbox code, 2026-10-06 to 2026-11-11)**

What it shows (for residents of Korea; not used in the article, whose reader is outside Korea): people with Korean Coupang accounts paid ₩32,800–53,800 for the boxed code through coupons that went mostly to accounts with no recent purchases, against the ₩89,800 list.

| Post | Date | What the poster reports |
|---|---|---|
| [cafe ps3friend 2356204](https://cafe.naver.com/ps3friend/2356204) | not shown | paid ₩32,800; account unused for years |
| [cafe ps3friend 2355770](https://cafe.naver.com/ps3friend/2355770) | not shown | ₩38,800 + ₩3,000 shipping + ₩7,890 Wow membership = ₩49,690 |
| [blog didcjddns](https://blog.naver.com/didcjddns/224472386996) | 2026-11-11 | ₩39,000 welcome-back coupon, ₩50,800, ₩53,800 with shipping |
| [blog kimsm8064](https://blog.naver.com/kimsm8064/224458513530) | 2026-10-30 | welcome-back + Wow coupons, ₩55,000 off |
| [cafe ps3friend 2355684](https://cafe.naver.com/ps3friend/2355684) | not shown | ₩30,000 coupon on a family member's new account |
| [cafe ps3friend 2356716](https://cafe.naver.com/ps3friend/2356716) | not shown | ₩36,000 coupon; box arrives on the 18th; plans the Ultimate upgrade separately |
| [cafe oldgamestravel 408553](https://cafe.naver.com/oldgamestravel/408553) | not shown | ₩10,000 coupon |
| [blog yookma](https://blog.naver.com/yookma/224432698786) | 2026-10-06 | welcome-back coupon, no amount |

Paid prices stated: ₩32,800, ₩49,690, ₩53,800, so the range is ₩32,800–53,800; coupon amounts stated run ₩10,000–55,000. One post describes the coupon as going irregularly to members with no purchases for a while (didcjddns). Counter-signal: "Coupang preorder seems over… only Xbox left" ([cafe ps3friend 2352421](https://cafe.naver.com/ps3friend/2352421), date not shown).

Box-vs-digital doubts in the same saves: [2356473](https://cafe.naver.com/ps3friend/2356473) (bought on PS Store, is the online market better?), [2349957](https://cafe.naver.com/ps3friend/2349957) (is GTA+ worth it, digital preorder vs code box), [2351829](https://cafe.naver.com/ps3friend/2351829) (cancel Ultimate for the box, is it just a code slip in an empty case?).

**Region-lock posts**
- [blog voodoo7, 2026-07-28](https://blog.naver.com/voodoo7/224360161133): summary of Rockstar's PS5 code regions; a country's PS5 codes work only on a PlayStation account registered in that country, and some versions' codes carry no region lock (the search snippet is cut before naming them).
- [cafe ps3friend 2356093](https://cafe.naver.com/ps3friend/2356093): someone buying the Korean box as a winter gift for in-laws in Italy asks whether it will download on an Italian account. By the rule in section 3: a PS5 code no, an Xbox code yes.
- The foreigner-side search returned nothing on topic: foreigners do not ask this on Naver; that side of the question comes from English autocomplete ("gta 6 region lock ps5", "gta 6 codes region locked", "gta 6 south korea psn").

**Pre-load reports from 2026-11-10 (official size "at least 212GB")**

| Post | Size shown | Time | Line |
|---|---|---|---|
| [cafe aenggo 16191](https://cafe.naver.com/aenggo/16191) | 209GB | about 1 hour, finished | 500Mbps, Wi-Fi |
| [cafe ps3friend 2356662](https://cafe.naver.com/ps3friend/2356662) | – | a little over 1 hour, finished | 1Gbps |
| [cafe ps3friend 2356605](https://cafe.naver.com/ps3friend/2356605) | about 210GB | about 1 h 30 min, on-screen estimate | 500Mbps |
| [cafe ps3friend 2356593](https://cafe.naver.com/ps3friend/2356593) | 210GB | 30–37 min remaining, on-screen | – |
| [cafe ps3friend 2356576](https://cafe.naver.com/ps3friend/2356576) | 210GB | 2 hours | – |
| [cafe ps3friend 2356574](https://cafe.naver.com/ps3friend/2356574) | – | about 2 h 5 min, on-screen | – |
| [cafe seboming 104134](https://cafe.naver.com/seboming/104134) | – | finished 2 h 5 min after start (title only) | – |

Screens showed 209–210GB, under the official 212GB; times ran from about half an hour to about two hours.

## 5. Why ₩89,800 sits under $79.99: tax basis and the won price tier (read 2026-11-11)

**Korean VAT is inside the price.**
- Rate: Value-Added Tax Act (부가가치세법, in force 2026-01-02), Article 30: "부가가치세의 세율은 10퍼센트로 한다." ("The VAT rate is 10 percent.") https://www.law.go.kr/법령/부가가치세법
- Inclusion: PlayStation Terms of Service (Korea) v13.0 (2026-04-23), end of Article 15: "스토어 내 표시되어 있는 가격은 부가세를 포함하여 표시되며 한국 내에서의 모든 거래는 한국 통화(원)로 표시됩니다." ("Prices shown in the store include VAT, and all transactions in Korea are shown in Korean won.") https://www.playstation.com/ko-kr/legal/psn-terms-of-service/
- Not used: the Price Labeling Guidelines (가격표시제 실시요령, Ministry of Trade, Industry and Energy notice 2025-51, https://www.law.go.kr/LSW/admRulLsInfoP.do?admRulId=33397) were read in full and contain no VAT wording. Microsoft Store KR terms of sale returned no body, so the VAT inclusion is cited to Sony's terms only (the Xbox KR price equals the PS KR price, section 2).

**US sales tax is outside the price.** Sales tax is set state by state and added at checkout, so $79.99 is a pre-tax list price. Two official examples in opposite directions:
- California CDTFA Special Notice L-1036 (https://cdtfa.ca.gov/formspubs/l1036.pdf): digital products become taxable from 2027-01-01, and "Digital video game products" are listed as not digital products for that rule.
- Washington DOR (https://dor.wa.gov/digitalproducts): sales or use tax applies to digital products however they are accessed (downloaded, streamed, subscription).

**Calculations [estimates]**
- ₩89,800 ÷ 1.1 = ₩81,636 before VAT → $60.97 at ₩1,339.0 (ECB, 2026-11-10); $52.79 at ₩1,546.43 (2026-06-24).
- $79.99 converted at the 2026-06-24 rate: 79.99 × 1,546.43 = ₩123,699; at the 2026-11-10 rate: ₩107,107. The Korean price is well under either, so the gap is not only exchange-rate drift.

**The won price tier.**
- Korean gamers read ₩89,800 as low: a cafe post on the price announcement notes that $70 games abroad had usually sold in Korea for ₩88,000–95,000 and calls this price unusual ([cafe enff 9654](https://cafe.naver.com/enff/9654), date not shown).
- Mario Kart World sells for the same ₩89,800 in Korea (GameMeca EN, section 2).
- No statement from Rockstar explaining the Korean price was found.

## 6. The Korean Xbox Store route: Microsoft's region rules (read 2026-11-11)

Microsoft Support, "Change your country or region in Microsoft Store", https://support.microsoft.com/en-us/help/4039267/microsoft-store-change-your-country-or-region:
- A change is blocked if the region was changed within the last three months.
- "items you get in one region might not work in another".
- "The funds in your Microsoft account will not move with you".
- The first purchase in the new region asks for billing information for that locale.
- Microsoft recommends changing region only when moving for a long time.

Gift cards generally have to match the account region (Microsoft Q&A, secondary; not relied on).

No region change was attempted and no Korean Xbox Store checkout screen was opened (both need a login and an account change).

Result: the Korean Xbox Store price (₩89,800, section 2) is reachable only through a Korea-region Microsoft account, which these rules make impractical for anyone not moving to Korea.

## 7. The Korean Xbox box: price, redeeming, shipping (read 2026-11-11)

**List price.**
- Danawa price comparison, "락스타 게임즈 GTA 6 (XBOX Series, 패키지코드)", https://m.danawa.com/product/product.html?code=122722936: lowest price ₩89,800; listed as a download product (code in box), Korean language, adults only, on pre-order; "11월 12일 사전 다운로드 가능(판매점별 11일부터 배송시작)" ("pre-download from November 12; shipping from the 11th depending on the seller"); pre-order bonus Vintage Vice City Pack. Seller-by-seller rows load by script and were not read, so no seller is named.
- A Coupang pre-order listing for the PS5 and Xbox Korean boxes at ₩89,800 ([blog eggvoe, 2026-10-01](https://blog.naver.com/eggvoe/224428100563)).
- Korean news repeating the domestic store price of ₩89,800 ([greened, 2026-11-05](https://www.greened.kr/news/articleView.html?idxno=353953)).
- Naver Shopping is not available through our Naver API access, so no shopping-search table was made.

**Redeeming an Xbox code.**
- Xbox, https://www.xbox.com/en-US/redeem: on the console, Xbox button → Store → View button → Redeem → enter the 25-character code → Next. "Just make sure you're signed in to the correct Microsoft account before you redeem your code." No region or country sentence on the page.
- Microsoft Support, "Redeem a gift card or code to your Microsoft account", https://support.microsoft.com/en-us/help/10604: on the web, redeem.microsoft.com. Its region sentences are only about what gift-card balance can buy; nothing says a game code must match the account region.
- Result: nothing contradicts Rockstar's "Xbox codes are not region locked" (section 3).

**Shipping the box from Korea to the United States** (Korea Post, 0.5 kg band, rates read 2026-11-11):

| Service | ₩ | $ at ₩1,339.0 | Source |
|---|---|---|---|
| EMS, merchandise | 39,000 | 29.13 | https://ems.epost.go.kr/front.EmsDeliveryDelivery02.postal ("EMS 요금표 · 비서류" tab) |
| International air parcel | 23,500 | 17.55 | https://ems.epost.go.kr/front.EmsDeliveryDelivery071.postal |

EMS documents rate (₩26,000) exists but does not apply to a game box. Either parcel rate is larger than the ~$11 left after a 3% card fee (section 1), before any pickup fee or handling at the US end. Sending only the code costs nothing to post.

## 8. Code expiry (read 2026-11-11)

- Japan only: Rockstar's Japanese support says Japanese PS5 box codes expire 170 days after launch (VGC, https://www.videogameschronicle.com/news/gta-6-download-codes-expire-only-170-days-after-launch-in-japan/; Push Square, https://www.pushsquare.com/news/2026/07/gta-6s-physical-ps5-download-codes-expire-after-just-170-days-in-japan). Xbox boxes in Japan and PSN digital purchases are not affected.
- Korea: no report of a Korean code expiry in the Naver search below. One blog explains that the "Korean code expires 2027-03-31" claim is the GTA+ one-month claim deadline ([blog sosiktong12, 2026-09-27](https://blog.naver.com/sosiktong12/224423880528)), which matches the PS Store KR page (section 3).

## 9. Naver searches, second round, 2026-11-11

Naver Search API, relevance sort, first 25 results per type. Other people's posts, not verified by us.

| Search term (Korean) | Meaning | Results (blog / cafe / kin / news) | What the on-topic posts say |
|---|---|---|---|
| GTA6 엑스박스 패키지 가격 | "GTA6 Xbox box price" | 548 / 335 / 86 / 62 | price posts repeat ₩89,800 / ₩112,800 for both platforms; none gives a different Xbox box list price; the ₩88,000–95,000 reading (section 5) |
| GTA6 패키지 코드 유효기간 | "GTA6 box code expiry" | 62 / 49 / 5 / 4 | six on-topic posts, all about Japan's 170-day rule (July 2026); the GTA+ deadline explanation (section 8) |
| GTA6 엑박 우회 구매 지역 | "GTA6 Xbox workaround purchase region" | 2 / 3 / 0 / – | both GTA blogs describe switching an Xbox console to New Zealand to start early ([khg4057](https://blog.naver.com/khg4057/224463818931), [maori_korokia](https://blog.naver.com/maori_korokia/224405221642)); none is about buying from the Korean Xbox Store |

Foreigners buying through the Korean Xbox Store is not a question asked on Naver; that side comes from English autocomplete ("gta 6 korea xbox", "gta 6 south korea xbox", "gta 6 xbox region", "why is gta 6 cheaper in south korea").

## Limits

- ECB reference rates are mid-market rates. A card issuer's rate and foreign-transaction fee add to every dollar figure here.
- The US $79.99 / $99.99 list prices come from consistent press reports, not from a fetch of Rockstar's store.
- Rockstar's own support page never loaded; the region-lock rule rests on two outlets quoting it.
- The VAT inclusion is cited to Sony's Korean terms; Microsoft's Korean terms of sale did not load.
- No PSN or Microsoft account region change was attempted, and no Korean store checkout was opened.
- Box sellers are not named: the Danawa seller rows did not load and Naver Shopping was not available.
- Shipping rates are Korea Post's 0.5 kg band to the US only; other countries and couriers were not checked.
- The Naver tables are self-reported posts, sampled from the first 25–30 results per type. Coupang coupons are per account and irregular, and the Coupang app itself was not checked (it needs a login), so the ₩32,800–53,800 range is what others paid, not a price anyone can count on.

## 10. Moved out of the article body (reader checks, 2026-11-11)

Cold readers (a gamer outside Korea who saw "Korea ≈ $58") found these facts proved the research but did not change a step, or belonged to a different reader (someone living in Korea), so the body carries only their conclusions or drops them. Kept here so nothing is lost.

- Exact conversions: ₩1,546.43 per dollar on 2026-06-24 → $58.07; ₩1,339.0 on 2026-11-10 → $67.06; gap to US $79.99 about $22 (28%) in early July → about $13 (16%). Full table in section 1.
- Price point: Mario Kart World also sells for ₩89,800 in Korea (section 2).
- Gift case: a Korean PlayStation forum user buying the Korean box for in-laws in Italy (section 4).
- 30fps source chain and PS5 Pro image-quality features (section 3); PS5 Pro list price ₩1,118,000 until 2026-05-01, ₩1,298,000 since (section 2).
- Launch moment cross-check: PS Store KR header shows 2026/11/18 03:00 PM UTC, which is 00:00 KST on 2026-11-19.
- GTA+ month: claim by 2027-03-31 (PS Store KR page).
- Language and rating: Korean is among 13 launch languages for text and subtitles (GTA BOOM, https://www.gtaboom.com/gta-6-is-getting-13-languages-at-launch-5ced); Korea's private Game Content Rating Board rated it 19+ (Inven Global, https://www.invenglobal.com/articles/27299/gta-6-rated-adults-only-in-south-korea-following-private-board-review).
- Ultimate contents named on the Rockstar Store: a '95 Grotti Cheetah, two revolvers, Vice City Styles outfits, Jason's safehouse vehicles.
- Ultimate upgrade on PS Store KR: shown as not purchasable ("구매할 수 없음") before launch; on Xbox Store KR ₩23,000 (section 2).
- Coupang coupon codes and pre-load times (section 4): questions of a reader living in Korea, not of this article's reader.
- Wow membership fee ₩7,890 a month: as stated in one buyer's tally (cafe ps3friend 2355770, section 4), not checked on Coupang.

## 11. The Xbox box route for a buyer abroad: language, Ultimate, paying a friend back (read 2026-11-11)

Added after a cold reader (an Xbox owner outside Korea) asked what the Korean code gives them and what the one working route costs end to end.

**Same package in both stores.** Microsoft's display catalog (public API, fetched 2026-11-11 04:00 UTC; output in `xbox-catalog-us-kr-2026-11-11.txt`) returns the same product IDs for the Korean and US markets: GTA 6 9P3H4968GRSM bundles the base-game package 9NL3WWNZLZZN and the Vintage Vice City Pack 9PLVSSH8849X. The base package is identical in both markets: platform Windows.Xbox, console generation ConsoleGen9 (Xbox Series X|S), 225,336,918,016 bytes, and the same language list of 34 locale tags, English locales first, Korean among them. The catalog does not split languages into audio, interface and subtitles; GTA BOOM's 13-language list (section 10) is for text and subtitles according to a Rockstar localisation job ad it cites, and says nothing on voice. Result: a Korean code unlocks the same Xbox package a US buyer gets; audio and subtitle detail is whatever the buyer's own store page shows.

**Prices and tax basis, same catalog.** US: $79.99 Standard, $99.99 Ultimate, $20.00 Ultimate Edition Upgrade (9PN4LLBR8RCH), all `TaxesNotIncluded`. Korea: ₩89,800, ₩112,800, ₩23,000, all `VatIncluded`. This is Microsoft's own confirmation of the tax basis described in section 5 (until now cited to Sony's Korean terms only) and of the US list prices (section 2 relied on press reports).

**Ultimate in dollars.** ₩112,800 ÷ ₩1,339.0 (ECB, 2026-11-10) = $84.24, $15.75 under the US $99.99 (section 1 already had the gap).

**No boxed Ultimate.** GamingBolt, 2026-11-05 (https://gamingbolt.com/gta-6-standard-edition-supports-ultimate-edition-upgrade-even-for-physical-copies): "There is no physical copy of the Ultimate Edition"; Standard owners, physical included, can buy the digital Ultimate Edition Upgrade on the console store (attributed to Rockstar, not quoted). Rockstar's own page timed out again (WebFetch, 60 s, twice). The Danawa Korean Xbox listing (section 7) is the Standard box.

**Paying a friend in Korea back.** Wise's public price endpoint (the one behind https://wise.com/us/send-money/send-money-to-south-korea), read 2026-11-11 04:01 UTC for ₩89,800 landing in a Korean bank account (raw: `wise-quote-usd-krw-89800-2026-11-11.json`; mid rate ₩1,335.85):

| Paid with | You pay | Fee | Left of the US $79.99 |
|---|---|---|---|
| US debit card | $70.62 | $3.40 | $9.37 |
| ACH direct debit | $69.89 | $2.67 | $10.10 |
| Credit card (Visa/Mastercard) | $73.50–74.20 | $6.28–6.98 | $5.79–6.49 |
| Wire into Wise (SWIFT) | $75.89 | $8.67 | $4.10 |

Before US sales tax on the home purchase, which varies by state (section 5). Other countries and other transfer services were not checked. A friend in Korea pays the shop in won on a Korean card, so no card fee applies on that side.

**Redeem, pre-download, errors.** Pre-download for the Korean Xbox box: November 12 on the Danawa listing (section 7). Xbox Support's code-error pages render by script and returned no body to curl or WebFetch, so no official error wording is quoted; the article tells the reader to check the code against the photo and take the error to Xbox Support, resting on Rockstar's "Xbox codes are not region locked" (section 3).

**Moved out of the body in this round (reader check r1, round 4).** The author's own reading of the price ("I'd expected GTA 6 to go past ₩100,000. It landed on the sum I'd paid at a shop counter in August for Mario Kart World, bought along with my Switch 2", author interview); the PSN purchase week (June 24 rate "the week I paid ₩89,800 on PSN", author interview); the ₩123,700 counterfactual (section 5; the body says "over ₩120,000"); the ₩88,000–95,000 band Korean gamers cited (section 5); the 0.5 kg EMS rate ₩39,000 / $29 (section 7); the 170-day Japan figure (section 8, the body keeps the rule without the number); the $22 early-July gap (section 1, the chart shows it).
