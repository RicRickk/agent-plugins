# Die veröffentlichten Verträge — Kontakte und Konto-Einstellungen

Wort für Wort das, was der Server in `tools/list` für die 13 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## Inhalt

`search-contacts` · `get-contact` · `upsert-subscribed-contact` · `update-contact-values` ·
`update-contact-email` · `delete-contact` · `subscribe-contact-via-opt-in-process` ·
`unsubscribe-contact` · `get-contact-history` · `add-contact-history-note` ·
`search-duplicate-contacts` · `get-account-settings` · `update-account-settings`

## `search-contacts` · RI

**Search contacts**

Searches contact email and SMS channels by address, status, channel or tag (manual or smart tag), paginated by cursor. A contact with both channels appears twice. A contact with neither email address nor mobile number appears once with channel "none" and status "none"; an address or status filter leaves it out. Phone queries need a country code; contact fields are available through get-contact.

Parameter:

- `query` — null | string (maxLength 250): Case-insensitive fragment of an email address, or a mobile number with its country code; omit to match every contact
- `status` — null | string (einer von `pending`, `optin`, `subscribed`, `unsubscribed`): Subscription status to filter by; omit for every status
- `tagId` — null | integer (minimum 1): ID of a tag of the account the returned contacts must have, manual or smart tag
- `channel` — null | string (einer von `email`, `sms`, `none`): Restrict to email, sms, or none for contacts without either; omit for all
- `cursor` — null | string (maxLength 500): Opaque nextCursor value of the previous result page; omit for the first page
- `pageSize` — integer (minimum 1; maximum 100; Default `25`): Maximum contacts on the page, from 1 through 100
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-contact` · RI

**Get contact**

Reads one contact’s email and SMS statuses, fields for a reference, manual tag IDs and edit link. Missing channels are empty. Dates and times use the account’s displayed format and time zone.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `referenceId` — integer (minimum 0; Default `0`): Reference whose multi-value fields and manual tags to read; 0 for contact-wide values
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `upsert-subscribed-contact` · DO

**Create contact**

Creates or updates a contact by hand, immediately subscribing the supplied email address, mobile number or both without opt-in confirmation. Existing field values supplied here are overwritten; automations may start. Unsubscribed addresses and unknown field IDs or tags are refused, never skipped. Requires add-contacts permission and counts toward the daily import limit. To let an address confirm through an opt-in process, use subscribe-contact-via-opt-in-process instead.

Parameter:

- `email` — null | string (maxLength 250): Email address of the contact; at least one of email and phoneNumber is required
- `phoneNumber` — null | string (maxLength 50): Mobile number with country code, as +49170... or 0049170...; at least one of email and phoneNumber is required
- `tagId` — null | integer (minimum 1): Manual tag to assign to the contact; omit for none
- `fields` — array<object> (maxItems 50): Contact field values to write with the contact, each {fieldId, value} as get-contact and search-custom-fields name them
  - `fieldId`* — string (minLength 1; maxLength 15)
  - `value`* — string (maxLength 65535)
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-contact-values` · DO

**Update contact**

Updates specified contact-field values without changing subscription or channel state. Accepts displayed or ISO 8601 dates and times. An empty value clears a field.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `fields`* — array<object> (minItems 1; maxItems 50): Contact field updates; fieldId must be a global field key or an account-owned numeric custom-field ID, a date, time or datetime value takes the form get-contact answers with, and referenceId defaults to 0
  - `fieldId`* — string (minLength 1; maxLength 15)
  - `value`* — string (maxLength 65535)
  - `referenceId` — integer (minimum 0; Default `0`)
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-contact-email` · DOI

**Update Contact Email Address**

Replaces one email address of a contact while keeping its subscription status; no confirmation email is sent; the old address is gone, the change is recorded in the contact history and the mobile number stays. Without currentEmail the primary address is replaced; a contact merged from duplicates can have more, and the answer lists all of them. May start automations and counts toward the daily import limit. Refuses unsubscribed addresses, a currentEmail the contact does not have, addresses already used, invalid or blacklisted, accounts without the feature and calls once the daily import limit is reached.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `email`* — string (minLength 3; maxLength 254): The new email address
- `currentEmail` — null | string (minLength 3; maxLength 254): The contact's address to replace; omit for its primary address
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `delete-contact` · D

**Delete Contact**

Permanently deletes a contact, both channels, subscriptions, tags, field values and history. The contact leaves campaigns and automations; there is no undo. Only delete a contact the user explicitly asked to delete, after naming the contact back to them. To keep it, use unsubscribe-contact.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `subscribe-contact-via-opt-in-process` · DO

**Subscribe contact**

Subscribes one contact email or SMS channel via an opt-in process, creating or reusing the contact. May send confirmation and start automations; the optional tag may start further automations or outbound events. Accepts an email or phone number, never both; other channels stay unchanged.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process to run
- `approval`* — string (einer von `subscribe-contact`): Exactly "subscribe-contact": acknowledges a confirmation message, automations and a changed real recipient
- `email` — null | string (maxLength 250): Email channel to subscribe; mutually exclusive with phoneNumber
- `phoneNumber` — null | string (maxLength 50): SMS channel to subscribe in E.164 format; mutually exclusive with email
- `referenceId` — integer (minimum 0; Default `0`): Subscription reference context to create or reuse; a non-zero ID must exist in the account
- `tagId` — null | integer (minimum 1): Tag to additionally assign to the contact after a successful subscription
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `unsubscribe-contact` · DOI

**Unsubscribe contact**

Unsubscribes one contact email or SMS channel, stopping future subscribed-audience messages on it and possibly starting automations. Takes email or phone, never both; other channels stay unchanged.

Parameter:

- `approval`* — string (einer von `unsubscribe-contact`): Exactly "unsubscribe-contact": acknowledges a changed real recipient and automations
- `email` — null | string (maxLength 250): Email channel to unsubscribe; mutually exclusive with phoneNumber
- `phoneNumber` — null | string (maxLength 50): SMS channel to unsubscribe in E.164 format; mutually exclusive with email
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-contact-history` · RI

