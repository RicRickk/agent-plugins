# Die veröffentlichten Verträge — Opt-in-Prozesse und Bestätigungsmail

Wort für Wort das, was der Server in `tools/list` für die 12 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## Inhalt

`search-opt-in-processes` · `get-opt-in-process` · `create-opt-in-process` · `update-opt-in-process`
· `delete-opt-in-process` · `get-opt-in-confirmation-email` · `update-opt-in-confirmation-email` ·
`get-opt-in-confirmation-email-content` · `update-opt-in-confirmation-email-content` ·
`preview-opt-in-confirmation-email` · `send-opt-in-confirmation-email-test` ·
`get-opt-in-process-redirect-url`

## `search-opt-in-processes` · RI

**Search opt-in processes**

Searches active opt-in processes (subscriber lists) by name, sorted by name, with ID, opt-in mode and distinguishing flags. Deleted processes are excluded; get-opt-in-process reads full settings.

Parameter:

- `query` — null | string (maxLength 250): Case-insensitive name fragment to search for; omit to return every active process
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-opt-in-process` · RI

**Get opt-in process**

Reads an opt-in process (subscriber list) by ID: mode, confirmation email ID, redirect URLs and parameters, pending-subscriber deletion, labels and notes.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process, as shown in the KlickTipp app URL
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `create-opt-in-process`

**Create opt-in process**

Creates an opt-in process (subscriber list) and its confirmation email, without subscribing anyone or sending. Defaults to double opt-in; single opt-in skips confirmation and requires the user’s approval. copyFromOptInProcessId also copies the confirmation email text; supplied settings override the copy. A page parameter is a name the platform fills with contact data; a UTM parameter is a value under a fixed name; both require the redirect URL in the same call. The change-email role is set separately with update-opt-in-process. Returns both process and email IDs.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Name of the new process; must be free within the account
- `notes` — null | string (maxLength 2000): Internal note, not visible to contacts
- `optInMode` — null | string (einer von `double`, `single`): "double" for a confirmation email, "single" without one; defaults to double
- `pendingRedirectUrl` — null | string (maxLength 2000): URL a contact reaches after subscribing, before confirming; omit for the KlickTipp page
- `confirmedRedirectUrl` — null | string (maxLength 2000): URL a contact reaches after confirming; omit for the KlickTipp page
- `resendConfirmationEmail` — null | boolean: Whether an already pending contact receives the confirmation email again on a repeated subscription
- `deletePendingSubscribersAfterDays` — null | integer (einer von `0`, `1`, `3`, `7`, `14`): Days after which unconfirmed contacts are deleted, one of 0, 1, 3, 7, 14; 0 keeps them
- `metaLabels` — array<string> (maxItems 50): Labels of the new process
- `pendingPageParameters` — object: Query parameters appended to pendingRedirectUrl, by the name each is appended under; needs pendingRedirectUrl in the same call
  - `subscriberParameterName` — string (maxLength 100)
  - `emailParameterName` — string (maxLength 100)
  - `listParameterName` — string (maxLength 100)
  - `subscriberKeyParameterName` — string (maxLength 100)
- `confirmedPageParameters` — object: Query parameters appended to confirmedRedirectUrl, by the name each is appended under; needs confirmedRedirectUrl in the same call
  - `subscriberParameterName` — string (maxLength 100)
  - `emailParameterName` — string (maxLength 100)
  - `listParameterName` — string (maxLength 100)
  - `subscriberKeyParameterName` — string (maxLength 100)
  - `referralLinkParameterName` — string (maxLength 100): Name the referral link is appended under; only together with referralLinkId
  - `referralLinkId` — integer (minimum 0): ID of the account's own referral-link tool, as get-opt-in-process reports it; 0 means no referral link, and then referralLinkParameterName has to be empty too
- `pendingUtmParameters` — object: Campaign tracking values appended to pendingRedirectUrl, by query name; the value, not the name; needs pendingRedirectUrl in the same call
  - `utm_source` — string (maxLength 200)
  - `utm_medium` — string (maxLength 200)
  - `utm_campaign` — string (maxLength 200)
  - `utm_term` — string (maxLength 200)
  - `utm_content` — string (maxLength 200)
- `confirmedUtmParameters` — object: The same for confirmedRedirectUrl; needs confirmedRedirectUrl in the same call
  - `utm_source` — string (maxLength 200)
  - `utm_medium` — string (maxLength 200)
  - `utm_campaign` — string (maxLength 200)
  - `utm_term` — string (maxLength 200)
  - `utm_content` — string (maxLength 200)
- `copyFromOptInProcessId` — null | integer (minimum 1): Existing process to copy settings and confirmation email from; the arguments above still win
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-opt-in-process` · I

