# What do you do when 1Password for Claude stops filling logins?

Research note for the loopnotes.dev article "1Password for Claude". It collects what the official pages say, what public failure reports say, and what the 1Password extension release notes show, so a reader can check the article's troubleshooting advice. Everything below was read on 2026-11-12 unless a row says otherwise. Forum and issue threads are other people's reports, not our own experience and not an official diagnosis; they are linked with a one-line summary.

## Conclusions

1. The 1Password support page for Claude covers a wrong login, cancelling a request and disconnecting, but says nothing about a request that fails to connect, so a reader who sees "not connected" or `relayUnavailable` will not find the fix there and should move straight to the cheap checks and then to support.
2. No 1Password extension release after 8.12.34 (2026-08-25) through 8.12.44 (2026-11-03) mentions Claude, agents or the relay, so updating the extension is not a known fix for a stuck connection and a reader should not wait for one.
3. The public `relayUnavailable` report has stayed open since 2026-07-18 through restarts, re-pairing and a Mac reboot, staff answered by asking for diagnostics, and a reply on 2026-10-16 says it still happens on current versions, so once a reader's symptom matches it they stop re-pairing in a loop and send diagnostics to 1Password support.
4. User-filed issues report `not_connected` while the extension looks healthy, and one of them suggests the consent prompt can open in a window the user cannot see, so before reinstalling anything a reader looks for an approval window hidden behind other windows (a user hypothesis, not a confirmed cause).
5. 1Password fills a "Sign in with Google"-style login only when the site's Login item is linked to a provider item (extension 8.12.34+), so a reader links that item and updates the extension before handing a Google-only site to Claude, or does that sign-in by hand.

## 1. Official pages compared

