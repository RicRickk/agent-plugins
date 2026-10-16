# Die veröffentlichten Verträge — Newsletter, Versand, Signaturen und Absenderdomains

Wort für Wort das, was der Server in `tools/list` für die 22 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## Inhalt

`search-newsletters` · `get-newsletter` · `create-newsletter-draft` · `update-newsletter-draft` ·
`delete-newsletter-draft` · `configure-newsletter-delivery` · `send-newsletter-test` ·
`preview-personalized-newsletter` · `prepare-newsletter-dispatch` · `cancel-newsletter-dispatch` ·
`search-signatures` · `get-signature` · `create-signature` · `update-signature` ·
`replace-signature-content` · `configure-signature-delivery` · `list-sender-domains` ·
`get-sender-domain` · `get-sender-domain-dns-setup` · `create-sender-domain` ·
`request-sender-domain-dns-check` · `validate-account-sending-readiness`

## `search-newsletters` · RI

**Search newsletters**

Searches email newsletters by name, delivery status or creation/dispatch dates, newest first and cursor-paginated. Drafts have no dispatch date; split tests have no single email ID. Excludes SMS newsletters and follow-ups.

Parameter:

- `query` — null | string (maxLength 250): Text the name of a newsletter has to contain; omit to list them all
- `status` — null | string (einer von `draft`, `scheduled`, `outgoing`, `sent`): Only newsletters in this delivery state: "draft", "scheduled", "outgoing" or "sent"
- `createdFrom` — null | string (Muster `^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(:\d{2})?([Zz]|[+-]\d{2}:?\d{2})$`): Created at or after this moment, ISO 8601 with UTC offset ("2026-09-01T10:00:00+02:00")
- `createdBefore` — null | string (Muster `^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(:\d{2})?([Zz]|[+-]\d{2}:?\d{2})$`): Only newsletters created before this moment, exclusive, same format
- `sendDateFrom` — null | string (Muster `^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(:\d{2})?([Zz]|[+-]\d{2}:?\d{2})$`): Dispatch moment at or after this one, same format; a draft has none and never matches
- `sendDateBefore` — null | string (Muster `^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(:\d{2})?([Zz]|[+-]\d{2}:?\d{2})$`): Only newsletters whose dispatch moment lies before this one, exclusive, same format
- `limit` — null | integer (minimum 1; maximum 100): How many newsletters to return at most, 1 to 100, 25 by default
- `cursor` — null | string (minLength 8; maxLength 200): nextCursor of the previous page, with the same filters; omit for the first page
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-newsletter` · RI

**Get newsletter**

Reads an email newsletter’s identity and lifecycle, with optional metadata, audience, delivery, reach and conversion-pixel projections. The body is in get-email-editor-content. For split tests, deliveryConfiguration needs a variant editorUrl; there is no single email ID. Hand conversion-pixel snippets to the user verbatim for installation.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter, as shown in the KlickTipp app URL
- `include` — array<string> (maxItems 6): Projections to add: "metadata", "audience", "deliveryConfiguration", "deliveryStatus", "audienceReach", "conversionPixel"; omit for identity and lifecycle only. The body is get-email-editor-content
- `editorUrl` — null | string (minLength 12; maxLength 500): Editor URL naming one variant of a split test, from splitTestVariants; omit for a newsletter with a single email
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `create-newsletter-draft`

**Create newsletter draft**

Creates an email newsletter draft with a subject and optional preheader. The subject is the line every recipient sees; correcting it through update-newsletter-draft invalidates the content revisions read before. Audience defaults to all_contacts, reaching every active contact when sent. splitTest is irreversible, needs a premium account (conversions/revenue also the conversion pixel) and starts with one variant; add more with add-newsletter-split-test-variant. emailEditor defaults to drag-and-drop and is fixed at creation. Next steps: body with the block tools, audience with update-newsletter-draft, sender with configure-newsletter-delivery. Nothing is sent.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Name of the newsletter, unique within the account
- `subject`* — string (minLength 1; maxLength 998): Subject line, without HTML. It is the line every recipient sees, and no part of it is derived from anything else in this call. Correcting it later is update-newsletter-draft, which invalidates the content revisions read before
- `notes` — null | string (maxLength 1000): Internal note about the purpose of this newsletter, never part of the email
- `preheader` — null | string (maxLength 120): Inbox preview line, at most 120 characters, without HTML; omit to leave it empty. Not part of the content document: an HTML import cannot set it
- `splitTest` — null | object: Makes the newsletter a split test, irreversibly: "testSizePercent" (2-98), "testDurationHours" (1-27777), "winnerBy" ("opens", "clicks", "conversions", "revenue"; the last two need the conversion pixel). All three are required and KlickTipp has no default for any of them, so any value here is a choice somebody made; together they settle what share of real recipients gets a test version and for how long. Needs a premium account; omit for a normal newsletter
  - `testSizePercent`* — integer (minimum 2; maximum 98)
  - `testDurationHours`* — integer (minimum 1; maximum 27777)
  - `winnerBy`* — string (einer von `opens`, `clicks`, `conversions`, `revenue`)
- `emailEditor` — null | string (einer von `drag-and-drop`, `rich-text`): Editor the email is created for. Omit it, which means "drag-and-drop": that is the editor KlickTipp builds on and the one every content and design tool works with. Pass "rich-text" only when the account authors in the previous HTML editor and asked for it. The choice cannot be changed afterwards
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-newsletter-draft` · I