**Update opt-in process**

Updates an opt-in process’s name, mode, redirects, resend policy, change-email role, pending-contact deletion, labels and notes. Omitted settings stay; changes affect future signups without sending now. Single opt-in skips confirmation and requires the user’s approval. A page parameter is a name the platform fills with contact data; a UTM parameter is a value under a fixed name. Both require the corresponding redirect URL in the same call; taking the change-email role removes it from the previous process. Confirmation email content is updated separately.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process to change
- `name` — null | string (minLength 1; maxLength 250): New name; omit to keep the current one
- `notes` — null | string (maxLength 2000): Internal note, not visible to contacts; empty string clears it
- `optInMode` — null | string (einer von `double`, `single`): "double" for a confirmation email, "single" without one
- `pendingRedirectUrl` — null | string (maxLength 2000): URL a contact reaches after subscribing, before confirming; empty string restores the KlickTipp page
- `confirmedRedirectUrl` — null | string (maxLength 2000): URL a contact reaches after confirming; empty string restores the KlickTipp page
- `resendConfirmationEmail` — null | boolean: Whether an already pending contact receives the confirmation email again on a repeated subscription
- `useForChangeEmail` — null | boolean: Whether this process handles email address changes; true takes that role away from the process that holds it
- `deletePendingSubscribersAfterDays` — null | integer (einer von `0`, `1`, `3`, `7`, `14`): Days after which unconfirmed contacts are deleted, one of 0, 1, 3, 7, 14; 0 keeps them
- `metaLabels` — array<string> (maxItems 50): Complete list of labels; replaces the existing labels, empty array removes them all
- `pendingPageParameters` — object: Query parameters appended to pendingRedirectUrl, by the name each is appended under; needs pendingRedirectUrl in the same call
  - `subscriberParameterName` — string (maxLength 100)
  - `emailParameterName` — string (maxLength 100)
  - `listParameterName` — string (maxLength 100)
  - `subscriberKeyParameterName` — string (maxLength 100)
- `confirmedPageParameters` — object: Query parameters appended to confirmedRedirectUrl, by the name each is appended under; needs confirmedRedirectUrl in the same call
  - `subscriberParameterName` — string (maxLength 100)
  - `emailParameterName` — string (maxLength 100)
  - `listParameterName` — string (maxLength 100)
  - `subscriberKeyParameterName` — string (maxLength 100)
  - `referralLinkParameterName` — string (maxLength 100): Name the referral link is appended under; only together with referralLinkId
  - `referralLinkId` — integer (minimum 0): ID of the account's own referral-link tool, as get-opt-in-process reports it; 0 means no referral link, and then referralLinkParameterName has to be empty too
- `pendingUtmParameters` — object: Campaign tracking values appended to pendingRedirectUrl, by query name; the value, not the name; needs pendingRedirectUrl in the same call
  - `utm_source` — string (maxLength 200)
  - `utm_medium` — string (maxLength 200)
  - `utm_campaign` — string (maxLength 200)
  - `utm_term` — string (maxLength 200)
  - `utm_content` — string (maxLength 200)
- `confirmedUtmParameters` — object: The same for confirmedRedirectUrl; needs confirmedRedirectUrl in the same call
  - `utm_source` — string (maxLength 200)
  - `utm_medium` — string (maxLength 200)
  - `utm_campaign` — string (maxLength 200)
  - `utm_term` — string (maxLength 200)
  - `utm_content` — string (maxLength 200)
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `delete-opt-in-process` · D

**Delete opt-in process**

