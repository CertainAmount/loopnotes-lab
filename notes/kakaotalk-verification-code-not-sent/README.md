# Why isn't KakaoTalk's verification code arriving, and what should you check first?

Research note for the loopnotes.dev article "KakaoTalk verification code not sent". Evidence was gathered on 2026-11-17 unless a row says otherwise. Korean Naver posts and App Store reviews are other people's reports, not our own experience; they are linked with at most a one-line summary.

## Conclusions

1. On a foreign number, the most common named failure in Naver reports (8 of 28 posts) is not a code that never arrives but the step where KakaoTalk asks you to send a text yourself, in two reports to a UK (+44) or Swedish (+46) number. So a reader on a foreign number first checks whether their line can send an international SMS (a data-only eSIM cannot) instead of tapping resend.
2. When the text has gone out and "verification is still in progress" stays on screen, the reports we found show sending again did not move it (one person sent it 4 times with an international SMS pack, another waited two days). So the reader sends once, stops, and contacts Kakao by mail after a day, which is the wait Kakao's own help page gives.
3. Korean numbers fail on the receiving side: of 62 Korean-number Q&A posts, a new phone or reinstall (12) and a resend lock (12) tie as the most common named cause, followed by spam or block filters (10), and none describes a send-a-text step. So a reader with a Korean number on a new phone opens the filtered or spam folder before requesting another code.
4. Five people wrote that they saw a 24-hour wait after about 4 to 5 back-to-back requests, while Kakao's help pages state no limit at all. So a reader stops at three requests and checks the line and the filters instead.
5. Kakao's help pages allow only SMS or a call (no email, no skipping), list four cases where a number cannot receive the code, and ask for the country first and the number without its country code, leading 0 kept. So "cannot be sent to this number" sends the reader to the input and the line, not to resend.

## 1. Official pages compared

Fetched and read on 2026-11-17 (Korean UI for Kakao, English UI for Apple, Samsung and Google). Quoted page text is in [official-checks-2026-11-17.md](official-checks-2026-11-17.md) in this folder.

