# Why can't my phone open the dev server that works on localhost?

Research note for the loopnotes.dev article "access localhost from phone". It collects what we gathered for that article so a reader can check it. Gathered on 2026-11-20 unless a row says otherwise.

## Conclusions

1. The usual advice, "bind to 0.0.0.0", fits only half the dev servers we started on this machine (2026-11-20, two runs each, results below): Vite 8.3.8, Flask 3.1.3 and uvicorn 0.54.0 listen on `127.0.0.1` only, while Next.js 16.4.6 dev, Python 3.11 `http.server` and Express 5.3.0 with no host already listen on every address. A request to a closed server from another address was refused in about 0.0003 s; it does not hang. So an instant refusal points at the server's bind, and a long spin points at the network.
2. Opening the bind is not the last door. Vite answers IP addresses but refuses host names (Tailscale MagicDNS, tunnels) that are not in `server.allowedHosts` (reproduced: 200 by IP, 403 by name, 200 after adding `'.ts.net'`). Next.js 16.4.6, open by default, serves the page to a LAN IP but blocks its live-reload connection from that origin until the IP is in `allowedDevOrigins`.
3. When the server is started through an npm script, the flag needs the extra `--` (`npm run dev -- --host`); without it npm prints a warning, keeps the flag, and Vite stays on `127.0.0.1` (measured).
4. None of the three top results we read shows a command to check which address the server is actually listening on; reading one line of `ss -ltnp` (Linux) or `lsof -iTCP -sTCP:LISTEN` (Mac) settles whether the server is the problem: `127.0.0.1` or `[::1]` means this computer only, `0.0.0.0`, `*` or `[::]` means open.
5. On WSL2, Vite's docs say `host: true` alone is not enough for LAN access, so a Windows reader on WSL2 should not stop at the flag.

## The question

A searcher's dev server loads at `localhost:<port>` in the laptop browser, but a phone on the same Wi-Fi shows nothing. They have usually already been told "use the LAN IP and bind to 0.0.0.0". What they need to know is whether the server or the network is the problem, and what to change.

## Experiment results (run on this machine, 2026-11-20)

Setup: one Linux laptop (kernel 6.8), Node 24.21.0, Python 3.11.4. Each server was started with its defaults, then with the flag that opens or closes it, each twice (stopped and started again), inside a memory-capped scope. We read the listening address with `ss -ltnp`, then requested `/` with curl from `127.0.0.1`, `[::1]` and the laptop's own Wi-Fi address. There was no phone in the loop: a request to the Wi-Fi address from the same laptop stands in for the phone's request, because it only succeeds when the server listens beyond loopback. No firewall rule, port forward or tunnel was changed. Raw rows: [bind-runs.csv](bind-runs.csv); server logs: [runs/](runs/) (the LAN address is replaced by `<LAN-IP>`).

| Server (version) | Default listen | Wi-Fi address, default | Flag tried | Listen with flag | Wi-Fi address, with flag |
|---|---|---|---|---|---|
| Vite 8.3.8 | `127.0.0.1:5173` | refused, 0.0002 s | `npm run dev -- --host` | `*:5173` | 200 |
| Flask 3.1.3 | `127.0.0.1:5000` | refused, 0.0002 s | `--host=0.0.0.0` | `0.0.0.0:5000` | 200 |
| uvicorn 0.54.0 + FastAPI 0.165.0 | `127.0.0.1:8000` | refused, 0.0002 s | `--host 0.0.0.0` | `0.0.0.0:8000` | 200 |
| Next.js 16.4.6 dev (Turbopack) | `*:3000` | 200 | `-H 127.0.0.1` (closing) | `127.0.0.1:3000` | refused |
| Python 3.11.4 `http.server` | `0.0.0.0:8000` | 200 | `--bind 127.0.0.1` (closing) | `127.0.0.1:8000` | refused |
| Express 5.3.0, `app.listen(3001)` | `*:3001` | 200 | `listen(3001, '127.0.0.1')` (closing) | `127.0.0.1:3001` | refused |

Both runs matched for every row.

- Split: 3 of 6 closed by default, 3 of 6 open. The flag mattered only for the closed three; on the open three the page answered on the Wi-Fi address with no flag at all.
- Failure speed: every refused request returned in 0.0002–0.0005 s (connection refused, curl code 000). A server that is not listening does not make the client wait; a long spin before failing has to come from somewhere between the devices.
- Vite's own start-up line already says which case you are in: `Network: use --host to expose` by default, `Network: http://<LAN-IP>:5173/` with `--host`. Next.js prints a Network line with the LAN address by default.
- `0.0.0.0` (Flask, uvicorn, `http.server`) is IPv4 only: `[::1]` was refused while the IPv4 addresses answered. Vite with `--host`, Next.js and Express listened on `*` and answered both.
- Vite default bound to `127.0.0.1`, not `[::1]`, on this machine.
- `npm run dev --host` (no `--`): npm printed `npm warn Unknown cli config "--host"`, ran plain `vite`, and Vite printed `Network: use --host to expose` and listened on `127.0.0.1:5173` in both runs.