**Update newsletter draft**

Updates an email newsletter draft’s name, note, subject, preheader, audience or UTM campaign name. Omitted fields stay; the supplied audience replaces the old one. Subject or preheader changes invalidate earlier content revisions. On split tests subject and preheader are refused; set them per variant with update-newsletter-split-test-variant. Sends nothing and sets no send date.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter to write, as returned by create-newsletter-draft
- `name` — null | string (maxLength 250): New name, unique within the account, at most 250 characters, without HTML; omit to keep
- `note` — null | string (maxLength 1000): Internal note, at most 1000 characters, without HTML; omit to keep
- `subject` — null | string (maxLength 998): New subject line, without HTML. Invalidates every contentRevision read before
- `audience` — object: Replaces the audience: "mode" is "all_contacts", "saved_audience" (with "audienceId") or "tag_conditions" (with the tag fields, at most 50 tags together); omit to keep
  - `mode`* — string (einer von `all_contacts`, `saved_audience`, `tag_conditions`): "all_contacts" (every active contact, no further field), "saved_audience" or "tag_conditions".
  - `audienceId` — integer (minimum 1): ID of the saved audience, for mode "saved_audience" only.
  - `includeTagIds` — array<integer> (maxItems 50): Tags a contact must carry, for "tag_conditions"; include and exclude together at most 50.
  - `includeTagsMatch` — string (einer von `any`, `all`): Whether "any" required tag is enough or "all" are needed.
  - `excludeTagIds` — array<integer> (maxItems 50): Tags that keep a contact out, for "tag_conditions"; include and exclude together at most 50.
  - `excludeTagsMatch` — string (einer von `any`, `all`): Whether "any" excluded tag already excludes or only "all" together do.
- `preheader` — null | string (maxLength 120): New inbox preview line, at most 120 characters, without HTML; empty string removes it, omit keeps it. Invalidates every contentRevision read before
- `utmCampaignName` — null | string (maxLength 120): Campaign name appended to tracked links as utm_campaign, at most 120 characters, without HTML; empty string restores the account default, omit keeps it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `delete-newsletter-draft` · D

**Delete newsletter draft**

Deletes an email newsletter draft, its email, audience conditions and system tags without undo. Refuses scheduled or sent newsletters, referenced drafts and split tests; dependency refusals name what still uses the draft; a split-test refusal returns the appUrl for manual deletion. Only delete a draft the user explicitly asked to delete.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter to delete
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `configure-newsletter-delivery` · I

**Configure newsletter delivery**