| # | Source | What it says that matters here |
|---|---|---|
| 1 | [Kakao Help 1073209443: the code doesn't arrive](https://cs.kakao.com/helps_html/1073209443?locale=ko) | Recheck the number; enter it without the country code (example 010-0000-0000, the 0 stays). In some countries or regions carriers can delay the code. If nothing arrives after a day, contact customer service (mail form on the page). No resend limit or lock time is stated. |
| 2 | [Kakao Help 1073209446: using a non-Korean country code](https://cs.kakao.com/helps_html/1073209446?locale=ko) | Pick the country first, then type the number without its country code and finish SMS verification. Mentions SMS verification only; no send-a-text step. |
| 3 | [Kakao Help 1073209503: is login verification only SMS or a call?](https://cs.kakao.com/helps_html/1073209503?locale=ko) | Verification needs a number that can receive SMS or a call; no skipping and no email or other method. A number cannot receive the code when calls are forwarded, when roaming is unavailable abroad, when it is an unregistered handset, or when the line is suspended or cancelled. Customer Center channel (chatbot 24 hours, chat weekdays 10:00 to 18:30) and 1577-3754 (paid). The page also shows an "SMS verification" pop-up asking the user to send a text directly for security, in a QR-scan-then-confirm-on-PC flow, not app sign-up; we do not read it as an explanation of the app's send-a-text step. |
| 4 | [Kakao Talk Safety: Talk Safety Pass](https://talksafety.kakao.com/en/toolandguide/verify/alleviate) | Limit relief is for +82 numbers registered with Kakao Certificate only, so a foreign number has no official way to lift a limit. |
| 5 | [Apple: Screen and filter text messages on iPhone](https://support.apple.com/guide/iphone/screen-and-filter-texts-iph203ab0be4/ios) | Messages from unknown senders go to another folder with no notification. Path: Filter button, then Unknown Senders. The setting is now called Screen Unknown Senders (older posts say Filter Unknown Senders). "Allow Notifications" can let time-sensitive texts such as verification codes notify (options vary by country). |
| 6 | [Apple: cellular data roaming options](https://support.apple.com/en-us/109037) | Data Roaming controls internet data abroad only. |
| 7 | [Apple: use eSIM while traveling](https://support.apple.com/en-us/118227) | With only a travel eSIM on, the home line keeps iMessage and FaceTime, not carrier SMS. What decides whether an SMS code reaches a home number abroad is that the home line is on and served by a carrier. |
| 8 | [Samsung US: block a number on a Galaxy phone](https://www.samsung.com/us/support/answer/ANS10002869/) | Samsung Messages: More options, Settings, Block numbers and spam. |
| 9 | [Google Messages: report spam](https://support.google.com/messages/answer/9061432?hl=en&co=GENIE.Platform%3DAndroid) and [hide unknown international messages](https://support.google.com/messages/answer/15720740?hl=en) | Reported or blocked senders go to "Spam & blocked". Hiding international messages works only with a Singapore SIM, so it is not a general cause for foreign readers. |

What the comparison concludes: Kakao's pages describe receiving a code and its input rules, give no resend limit, and do not explain the send-a-text step or the "still in progress" message that foreign-number users report. The phone makers' pages explain where a filtered code goes.

## 2. Naver reports (Korean web)

Naver Search API, queried 2026-11-17, relevance sort, top 40 read per type. "Total hits" is Naver's document count for the term, not a demand figure.

| Search term (Korean) | Meaning | Total hits (blog / cafe / KnowledgeiN) | Used in the counts |
|---|---|---|---|
| 카카오톡 인증번호 안옴 | KakaoTalk verification code not arriving | 160,904 / 111,577 / 16,778 | Yes (Korean numbers) |
| 카카오톡 인증문자 안옴 | KakaoTalk verification text not arriving | 86,950 / 99,689 / 9,756 | Yes (Korean numbers) |
| 해외번호 카카오톡 인증 | KakaoTalk verification with an overseas number | 98,138 / 124,910 / 5,126 | Yes (foreign numbers) |
| 외국인 친구 카카오톡 가입 인증번호 | signing a foreign friend up for KakaoTalk, verification code | 3,085 / 483 / 136 | No: few relevant posts, many prepaid-SIM ads |
| 카카오톡 인증이 아직 진행중입니다 | "KakaoTalk verification is still in progress" | 89,128 / 14,395 / 3,962 | No: Naver split the phrase and most results were unrelated |

How the posts were classified: one cause per post, the first cause named by the asker or the first reply, read from the title, question text and first-reply snippet. Pages were not opened in full. Duplicates and unrelated posts were removed. Blog results were left out of the cause counts because the top blog posts are mostly "7 ways to fix it" lists, not reports.

### 2a. Korean numbers (KnowledgeiN, first two terms, N = 62)

| Named cause | Posts |
|---|---|
| New phone or reinstall | 12 |
| Resend lock or wait | 12 |
| Spam, block or reject-messages setting | 10 |
| Account suspended or restricted | 4 |
| Line suspended | 2 |
| Number format (for example, 010 left out) | 2 |
| Virtual number | 1 |
| Delay | 1 |
| Other (name mismatch, number already in use, and similar) | 8 |
| No cause given | 10 |

No post in this group describes a send-a-text step. Where askers quoted "cannot be sent to this number", 3 replies read it as a suspended number or account rather than a delivery problem.

### 2b. Foreign numbers, sign-up or re-verification (third term: KnowledgeiN 20 + cafe 8, N = 28)

| Named cause | Posts |
|---|---|
| Send-a-text step | 8 |
| Replies saying foreign numbers are blocked or documents are needed (repliers' claims, not official) | 7 |
| Wait after a number change or re-sign-up (not a resend lock, see below) | 2 |
| Number format (leading 0, country choice) | 2 |
| No cause given | 2 |
| Other (re-sign-up, expired number, and similar) | 7 |

The 8 send-a-text posts split as: sent, then "still in progress" or "processing" stayed (3); sending cancelled or the overseas SMS did not go out (2); the app asked for a text to +44 or +46, reported by users of Vietnamese and US numbers (2); other (1). Posts quoted:

- [KnowledgeiN 431383808](https://kin.naver.com/qna/detail.naver?dirId=1060801&docId=431383808&answerNo=0): sent the text to a +44 number, sending was confirmed, but the screen kept saying verification is still in progress.
- [Cafe post, vietnamsketch 461658](https://cafe.naver.com/vietnamsketch/461658): the text went out, verification stays "in progress".
- [Cafe post, vietnamsketch 436938](https://cafe.naver.com/vietnamsketch/436938): a Vietnamese number was told to text +44 or +46, and the overseas SMS would not send.
- [Cafe post, nameyee 38788](https://cafe.naver.com/nameyee/38788): a US (+1) number was told to send a text to a UK (+44) number.

Correction to the first count: the two posts first coded as "resend lock" for foreign numbers are not back-to-back request locks. [KnowledgeiN 246892680](https://kin.naver.com/qna/detail.naver?dirId=1060801&docId=246892680&answerNo=0) is a 72-hour wait after dropping a Korean number for a Canadian one, and [KnowledgeiN 372649827](https://kin.naver.com/qna/detail.naver?dirId=1060801&docId=372649827&answerNo=0) is a re-sign-up restriction after leaving. They are counted as "wait after a number change or re-sign-up", which leaves foreign numbers with 0 resend-lock reports.

### 2c. First-hand lock reports (all three counted terms, N = 5)

Five posts say the writer saw a 24-hour wait after repeated requests. Two give the number of requests before the lock:

- [Cafe post, songpalogue 196915](https://cafe.naver.com/songpalogue/196915): about 4 code requests while switching numbers, then a 24-hour block.
- [KnowledgeiN 237132168](https://kin.naver.com/qna/detail.naver?dirId=1060801&docId=237132168&answerNo=0): about 5 tries, then told to try again in 24 hours.

Reply-side claims, not confirmed anywhere official: the 24 hours count from the last attempt; only 5 tries are allowed per 24 hours. An earlier version of this count listed six reports (five at 24 hours, one at 72 hours); the 72-hour case is the number-change wait in 2b and is removed here.

Two replies named a sender number for Kakao's codes. No official source lists it, so it is not used.

## 3. English reports (App Store)

Read 2026-11-17. These cross-check the Naver send-a-text reports; they add no new step for the reader.

- [App Store KakaoTalk, Philippines](https://apps.apple.com/ph/app/kakaotalk/id362057947): review dated 2024-01-21, the app wanted the user to send a text to a Korean number and the text would not send.
- [App Store KakaoTalk, India](https://apps.apple.com/IN/app/id362057947): review dated 2024-10-16, the user bought an international SMS pack and sent the text 4 times, and verification still did not move on. The listing showed version 26.9.2, dated November 3.

## Limits

- One person classified the posts by hand, from snippets, without opening the pages. Another reader could code some posts differently.
- KnowledgeiN posts show no date, so the counts cannot say whether a cause is recent.
- The foreign-number group is small (28 posts), and the destination numbers (+44, +46) come from two reports; other countries may be told to text other numbers.
- Kakao's help does not describe the send-a-text step, so everything about it here comes from users' reports, not from Kakao.
- App behaviour can change between versions; the screens described here match reports and the App Store listing as of November 2026.

## 4. Added for the reader fix (2026-11-17)

Pages fetched on 2026-11-17 to fill steps a test reader could not finish. Quoted lines are the page text as served that day.

- [Kakao Customer Service: KakaoTalk Question form](https://cs.kakao.com/requests?service=8&locale=en): the mail inquiry form linked as "문의하기" from help page 1073209443. Categories include "Verification Code Related"; required fields are category, email address, phone number with a country-code picker, title and contents; "you can attach up to 5 files, 30MB each". Logging in is offered, not required ("Do you want to log in? If you log in, you can view your inquiry history"). The same page holds the "SMS Verification" pop-up noted in section 1 ("Send the message from the opened messaging app without modifying the text"); that is the form's own phone check, not the app's sign-up step.
- [Apple: If you can't send or receive messages on your iPhone or iPad](https://support.apple.com/en-us/118433): "If you try to send a message and you see a red exclamation point with an alert that says Not Delivered…". Used as the check for whether the text left the phone.
- [Samsung US: SIM cards for your Galaxy phone or tablet](https://www.samsung.com/us/support/answer/ANS10001619/): "open Settings, and then tap Connections. Tap SIM manager. From here, you can tap the switch next to your physical SIM or activated eSIM to enable or disable their connections." Used as the Galaxy version of the iPhone Settings > Cellular check.
- [Samsung UK: How to send text messages & access settings](https://www.samsung.com/uk/support/mobile-devices/how-do-i-use-text-messages-on-my-device/): "Tap Settings. Tap Block messages or Block numbers and messages. Tap Blocked messages. Any messages that have been blocked will now show."

Not found: what the send-a-text screen asks the user to type, and whether KakaoTalk fills the message in and opens the messaging app itself. The Naver posts quoted in section 2b and the App Store reviews in section 3 describe sending to +44 or +46 but not the message body, the author never saw the screen, and two web searches on 2026-11-17 found no description. The article tells the reader to send exactly what the screen shows, unchanged.

### Moved out of the article body (reader fix r1)

These sentences proved the advice rather than helping the reader act; the counts they carried stay in sections 2a and 2b and in the chart.

- "In a November 2026 count of 28 Naver posts about foreign numbers, this step was the most common problem, in 8 of them. None of the 62 posts about Korean numbers mentioned it."
- "In the 62 Naver posts about Korean numbers, a new phone or a reinstall was one of the two most common causes, with spam and blocking settings close behind."
- The India App Store review (section 3) as a second anecdote beside the Naver poster in the "still in progress" step.

### Reader fix r2 (2026-11-17)

- [Kakao Help 1073209503](https://cs.kakao.com/helps_html/1073209503?locale=ko), fetched 2026-11-17: the "문의하기" link to the mail form reads "간편하게 메일로 답변을 받을 수 있어요" (you get the answer by mail). The [form page](https://cs.kakao.com/requests?service=8&locale=en) asks for consent to use the email address and phone number to "reply to processing results". Neither page gives a reply time, so the article says only that the answer comes by email.
- Moved out of the body as detail the reader skipped: the send-to numbers in [the Vietnamese-number cafe post](https://cafe.naver.com/vietnamsketch/436938) and [KnowledgeiN 431383808](https://kin.naver.com/qna/detail.naver?dirId=1060801&docId=431383808&answerNo=0) were UK (+44) and Swedish (+46) numbers, given to people with Vietnamese and US numbers; the KnowledgeiN 431383808 poster saw "still in progress" for two days after the text went through. The body keeps the conclusions: the number to text may be outside Korea, and waiting days after one text did not move the screen.

### Reader fix r3 (2026-11-17)

- [Kakao Help 1073209443](https://cs.kakao.com/helps_html/1073209443?locale=ko), quoted in [official-checks-2026-11-17.md](official-checks-2026-11-17.md): "다만 일부 국가 또는 지역의 경우 통신사 사정에 따라 인증번호가 도착하기까지 다소 시간이 걸릴 수 있습니다" (in some countries or regions the code can take a while to arrive because of the carrier) and "하루가 지나도 … 고객센터를 통해 문의해 주세요" (contact customer service if a day passes). Used for the step when the home line is on and the code still has not come.
- Leading zero on non-Korean numbers: Kakao's pages (1073209443, 1073209446) give only a Korean example (010-0000-0000, zero kept). The article tells readers with another country's number to type it as dialled at home and, if refused, try once without the leading zero; it states no rule.
- Moved out of the body as detail the reader skipped: the author's new phone was an iPhone 18 Pro; in the visiting engineer's case the code landed within about two minutes after one resend.

Article: [KakaoTalk Verification Code Not Sent or Still in Progress?](https://loopnotes.dev/kakaotalk-verification-code-not-sent/)
