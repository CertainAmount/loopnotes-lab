# Where do AI assistants already stop before they send email or pay, and what turns that stop off?

Research note for the loopnotes.dev article "AI agent access to email and payments" (https://loopnotes.dev/meta-muse-permissions-email-payments/). Compiled 2026-11-15.

## Conclusions

- In both products we could compare from official help pages (Meta Muse and OpenAI Dots), asking before an action that leaves your account, such as sending or buying, is already the default. The reader does not need to add approvals; the step that matters is leaving the one standing-permission option off for sending and paying (Muse's "Always allow", a Dots Custom Rule set to act without asking).
- Muse pays new merchants with a one-time card locked to one merchant, one amount and an expiry. That limits a leaked card number or an overcharge, but the card has no say over which item, how many, or whether a subscription went into the cart, so the reader's stop point stays at the cart, not at the card.
- On Muse, disconnecting a connector stops future actions but does not delete what was already read; resetting does. A reader leaving the product should know which of the two they pressed.
- Muse's mail connector filters one-time codes, password-reset links and magic links, and Meta itself says the design "isn't immune to attack"; a reported (and patched) Muse zero-day used permissions the user had already granted. A good security design is a reason to trust where credentials are kept, not a reason to widen what the agent may do without asking.
- We could not find an official OpenAI help page for ChatGPT agent's confirmation behaviour, only press coverage, so it is left out of the comparison. A reader on any other assistant should look in its own help page for a "remember" or "always" option on send and pay actions, because that is where the products differ.

## Evidence 1: official-page comparison of default stop points

Method: read each product's own help or announcement pages and recorded, for each stage (read, send, pay, standing permission), what the page says happens by default. Only values stated on official pages are listed. No account was connected for this comparison.

| Stage | Meta Muse | OpenAI Dots |
|---|---|---|
| Read (mail, calendar) | Connector defaults "Ask for some actions" / "Always ask"; read and write access described per connector [M1] | Local computer access off by default [O1] |
| Send | Approval prompt with responses including "Allow once", "Always allow", "Deny" [M1] | Approving one message is not a standing permission [O2] |
| Pay | New merchant: one-time card via Link by Stripe, fixed merchant, amount and expiry [M2][M3]; merchant with a saved payment method: approval every payment [M3] | Not on the 2026-10-30 pages; since 2026-11-13, ChatGPT Wallet with biometric approval per purchase (Evidence 5) |
| Standing permission at the act stage | "Always allow" exists [M1] | Custom Rules offer four behaviours, one of which acts without asking [O1] |

Sources and read dates:

- [M1] Meta Help, "How Muse works with your guidance and approval": https://www.meta.com/help/artificial-intelligence/1385290430137537/ — read 2026-10-30. A re-read on 2026-11-15 returned only the page title, so values are as of 2026-10-30. The page lists five approval responses; only the three whose English labels were confirmed are named above. It also covers disconnect vs reset, the activity log and actions that cannot be undone.
- [M2] Meta Newsroom, "Introducing Muse": https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/ — read 2026-11-15 (page shows 2026-09-08 and 2026-11-10). One-time-use card through Link by Stripe; Shop Pay "coming soon"; 1Password sign-in planned; Confidential VM "later this year"; available in the US.
- [M3] Meta research blog, "Security and safety for AI agents: our approach with Muse": https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse — read 2026-10-30. One-time card scoped to merchant, amount and expiry; approval for every payment at merchants with saved payment details; Sentinel and authd; mail connector filters one-time codes, reset links and magic links; "isn't immune to attack".
- [O1] OpenAI Help, "Getting started with your dot": https://help.openai.com/en/articles/20001530-getting-started-with-your-dot — read 2026-10-30. Custom Rules with four behaviours; local computer access off by default.
- [O2] OpenAI Help, "Dots privacy, security and safety FAQs": https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs — read 2026-10-30. Approving a single message does not create a standing permission.
- ChatGPT agent: searched on 2026-11-15 for an official OpenAI help page on confirmation before purchases or sending; only secondary coverage came back, so the column was dropped.
- 1Password for Claude (https://support.1password.com/1password-claude/): an approval prompt for each sign-in and the agent never sees the password. Not re-read for this note, so it is not in the table.

## Evidence 2: availability and roadmap facts for Muse (checked 2026-11-15)

- US launch: https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
- US and Canada (small business): https://about.fb.com/news/2026/09/introducing-muse-small-business/
- Singapore: https://about.fb.com/news/2026/10/muse-is-now-available-in-singapore-the-worlds-first-personal-ai-agent-built-for-everyone/
- A search of Meta's newsroom on 2026-11-15 found no announcement for further countries, including Korea. Claims about other countries in a single secondary outlet were not used.

## Evidence 3: what the current top results cover

Query: "is it safe to give an AI agent access to my email and credit card", English results, 2026-11-15. Of the top 10: five large media outlets, three vendor blogs, one security blog; no Reddit thread on the first page. None reports a hands-on test or compares products' default stop points.

- Tom's Guide, "3 accounts you should think twice about letting an AI agent access" — expert-quote list (page body did not load; judged from the snippet).
- NerdWallet, "Can you get your money back if an AI agent makes a financial mistake?": https://www.nerdwallet.com/credit-cards/news/ai-agent-makes-mistake — liability and refunds (returned 403; snippet only).
- privacy.com, "Is OpenClaw Safe?" — about 1,400 words, risk list plus a virtual-card pitch and FAQ, no own testing.
- Security reference: OWASP LLM06:2025 Excessive Agency (https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) and OWASP Top 10 for Agentic Applications 2026, "Least Agency" (https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/).
- Muse zero-day report: https://venturebeat.com/security/meta-patched-muses-zero-day-but-security-teams-still-lack-visibility-into-what-the-agent-can-access — malware used the agent's standing permissions; patched.

## Evidence 4: cost of removing approvals (earlier measurement)

The 18-minute vs 12-minute comparison cited in the article (the same refactor run five times with approvals and five times with auto-proceed in Antigravity CLI, on a local worktree; 6 to 7 approvals per approved run; 4 commands or changes stopped at an approval that auto-proceed would have run) comes from our earlier post, where the setup is described: https://loopnotes.dev/antigravity-cli-always-proceed-permissions/. It is one person's project, not a general saving rate, and the tool version was not part of that record.

## Evidence 5: where the settings live (checked 2026-11-15)

Added after a reader asked where to undo a standing permission and which control gives read-only mail. Direct fetches of the Meta and OpenAI help pages failed today (Meta returned only the page title, OpenAI returned 403), so the values below come from search-engine extracts of the official pages, restricted to meta.com and help.openai.com. Labels can change; read them with the date.

- Meta Help, "How Muse works with your guidance and approval" (https://www.meta.com/help/artificial-intelligence/1385290430137537/): permissions are set per connector under Settings > Permissions > Connectors; connector default modes are "Ask for some actions" (asks before every write action and important read actions) and "Always ask"; approval answers include allow once, allow for this task, always allow for this connector, and deny; "Always allow" lets Muse take that type of action for that connector in future without asking. Many connectors can be set to retrieve data only.
- Meta Help, "How Muse works with Connectors" (https://www.meta.com/help/artificial-intelligence/1687253048996149/): disconnect under Settings > Connectors; disconnecting stops data exchange, but information Muse already used may remain in memories and conversation history.
- Not found on Meta's pages: a list of individual past "Always allow" answers. The article therefore points the reader to the per-connector screen and, as the fallback, to disconnecting.
- OpenAI Help, "Getting started with your dot" (https://help.openai.com/en/articles/20001530-getting-started-with-your-dot): on mobile, Customize > Custom rules to review default rules or add one; four behaviours: take action without asking, take action if pre-approved, ask before taking action, hand off to you. Pre-approval means you asked for the action explicitly; asking for a draft does not authorize sending it. Custom Rules do not grant app or computer access.
- OpenAI Help, "Managing app permissions in ChatGPT" (https://help.openai.com/en/articles/20001495-managing-app-permissions-in-chatgpt): levels "Always ask", "Allow read actions", "Allow low-risk actions", "Allow all actions"; personal accounts manage them under Settings > Apps. An older version of the page used different labels, so the exact menu may differ by account.
- OpenAI Help, "Making purchases with ChatGPT Wallet" (https://help.openai.com/en/articles/20001654-making-purchases-with-chatgpt-wallet) and ChatGPT release notes, 2026-11-13: Wallet lets a dot buy for you, rolling out to US Pro subscribers 18+ with an eligible US-issued card; before payment you review merchant, items, total and card and approve with biometrics (Face ID or Touch ID). This replaces the empty Dots "Pay" cell in Evidence 1.

## Moved from the article body (reader fix r1, 2026-11-15)

- Measurement detail: about 18 minutes with approvals against about 12 on auto, 6 to 7 approvals per approved run, 4 commands or changes stopped at an approval (Evidence 4). The article keeps "about half again as long" and "about six minutes".
- The auto-proceed run that spent about 20 minutes editing config and test fixtures before the result was thrown away and the worktree rebuilt; the article keeps the scene without the minutes.
- The author's MCP gateway: the first prototype kept tokens in the server process's environment variables, so one session using GitHub, Slack and a database left one agent process holding all of them; credentials later moved behind the gateway per tool, about 7 servers and more than 40 tools. The article keeps the conclusion (the agent may call a tool without seeing the password, which does nothing about which tool it calls).
- Muse macOS zero-day, patched, in which malware used permissions the user had already granted (https://venturebeat.com/security/meta-patched-muses-zero-day-but-security-teams-still-lack-visibility-into-what-the-agent-can-access), and Meta's own line that Muse "isn't immune to attack" (Meta research blog).

## Limits

- Two products only. ChatGPT agent has no official page in this comparison, and 1Password for Claude was not re-read.
- The Muse help page values date from 2026-10-30; the 2026-11-15 re-read failed. Option names in these products change, so the table should be read with its dates.
- No email account or card was connected to Muse for this note; the table is what the official pages say, not observed behaviour.
- Tom's Guide and NerdWallet were judged from search snippets because their pages did not load.

## Moved from the article body (reader fix r1, second pass, 2026-11-15)

- Where Dots settings live: OpenAI describes dots as always-on agents in ChatGPT with their own cloud computer and browser that use connected tools (GPT-6 Astra system card, dots appendix: https://deploymentsafety.openai.com/gpt-6-astra/sec:appendix-dots, as cited in our Dots post). The mail permission a dot uses is therefore ChatGPT's app permission (Settings > Apps, Evidence 5), not a separate Dots screen; Custom Rules (Customize > Custom rules) only set when the dot asks.
- Muse connector modes (Evidence 5): "Ask for some actions" already asks before every write action, so it is enough for the read-yes, send-and-pay-ask rule; "Always ask" adds a prompt before reads.
- Sentinel, from Meta's research blog (read 2026-10-30): "Sentinel is the sole permission authority for connector actions and network egress"; the blog also says the agent never sees real tokens. Both enforce permissions already granted; neither chooses them.
- Log detail: in the author's dot Activity View, the scheduling-reply task showed as one line from the start to the approval request. The article keeps only the check (ask for a draft and watch it stop at send).
- Measurement wording: the article now gives the 18-minute (approvals) and 12-minute (auto) times directly so the six-minute difference has a baseline; run count and approval count stay here (Evidence 4).

## Moved from the article body (reader fix r2, 2026-11-15)

- The "Hidden passwords are a different setting from permission" subsection: action permission (read, write, send, pay) and credential exposure (whether the agent sees passwords and tokens) are two separate axes; Meta built Muse so the agent never sees real tokens, and Sentinel enforces what each connector may do (Meta research blog, read 2026-10-30). The author's MCP gateway keeps the same split: an agent knows only that it may call a tool, not the credential behind it. The article keeps one sentence: hiding credentials decides where they live, not what the agent may do with the access granted.
- The author's first-dot setup in full: reading and search on, document edits and outside sending through approval, no card connected. The article keeps the read-only and no-card facts on its first screen and the choice of the everyday personal inbox in the read-access section.
- Check steps added for the reader, from Evidence 5: under Muse's "Ask for some actions", every write action (a send included) asks first, so asking Muse to send a one-line email to yourself should bring up the approval prompt; under ChatGPT's "Allow read actions", a dot can still write a reply for you and stops when it would send (the author's scheduling-reply scene, read-only mail access). Whether saving into the mailbox's Drafts folder counts as a write at that level is not stated on OpenAI's page.