Configures a never-scheduled email newsletter’s sender, reply address, domain, signature and tracking settings. Omitted settings stay. Turning off link tracking requires a valid sending domain. Reports missing send requirements and usable identities; a changed sender address derives its verified domain. senderEmailMode and senderDomainMode use signature_dispatch_profile together or not at all. Split tests are refused; their variant senders are set in the app. Does not schedule or send.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter to configure
- `senderNameMode` — null | string (einer von `explicit`, `account_default`, `signature_dispatch_profile`): "explicit" (pass senderName), "account_default" or "signature_dispatch_profile"; omit to keep
- `senderName` — null | string (maxLength 250): Name the recipients see as the sender, for mode "explicit" only; omit to keep the current one
- `senderEmailMode` — null | string (einer von `explicit`, `account_default`, `signature_dispatch_profile`): "explicit" (pass senderEmail), "account_default" or "signature_dispatch_profile"; omit to keep
- `senderEmail` — null | string (maxLength 250): Sender address configured for the account; for mode "explicit"; omit to keep
- `replyToEmailMode` — null | string (einer von `explicit`, `account_default`, `signature_dispatch_profile`): "explicit" (pass replyToEmail), "account_default" or "signature_dispatch_profile"; omit to keep
- `replyToEmail` — null | string (maxLength 250): Address answers go to, for mode "explicit" only; omit to keep the current one
- `senderDomainMode` — null | string (einer von `explicit`, `account_default`, `signature_dispatch_profile`): "explicit" (pass senderDomain), "account_default" for automatic resolution or "signature_dispatch_profile"; omit to keep
- `senderDomain` — null | string (maxLength 250): Matching verified domain; for mode "explicit"; omit to derive it when changing the sender address
- `signatureId` — null | integer (minimum 0): ID of the signature under the newsletter; 0 lets KlickTipp pick one by tagging; omit to keep
- `linkTracking` — null | boolean: Whether KlickTipp rewrites the links so clicks are counted; true is the normal case, omit to keep
- `headerLinks` — null | boolean: Whether KlickTipp puts its own line above the body with browser view, unsubscribe and report-spam links; omit to keep
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `send-newsletter-test` · DO

**Send newsletter test**

Sends a newsletter’s published email as a test to one specified address, not its audience. An address not yet in the account becomes a tagged test contact and may start automations. Name the address and disclose that effect before calling. A never-published body is refused (publish it with publish-newsletter-email-content); edits made since publication are not sent (the test uses the older published body). For a split test, messageId selects the variant emailId.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter to send a test of
- `recipientEmail`* — string (minLength 3; maxLength 250): Address to send the test to; any address, and one that is not a contact yet becomes one
- `messageId` — null | integer (minimum 1): For a split test: the emailId of the variant to test, as get-newsletter-split-test lists it; omit otherwise
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `preview-personalized-newsletter` · DO

**Preview Personalized Newsletter**

Previews a published newsletter email personalized for one contact, including placeholders and signature. Unpublished edits are not shown; preview-email-editor shows the draft instead. AI previews may consume credits. For a split test specify messageId. Sends nothing and changes no contact. Campaign and notification emails use preview-personalized-email.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the email newsletter
- `contactId`* — integer (minimum 1): ID of the contact to personalize for, from search-contacts or get-contact
- `referenceId` — integer (minimum 0; Default `0`): Reference of the contact's subscription; 0 for the default one
- `messageId` — null | integer (minimum 1): For a split test: messageId of the variant, from get-newsletter-split-test; omit otherwise
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account of the access token

## `prepare-newsletter-dispatch` · DO

**Activate newsletter**

Sends or schedules an email newsletter after the user confirms the recipient estimate in the client's elicitation dialog; no, cancel or no answer sends nothing. Clients without elicitation are refused with the newsletter's schedule page, where the user sends in KlickTipp. Sent mail cannot be recalled. Unpublished edits are refused; publish them with publish-newsletter-email-content first. Requires an explicit mode and UTC offset for scheduled sends; split tests require every variant published. Read deliveryStatus via get-newsletter.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter to send
- `mode`* — string (einer von `immediate`, `scheduled`): "immediate" or "scheduled"; no default
- `scheduledAt` — null | string (Muster `^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(:\d{2})?([Zz]|[+-]\d{2}:?\d{2})$`): Moment to send at, ISO 8601 with UTC offset; required for "scheduled", forbidden for "immediate"
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `cancel-newsletter-dispatch` · D

