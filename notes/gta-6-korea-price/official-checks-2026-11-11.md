# Official-page checks, 2026-11-11 (UTC ~02:30)

Fetched with curl (no login). Excerpts are verbatim from the page text.

## 1. Xbox Store KR prices
See `xbox-kr-prices-2026-11-11.txt` (Microsoft display catalog, market=KR):
- Grand Theft Auto VI (9P3H4968GRSM): ₩89,800
- Grand Theft Auto VI: Ultimate Edition (9NNZSNHLR63L): ₩112,800
- Ultimate Edition Upgrade (9PN4LLBR8RCH): ₩23,000
Same as PS Store KR (₩89,800 / ₩112,800); upgrade = ₩112,800 − ₩89,800.

## 2. PS5 / PS5 Pro list price on playstation.com/ko-kr
- https://www.playstation.com/ko-kr/ps5/ and /ko-kr/ps5/ps5-pro/: no KRW price on either page. The PS5 FAQ says: "구매 가능 여부 및 가격 세부 정보는 온라인 소매점에서 확인하세요."
- https://direct.playstation.com/ko-kr/buy-consoles: HTTP 403.
- Result: base PS5 Korean list price NOT confirmed from an official Sony page. Do not use ₩948,000 (GameMeca zh only). PS5 Pro ₩1,298,000 stays on Yonhap.

