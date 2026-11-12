# Mac mini M6 32GB or M5 Pro 24GB for development?

Research note for the loopnotes.dev post "Mac mini M6 vs M5 Pro for developers". Compiled 2026-11-12.

## Conclusions

1. At the same 512GB of storage, the M6 32GB is $1,499 in the US against $1,699 for the 24GB/512GB M5 Pro: 8GB more memory for $200 less (US retail listings read 2026-11-12, section 2a). The 32GB/1TB M6 is $1,799, so of the $500 between the M6 24GB/512GB ($1,299) and 32GB/1TB, $200 is memory and $300 is storage. The reader is choosing 8GB more memory against a faster chip and Thunderbolt 5, not the $800 between starting prices.
2. A 32GB/1TB M6 lands next to the base M5 Pro in both the US ($1,799 vs $1,699) and Korea (₩3,029,000 vs ₩2,990,000) because of the extra 512GB of storage, not the memory. Match storage before comparing prices.
3. The M5 Pro has no 32GB step: its memory goes 24GB, then 48GB, then 64GB. A developer who needs about 30GB is choosing between the M6 32GB and an M5 Pro 48GB, not the base M5 Pro. The 15-core M5 Pro with 48GB/512GB is $2,299, $800 above the M6 32GB/512GB.
4. One real development set (IDE, containers, browser, one to three coding agents) reached nearly 30GB of Memory Used on a 32GB M6, and swap appeared. Korean users report the same pattern on 24GB machines: builds keep running and app switching gets slow. Before buying, read Memory Used, Swap Used and the pressure colour on your current Mac rather than going by core counts.
5. Apple is reported to be skipping an M6 Pro, with the next Pro chip reported for late 2027, so waiting is not a 2026 option.

## Question

A developer is choosing between a Mac mini M6 maxed at 32GB and a Mac mini M5 Pro starting at 24GB. Memory can't be added later. Which one should they buy, and how can they tell whether their work fits in 32GB?

## Evidence

### 1. Official specs compared (read 2026-11-12)

| Item | Mac mini M6 | Mac mini M5 Pro |
|---|---|---|
| CPU / GPU | 12-core CPU, 12-core GPU | 15-core CPU, 16-core GPU; or 18-core CPU, 20-core GPU |
| Memory options | 16GB, 24GB, 32GB | 24GB, 48GB, 64GB (no 32GB) |
| Memory bandwidth | 153GB/s (16GB); 170GB/s (24GB, 32GB) | 307GB/s |
| Max storage | 2TB | 8TB |
| Ports | Thunderbolt 4 x3 | Thunderbolt 5 x3 |
| US starting price | $899 ($799 education) | $1,699 ($1,599 education); 18-core preset $1,899 |
| Announced / on sale | 2026-08-25 / 2026-09-22 | same |

Sources:
- Apple Newsroom, 2026-08-25: https://www.apple.com/newsroom/2026/08/apple-unveils-a-more-powerful-mac-mini-featuring-the-all-new-m6-and-m5-pro/
- Apple Mac mini Tech Specs: https://www.apple.com/mac-mini/specs/
- Apple Store, Buy Mac mini (US): https://www.apple.com/shop/buy-mac/mac-mini. Presets listed: M6 16/256, 16/512, 24/512, 32/1TB; M5 Pro 15-core 24/512; M5 Pro 18-core 64/1TB. Prices on this page load dynamically and were not read here (see Limits).

### 2. Configured-price calculation (US, not used in the post)