**Cancel a newsletter dispatch**

Cancels a scheduled or ongoing email newsletter dispatch while canBeCancelled is true, returning it to draft and stopping further sends. Already sent mail cannot be recalled. Content and audience stay; prepare-newsletter-dispatch activates it again. Requires the user’s approval before stopping a deliberate dispatch.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter whose dispatch is to be called off
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `search-signatures` · RI

**Search email signatures**

Searches email signatures by name with sender readiness, selection tags and business-card availability (required by add-email-editor-contact-card). Unusable signatures are excluded unless includeUnusable is true, which also returns blockers. Content is read by get-signature; to select signatures automatically by tags, pass signature ID 0 to configure-newsletter-delivery.

Parameter:

- `query` — null | string (maxLength 250): Text the name of a signature has to contain; omit to list them all
- `includeUnusable` — null | boolean: True to also return signatures that cannot currently be used, with their blockers; omit to leave them out
- `limit` — null | integer (minimum 1; maximum 200): How many signatures to return at most, 1 to 200, 50 by default
- `accountId` — null | integer (minimum 1): User ID of the account to list signatures for; omit for the token account, or pass an accessible subaccount ID

## `get-signature` · RI

**Get email signature**

Reads one email signature with its name, notes, labels, tag IDs, sender profile, digital business card, content flags, usability and blockers. includeContent adds the HTML, plain and transactional content itself, which is the bulk of the answer. isUsable includes the effective sender identity and domain; an empty stored senderEmail follows the account address.

Parameter:

- `signatureId`* — integer (minimum 1): ID of the signature to read
- `includeContent` — null | boolean: True to include HTML, plain and transactional content; omit to return only content flags
- `accountId` — null | integer (minimum 1): User ID of the account that owns the signature; omit for the token account, or pass an accessible subaccount ID

## `create-signature` · O

**Create email signature**

Creates or copies an email signature. Name and tag IDs replace the source values; other supplied fields override copied ones, and omitted copied fields stay. HTML requires %Link:Unsubscribe% as the href of a link and %User:FirstName%, %User:LastName%, %User:Street%, %User:Zip%, %User:City% and %User:Country% (permitted address omissions excepted); plain text needs these too, though unsubscribe may be text. Transactional HTML requires address fields but no unsubscribe link; %Link:SubscriberInfo% is recommended. Plain text is stored only when plain-content editing is allowed, otherwise regenerated from HTML. Tags and sender address must exist; the sender needs a verified domain, and an omitted sender domain is derived and stored. Returns content flags only; use get-signature with includeContent true. No newsletter changes.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Unique name of the new signature
- `tagIds`* — array<integer> (maxItems 50): At least one existing tag ID for the new signature; every tag must be unassigned to another signature
- `sourceSignatureId` — null | integer (minimum 1): Existing signature of the same account to copy; omit when supplying content for a new signature
- `content` — object: Complete HTML, plain and transactional content block; required without a source and replaces copied content when supplied
  - `html`* — string (minLength 1; maxLength 65536)
  - `plain` — string (maxLength 65536)
  - `useInTransactionalEmails` — boolean
  - `transactionalHtml` — string (maxLength 65536)
- `senderProfile` — object: Optional sender, reply, CC, BCC, recipient and sender-domain fields; omitted copied fields are preserved, and the sender domain is derived from the resulting sender address when omitted
  - `senderName` — string (maxLength 250)
  - `senderEmail` — string (maxLength 250)
  - `replyToEmail` — string (maxLength 250)
  - `ccEmail` — string (maxLength 250)
  - `bccEmail` — string (maxLength 250)
  - `toEmail` — string (maxLength 250)
  - `senderDomain` — string (maxLength 250)
