# Die veröffentlichten Verträge — Eigene Felder

Wort für Wort das, was der Server in `tools/list` für die 5 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## Inhalt

`search-custom-fields` · `get-custom-field` · `create-custom-field` · `update-custom-field` ·
`delete-custom-field`

## `search-custom-fields` · RI

**Search custom fields**

Searches custom-field definitions by name or data type, including IDs and email placeholders, the account's own fields newest first, then the global ones; paginated by cursor. Global fields are read-only; contact values are read with get-contact.

Parameter:

- `query` — null | string (maxLength 250): Text the name of a field has to contain; omit to list them all
- `types` — null | array<string>: Only fields of these data types, for example ["field-date", "field-datetime"]; omit for every type
- `onlyWritable` — null | boolean: Only the account's own fields, the ones the write tools may touch; omit to include the global fields
- `limit` — null | integer (minimum 1; maximum 200): How many fields to return at most, 1 to 200, 50 by default
- `cursor` — null | string (minLength 1; maxLength 500): nextCursor of the previous page, with the same filters; omit for the first page
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-custom-field` · RI

**Get custom field**

Reads one custom-field definition: type, placeholder, API key, metadata, copy target and whether values are per subscription. Contact values are read with get-contact.

Parameter:

- `customFieldId`* — string (minLength 1; maxLength 100; Muster `^[A-Za-z0-9_]+$`): Field ID: a number for the account's own field, a name such as "FirstName" for a global one
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `create-custom-field`

**Create custom field**

Creates a custom-field definition and returns its ID and email placeholder. The type cannot change later. multiValue defaults to one value per subscription; changing to one value per contact later deletes extra values and cannot be reversed. Stores no contact values.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Name of the field, which has to be unique within the account
- `type`* — string (einer von `field-single`, `field-paragraph`, `field-email`, `field-number`, `field-url`, `field-date`, `field-time`, `field-datetime`, `field-html`, `field-decimal`): Data type of the field, which decides what can be stored in it and cannot be changed afterwards
- `description` — null | string (maxLength 2000): What the field holds, so a person or a model reading it later knows what to write into it
- `multiValue` — null | boolean: True: one value per subscription; false: one value overall; omit for true
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-custom-field` · DI

**Update custom field**

Updates an account-owned custom field’s metadata, copy target or cardinality. Type and global fields cannot be changed. Setting multiValue false permanently deletes extra per-subscription values; ask the user before making that change. copyToFieldId needs a field of compatible type; fields sharing a requestName resolve to the first. Omitted fields stay.

Parameter:

- `customFieldId`* — string (minLength 1; maxLength 100; Muster `^[A-Za-z0-9_]+$`): ID of the field to change
- `name` — null | string (maxLength 250): New name of the field, which has to stay unique within the account; omit to keep the current one
- `description` — null | string (maxLength 2000): New description of what the field holds; omit to keep the current one
- `category` — null | string (maxLength 250): Group in the app; empty string sorts into none; omit to keep
- `metaLabels` — null | array<string> (maxItems 50): New set of labels of the field, which replaces the current one; omit to keep the current labels
- `multiValue` — null | boolean: False collapses the field to one value per contact and DELETES the others; true is refused on a field that is already false; omit to keep
- `requestName` — null | string (maxLength 250): Key this field is addressed by in a subscription email body; empty string removes it; omit to keep
- `notes` — null | string (maxLength 1000): Internal note on the field, which nobody outside the account sees; empty string removes it; omit to keep
- `copyToFieldId` — null | string (maxLength 100; Muster `^[A-Za-z0-9_]*$`): ID of the field every value written here is also copied into; empty string stops the copying; omit to keep
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `delete-custom-field` · DI

**Delete custom field**

Permanently deletes an account-owned custom field and all contacts’ values in it. Global fields and fields still used by forms, automations or other entities are refused, naming them; remaining placeholders render empty. Only delete a field the user explicitly asked to delete.

Parameter:

- `customFieldId`* — string (minLength 1; maxLength 100; Muster `^[A-Za-z0-9_]+$`): ID of the field to delete
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