### Vite name check (E2)

With `npm run dev -- --host`, both runs: request by IP → 200; the same request with `Host: mymac.tail1234.ts.net:5173` (a made-up MagicDNS-style name) → 403 with the body `Blocked request. This host ("mymac.tail1234.ts.net") is not allowed. To allow this host, add "mymac.tail1234.ts.net" to `server.allowedHosts` in vite.config.js.`; after adding `server: { allowedHosts: ['.ts.net'] }` and restarting → 200.

### Next.js dev resources from a LAN IP (E1-b)

Next.js 16.4.6 dev, defaults, both runs: the page and its script chunks load over `http://<LAN-IP>:3000` (200). The live-reload socket `/_next/webpack-hmr` requested with `Origin: http://<LAN-IP>:3000` is refused, and the terminal prints `Blocked cross-origin request to Next.js dev resource /_next/webpack-hmr from "<LAN-IP>"` and `Cross-origin access to Next.js dev resources is blocked by default for safety.` With `allowedDevOrigins: ['<LAN-IP>']` in `next.config.js`, both runs printed no block. So on this version it is a block, not only a warning: the page opens on a phone, but edits do not reload there until the LAN address is allowed.

### Not run

Angular (`ng serve`) and Spring Boot were not run: no JDK on this machine for Spring Boot, and the Angular CLI install was left out to stay inside the memory cap. Their rows stay as documented defaults in Evidence 1.

## Evidence 1: default bind address by dev server, from official docs

Each row is what the official page says about the server's default listening address and how to open it. "Read" means we opened the page; "snippet" means we read the search-result excerpt of the official page this round and the drafting stage rechecks the page.