| # | Source | Read | What it says that matters here |
|---|---|---|---|
| 1 | [1Password Support: 1Password for Claude](https://support.1password.com/1password-claude/) | 2026-11-12 (page published 2026-11-04) | Mac only; 1Password for Mac and the browser extension at 8.12.28 or later; Claude desktop app plus Claude in Chrome; Claude plans Pro, Max, Team, Enterprise (no Ultra on this page). Fills Login items only: username, password, one-time code; not passkeys, cards or identities. Signing in through a provider (such as Google) works only when the Login item links to a provider item. Each request is approved in a 1Password window; Agentic Mode limits the extension to approved items until the Claude tab group closes. Covers a wrong login suggested, cancelling, and disconnecting (Customize > Connectors). 1Password Business admins allow it under Policies > Sharing and permissions > "Allow AI agents to autofill for users". **No section on connection failures, "not connected" or relay errors.** About 900 words, 5 H2s. |
| 2 | [Anthropic Help: Get started with 1Password for Claude](https://support.claude.com/en/articles/15936181-get-started-with-1password-for-claude) | 2026-11-09 (full page); 2026-11-12 (search snippet only) | Beta; macOS Claude Desktop. Team/Enterprise: off by default; an Owner or Primary Owner turns on Organization settings > Claude in Chrome > "Enable for your team" and "Password managers". The 2026-11-09 read listed Ultra among the plans; on 2026-11-12 the English snippet showed four plans, with Ultra only in translated versions. |
| 3 | [1Password browser extension release notes](https://releases.1password.com/b5x/stable/) | 2026-11-12 | Claude-related lines appear in 8.12.32 (2026-08-11) and 8.12.34 (2026-08-25, provider sign-in). 8.12.37 to 8.12.44 (latest, 2026-11-03) contain no Claude, agent or relay line. |
| 4 | [Anthropic Help: Use the built-in browser in Claude Cowork](https://support.claude.com/en/articles/16607400-use-the-built-in-browser-in-claude-cowork) | 2026-11-12 (full page) | A browser inside Cowork, separate from your own; first-run offer to import cookies from your browser, site by site; banking, email and single sign-on sites unchecked by default; Safari not supported; "Anything you sign in to inside the built-in browser is available to Claude in future Cowork sessions on that computer." |
| 5 | [1Password Developer: Claude Code plugin](https://www.1password.dev/integrations/claude-plugin) | 2026-11-12 (search snippet only) | A separate beta plugin for Claude Code (MCP config, skill, .env validation hook); MCP and mounting on Mac/Linux only; Claude Code 2.1.273+; MCP enabled under Settings > Labs. 1Password for Claude itself does not cover Claude Code. |
| 6 | [1Password press release, 2026-07-16](https://1password.com/press/2026/july/1password-for-claude) | 2026-11-12 | Launch announcement. |

What the comparison concludes: the two help pages agree on the setup path and on per-request approval, and neither has connection troubleshooting; the release notes show no Claude fix since August. The plan list differs between the pages (Ultra), so the article names the plans both pages agree on or sends the reader to check their own plan page.

## 2. Public failure reports

| # | Report | Dates | Error | Surface | Tried | Status (as of 2026-11-12) |
|---|---|---|---|---|---|---|
| 1 | [1Password Community thread 25103: "Agentic autofill for Claude always fails with relayUnavailable"](https://www.1password.community/1password-at-home-31/agentic-autofill-for-claude-always-fails-with-relayunavailable-25103) | opened 2026-07-18; staff asked for diagnostics 2026-07-21/22; latest reply 2026-10-16 | `relayUnavailable` (transport_error) | Cowork and Claude Code; Mac, 1Password 8.12.28, Chrome | restart, re-pair, Mac reboot: none helped | open, no fix posted; latest reply says it still happens on current versions |
| 2 | claudeissues.com #79976 (user-filed mirror of a GitHub issue) | not collected | `not_connected` | reported with a healthy extension | not collected | user-filed, no maintainer fix seen |
| 3 | claudeissues.com #87365 (user-filed mirror of a GitHub issue) | not collected | `tab_unavailable` | a Claude Code session in the desktop app | not collected | user-filed, no maintainer fix seen |
| 4 | claudeissues.com #91969 (user-filed mirror of a GitHub issue) | not collected | consent prompt rendered in a window the user cannot see | not collected | n/a | offered by its filer as a possible cause of #79976; a hypothesis |

What the reports conclude: connection failures exist in more than one surface (Cowork and Claude Code), the usual resets did not clear the longest-running one, and the only next step any official party has offered in public is sending diagnostics to 1Password support.

## 3. Dated timeline

| Date | Event | Source |
|---|---|---|
| 2026-07-16 | 1Password for Claude announced | press release |
| 2026-07-18 | `relayUnavailable` thread opened | Community 25103 |
| 2026-08-11 | Extension 8.12.32, first Claude-related release-note line | release notes |
| 2026-08-25 | Extension 8.12.34, provider sign-in | release notes |
| 2026-10-16 | Latest reply in the `relayUnavailable` thread: still failing | Community 25103 |
| 2026-11-03 | Extension 8.12.44 (latest), no Claude line since 8.12.34 | release notes |
| 2026-11-04 | 1Password support page published in its current form | 1Password support |

## 4. What people search for (English autocomplete, 2026-11-12)

| Seed | Suggestions |
|---|---|
| `1password for claude` | windows, code, chatbot feature, reddit, integration for claude ai, mcp for claude, connector for claude, claude integration, claude plugin |
| `1password claude` | integration, code, connector, mcp, plugin, windows, code integration, code plugin, reddit |
| `claude 1password` | mcp, integration, connector, cli, plugin, skill, windows, access, reddit |
| `1password agentic` | agentic ai, agentic autofill, agentic mode, secure agentic autofill |
| `can claude log into` | websites, your indeed account, cowork log into websites |
| `how to use 1password with claude` | claude use 1password |

"not", "vs" and "why" variants returned no suggestions. Failure queries in search results surfaced forum and issue threads, not articles.

## Limits

- The failure reports are user-filed. They show that the failures happen and what did not fix them; they do not establish a cause.
- For the three claudeissues.com threads we did not collect dates, attempted fixes or the original github.com/anthropics/claude-code issue URLs; their rows carry only the error string and surface.
- The Anthropic built-in-browser page and the 1Password Claude Code plugin page were read as search snippets, not fetched in full. The Anthropic 1Password page was read in full on 2026-11-09 and only as a snippet on 2026-11-12.
- No connection failure was reproduced for this note: reproducing one needs a signed-in account and a failing state on demand.
- No Korean (Naver) data was collected; the topic has no Korea angle.

## Update, 2026-11-12 (later the same day)

- Anthropic Help 15936181, read in full on 2026-11-12: "in beta for paid plans (Pro, Max, Ultra, Team, Enterprise) using Claude Desktop on macOS". The English page does list Ultra; the article now names all five plans. The 1Password support page still lists four.
- Report row 2 (#79976): original issue is [anthropics/claude-code #79976](https://github.com/anthropics/claude-code/issues/79976), "1Password credential-request (Claude in Chrome) fails with 'not_connected' despite healthy 1Password app/extension", opened 2026-07-22, auto-closed as stale 2026-11-08 (not planned), no maintainer reply. In the thread, one user traced the cause to the consent prompt opening in a Chrome window the user cannot see (moved on to #91969) and gave a workaround: open Claude's side panel in Chrome before the request, after which the status came back approved. The article's "no approval window" row uses that workaround, labelled as a user's.
- Official row 4 (Anthropic 16607400) was read in full on 2026-11-12, not only as a snippet: "Import works site by site", "Banking, email, and single sign-on sites stay unchecked by default", "Anything you sign in to inside the built-in browser is available to Claude in future Cowork sessions on that computer."
- "MCP-based" is not used for the 1Password connector: the 1Password support page, Anthropic 15936181 and the 1Password press release (all read 2026-11-12) do not say it. The MCP server mentioned in the article belongs to the separate Claude Code plugin.

## Update, 2026-11-12 (reader fix r1): moved from the article body, plus how-to pages

Moved here from the article's troubleshooting section, so the body keeps only the action:

- The 1Password support page for Claude has no section on failed connections (see official row 1).
- No extension release since 8.12.34 (2026-08-25) mentions Claude, through 8.12.44 (see official row 3).
- Other users report `not_connected` failures ([anthropics/claude-code #79976](https://github.com/anthropics/claude-code/issues/79976)) and a `relayUnavailable` failure that restarts, re-pairing and a Mac reboot did not clear; the longest thread (Community 25103) has no posted fix since July 2026, and 1Password staff answered it by asking for diagnostics.
- Author usage count kept out of the body: fewer than ten more hand-offs since connecting in August 2026, all in Cowork, mostly expired sessions.

How-to pages read on 2026-11-12 for the reader's missing steps:

| Page | What it gives |
|---|---|
| [Find the version numbers for 1Password](https://support.1password.com/version/) | Mac: 1Password > About 1Password in the menu bar |
| [How to keep 1Password up to date in your browser](https://support.1password.com/update-1password-browser/) | Chrome: Chrome menu > Extensions > Manage Extensions > 1Password > Details; Chrome updates extensions automatically |
| [Update 1Password](https://support.1password.com/update-1password/) | Mac app: Settings > Advanced > "Install updates automatically" |
| [Sign in with Google, Apple and other providers](https://support.1password.com/sign-in-with-provider/) | Existing item: select the item > Edit > Add More > Sign in with > "Add a login to sign in with" > choose the provider's Login item > Save |
| [Send a diagnostics report](https://support.1password.com/diagnostics/) | Mac: unlock, Help > Send Diagnostic Report > Open file location; email the `.1pdiagnostics` file with a description to support@1password.com, or attach to an existing support reply |
| [1Password for Claude](https://support.1password.com/1password-claude/) (re-read) | Connect: Touch ID or account password authorizes the connection; test: +New > Cowork, ask Claude to sign in and check an order, a prompt with a suggested Login item appears; Agentic Mode starts when Claude takes control of the browser; close the Claude tab group to use the extension elsewhere |
| [Anthropic Help 15936181](https://support.claude.com/en/articles/15936181-get-started-with-1password-for-claude) (re-read) | Connect also via a banner or an in-chat prompt; no description of a connection status indicator or of the connection permission screen |

Neither help page describes the exact wording of the connection authorization screen or the connected-state label in Claude's Connectors list; the author remembers the flow (allow, then a connected state in the list, then a test login) but not the wording.

## Update, 2026-11-12 (reader fix r2): how-to pages for the reader's missing steps

| Page | Read | What it gives |
|---|---|---|
| [Claude docs: Get started with connectors](https://claude.com/docs/connectors) | 2026-11-12 | "In the desktop app, select **Customize** in the sidebar, then **Connectors**." A connected connector is "listed under **Your connectors** with the status **Connected**" (general connector page; the 1Password pages don't describe the status label). |
| [1Password Support: If 1Password isn't working in your browser](https://support.1password.com/1password-browser-troubleshooting/) | 2026-11-12 | To reconnect the extension with the app: 1Password toolbar button > account menu (top left) > Settings > General > "Integrate this extension with the 1Password desktop app" on > restart the browser. |
| [1Password Support: 1Password for Claude](https://support.1password.com/1password-claude/) (re-read) | 2026-11-12 | Business policy path starts at 1Password.com: sign in, Policies in the sidebar, Manage under "Sharing and permissions", "Allow AI agents to autofill for users". No error messages described. |
| [Anthropic Help 15936181](https://support.claude.com/en/articles/15936181-get-started-with-1password-for-claude) (re-read) | 2026-11-12 | Team/Enterprise switch is turned on by an Owner or Primary Owner at Organization settings > Claude in Chrome (claude.ai/admin-settings/browser-extension). Connect also via a banner when 1Password is detected or an in-chat prompt. No troubleshooting. |
| [anthropics/claude-code #79976](https://github.com/anthropics/claude-code/issues/79976) (re-read) | 2026-11-12 | Where the failure shows: a Claude banner "Claude needs credentials to continue — Connect 1Password", and after approving, "Couldn't connect to 1Password. Check that it's open, then try again." Side-panel workaround: opening Claude's side panel revealed a "Claude for Chrome" window "Waiting for permission request...", after which the request was approved. |
| [1Password Community 25103](https://www.1password.community/1password-at-home-31/agentic-autofill-for-claude-always-fails-with-relayunavailable-25103) (re-read) | 2026-11-12 | "every credential request from Claude fails with relayUnavailable", in the Claude desktop app and Claude Code; the thread does not say exactly which screen shows the string. The article says Claude reports its login request failed with it. |

Moved here from the article body in r2:

- The 1Password plugin for Claude Code (beta) manages secrets in 1Password Environments, mounts `.env` files and ships an MCP server, Mac and Linux only (official row 5). The article keeps one line: it doesn't sign in to websites.
- Release-notes survey (no extension release since 8.12.34 mentions Claude) stays in official row 3; the article says only that no fix has been posted.

## Update, 2026-11-12 (reader fix r1b): which browser Cowork drives, and the side panel

| Page | Read | What it gives |
|---|---|---|
| [Anthropic Help 16607400: Use the built-in browser in Claude Cowork](https://support.claude.com/en/articles/16607400-use-the-built-in-browser-in-claude-cowork) (re-read) | 2026-11-12 | "Open the Claude Desktop app and go to Settings > Cowork." "Under Preferred browser, choose "Built-in browser" or "Chrome (Claude in Chrome)"." "If you already use Claude in Chrome, it stays your default for web tasks in Cowork." "If you don't have the extension, or you're new to browser use in Cowork, Claude uses the built-in browser." "Claude uses your preferred browser for web tasks unless you ask it to use the other one." "If your preferred browser isn't available, Claude tells you and continues with the other one." |
| [Anthropic Help 12012173: Get started with Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome) | 2026-11-12 | Install from the Chrome Web Store ("Add to Chrome"), sign in with your Claude account; "Pin the extension by clicking the puzzle piece icon, then the thumbtack next to "Claude.""; "To open the side panel, click the Claude icon in your Chrome toolbar." No keyboard shortcut given. The Claude in Chrome connector under Customize > Connectors is for chats; the page describes no separate pairing step with the desktop app, and says the native-messaging integration with Claude Desktop is not yet enabled. |

What the article takes from these: step 2 sets Preferred browser to Chrome so Cowork drives the Chrome that holds the 1Password extension; the first stall row gives the toolbar-icon click path for the side panel. The chat-only connector toggle is left out (the article's path is Cowork).

Article: [1Password for Claude: My Mac Setup and What It Can't Do](https://loopnotes.dev/1password-for-claude-setup/)
