# Official-page checks, 2026-11-17 (rewrite r2, step 2.5)

Fetched on this machine with curl (desktop user agent), text extracted from HTML. Quoted lines are the page text as served on 2026-11-17.

## Kakao Help (Korean UI)

### 1073209443 — 인증문자가 오지 않아요. 어떻게 하나요?
<https://cs.kakao.com/helps_html/1073209443?locale=ko> — HTTP 200
> 전화번호를 올바르게 입력하였는지 다시 한번 확인해 주세요.
> 전화번호 입력창에는 국가번호를 제외한 본인의 휴대폰 번호를 입력하여야 합니다.
> ※ 예) 010-0000-0000
> 다만 일부 국가 또는 지역의 경우 통신사 사정에 따라 인증번호가 도착하기까지 다소 시간이 걸릴 수 있습니다.
> 하루가 지나도 인증번호가 도착하지 않을 경우 고객센터를 통해 문의해 주세요.

Findings: example keeps the leading 0 (010-…); only the country code is left out. No resend limit or lock duration is stated. Contact route on the page: "문의하기 — 간편하게 메일로 답변을 받을 수 있어요" (mail form).

### 1073209446 — 한국 외 국가번호로 카카오톡을 이용하려면 어떻게 하나요?
<https://cs.kakao.com/helps_html/1073209446?locale=ko> — HTTP 200 (re-checked; research had it as 2026-10-30 only)
> 전화번호 입력란에 국가코드를 제외한 휴대폰 번호를 입력하여 SMS 인증을 완료한 후 이용할 수 있습니다.
> 기본 설정되어있는 국가코드가 다른 경우에는 국가를 선택한 후 해당 전화번호의 국가코드를 선택하면 이용할 수 있습니다.

Findings: pick the country first, then type the number without the country code. Page says "SMS 인증" only; no mention of a send-a-text (MO) step.

### 1073209503 — 카카오톡 로그인 인증은 SMS와 전화 수신만 가능한가요?
<https://cs.kakao.com/helps_html/1073209503?locale=ko> — HTTP 200
> SMS나 전화 수신이 가능한 휴대폰 번호를 통해 인증을 완료해야만 이용할 수 있습니다.
> 인증 과정을 생략하거나 이메일 등 다른 수단을 통한 인증 절차는 제공되지 않습니다.
> 카카오톡 이용을 위해 인증을 요청한 번호가 인증번호 수신이 불가한 경우 카카오톡을 이용할 수 없습니다.
> ※ 인증번호 수신이 불가한 경우: 착신이 전환된 경우 / 해외에서 로밍이 불가한 경우 / 공기기 사용 중인 경우 / 일시 정지 또는 해지 상태인 경우

Findings: no email verification, no skipping. Four cannot-receive cases unchanged from 2026-10-30.

## Apple (iOS, English UI)

### Screen and filter text messages on iPhone
<https://support.apple.com/guide/iphone/screen-and-filter-texts-iph203ab0be4/ios> (old slug block-filter-and-report-messages redirects here) — HTTP 200, page lists iOS versions up to iOS 27
> Their messages are filtered into another folder, and you don't get notified about them unless you want to be.
> In the conversation list, tap [the Filter button], then tap Manage Filtering. Turn on Screen Unknown Senders.
> To get notifications from some unknown senders—for example, for time-sensitive texts, like verification codes—tap Allow Notifications, then turn on the categories you want to allow. (Options vary by country and region.)
> In the conversation list, tap [the Filter button], then tap Unknown Senders.

Findings: English names: Filter button → Unknown Senders; setting is "Screen Unknown Senders" (iOS 26+ name; older posts say "Filter Unknown Senders"). Apple itself says filtered senders give no notification. "Allow Notifications" for time-sensitive texts like verification codes is an official fix to name once.

### About cellular data roaming options for your iPhone and iPad
<https://support.apple.com/en-us/109037> — HTTP 200
> Data Roaming permits internet access over a cellular data network in regions that are not covered by your carrier's network.
> Settings > Cellular (or Cellular Data) > Cellular Data Options > Data Roaming

### Use eSIM while traveling internationally with your iPhone
<https://support.apple.com/en-us/118227> — HTTP 200
> If you choose to keep both lines on, the capabilities on your primary line will continue to work. If you choose to only use your travel eSIM, FaceTime and iMessage will continue to work on your home line.

Findings: per Apple, the Data Roaming switch governs internet data only. What decides whether the SMS code reaches a home number abroad is that the home line is turned on in Settings > Cellular and the carrier serves it there (carrier name + signal bars). With only a travel eSIM on, the home line still gets iMessage/FaceTime, not carrier SMS. → In the article: check the home line is on and shows the carrier and signal; do not tell readers Data Roaming is what makes the code arrive.

## Samsung / Google (Android, English UI)

### Block a phone number or contact on your Galaxy phone (Samsung US)
<https://www.samsung.com/us/support/answer/ANS10002869/> — HTTP 200
> Navigate to and open the Samsung Messages app. Tap More options (the three vertical dots), and then tap Settings. Tap Block numbers and spam to view or edit your blocked list.

### Google Messages — Report spam / Hide unknown international messages
<https://support.google.com/messages/answer/9061432?hl=en&co=GENIE.Platform%3DAndroid> — HTTP 200
> When you report a conversation as spam, you also block the sender and move the message to your "Spam & blocked" folder.
<https://support.google.com/messages/answer/15720740?hl=en> — HTTP 200
> This feature moves messages from international phone numbers that aren't in your contacts to the "Spam & blocked" folder. … Important: This feature only works if your device has a Singapore SIM card.

Findings: on Galaxy phones the path depends on the Messages app: Samsung Messages → ⋮ → Settings → Block numbers and spam; Google Messages → profile/More → Spam & blocked. The "Hide international messages" setting is Singapore-SIM only, so it is not a general cause for foreign readers — do not use it as one.

## Not checked (out of this article after the outline cuts)
- Globe Signal 1073199441, Talk Cloud 1073203602, emergency email login 1073209977 — cut from the body (outline 전제), no re-check needed.
- Sender number 1644-4174 — no official source found in research; stays banned from the body.