| Server | Default (per docs) | How to open / change | Source | How read, date |
|---|---|---|---|---|
| Vite | `server.host` defaults to `'localhost'` (this machine only) | `--host` or `host: true` / `'0.0.0.0'` (LAN and public addresses) | [vite.dev server options](https://vite.dev/config/server-options) (page shows v8.3.7) | read, 2026-11-20 |
| Next.js dev | `next dev -H` defaults to `0.0.0.0` (all addresses), port 3000 | already open; `-H` to change | [Next.js CLI](https://nextjs.org/docs/app/api-reference/cli/next) | snippet, 2026-11-20 |
| Python `http.server` | all interfaces | `-b` / `--bind` to restrict | [docs.python.org http.server](https://docs.python.org/3/library/http.server.html) | snippet, 2026-11-20 |
| Flask dev server | only this computer | `flask run --host=0.0.0.0` | [Flask quickstart, Externally Visible Server](https://flask.palletsprojects.com/en/stable/quickstart/) | snippet via a secondary page, 2026-11-20 |
| Node `net` / Express | host omitted → `::` if IPv6 is available, else `0.0.0.0`; on most systems `::` also takes IPv4 | `listen(port, '127.0.0.1')` to restrict | [Node.js server.listen](https://nodejs.org/api/net.html#serverlistenport-host-backlog-callback) | snippet, 2026-11-20 |
| Spring Boot | `server.address` "Network address to which the server should bind", default empty | `--server.address=...` | [Spring Boot common properties](https://docs.spring.io/spring-boot/appendix/application-properties/index.html) | snippet of an older appendix, 2026-11-20 |
| Angular `ng serve` | `host` default `"localhost"` | `--host 0.0.0.0` | [angular-cli dev-server schema](https://github.com/angular/angular-cli/blob/main/packages/angular/build/src/builders/dev-server/schema.json), [angular.dev/cli/serve](https://angular.dev/cli/serve) | read, 2026-11-09 (not rechecked this round) |

What the docs split into: closed by default = Vite, Flask, Angular; open by default = Next.js dev, `http.server`, Node/Express with no host, Spring Boot with `server.address` unset.

## Evidence 2: the name check after the bind (Vite)

From [vite.dev server options](https://vite.dev/config/server-options), read 2026-11-20:

- `server.allowedHosts` defaults to `[]`; `localhost` and all IP addresses are allowed by default, so a request to `http://<LAN IP>:5173` passes.
- A host name not in the list is refused; a value with a leading `.` allows that domain and all its subdomains (for example `'.ts.net'` for Tailscale MagicDNS names).
- The check came with Vite 6.0.9 (security fix, January 2025).
- The same page warns that the browser may resolve `localhost` to a different address than Node did (Node `dns.setDefaultResultOrder`), so a "localhost" bind can be `[::1]` rather than `127.0.0.1`, and that on WSL2 `host: true` is not enough for LAN access.

Next.js has a related setting, [`allowedDevOrigins`](https://nextjs.org/docs/app/api-reference/config/next-config-js/allowedDevOrigins), for dev resources requested from another origin such as a LAN IP; on 16.4.6 it blocks the live-reload socket by default (measured above).

## Evidence 3: what the top results cover

Target query "can't access localhost from phone", results read on 2026-11-20:

- [sizzy.co: test localhost on mobile](https://sizzy.co/blog/test-localhost-on-mobile) — about 600 words; general "bind to 0.0.0.0" advice; no per-server table, no bind-check command, no device isolation, no `allowedHosts`.
- [rabinarayanpatra.com: access local dev server from phone](https://rabinarayanpatra.com/blogs/access-local-dev-server-from-phone) — about 1,500 words; Vite, Next.js, Flask and Node defaults in prose from docs (no measurement, no table); covers isolation and secure context; no bind-check command, no `allowedHosts` 403, no `[::1]`.
- [Laracasts thread: localhost not accessible from mobile](https://laracasts.com/discuss/channels/general-discussion/localhost-not-accessible-from-mobile) — individual answers for one setup.

The wider top 10 is personal and tool blogs, forums (Laracasts, Apple Discussions, Sky help forum, roots discourse, Ionic forum), dev.to and tunnel-vendor pages; the common answer is "use the LAN IP, bind to 0.0.0.0, check the firewall, else a tunnel". The `npm run dev --host` trap (missing `--`) appears only in forum threads.

## Evidence 4: what searchers type

Google autocomplete, collected 2026-11-20 (r1 rows from 2026-11-09 marked):

- access localhost from phone; can't access localhost from phone; why can't i access localhost on my phone
- localhost not working on phone / on mobile; can i access localhost from my phone
- access localhost from phone mac; access localhost from mobile on same network
- how to access localhost from another device / laptop / pc from mobile; connect to localhost from phone; how to use local host on phone
- access angular localhost from phone; access laravel localhost from phone; how to access xampp localhost from mobile
- express listen 0.0.0.0; is 127.0.0.1 the same as 0.0.0.0; 0.0.0.0 vs 127.0.0.1 vs localhost; bind 0.0.0.0 vs 127.0.0.1 docker / uvicorn
- vite localhost on phone; vite host 0.0.0.0; localhost 3000 on phone (r1, 2026-11-09)

Laravel, XAMPP, Docker and uvicorn-vs-Docker binds are left out of the article: they are different setups we have no material for or a different question.

## Other official pages the article may cite

- macOS firewall location: [Apple, block connections with a firewall](https://support.apple.com/guide/mac-help/block-connections-to-your-mac-with-a-firewall-mh34041/mac) (read 2026-11-09)
- iPhone Local Network permission: [Apple 102229](https://support.apple.com/102229) (read 2026-11-09)
- Tailscale: [install](https://tailscale.com/kb/1017/install), [MagicDNS](https://tailscale.com/kb/1081/magicdns) (read 2026-11-09)
- Windows LAN IP: [ipconfig](https://learn.microsoft.com/windows-server/administration/windows-commands/ipconfig) ("Used without parameters, ipconfig displays Internet Protocol version 4 (IPv4) and IPv6 addresses, subnet mask, and default gateway for all adapters"); the per-adapter `IPv4 Address. . . :` label appears in Microsoft's sample output in [Assign multiple IP addresses to virtual machines](https://learn.microsoft.com/azure/virtual-network/ip-services/virtual-network-multiple-ip-addresses-portal) (both read 2026-11-20)

## Questions moved out of the article

These answer different questions than "why can't my phone open my dev server", so the article leaves them out: camera / `getUserMedia` failing over a `http://` LAN IP (secure context), mobile Safari `100vh` and keyboard layout, the Android emulator's `10.0.2.2`, Chrome USB port forwarding, Cloudflare Quick Tunnel and `ssh -R` for webhook tests. The first is a candidate for its own article.

## Limits

- The on-machine run used one Linux laptop and the versions named above; a phone was not part of the run (the laptop's own Wi-Fi address stood in for it). Angular and Spring Boot are documented defaults, not measurements.
- Several doc rows were read from official-page snippets, not the full page, and are marked so above.
- Results are for each tool's documented current version on 2026-11-20 (Vite page v8.3.7); defaults can change between versions.
- No Korean web data was gathered: the question has no Korea-specific angle.

## Scene details and timings moved out of the article (reader fix r1, 2026-11-20)

The article keeps the scenes but not their clock; the details stay here (from author interviews):

- Vite bind incident: about 20–30 minutes spent on the firewall and router before reading the listen address; the next time, reading the `Network:` line first took two or three minutes.
- Cafe scene: around April 2025, a weekend, a neighborhood cafe, a 14-inch MacBook Pro and an iPhone. Tailscale install to `100.x:5173` opening took about ten minutes; the `allowedHosts` 403 on the MagicDNS name took another 15–20 minutes, about half an hour in all.
- The six-server runs above were started by Claude Code on the author's Linux laptop; the refusal time on the Wi-Fi address was 0.0002–0.0005 s (the article says "at once").
- Next.js version measured: 16.4.6 (the article says "Next.js 16").

## Official pages added for the reader's how-to steps (reader fix r1, read 2026-11-20)

- Windows listen check: [netstat](https://learn.microsoft.com/windows-server/administration/windows-commands/netstat) (Microsoft Learn, updated 2026-09-08): `-a` shows listening ports, `-n` numeric addresses, `-o` the PID; the Local address column holds the IP and port. The article uses `netstat -ano | findstr :5173`.
- Windows firewall: [Risks of allowing apps through Windows Firewall](https://support.microsoft.com/help/4525108): Windows Security > Firewall & network protection > Allow an app through firewall > Change settings, then tick the app or Allow another app.
- macOS firewall: [Apple](https://support.apple.com/guide/mac-help/block-connections-to-your-mac-with-a-firewall-mh34041/mac): System Settings > Network > Firewall > Options, Add, then allow or block per app.
- Ubuntu: [Firewalls](https://ubuntu.com/server/docs/how-to/security/firewalls/): ufw is disabled by default; `sudo ufw allow <port>` opens a port.
- Next.js: [allowedDevOrigins](https://nextjs.org/docs/app/api-reference/config/next-config-js/allowedDevOrigins) (updated 2026-08-26): only the hostname of the `Origin` header is matched; write entries without scheme or port; `*` and `**` wildcards. The article shows a bare-IP entry.
- Angular: [ng serve](https://angular.dev/cli/serve): `--host` "Host to listen on", default `localhost`; `--allowed-hosts` exists (not used in the article).
- Tailscale: [MagicDNS](https://tailscale.com/kb/1081/magicdns): a device name is the machine name plus the tailnet name ending in `.ts.net` (doc example `monitoring.yak-bebop.ts.net`).
- Not found on an official page: the wording of the Windows Security alert that appears when a program first listens (only third-party guides describe it), so the article gives the allowed-apps path instead.

## Official pages added for reader fix r2 (read 2026-11-20)

- macOS first-run alert: [Block connections to your Mac with a firewall](https://support.apple.com/guide/mac-help/block-connections-to-your-mac-with-a-firewall-mh34041/mac) (Apple): when an app not in the list is contacted, "an alert message appears asking if you want to allow or deny the connection"; until you respond, "any attempts to connect to the app are denied". A blocked app is switched to allow in Firewall > Options. The article says: a Deny, or a prompt left unanswered, blocks the phone.
- Windows first-run prompt: [Windows Firewall rules](https://learn.microsoft.com/windows/security/operating-system-security/network-security/windows-firewall/rules) (Microsoft Learn, updated 2026-10-08): with no allow rule, a dialog asks to allow or block the first time the app communicates on the network; answering No or cancelling creates block rules (typically one TCP, one UDP); a user without admin rights gets block rules whatever they click; explicit block rules take precedence over allow rules; the rules must be deleted for the prompt to come back. The article says: delete the app's Block rules under Windows Defender Firewall with Advanced Security > Inbound Rules.
- Client isolation check: no official cross-vendor page gives a device-side test. The article gives a comparison the reader can run without one: load the laptop's address with both devices on a network they control (home Wi-Fi); if it opens there, the first network keeps devices apart. Router "AP/client isolation" setting names differ by vendor and are not named in the article.
- Docker and WSL2: the reader asked about ports that must be published or forwarded. Vite's server options page notes `host: true` alone is not enough on WSL2 (see Evidence 1). Left out of the article as a different setup with no material of ours; candidate on the long-tail map.

## Moved out in reader fix r3 (2026-11-20)

- Cafe scene: with `--host` already on, the phone's loading bar ran for over thirty seconds before the can't-open page (author interview; the article now says "a long while").
- Which docs say Next.js dev, `python -m http.server` and Express (no host) listen on every address: [next CLI](https://nextjs.org/docs/app/api-reference/cli/next), [http.server](https://docs.python.org/3/library/http.server.html), [Node `net.Server.listen()`](https://nodejs.org/api/net.html#serverlistenport-host-backlog-callback) (all also in the article's Sources).
- The six-server runs requested each server at the laptop's Wi-Fi address, where a phone's request lands (the article now only shows the result).

Article: [Can't Access Localhost From Your Phone? Check the Bind First](https://loopnotes.dev/access-localhost-from-phone/)