**Get Contact History**

Reads a contact’s history of subscriptions, tagging, messages, feedback and notes, newest first and cursor-paginated. Entries include time, type, category and app text.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `category` — null | string (einer von `subscription`, `tagging`, `miscellaneous`, `other`): Only entries of this group of the app's history filter; omit for every entry
- `cursor` — null | string (maxLength 500): Opaque nextCursor value of the previous page; omit for the first page
- `pageSize` — integer (minimum 1; maximum 100; Default `50`): Maximum entries on the page, from 1 through 100
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-contact-history-note`

**Add Note to Contact History**

Adds a permanent internal note to a contact’s history. The contact never sees it; it does not start automations. Notes cannot be edited or removed.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `text`* — string (minLength 1; maxLength 5000): The note as plain text; line breaks are kept
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `search-duplicate-contacts` · RI

**Search Duplicate Contacts**

Searches potential duplicate contact pairs with detection reason and confidence, cursor-paginated. Defaults to open pairs; a pair can appear from both sides. Merging or rejecting happens in the app; merging deletes the duplicate contact without undo.

Parameter:

- `status` — string (einer von `open`, `rejected`, `completed`, `all`; Default `open`): open, rejected, completed or all; default open
- `probability` — null | string (einer von `middle`, `high`, `very-high`, `maximum`, `manual`): Only this detection level: middle, high, very-high, maximum or manual; omit for every level
- `contactId` — null | integer (minimum 1): Only duplicates of this primary contact
- `cursor` — null | string (maxLength 500): Opaque nextCursor value of the previous result page; omit for the first page
- `pageSize` — integer (minimum 1; maximum 50; Default `25`): Maximum duplicates on the page, from 1 through 50
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-account-settings` · RI

**Get Account Settings**

Reads editable account switches, preview marker tag and email blacklist. Inaccessible settings are absent, not false; connected-service credentials are reported only as configured or not, never by value. Personal, privacy, legal and sender-address settings are excluded.

Parameter:

- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-account-settings` · I

**Update Account Settings**

Updates only named account settings and returns the current state. Inaccessible settings, unknown preview tags or malformed blacklists refuse the whole call before writing; credentials cannot be changed here. The result’s refusals lists settings the platform rejected during save, while other changes may have been stored.

Parameter:

- `settings`* — object: The settings to change, by name; every setting left out keeps its value
  - `enableMetaLabels` — boolean
  - `enableNotes` — boolean
  - `enableDdEditorManualSaveButton` — boolean
  - `disableEmailSignatureSeparator` — boolean
  - `deactivateUserNotificationEmails` — boolean
  - `plainTextContentByUser` — boolean
  - `useEnglishSubscriberArea` — boolean
  - `deactivateGlobalBounceManagement` — boolean
  - `unlimitedEmailsPerDay` — boolean
  - `allowSingleOptInProcess` — boolean
  - `allowSignaturesWithoutParameters` — boolean
  - `allowKlicktippSenderAddress` — boolean
  - `allowEmailRewriting` — boolean
  - `knownForSpamActivity` — boolean
  - `previewSubscriberMarkerTag` — string (maxLength 100; Muster `^[0-9]*$`): ID of an existing tag of this account that marks preview subscribers; empty string removes it
  - `emailBlacklist` — string (maxLength 100000): Addresses and domains this account never sends to, one per line; empty string clears it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
