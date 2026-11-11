# What Genspark Code's own pages promise, leave out and charge for, before you trust a first build

Research note for the loopnotes.dev article "Genspark AI Developer review" (the product is now called Genspark Code). All evidence below was gathered on 2026-11-12. The round-by-round account of one build is the author's own story and lives in the article; this note holds what anyone can re-check: the official pages, the npm registry, the top English search results and two Korean web searches. Other people's posts are linked with at most a one-line summary.

## Conclusions

1. Genspark's help page sells Genspark Code as an autonomous agent that "plans, codes, tests, and deploys" across five project types, yet none of the three official pages mentions previewing a build at phone or tablet width or limiting a fix to one part of the page, so a reader checks desktop, tablet and phone widths themselves and writes the scope into every fix request.
2. No official page gives a credit cost per build or per fix, and the Credits Guide says each failed agent retry costs credits, so a reader cannot budget a finished page in advance and should cut the number of fix rounds rather than count on a fixed price.
3. The Free plan gives 100 credits a day up to a lifetime allowance with "limited access" to agents, while full access to Genspark Code starts at Plus ($24.99 a month, or $19.99 a month billed yearly, from 10,000 monthly credits), so a reader can look at a first build for free but should expect to need Plus to carry a fix loop to the end.
4. GenCode, published on npm on 2026-09-03, is a separate terminal coding agent, so a reader who searched "genspark code cli" is looking at a different product from the web builder this article reviews.
5. The top three English results and two Korean web searches describe speed, features and pricing but not what breaks after the first build (across the 100 Korean results read, 2 posts mention mobile breakage and none covers scoping a Genspark Code fix), so a reader should not take "built in minutes" claims as covering the mobile check and the fix rounds.

## 1. Official pages compared

Read in full on 2026-11-12. None of the three help-center pages showed an "updated" date on that day.

| # | Source | What it says that matters here | What it does not say |
|---|---|---|---|
| 1 | [Genspark Help Center: Genspark Code](https://www.genspark.ai/helpcenter/ai-developer) | Name "Genspark Code" (formerly AI Developer); "L4 autonomous AI coding agent"; "AI independently plans, codes, tests, and deploys"; project types Web, Mobile Apps, Game, E-commerce, Existing code. | Previewing at device widths; how to keep a fix to one part of the page; limits or credit cost per build. |
| 2 | [Genspark Help Center: Credits Guide](https://www.genspark.ai/helpcenter/credits-guide) | "Agent retries — each failed retry costs credits." (under What Compounds Your Costs). Free: 100 credits a day until the lifetime free allowance is used. Plus and Pro: credits renew monthly at the start of the billing cycle; a weekly Free Quota for Standard-mode agents (amount not stated). | Credits used by one Genspark Code build or one fix request. |
| 3 | [Genspark Help Center: Membership Plans](https://www.genspark.ai/helpcenter/membership-plans) | Free $0: "100 credits per day, up to a lifetime allowance of free credits", "Limited access to AI models and agents". Plus $24.99/month, or $19.99/month billed yearly ($239.99/year): "From 10,000 monthly credits", "Full access to AI Slides, Genspark Code, and more agents". Pro $249.99/month, or $199.99/month yearly ($2,399.99/year): from 125,000 monthly credits. Team $40/seat/month ($35 yearly), 10,000 credits per seat a month. Benefits "valid through June 30, 2027". | The size of the lifetime free allowance; Genspark Code is not named on the Free row; per-build cost. |
| 4 | [npm: @genspark/gencode](https://www.npmjs.com/package/@genspark/gencode) | "GenCode — Genspark's AI coding agent for the terminal: an interactive TUI and headless CLI…"; first published 2026-09-03; latest 1.19.3-gencode.6 (registry modified 2026-11-10). | Any link to the web builder's plans. Genspark's own GenCode page blocked automated reading, so only npm was checked. |

What the comparison concludes: the official pages promise an end-to-end agent and publish plan prices, but leave out the three things that decide whether a first build becomes a usable page: checking it at other widths, keeping a fix to one part, and what each round costs. Failed retries cost credits, so every extra fix round is paid for.

## 2. Top English search results

Searched "Genspark AI Developer review" on 2026-11-12.

| Rank | Result | One-line summary |
|---|---|---|
| 1 | [Trustpilot: genspark.ai](https://www.trustpilot.com/review/genspark.ai?page=1) | Platform-wide reviews; complaints that credits run out fast and support does not answer; no specific defects in Genspark Code output. |
| 2 | [salesdorado: review Genspark](https://salesdorado.com/en/ai/review-genspark/) | Features and pricing overview; no real build shown. |
| 3 | [hackmd: vicverdict](https://hackmd.io/@vicverdict/B1Z62quwZg) | Affiliate-style review; says it builds landing pages, internal tools and full apps; no failure case. |

Also on page one: [fast.io 2026 review](https://fast.io/resources/genspark-ai-review-2026/), [G2](https://www.g2.com/products/genspark-ai/reviews), The Neuron, Lindy, an intercom-hosted review. None shows a single build fixed round by round or a page checked at phone width.

## 3. Naver searches (Korean web)

Naver Search API, queried 2026-11-12, sorted by relevance. "Total" is Naver's hit count; we read the top 25 blog and top 25 cafe results for each term (kin had none).

| Search term (Korean) | Meaning | Total hits (blog / cafe / kin) | Read |
|---|---|---|---|
| 젠스파크 AI 개발자 모바일 | Genspark AI Developer mobile | 370 / 72 / 0 | 25 / 25 / 0 |
| 젠스파크 AI 개발자 수정 요청 | Genspark AI Developer fix request | 371 / 73 / 0 | 25 / 25 / 0 |

Posts in those results that touch mobile breakage or fix requests (judged from result snippets):

| Post | One-line summary |
|---|---|
| [cafe.naver.com/powerpoint/140102](https://cafe.naver.com/powerpoint/140102) | Email signature HTML built with Genspark's AI Developer; renders in Gmail but breaks in Naver Mail and on mobile. |
| [cafe.naver.com/orangeztmch/55](https://cafe.naver.com/orangeztmch/55) | A Google Apps Script project where Genspark only helped; lists "improve mobile responsive design" as a to-do and suggests naming the code location when asking for fixes, as a way to learn the code. |

The rest are how-to guides, pricing summaries, refund guides and course ads. With two loosely related posts, this sample is too thin to support a claim in the article; it only shows that Korean coverage also presents Genspark Code as "a website in minutes".

## Limits

- No build was run on this machine for this note: Genspark Code needs an account and credits.
- Plan prices are the help-center values on 2026-11-12; app-store prices may differ and were not checked.
- The Naver rows come from result snippets, not full reads of every post.
- Search rankings change; the top-three table reflects one search on one day.

Article: [Genspark AI Developer Review: What Broke on Mobile](https://loopnotes.dev/genspark-ai-developer-review/)
