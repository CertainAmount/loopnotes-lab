# Mac mini M6 32GB or M5 Pro for development: does the work fit in 32GB, and what is the real price gap?

Research note for the loopnotes.dev post "Mac mini M6 vs M5 Pro for Developers: Is 32GB Enough?". First compiled 2026-11-12, revised 2026-11-26.

## Conclusions

1. On a 32GB Mac mini M6 running the same IDE, database containers and browser, one coding agent already brings Memory Used to the 24GB line (23–25GB), and an ordinary day with two agents sits at 26–28GB, so a developer who runs agents should drop the 24GB base M5 Pro whatever its core count.
2. The heaviest day recorded, three agents in separate worktrees plus five containers, peaked in the low 30s of GB with about 2GB of swap, a few minutes of yellow pressure and no failed build or test, so a buyer whose load looks like this can treat 32GB as enough and spend nothing more.
3. At that peak the CPU load was 50–70% while memory was at its ceiling, and builds slowed rather than failed, so for parallel agent work memory should be chosen before the CPU tier.
4. The M5 Pro has no 32GB option (24GB, then 48GB, then 64GB), so someone who needs more than 24GB is choosing between the M6 32GB and the M5 Pro 48GB, which are $800 apart at both 512GB ($1,499 vs $2,299) and 1TB ($1,799 vs $2,599): that is the gap to price, not the $800 between the two starting prices.
5. The $1,799 32GB/1TB M6 lands next to the $1,699 base M5 Pro (and ₩3,029,000 vs ₩2,990,000 in Korea) because of the extra 512GB of storage, so a buyer should match storage before comparing the two machines.
6. Apple is reported to be skipping an M6 Pro, with M7 Pro chips reported for the second half of 2027, so waiting for a cheaper higher-memory chip is not a 2026 option.

## Question

A developer is choosing between a Mac mini M6 maxed at 32GB and a Mac mini M5 Pro starting at 24GB. Memory can't be added after checkout. Does an IDE + containers + coding-agents workload fit in 24GB or 32GB, and once that is known, which two configurations should be priced against each other?

## Evidence

### 1. Memory readings on a 32GB Mac mini M6 (author's machine, Oct–Nov 2026)

Machine: Mac mini M6, 32GB unified memory, 1TB SSD, bought September 2026. Readings are Activity Monitor → Memory → **Memory Used** (not App Memory), read by eye from the live window, with Swap Used and the memory pressure colour noted at the same moment. Nothing was logged automatically and no screenshots were kept, so each value is a range.

Base set in every row: IntelliJ with a Spring Boot/Gradle project of 15–20 modules, PostgreSQL and Redis in OrbStack, Chrome, several terminals. Agents are Claude Code/Codex-type CLI agents (the models run in the cloud, not locally).

| Load on top of the base set | Memory Used | Swap / pressure | Figure 1 bar |
|---|---|---|---|
| No agents | 21–23GB | none / green | "No agents" |
| One agent | 23–25GB | none / green | "1 agent" (accent) |
| Two agents (an ordinary day) | 26–28GB | under 1GB / green | not drawn (sits between bars 2 and 3) |
| Three agents | 27–29GB | — | "3 agents" |
| Three agents in separate git worktrees + five OrbStack containers (limit raised from 8GB to 12GB), ~20 Chrome tabs, integration tests; afternoon of 2026-11-10 | low 30s (drawn 30–32) | about 2GB / yellow, back to green about 5 minutes after the tests ended | "+5 containers" |

What each agent adds: about 2–3GB per agent, of which the agent process itself is around 1GB; the rest is the Gradle daemon and test JVMs the agent starts when it runs `gradle test`. When the third agent ran its first test in a fresh worktree, the memory graph stepped up 3–4GB and crossed 28GB.

At the 2026-11-10 peak the CPU load was 50–70%, not pinned; the top CPU processes were several `java` processes (Gradle test workers), OrbStack Helper, `node` (agents) and Chrome renderer helpers. CPU fell below 20% after the tests ended. The symptom the author noticed was a window switch lagging by a beat about ten minutes into the tests, with swap and yellow pressure at that moment.