Upgrade steps for the M6 as reported by secondary US sources (TechRepublic's M6 cheat sheet and aicybr): +$200 for 24GB, +$400 for 32GB, +$200 for 512GB, +$500 for 1TB.

| Configuration | Calculation | Price |
|---|---|---|
| M6 32GB / 512GB | $899 + $400 + $200 | about $1,499 (calculated) |
| M6 32GB / 1TB | $899 + $400 + $500 | $1,799 (matches the secondary sources' listed figure) |
| M5 Pro 24GB / 512GB | base | $1,699 |

Same storage (512GB): the calculation puts the M6 32GB about $200 below the M5 Pro 24GB. Apple's configurator was read on 2026-11-12 with curl and only returns the three starting prices ($899, $1,699, $1,899) in static HTML; configured prices load dynamically, so this figure stays unconfirmed and the post does not use it. Different storage (M6 at 1TB, M5 Pro at 512GB): the M6 is $100 more.

### 2a. US prices read from retail listings (2026-11-12, reader fix r1)

Apple's configurator still returns only starting prices in static HTML ($899, $1,699 for the 15-core M5 Pro, $1,899 for the 18-core M5 Pro, read 2026-11-12). The configured builds were read from Abt's listings of Apple's build-to-order models (Z1UA/Z1UD part numbers):

| Build | Part | Price | URL |
|---|---|---|---|
| M6 24GB / 512GB | MHQM4LL/A | $1,299 (also EveryMac, 2026-10-09) | https://www.abt.com/Apple-Mac-mini-Desktop-M6-Chip-24GB-Unified-Memory-512GB-SSD-in-Silver-MHQM4LLA/p/248221.html |
| M6 32GB / 512GB | Z1UA0004B | $1,499 | https://www.abt.com/Apple-Mac-mini-Compact-Desktop-M6-32GB-RAM-512GB-SSD-in-Silver-Z1UA0004B/p/248234.html |
| M6 32GB / 1TB | Z1UA0004C | $1,799 | https://www.abt.com/Apple-Mac-mini-Compact-Desktop-M6-32GB-Unified-Memory-1TB-SSD-in-Silver-Z1UA0004C/p/248236.html |
| M5 Pro 15-core, 48GB / 512GB | Z1UD0007G | $2,299 | https://www.abt.com/Apple-Mac-mini-Compact-Desktop-M5-Pro-48GB-Unified-Memory-512GB-SSD-in-Silver-Z1UD0007G/p/248229.html |

These match the secondary sources' upgrade steps in section 2 (+$400 for 32GB, +$200 for 512GB, +$500 for 1TB on the M6; +$600 for 24GB to 48GB on the M5 Pro, reported by Tom's Hardware via secondary coverage), so the section 2 calculation is now backed by listed prices.

Benchmarks (EveryMac, 2026-10-09, Geekbench): M6 about 9% ahead in single-core, M5 Pro 36–52% ahead in multi-core. The post keeps only the direction.

Bandwidth: Apple Newsroom (2026-08-25) ties the M5 Pro's 64GB and 307GB/s of memory bandwidth to running larger local AI models; the M6's up to 170GB/s is tied to multitasking. The post uses bandwidth only in the local-LLM case.

### 3. Configured prices at Apple Korea (2026-10-10)

From the author's original Korean post (https://jjeongil.tistory.com/3578), read from Apple Korea's configuration page that day:

| Configuration | Price | Education |
|---|---|---|
| M6 base | ₩1,499,000 | ₩1,329,000 |
| M5 Pro base (24GB / 512GB) | ₩2,990,000 | ₩2,809,000 |
| M6 32GB / 1TB | ₩3,029,000 | ₩2,774,000 |

Breakdown: ₩1,499,000 + ₩680,000 (32GB) + ₩850,000 (1TB) = ₩3,029,000. These are list prices on the configuration page, not an amount paid. Korea shows the same thing as the US: the 1TB M6 sits just above the base M5 Pro.

### 4. Memory readings on a 32GB M6 (from the author's original post, September 2026)

Setup: IntelliJ with a Spring Boot/Gradle project of 15–20 modules, PostgreSQL and Redis in OrbStack (about 8GB allotted), Chrome, several terminals, and one to three Claude Code/Codex-type agents. Readings are Activity Monitor → Memory → Memory Used (not App Memory).

| Load | Memory Used | Note |
|---|---|---|
| Light work | — | pressure green |
| IDE, containers, browser and agents all open | mid-to-high 20s GB | |
| Several agents and containers at once | near 30GB | swap appeared |

Under swap, builds did not stop or fail; switching projects, files and apps got slightly sluggish. Incremental build and test ran 40–50 s with a warm Gradle daemon and cache, and did not swing much with the other work running. With three agents running in parallel, memory rose across their processes before the CPU became the limit. The month of follow-up data on the same machine is in the separate post https://loopnotes.dev/mac-mini-m6-32gb-review/.

### 5. Korean web reports (Naver, searched 2026-11-12)

Other people's posts, not the author's experience. Sort: relevance; types: blog, cafe, Q&A.

| Search term | Blog | Cafe | Q&A |
|---|---|---|---|
| 맥미니 M6 32GB M5 Pro 개발 (Mac mini M6 32GB M5 Pro development) | 342 | 8 | 0 |
| 맥미니 M6 스왑 메모리 도커 (Mac mini M6 swap memory Docker) | 6 | 0 | 0 |

Most of the 25 sampled blog results for the first term are spec and price roundups. One is the author's own Korean post (excluded). The posts relevant to this question:

- https://blog.naver.com/tiger_jim/224395535452 (2026-08-31): notes the M6 32GB/1TB configuration costs ₩39,000 more than the base M5 Pro.
- https://blog.naver.com/tech_kong/224465482193 (2026-11-06): points out the M5 Pro Mac mini has no 32GB option.
- https://blog.naver.com/psister3/224473687421 (2026-11-12): explains why the newer-numbered M6 is cheaper than the M5 Pro (chip tiers).
- https://blog.naver.com/zestgo/224392601136 (2026-08-28): states 153GB/s for the 16GB M6 and 170GB/s for 24GB and 32GB.
- https://blog.naver.com/sodong3504/224402747116 (2026-09-06): 24GB vs 32GB with browser tabs, Docker and an IDE; 24GB does not freeze but lags when switching apps.
- https://blog.naver.com/z4h1027/224453017719 (2026-10-25): an M4 24GB after a year with OrbStack running reports 4.4GB of swap.
- https://cafe.naver.com/inmacbook/2763872: a developer weighing M5 Pro vs Max for AI-agent work.

### 6. Release timeline

- 2026-08-25: M6 and M5 Pro Mac mini announced; on sale 2026-09-22 (Apple Newsroom).
- 2026-07-12: MacRumors reports Apple is skipping the M6 Pro and M6 Max; the next high-end chip is the M7 Pro, reported for the end of 2027. This is a rumor-based report. https://www.macrumors.com/2026/07/12/why-apple-is-skipping-m6-pro-m6-max-chips/

### 7. What the top English results cover (read 2026-11-12)

- MacRumors buyer's guide (2026-09-03): calls memory the clearest dividing line; compares starting prices only; no measurements.
- EveryMac (2026-10-09), https://everymac.com/systems/apple/mac_mini/mac-mini-silicon-faq/differences-between-m5-pro-m6-mac-mini-2026.html: Geekbench 7 single-core M6 about 9% faster, multi-core M5 Pro 36–52% faster; RAM can't be upgraded later; preset prices not mapped to configurations.
- TechRepublic: frames the choice as an "$800 upgrade" (page returned 403; read from search snippets).

None compares configurations at matched storage or shows memory readings from a development workload.

### 8. How Activity Monitor reports memory (Apple Support, read 2026-11-12)

- "View memory usage in Activity Monitor on Mac": Physical Memory is "the amount of RAM installed"; Memory Used is "the amount of RAM being used"; Swap Used is space on the startup disk. Since Memory Used counts RAM only, it cannot exceed the installed amount, and a shortfall shows up as Swap Used and memory pressure. https://support.apple.com/guide/activity-monitor/view-memory-usage-actmntr1004/mac
- "Check if your Mac needs more RAM": green pressure means RAM is used efficiently, yellow means the Mac "might eventually need more RAM", red means it needs more. https://support.apple.com/guide/activity-monitor/check-if-your-mac-needs-more-ram-actmntr34865/mac

## Limits

- The US configured prices were not read from Apple's configurator; the page loads them dynamically. They come from Abt's US retail listings of Apple's build-to-order models (section 2a, read 2026-11-12), which agree with the secondary sources' upgrade steps. A retailer can change or discount a listing; check Apple's configurator at checkout.
- The memory readings come from one machine and one development setup. Nothing here was measured on an M6 16GB or 24GB or on any M5 Pro; the 24GB symptoms come from other people's reports.
- The 40–50 s build time is incremental with a warm cache on one project; there are no clean-build figures and no M1 baseline.
- Naver counts are result totals for one search on one date and change over time.

Article: [Mac mini M6 vs M5 Pro for Developers: Is 32GB Enough?](https://loopnotes.dev/mac-mini-m6-vs-m5-pro/)