Deletes an opt-in process and its confirmation email permanently; existing contacts keep their subscriptions. Refuses the default process or one still referenced by forms, campaigns or other entities, naming dependencies. Requires the user to request deletion of this process ID.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process to delete
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-opt-in-confirmation-email` · RI

**Get opt-in confirmation email**

Reads an opt-in confirmation email’s subject and sender settings, with sendable sender addresses, confirmed CC/BCC options, domains and identity status. An empty stored sender or reply-to follows the account address. Single opt-in processes store this email but do not send it. The body is read by get-opt-in-confirmation-email-content; drag-and-drop block tools do not support it. Change settings with update-opt-in-confirmation-email.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is read
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-opt-in-confirmation-email` · I

**Update opt-in confirmation email**

Updates an opt-in confirmation email’s subject, sender, reply-to, CC, BCC or domain. Omitted values stay, though the domain may be normalized; ordinary senders need a configured address with a verified domain, derived when omitted. A dispatch profile decides its own sender and domain. The body is updated separately. This email records consent: change sender or subject only at the user’s request.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is changed
- `subject` — null | string (minLength 1; maxLength 250): Subject line of the confirmation email
- `senderName` — null | string (minLength 1; maxLength 250): Name the email comes from
- `senderEmail` — null | string (maxLength 250): Configured sender address; empty uses the account's address; "dispatchProfile" uses the sender profile for both address and domain (omit senderDomain)
- `replyToEmail` — null | string (maxLength 250): Address a reply goes to; empty string returns it to the account's own address
- `ccEmail` — null | string (maxLength 250): Address that receives a copy; empty string removes it
- `bccEmail` — null | string (maxLength 250): Address that receives a blind copy; empty string removes it
- `senderDomain` — null | string (maxLength 250): Domain the email is sent through; omit to derive it from the resulting sender address
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-opt-in-confirmation-email-content` · RI

**Get opt-in confirmation email content**

Reads an opt-in confirmation email’s subject, HTML and plain-text bodies and content type. Both bodies are returned; the recipient’s mail client chooses which to show. This is rich text, not a drag-and-drop document. Sender settings are read by get-opt-in-confirmation-email.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is read
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-opt-in-confirmation-email-content` · I

**Update opt-in confirmation email content**

Replaces the supplied HTML or plain-text body of an opt-in confirmation email in full; omitted parts stay and may then disagree, so supply both for a consistent message. Validation errors refuse the write with stored false and validationMessages; warnings do not. This email records consent and must still identify who is subscribing to what. Change it only at the user’s request.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is written
- `html` — null | string (maxLength 500000): Complete HTML body; replaces the current one, empty string makes the email plain-text only
- `plain` — null | string (maxLength 500000): Complete plain-text body; replaces the current one
- `subject` — null | string (minLength 1; maxLength 150): Subject line
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `preview-opt-in-confirmation-email` · ROI

**Preview opt-in confirmation email**

Previews an opt-in confirmation email’s stored body without sending or creating a contact. Recipient data, signature and confirmation link are added only at send time; plain-only emails show their text. Returns contentHtml when MCP Apps are unavailable. To receive a real one, use send-opt-in-confirmation-email-test.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is shown
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `send-opt-in-confirmation-email-test` · DO

**Send opt-in confirmation email test**

Sends an opt-in confirmation email test to one named address. A new address becomes a tagged test contact, potentially starting automations; tell the user before sending. The test confirmation link confirms nobody, and the process’s subscribers are not recipients.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is sent
- `recipientEmail`* — string (minLength 3; maxLength 250): Address the test goes to; becomes a contact of the account if it is not one yet
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-opt-in-process-redirect-url` · RI

**Get subscription redirect URL**

Resolves the opt-in redirect URL for a specified contact email. The URL includes that contact’s ID, address and subscriber key: use only the intended person’s address. It points to the pending or confirmed page according to status; without a custom page it uses KlickTipp’s hosted page.

Parameter:

- `email`* — string (minLength 3; maxLength 250): Email address of the contact the URL is resolved for; required, and it identifies which contact the URL points at
- `optInProcessId` — null | integer (minimum 1): Opt-in process to resolve for; omit for the one the subscriber signed up through
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