Other recorded points on the same machine:
- Highest swap seen: about 3GB, on the worst October day, when a 7–8B 4-bit local model was briefly loaded on top of the work. Memory Used has not been seen above 32GB (it can't exceed installed RAM; see section 7).
- A second yellow episode on 2026-11-19 (three agents plus an integration test): low 30s, swap about 2GB, green again within 5 minutes.
- Swap did not shrink when pressure went back to green; on 2026-11-10 it stayed until the author logged off, so a Swap Used reading late in the day reflects the day's peak, not the current load.
- The author's own line on 32GB for closing one agent: yellow pressure lasting more than 20 minutes, or Swap Used past 4GB. Neither has happened yet: yellow has always cleared within about 5 minutes of the tests ending and the highest swap was about 3GB. The article gives this line to the reader as the difference between touching 32GB and outgrowing it.
- Incremental build and test with a warm Gradle daemon and cache: 40–50 s with one agent or none, 60–80 s with three agents running, never above 90 s, no failures (1.2–1.7×). Not a controlled benchmark: one project, no clean builds, no M1 baseline.

Figure 1 in the article plots rows 1, 2, 4 and 5 as ranges against two reference lines: 24GB (M5 Pro base) and 32GB (M6 maximum). Spec (viz engine `range` frame):

```json
{
  "frame": "range",
  "points": [
    {"label": "No agents", "lo": 21, "hi": 23, "text": "21–23"},
    {"label": "1 agent", "lo": 23, "hi": 25, "text": "23–25", "hi_light": true},
    {"label": "3 agents", "lo": 27, "hi": 29, "text": "27–29"},
    {"label": "+5 containers", "lo": 30, "hi": 32, "text": "~2GB swap"}
  ],
  "ylim": [16, 36],
  "yticks": [16, 24, 32],
  "suffix": "GB",
  "ylabel": "Memory Used",
  "hlines": [
    {"y": 24, "label": "M5 Pro base"},
    {"y": 32, "label": "M6 max"}
  ],
  "note": "Mac mini M6 32GB, Activity Monitor, read by eye, Oct–Nov 2026"
}
```

The top of the last bar is capped at 32 because Memory Used stops at installed RAM; past that point load shows up as swap.

Estimating a total on a 16GB or 24GB Mac (calculation from the rows above, used in the article's H3; added 2026-11-26 after reader verdict r2):
- Memory Used can't exceed installed RAM (section 7), so a reader on 16GB or 24GB adds up a total instead of reading it.
- Containers: with three agents, five OrbStack containers (limit 12GB) read low 30s against 27–29GB with the usual two (PostgreSQL, Redis), so several extra containers put this machine about 3GB higher. Same-day conditions also differed (integration tests, ~20 Chrome tabs), so this is a rough step, not a per-container value.
- Agents: 2–3GB each when the agent runs tests in its own Gradle daemon and test JVMs; the agent process itself is about 1GB.
- Four agents on the author's base: 21–23 + 4 × (2–3) = 29–35GB, centred in the low 30s. This is an estimate; the author runs two on an ordinary day and three on the heaviest.

### 2. Official specs compared (Apple, read 2026-11-12; specs re-checked 2026-11-26)

| Item | Mac mini M6 | Mac mini M5 Pro |
|---|---|---|
| CPU / GPU | 12-core CPU, 12-core GPU | 15-core CPU, 16-core GPU; or 18-core CPU, 20-core GPU |
| Memory options | 16GB, 24GB, 32GB | 24GB, 48GB, 64GB (no 32GB) |
| Memory bandwidth | 153GB/s (16GB); 170GB/s (24GB, 32GB) | 307GB/s |
| Max storage | 2TB | 8TB |
| Ports | Thunderbolt 4 x3 | Thunderbolt 5 x3 |
| US starting price | $899 | $1,699; 18-core preset $1,899 |
| Announced / on sale | 2026-08-25 / 2026-09-22 | same |

Apple Newsroom ties the M5 Pro's 64GB and 307GB/s to running larger local AI models and the M6's bandwidth to multitasking. The article uses bandwidth only for the reader whose reason is a local model. Ratio: 307 / 170 ≈ 1.8. For a model whose weights are read in full for every token, memory bandwidth divided by the weight-file size caps generation speed (method in the loopnotes guide https://loopnotes.dev/local-llm-hardware-what-to-buy/), so the same model's speed ceiling on the M5 Pro is about 1.8 times the 32GB M6's.

Sources:
- Apple Newsroom, 2026-08-25: https://www.apple.com/newsroom/2026/08/apple-unveils-a-more-powerful-mac-mini-featuring-the-all-new-m6-and-m5-pro/
- Apple Mac mini Tech Specs: https://www.apple.com/mac-mini/specs/
- Apple Store, Buy Mac mini (US), checked 2026-11-26: https://www.apple.com/shop/buy-mac/mac-mini. Six presets listed (M6 16/256, 16/512, 24/512, 32/1TB; M5 Pro 15-core 24/512; M5 Pro 18-core 64/1TB). Configured prices load dynamically and are not in the fetched page.

### 3. US configured prices: upgrade steps and calculation (read 2026-11-26)

Upgrade steps from Daring Fireball's configurations-and-pricing post (2026-08-25, read 2026-11-26): https://daringfireball.net/2026/08/configurations_and_pricing_for_new_mac_minis_and_mac_studios

| Chip | Memory steps | Storage steps |
|---|---|---|
| M6 (from $899, 16GB/256GB) | +$200 for 24GB, +$400 for 32GB | +$200 for 512GB, +$500 for 1TB, +$1,000 for 2TB |
| M5 Pro 15-core (from $1,699, 24GB/512GB) | +$600 for 48GB, +$1,000 for 64GB; no 32GB | +$300 for 1TB |

| Configuration | Calculation | Price | Retail listing (Abt, read 2026-11-12) |
|---|---|---|---|
| M6 24GB / 512GB | 899 + 200 + 200 | $1,299 | $1,299, MHQM4LL/A: https://www.abt.com/Apple-Mac-mini-Desktop-M6-Chip-24GB-Unified-Memory-512GB-SSD-in-Silver-MHQM4LLA/p/248221.html |
| M6 32GB / 512GB | 899 + 400 + 200 | $1,499 | $1,499, Z1UA0004B: https://www.abt.com/Apple-Mac-mini-Compact-Desktop-M6-32GB-RAM-512GB-SSD-in-Silver-Z1UA0004B/p/248234.html |
| M6 32GB / 1TB | 899 + 400 + 500 | $1,799 | $1,799, Z1UA0004C: https://www.abt.com/Apple-Mac-mini-Compact-Desktop-M6-32GB-Unified-Memory-1TB-SSD-in-Silver-Z1UA0004C/p/248236.html |
| M5 Pro 15-core 24GB / 512GB | base | $1,699 | — |
| M5 Pro 15-core 48GB / 512GB | 1,699 + 600 | $2,299 | $2,299, Z1UD0007G: https://www.abt.com/Apple-Mac-mini-Compact-Desktop-M5-Pro-48GB-Unified-Memory-512GB-SSD-in-Silver-Z1UD0007G/p/248229.html |
| M5 Pro 15-core 48GB / 1TB | 1,699 + 600 + 300 | $2,599 | calculated only |

Pairs that follow:
- Same storage, 512GB: M6 32GB $1,499 vs M5 Pro 24GB $1,699, 8GB more memory for $200 less.
- Next memory step past 32GB: M6 32GB vs M5 Pro 48GB, $800 apart at 512GB ($1,499 vs $2,299) and at 1TB ($1,799 vs $2,599).
- Mismatched storage: M6 32GB/1TB ($1,799) vs M5 Pro 24GB/512GB ($1,699), $100 apart; of the $500 between the M6 24GB/512GB and 32GB/1TB, $200 is memory and $300 is storage.

All are US list prices before education and retailer discounts.

### 4. Configured prices at Apple Korea (2026-10-10)

From the author's original Korean post (https://jjeongil.tistory.com/3578), read from Apple Korea's configuration page that day. These are list prices on the page, not an amount paid.

| Configuration | Price | Education |
|---|---|---|
| M6 base | ₩1,499,000 | ₩1,329,000 |
| M5 Pro base (24GB / 512GB) | ₩2,990,000 | ₩2,809,000 |
| M6 32GB / 1TB | ₩3,029,000 | ₩2,774,000 |

Breakdown: ₩1,499,000 + ₩680,000 (32GB) + ₩850,000 (1TB) = ₩3,029,000. Korea shows the same thing as the US: the 1TB M6 sits just above the base M5 Pro.

### 5. Korean web reports (Naver)

Other people's posts, not the author's experience. Sort: relevance; types: blog, cafe, Q&A.

| Search term | Date | Blog | Cafe | Q&A |
|---|---|---|---|---|
| 맥미니 M6 32GB M5 Pro 개발 (Mac mini M6 32GB M5 Pro development) | 2026-11-12 | 342 | 8 | 0 |
| 맥미니 M6 스왑 메모리 도커 (Mac mini M6 swap memory Docker) | 2026-11-12 | 6 | 0 | 0 |
| 맥미니 M5 Pro 48GB M6 32GB (Mac mini M5 Pro 48GB M6 32GB) | 2026-11-26 | 127 | 1,084 | 2 |

For the 2026-11-26 term, the first 25 blog results were read: about 9 of 25 say the M5 Pro has no 32GB option or that past 32GB the next step is 48GB/64GB; 2 of 25 note the ₩3,029,000 vs ₩2,990,000 inversion; 1 buyer picked 32GB because the M5 Pro 48GB build cost nearly twice as much; **0 of 25 report Memory Used or swap readings from a development workload**. The 25 sampled cafe results are almost all used-laptop buying ads and the 2 Q&A results are keyword-stuffed, so neither is counted.

Posts relevant to this question:
- https://blog.naver.com/tech_kong/224465482193 (2026-11-06): the M5 Pro Mac mini has no 32GB option; it goes 24GB to 48GB or 64GB.
- https://blog.naver.com/cattech-/224485578975 (2026-11-21): 48GB and 64GB only open on the M5 Pro.
- https://blog.naver.com/teambounce/224486171163 (2026-11-21): the M6 at ₩3,029,000 fully optioned passes the ₩2,990,000 base M5 Pro.
- https://blog.naver.com/techgyeol/224492768941 (2026-11-26): the M6 32GB/1TB is ₩39,000 above the base M5 Pro.
- https://blog.naver.com/trifan/224450375202 (2026-10-22): bought the M6 32GB because the M5 Pro 48GB build cost nearly twice as much.
- https://blog.naver.com/tiger_jim/224395535452 (2026-08-31): the same ₩39,000 inversion, noted at launch.
- https://blog.naver.com/zestgo/224392601136 (2026-08-28): 153GB/s for the 16GB M6, 170GB/s for 24GB and 32GB.
- https://blog.naver.com/sodong3504/224402747116 (2026-09-06): 24GB vs 32GB with browser tabs, Docker and an IDE; 24GB doesn't freeze but lags when switching apps.
- https://blog.naver.com/z4h1027/224453017719 (2026-10-25): an M4 24GB after a year with OrbStack running shows 4.4GB of swap.

### 6. What the top English results cover (read 2026-11-12 and 2026-11-26)

- TechRepublic, "Is the $800 Upgrade Worth It?": frames the choice as $800 between starting prices; the M5 Pro is "easier to justify when workloads regularly push beyond 32GB" (page returned 403; read from search snippets).
- MacRumors buyer's guide (2026-09-03): calls memory "the clearest dividing line"; starting prices only; no measurements.
- Engadget, "Why is the M5 Pro more expensive than the M6?" (2026-08-26, fetched 2026-11-26): about 600 words; starting prices only; doesn't note the missing 32GB step on the M5 Pro.
- EveryMac (2026-10-09), https://everymac.com/systems/apple/mac_mini/mac-mini-silicon-faq/differences-between-m5-pro-m6-mac-mini-2026.html: Geekbench single-core M6 about 9% faster, multi-core M5 Pro 36–52% faster; memory can't be upgraded later.
- MacRumors Forums, "Mac Mini M6 or M5 Pro for my use?" (2026-08-25), https://forums.macrumors.com/threads/mac-mini-m6-or-m5-pro-for-my-use.2487926/: the opening post frames the choice as M6 32GB/1TB vs M5 Pro 48GB/1TB, the same pair section 3 prices.

None compares configurations at matched storage in a table or shows Memory Used from a development workload.

### 7. How Activity Monitor reports memory (Apple Support, read 2026-11-12)

- "View memory usage in Activity Monitor on Mac": Physical Memory is the RAM installed; Memory Used is the RAM in use; Swap Used is space on the startup disk. Memory Used counts RAM only, so it can't exceed the installed amount; on a 16GB or 24GB Mac a heavier load shows up as Swap Used and pressure, not as a higher Memory Used. https://support.apple.com/guide/activity-monitor/view-memory-usage-actmntr1004/mac
- "Check if your Mac needs more RAM": green pressure means RAM is used efficiently, yellow means the Mac might eventually need more RAM, red means it needs more. https://support.apple.com/guide/activity-monitor/check-if-your-mac-needs-more-ram-actmntr34865/mac

### 8. Release timeline

- 2026-08-25: M6 and M5 Pro Mac mini announced; on sale 2026-09-22 (Apple Newsroom).
- 2026-06-25: MacRumors summary puts M7 Pro/Max Macs in the second half of 2027. https://www.macrumors.com/2026/06/25/2027-macs-m7-chips/
- 2026-07-12: MacRumors reports Apple is skipping the M6 Pro and M6 Max. https://www.macrumors.com/2026/07/12/why-apple-is-skipping-m6-pro-m6-max-chips/

Both are reports based on rumors, not Apple announcements.

## Limits

- The memory readings come from one machine, one project and one development setup, read by eye. Nothing was measured on an M6 16GB or 24GB or on any M5 Pro; the 24GB behaviour comes from where the readings sit against the 24GB line and from other people's reports, not from running the work on 24GB.
- Build times are incremental with a warm cache on one project and were not run as a controlled benchmark.
- No measurement was run on the machine that compiled this note (it has no Mac); the evidence here is the author's readings, public pages and calculations.
- US configured prices were not read from Apple's configurator, which loads them dynamically. They are calculated from Daring Fireball's upgrade steps and match Abt's listings of Apple's build-to-order parts, except the M5 Pro 48GB/1TB ($2,599), which is calculated only. Check Apple's configurator at checkout.
- M6 Pro / M7 Pro timing is rumor-based reporting.
- Naver counts are result totals for one search on one date and change over time; the 25-post readings are a sample of the first page, not the whole result set.

Article: [Mac mini M6 vs M5 Pro for Developers: Is 32GB Enough?](https://loopnotes.dev/mac-mini-m6-vs-m5-pro/)