- `vCard` — object: Optional plain-text digital-business-card fields; supplied fields override copied values, omitted copied fields stay, and empty strings clear fields
  - `firstName` — string (maxLength 128)
  - `lastName` — string (maxLength 128)
  - `companyName` — string (maxLength 128)
  - `emailAddress` — string (maxLength 128)
  - `phone` — string (maxLength 128)
  - `cellPhone` — string (maxLength 128)
  - `street` — string (maxLength 128)
  - `zip` — string (maxLength 128)
  - `city` — string (maxLength 128)
  - `state` — string (maxLength 128)
  - `country` — string (maxLength 128)
  - `website` — string (maxLength 250)
- `notes` — null | string (maxLength 1000): Internal note; on a copy, omit to preserve the source note
- `metaLabels` — null | array<string> (maxItems 50): Labels; on a copy, omit to preserve the source labels
- `accountId` — null | integer (minimum 1): User ID of the account in which to create the signature; omit for the token account, or pass an accessible subaccount ID

## `update-signature` · I

**Update email signature**

Updates an email signature's name, internal note, labels or digital business card; omitted fields stay and empty business-card strings clear them. Content, tag IDs and sender profile are never changed.

Parameter:

- `signatureId`* — integer (minimum 1): ID of the signature to update
- `name` — null | string (minLength 1; maxLength 250): New unique name; omit to keep it, and note that the default signature cannot be renamed
- `notes` — null | string (maxLength 1000): New internal note; omit to keep it, or pass an empty string to clear it
- `metaLabels` — null | array<string> (maxItems 50): Replacement labels; omit to keep them, or pass an empty array to clear them
- `vCard` — object: Plain-text digital-business-card fields to change; omitted fields stay unchanged and empty strings clear fields
  - `firstName` — string (maxLength 128)
  - `lastName` — string (maxLength 128)
  - `companyName` — string (maxLength 128)
  - `emailAddress` — string (maxLength 128)
  - `phone` — string (maxLength 128)
  - `cellPhone` — string (maxLength 128)
  - `street` — string (maxLength 128)
  - `zip` — string (maxLength 128)
  - `city` — string (maxLength 128)
  - `state` — string (maxLength 128)
  - `country` — string (maxLength 128)
  - `website` — string (maxLength 250)
- `accountId` — null | integer (minimum 1): User ID of the account that owns the signature; omit for the token account, or pass an accessible subaccount ID

## `replace-signature-content` · DOI

**Replace email signature content**

Replaces an email signature’s HTML and plain content in full, without MCP undo. HTML requires %Link:Unsubscribe% as the href of a link and %User:FirstName%, %User:LastName%, %User:Street%, %User:Zip%, %User:City% and %User:Country% (permitted address omissions excepted). Plain text needs the same but may show unsubscribe as text; it is stored only when plain-content editing is allowed, otherwise regenerated from HTML. Transactional fields change only when supplied; transactional content needs address fields and no unsubscribe link, %Link:SubscriberInfo% is recommended. useInTransactionalEmails false with an empty transactionalHtml disables and clears it. Returns content flags only; use get-signature with includeContent true. Metadata, tags and sender stay unchanged.

Parameter:

- `signatureId`* — integer (minimum 1): ID of the signature whose normal content is replaced and whose transactional content may be changed
- `html`* — string (minLength 1; maxLength 65536): Complete HTML signature content
- `plain` — null | string (maxLength 65536): Complete plain content; stored trimmed only when plain-content editing is enabled, otherwise regenerated from HTML
- `useInTransactionalEmails` — null | boolean: Whether the signature is used in transactional emails; omit to keep the current setting
- `transactionalHtml` — null | string (maxLength 65536): Complete transactional HTML content; omit to keep it, or pass an empty string with useInTransactionalEmails false to clear it
- `accountId` — null | integer (minimum 1): User ID of the account that owns the signature; omit for the token account, or pass an accessible subaccount ID

## `configure-signature-delivery` · OI

**Configure email signature delivery**

