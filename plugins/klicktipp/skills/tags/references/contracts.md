# Die veröffentlichten Verträge — Tags

Wort für Wort das, was der Server in `tools/list` für die 7 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## Inhalt

`search-tags` · `get-tag` · `create-manual-tag` · `update-manual-tag` · `delete-manual-tag` ·
`tag-contact` · `untag-contact`

## `search-tags` · RI

**Search tags**

Searches account tags by name, type, writability, per-subscription cardinality or system role. Includes manual and event-generated tags with ID, name and type; get-tag reads their meaning.

Parameter:

- `query` — null | string (maxLength 250): Text the name of a tag has to contain; omit to list them all
- `type` — null | string (einer von `apikey-subscribed`, `automation-finished`, `automation-started`, `businesscard-subscribed`, `campaign-clicked`, `campaign-converted`, `campaign-opened`, `campaign-sent`, `campaign-viewed`, `digistore-affiliation`, `email-clicked`, `email-opened`, `email-sent`, `email-viewed`, `event-subscribed`, `facebook-audience`, `form-subscribed`, `kajabi-activated`, `kajabi-deactivated`, `landing-page-subscribed`, `outbound-activated`, `payment-chargeback`, `payment-completed`, `payment-deferred`, `payment-expired`, `payment-received`, `payment-refunded`, `payment-subsequent`, `plugin-inbound-finished`, `plugin-inbound-inprogress`, `plugin-inbound-ready`, `plugin-inbound-started`, `rebill-canceled`, `rebill-canceled-lastday`, `rebill-resumed`, `request-email-subscribed`, `request-sms-subscribed`, `smartlink`, `sms-clicked`, `sms-sent`, `tag`, `taggingpixel-triggered`, `unknown`): Only tags of this type, "tag" being the manual ones; omit for every type
- `onlyWritable` — null | boolean: Only manual tags the write tools may touch; omit to include the ones KlickTipp sets itself
- `multiValue` — null | boolean: true: tags a contact can carry once per subscription; false: once overall; omit for both
- `systemRole` — null | string (einer von `test-contact`): Only tags with this system role; "test-contact" marks contacts that receive test emails
- `limit` — null | integer (minimum 1; maximum 200): How many tags to return at most, 1 to 200, 50 by default
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-tag` · RI

**Get tag**

Reads a tag’s type, meaning, origin, writability, notes, labels and contact count. Also reports tags automatically subscribed or unsubscribed when assigned, whether it marks test contacts, and usedBy: the automations, newsletters, forms and other entities that reference it.

Parameter:

- `tagId`* — integer (minimum 1): ID of the tag, as shown in the KlickTipp app URL
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `create-manual-tag`

**Create manual tag**

Creates a manual tag with a unique account name and optional meaning. Assigns it to no contacts and triggers no automations.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Name of the tag, which has to be unique within the account and cannot be a number alone
- `description` — null | string (maxLength 2000): What the tag stands for, so a person or a model reading it later knows when to assign it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-manual-tag` · I

**Update manual tag**

Updates a manual tag’s name or description; system-generated tags are refused. Renaming appears wherever the tag is displayed but keeps its ID, contacts and campaign references. Other tag settings stay unchanged.

Parameter:

- `tagId`* — integer (minimum 1): ID of the manual tag to change
- `name` — null | string (maxLength 250): New name of the tag, which has to stay unique within the account; omit to keep the current one
- `description` — null | string (maxLength 2000): New description of what the tag stands for; omit to keep the current one
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `delete-manual-tag` · DOI

**Delete manual tag**

Deletes a manual tag permanently and removes it from every contact carrying it. System tags and tags referenced by campaigns, automations or other entities are refused with dependencies. Requires the user to request deletion of this tag.

Parameter:

- `tagId`* — integer (minimum 1): ID of the manual tag to delete
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `tag-contact` · O

**Assign manual tag**

Assigns an existing manual tag to a contact; this may start campaigns, outbound events or automations. Requires approval of those effects; does not create tags.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `manualTagId`* — integer (minimum 1): Existing writable manual tag ID; unknown tags are rejected and never created
- `approval`* — string (einer von `I_ACCEPT_AUTOMATION_EFFECTS`): Exactly I_ACCEPT_AUTOMATION_EFFECTS: tagging may start campaigns and automations
- `referenceId` — integer (minimum 0; Default `0`): Reference for a multi-value manual tag; use 0 for contact-wide tags
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `untag-contact` · DOI

**Remove manual tag**

Removes an existing manual tag from a contact; this may alter campaign queues and automations. Requires approval of those effects. Does not unsubscribe the contact.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `manualTagId`* — integer (minimum 1): Existing writable manual tag ID to remove
- `approval`* — string (einer von `I_ACCEPT_AUTOMATION_EFFECTS`): Exactly I_ACCEPT_AUTOMATION_EFFECTS: removal may alter campaigns and automations
- `referenceId` — integer (minimum 0; Default `0`): Reference for a multi-value manual tag; use 0 for contact-wide tags
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