## 3. ECB series
See `fx-usd-krw-2026-06-22_2026-11-10.csv` (102 ECB business days, from `fx-usd-krw-raw.json`,
https://api.frankfurter.dev/v1/2026-06-22..2026-11-10?from=USD&to=KRW). Chart: `draw_chart.py` →
content/images/gta-6-korea-price-reactions/gta-6-korea-price-usd-jun-nov-2026.png

| date | ₩/USD | ₩89,800 in USD | ₩112,800 in USD | gap vs US $79.99 |
|---|---|---|---|---|
| 2026-06-24 | 1546.43 | 58.07 | 72.94 | 27.4% |
| 2026-06-25 (author's purchase day) | 1542.92 | 58.20 | 73.11 | 27.2% |
| 2026-07-01 (lowest USD value) | 1558.09 | 57.63 | 72.40 | 27.9% |
| 2026-10-23 (highest USD value) | 1324.45 | 67.80 | 85.17 | 15.2% |
| 2026-11-10 | 1339.00 | 67.06 | 84.24 | 16.2% |

## 4. Rockstar Support "Platforms, Editions, and Versions"
https://support.rockstargames.com/articles/4QfG4FmZCf5W1gS8jy4UVT/... — curl timeout (HTTP 000, 40 s), third failure. Keep Notebookcheck / PCGuide as cited secondary sources.

## 5. PlayStation Blog 2026-11-10 ("Pre-load Grand Theft Auto VI on PS5 starting today")
https://blog.playstation.com/2026/11/10/pre-load-grand-theft-auto-vi-on-ps5-starting-today/ — HTTP 200.
- States: pre-load open "nine days early"; "rolling midnight launch by country ... as respective countries hit midnight on November 19"; code-in-box buyers can activate the code to pre-load; PS5 Pro: "improved clarity through PlayStation Spectral Super Resolution (PSSR) and ray-traced shadows".
- Does NOT state: any frame rate (no "30fps"/"fps"/"frame"), nor the 212GB size.
- Correction for research/outline: "30fps on both" must not be attributed to PS Blog. Source for the 30fps target is Rockstar's Rob Nelson in interviews, reported by Push Square (2026-08, https://www.pushsquare.com/news/2026/08/gta-6-targeting-30fps-on-ps5-undecided-on-performance-mode) and VGC (https://www.videogameschronicle.com/news/gta-6-is-confirmed-to-be-30-frames-per-second-at-launch-no-performance-mode-at-launch/); a 60fps mode is unconfirmed, not ruled out. 212GB stays on the PS KR product page.

## 6. PS Store KR card rules (for the author's card scene)
https://www.playstation.com/ko-kr/support/store/ps-store-credit-debit-card-problems/ — verbatim:
"신용카드 또는 체크카드가 등록된 주소가 PlayStation Store 지역에 해당하는 국가/지역과 일치하지 않는 경우 연결되지 않을 수 있습니다. ... PlayStation Store 지역에 해당하는 국가/지역의 카드를 사용할 수 없는 경우 다른 결제 방법 또는 PlayStation Store 지갑 충전 코드를 사용하여 PlayStation Store에서 구매할 수 있습니다."
- Consistent with the scene (foreign card would not link). Correction: it is not impossible officially; a KRW wallet top-up code is Sony's stated alternative. Phone ID verification for a new KR account: no official page found → do not state it as a rule; keep only as what the colleague lacked, or drop.
- Accepted methods page: https://www.playstation.com/ko-kr/support/store/payment-methods-accepted-on-ps-store/

## 7. 30fps scope (gate recheck, 2026-11-11)
- Push Square and VGC originals return HTTP 403 to our fetch. Secondary reports read instead: Gfinity (2026-08-28): Rockstar North co-director Rob Nelson told YouTuber Davy Jones the game is developed at 30fps "on the consoles" and that a 60fps mode "at launch or later" depends on the technical team; tech-insider.org (2026-10): Rockstar has not named the PS5 Pro as an exception and no performance mode is confirmed; a final 30fps lock on Pro is not officially confirmed.
- Result for the article: "30fps on the consoles, 60fps mode undecided" holds; "both consoles" (implying PS5 and Pro by name) is not confirmed and was removed. The Pro judgment rests on the PS Blog Pro list (PSSR + ray-traced shadows, no frame-rate line).

## 8. VAT: Korean store prices include 10% VAT (round 4 experiment 1, 2026-11-11)
(a) Rate. 국가법령정보센터, 부가가치세법 [시행 2026. 1. 2.] [법률 제21065호], https://www.law.go.kr/법령/부가가치세법 — 제30조(세율) verbatim: "부가가치세의 세율은 10퍼센트로 한다."
(b) Inclusion on the store. PlayStation 서비스 이용약관 (한국) 버전 13.0 (2026년 4월 23일), https://www.playstation.com/ko-kr/legal/psn-terms-of-service/ — 제15조(청약철회) 끝, verbatim: "또한 스토어 내 표시되어 있는 가격은 부가세를 포함하여 표시되며 한국 내에서의 모든 거래는 한국 통화(원)로 표시됩니다."
- 가격표시제 실시요령 (산업통상자원부고시 제2025-51호, 시행 2025. 4. 7.), https://www.law.go.kr/LSW/admRulLsInfoP.do?admRulId=33397 — read in full: defines 판매가격 as "판매업자가 일반 소비자에게 판매하는 상품의 실제가격" (제2조 4호) but has no VAT wording. Not used as the inclusion source.
- Microsoft Store KR terms of sale: page returned no body to curl / WebFetch timed out. Not used; the Xbox KR price equals PS KR (§1), and the VAT claim is cited to Sony's terms only.
- Calculation [estimate]: ₩89,800 ÷ 1.1 = ₩81,636 before VAT → $60.97 at the ECB 2026-11-10 rate ₩1,339.0 (≈ $61); $52.79 at the 2026-06-24 rate ₩1,546.43.
(c) US side (one official source per direction; sales tax is state-by-state and added at checkout, so the US $79.99 is a pre-tax list price):
- California CDTFA Special Notice L-1036 "Sales and Use Tax Applies to Digital Products Beginning January 1, 2027", https://cdtfa.ca.gov/formspubs/l1036.pdf — under "What items are not digital products?": "Digital video game products".
- Washington DOR, https://dor.wa.gov/digitalproducts — sales or use tax applies to digital products regardless of how they are accessed (downloaded, streamed, subscription); DOR presentation lists games among digital goods.
- Result: H2-2 may say Korea's ₩89,800 includes 10% VAT (Sony terms) while the US $79.99 is before any state sales tax, which some states (Washington) charge on downloaded games and California excludes.

## 9. Redeeming an Xbox code (round 4 experiment 2, 2026-11-11)
- Xbox, https://www.xbox.com/en-US/redeem — console steps verbatim: "Press the XBOX button to open the guide, and then select Store." / "Press the View button to open the side menu, and then select Redeem." / "Enter the 25-character code, select Next, and then follow the prompts." Note: "Just make sure you're signed in to the correct Microsoft account before you redeem your code." No region or country sentence on the page.
- Microsoft Support, https://support.microsoft.com/en-us/help/10604 ("Redeem a gift card or code to your Microsoft account") — web flow: redeem.microsoft.com, sign in, "enter or paste the code or token value". Region sentences only about what gift-card balance can buy (e.g. hardware in Taiwan); no sentence that a game code must match the account region.
- Xbox Support redeem page (support.xbox.com/help/Subscriptions-Billing/redeem-codes-gifting/redeem-prepaid-codes) returned only a title to our fetch.
- Result: nothing contradicts Rockstar's "Xbox codes are not region-locked" (§4 via Notebookcheck). Codes redeemed on the wrong account cannot be moved, so the reader redeems on the account they play on.

## 10. Korean Xbox box price and where it is listed (round 4 experiment 3, 2026-11-11)
- Naver Shopping is not in our Naver API HUB (tools/naver.py note, 2026-10-19) → skipped. Used the Danawa price-comparison page instead (one fetch, no login).
- Danawa, https://m.danawa.com/product/product.html?code=122722936 — title "락스타 게임즈 GTA 6 (XBOX Series, 패키지코드) : 다나와 가격비교"; "최저가 89,800 원"; spec line "콘솔기종 : XBOX Series X / ... / 한국어 / 1인용 / 다운로드상품 / 청소년이용불가 / 예약판매중"; "11월 12일 사전 다운로드 가능(판매점별 11일부터 배송시작)"; 예약구매자 특전 "빈티지 바이스 시티팩". Store-by-store rows load by script and were not read.
- Matches the author's check (author interview): Coupang, 11st, SSG, emart mall showed no Xbox listing with seller + price; Danawa lowest ₩89,800, pre-order.
- Snapshot: content/00-index/naver-data/2026-11-11-gta-6-korea-price-reactions-xboxshop.md

## 11. Shipping the box abroad (round 4 experiment 4, 2026-11-11)
Korea Post EMS (ems.epost.go.kr), rates to the United States, 0.5 kg band:
- EMS 비서류 (merchandise): ₩39,000 — https://ems.epost.go.kr/front.EmsDeliveryDeliveryOz02.postal (POST paper=N, the JSON behind the "EMS 요금표 · 비서류" tab of https://ems.epost.go.kr/front.EmsDeliveryDelivery02.postal); EMS 서류 (documents) ₩26,000 for comparison, not applicable to a game box.
- 국제소포 항공일반소포 (air parcel): ₩23,500 — https://ems.epost.go.kr/front.EmsDeliveryDelivery071.postal
- At ₩1,339.0 per USD (ECB 2026-11-10): EMS $29.13, air parcel $17.55. Either is more than the ~$11 left after a 3% card fee (§README calc), before any EMS 방문수수료 or US-side handling.
- Result: shipping the box erases the saving; sending only the 25-character code keeps it (author's own choice, author interview).