Configures an email signature’s assigned tags and sender, reply, CC, BCC, recipient or domain. Omitted fields stay. Tag IDs must exist and be unassigned to another signature; a changed sender needs a verified domain; the sender domain is derived and stored when omitted. Content and business card stay unchanged.

Parameter:

- `signatureId`* — integer (minimum 1): ID of the signature whose delivery configuration is changed
- `tagIds` — null | array<integer> (maxItems 50): Replacement tag IDs that already exist; ordinary signatures require at least one, and every tag must be unassigned to another signature, while the default signature may use an empty array
- `senderProfile` — object: Sender name and configured account address/domain values; reply options are also used for CC, BCC and recipient, empty strings clear optional fields, omitted fields stay unchanged, and the sender domain is derived when the sender address changes
  - `senderName` — string (maxLength 250)
  - `senderEmail` — string (maxLength 250)
  - `replyToEmail` — string (maxLength 250)
  - `ccEmail` — string (maxLength 250)
  - `bccEmail` — string (maxLength 250)
  - `toEmail` — string (maxLength 250)
  - `senderDomain` — string (maxLength 250)
- `accountId` — null | integer (minimum 1): User ID of the account that owns the signature; omit for the token account, or pass an accessible subaccount ID

## `list-sender-domains` · RI

**Search sender domains**

Lists configured sender domains with verification status, DKIM-only flag, default marker and DNS propagation wait. Reads stored state only; shared fallback infrastructure is excluded.

Parameter:

- `accountId` — null | integer (minimum 1): User ID of the account whose configured sender domains to list; omit for the account the access token belongs to, or pass a subaccount the token owner may configure

## `get-sender-domain` · RI

**Get sender domain**

Reads a sender domain’s stored verification status, usability, last DNS recheck and covered sender addresses, including subdomains. Listed addresses may still be unconfirmed; no DNS lookup occurs.

Parameter:

- `domainId`* — integer (minimum 1): ID of the sender domain, as shown in the domain settings
- `accountId` — null | integer (minimum 1): User ID of the account that owns the domain; omit for the account the access token belongs to, or pass a subaccount the token owner may configure

## `get-sender-domain-dns-setup` · RI

**Get sender domain DNS setup**

Reads expected sender-domain DNS records and their last stored actual state; no live lookup. For an eligible account and DKIM-only domain, domain.mailserverSetupFormUrl opens the manual mailserver request form. Expected type/value pairs are alternatives: publish exactly one per record, normally the first. A check result is fresh only when every checkedAt is at least lastDnsCheckRequestedAt; null means no result yet.

Parameter:

- `domainId`* — integer (minimum 1): ID of the sender domain whose required DNS records to read
- `accountId` — null | integer (minimum 1): User ID of the account that owns the domain; omit for the account the access token belongs to, or pass a subaccount the token owner may configure

## `create-sender-domain`

**Create sender domain**

Creates a sender-domain registration. The domain must be valid, not reserved, not registered by any KlickTipp account and within the account limit. It starts unverified and cannot send until DNS verification passes; no email is sent and it does not become the default.

Parameter:

- `domain`* — string (minLength 1; maxLength 250): Domain or subdomain to register, without a protocol, path, wildcard, or trailing dot
- `accountId` — null | integer (minimum 1): User ID of the account to create the sender domain in; omit for the account the access token belongs to, or pass a subaccount the token owner may configure

## `request-sender-domain-dns-check` · O

**Trigger sender domain DNS check**

Requests an asynchronous sender-domain DNS check without sending email. The per-domain cooldown is enforced; during it, returns cooldownActive and the next available time without queueing another check.

Parameter:

- `domainId`* — integer (minimum 1): ID of the sender domain to recheck
- `accountId` — null | integer (minimum 1): User ID of the account that owns the domain; omit for the account the access token belongs to, or pass a subaccount the token owner may configure

## `validate-account-sending-readiness` · RI

**Get account sending readiness**

Checks account newsletter-sending readiness from stored DNS state, sender addresses, signatures, opt-in processes and contacts. Blocking findings make readyToSend false; no contacts is informational. Does not start DNS checks or evaluate billing and feature access.

Parameter:

- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
